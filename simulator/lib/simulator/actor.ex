defmodule Simulator.Actors do
  require Logger
  use GenServer

  def start_link(state = %{position: position, size: size}) do
    GenServer.start_link(__MODULE__, Map.put(state, :neighbors, neighbors_of(position, size)))
  end

  @impl true
  def init(state) do
    Process.send_after(self(), :tick, 0)
    {:ok, state}
  end

  @impl true
  def handle_info(
        :tick,
        state = %{position: position, neighbors: neighbors, type: type, size: size}
      ) do
    Process.send_after(self(), :tick, 200)

    if happy?(neighbors, type) do
      {:noreply, state}
    else
      {:noreply, %{state | position: move_away_from(position, type, size)}}
    end
  end

  defp neighbors_of({x, y}, size = {width, height}) do
    neighbor_offsets()
    |> Enum.map(fn {xoff, yoff} ->
      {rem(width + x + xoff, width), rem(height + y + yoff, height)}
    end)
    |> Enum.filter(fn new_xy -> valid?(new_xy, size) end)
  end

  defp valid?({x, y}, {width, height}) do
    x >= 0 and x < width and y >= 0 and y < height
  end

  defp happy?(neighbor_xys, type) do
    neighbors = GenServer.call(Simulator.World, {:look, neighbor_xys, type})
    Enum.sum(neighbors) >= length(neighbors) * 0.3
  end

  defp move_away_from(xy, type, size) do
    possible_xy =
      neighbor_offsets()
      |> Enum.random()
      |> advance(xy, :rand.uniform(3))

    if valid?(possible_xy, size) do
      GenServer.call(Simulator.World, {:move, xy, possible_xy, type})
    else
      xy
    end
  end

  defp neighbor_offsets do
    [{-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}]
  end

  defp advance({xoff, yoff}, {x, y}, distance) do
    {x + xoff * distance, y + yoff * distance}
  end
end
