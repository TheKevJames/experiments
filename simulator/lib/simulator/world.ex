defmodule Simulator.World do
  require Logger
  use GenServer

  defstruct actors: %{}, changes: []

  def start_link(state) do
    GenServer.start_link(__MODULE__, state, name: __MODULE__)
  end

  @impl true
  def init(%{size: size = {width, height}, actors: actor_count}) do
    types = [:green, :red, :blue]

    actors =
      for x <- 0..(width - 1), y <- 0..(height - 1) do
        {x, y}
      end
      |> Enum.take_random(actor_count)
      |> Enum.map(fn x ->
        type = types |> Enum.random()

        {:ok, _} =
          DynamicSupervisor.start_child(
            Simulator.DynamicSupervisor,
            {Simulator.Actors, %{position: x, type: type, size: size}}
          )

        {x, type}
      end)
      |> Enum.reduce(%{}, fn {pos, type}, acc -> Map.put(acc, pos, type) end)

    changes = actors |> Enum.map(fn {pos, type} -> {:add, type, pos} end)

    {:ok, %__MODULE__{actors: actors, changes: [{:init} | changes]}}
  end

  @impl true
  def handle_call({:look, neighbor_xys, type}, _from, state = %__MODULE__{actors: actors}) do
    neighbors =
      neighbor_xys
      |> Enum.filter(&Map.has_key?(actors, &1))
      |> Enum.reduce(%{}, fn position, acc ->
        same_type = if Map.get(actors, position) == type, do: 1, else: 0
        Map.put(acc, position, same_type)
      end)
      |> Map.values()

    {:reply, neighbors, state}
  end

  @impl true
  def handle_call(
        {:move, old_xy, new_xy, type},
        _from,
        state = %__MODULE__{actors: actors, changes: changes}
      ) do
    if Map.has_key?(actors, new_xy) do
      {:reply, old_xy, state}
    else
      {_, new_actors} =
        actors
        |> Map.put(new_xy, type)
        |> Map.pop(old_xy)

      new_changes = [{:add, type, new_xy} | [{:remove, old_xy} | changes]]

      {:reply, new_xy, %__MODULE__{actors: new_actors, changes: new_changes}}
    end
  end

  @impl true
  def handle_call(:changes, _from, %__MODULE__{actors: actors, changes: changes}) do
    {:reply, changes, %__MODULE__{actors: actors, changes: []}}
  end
end
