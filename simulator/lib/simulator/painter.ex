defmodule Simulator.Painter do
  def paint(canvas, width, height, scale) do
    GenServer.call(Simulator.World, :changes)
    |> Enum.each(fn change -> paint_change(change, canvas, width, height, scale) end)
  end

  defp paint_change({:init}, canvas, width, height, _) do
    paint_world(canvas, width, height)
  end

  defp paint_change({:remove, xy}, canvas, _, _, scale) do
    paint_actor(canvas, scale, xy, :black)
  end

  defp paint_change({:add, color, xy}, canvas, _, _, scale) do
    paint_actor(canvas, scale, xy, color)
  end

  defp paint_world(canvas, width, height) do
    Canvas.GUI.Brush.draw_rectangle(canvas, {0, 0}, {width, height}, :black)
  end

  defp paint_actor(canvas, scale, {x, y}, color) do
    Canvas.GUI.Brush.draw_circle(canvas, {x * scale + 2, y * scale + 2}, 2, color)
  end
end
