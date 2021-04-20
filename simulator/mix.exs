defmodule Simulator.Mixfile do
  use Mix.Project

  def project do
    [
      app: :simulator,
      version: "0.1.0",
      elixir: "~> 1.10",
      build_embedded: Mix.env() == :prod,
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [applications: [:logger], mod: {Simulator, []}]
  end

  defp deps do
    # TODO: seriously, v0.0.1?
    [{:canvas, "~> 0.0.1"}]
  end
end
