defmodule Simulator do
  use Application

  @width 128
  @height 128
  @scale 5

  def start(_type, _args) do
    canvas_options = [
      width: @width * @scale,
      height: @height * @scale,
      paint_interval: 100,
      painter_module: Simulator.Painter,
      painter_state: @scale,
      brushes: %{
        black: {0, 0, 0, 255},
        blue: {0, 0, 120, 255},
        green: {0, 120, 0, 255},
        red: {150, 0, 0, 255}
      }
    ]

    children = [
      {DynamicSupervisor, strategy: :one_for_one, name: Simulator.DynamicSupervisor},
      {Simulator.World, %{size: {@width, @height}, actors: 2000}},
      %{id: Canvas.GUI, start: {Canvas.GUI, :start_link, [canvas_options]}}
    ]

    opts = [strategy: :one_for_all, name: Simulator.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
