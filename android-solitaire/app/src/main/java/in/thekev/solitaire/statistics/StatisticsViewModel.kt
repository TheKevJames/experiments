/*
 * Copyright (C) 2019 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package `in`.thekev.solitaire.statistics

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import `in`.thekev.solitaire.data.Result
import `in`.thekev.solitaire.data.Result.Success
import `in`.thekev.solitaire.data.Task
import `in`.thekev.solitaire.data.source.TasksRepository
import `in`.thekev.solitaire.util.Async
import `in`.thekev.solitaire.util.WhileUiSubscribed
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UiState for the statistics screen.
 */
data class StatisticsUiState(
    val isEmpty: Boolean = false,
    val isLoading: Boolean = false,
    val activeTasksPercent: Float = 0f,
    val completedTasksPercent: Float = 0f
)

/**
 * ViewModel for the statistics screen.
 */
@HiltViewModel
class StatisticsViewModel @Inject constructor(
    private val tasksRepository: TasksRepository
) : ViewModel() {

    val uiState: StateFlow<StatisticsUiState> =
        tasksRepository.getTasksStream()
            .map { Async.Success(it) }
            .onStart<Async<Result<List<Task>>>> { emit(Async.Loading) }
            .map { taskAsync -> produceStatisticsUiState(taskAsync) }
            .stateIn(
                scope = viewModelScope,
                started = WhileUiSubscribed,
                initialValue = StatisticsUiState(isLoading = true)
            )

    fun refresh() {
        viewModelScope.launch {
            tasksRepository.refreshTasks()
        }
    }

    private fun produceStatisticsUiState(taskLoad: Async<Result<List<Task>>>) =
        when (taskLoad) {
            Async.Loading -> {
                StatisticsUiState(isLoading = true, isEmpty = true)
            }
            is Async.Success -> {
                when (val result = taskLoad.data) {
                    is Success -> {
                        val stats = getActiveAndCompletedStats(result.data)
                        StatisticsUiState(
                            isEmpty = result.data.isEmpty(),
                            activeTasksPercent = stats.activeTasksPercent,
                            completedTasksPercent = stats.completedTasksPercent,
                            isLoading = false
                        )
                    }
                    else -> StatisticsUiState(isLoading = false)
                }
            }
        }
}
