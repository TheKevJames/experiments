use noise::NoiseFn;
use noise::Perlin;
use noise::Seedable;

pub fn generate_map(
    height: usize,
    width: usize,
    seed: u32,
    scale: f64,
    octaves: u8,
    persistence: f64,
    lacunarity: f64,
) -> Vec<Vec<f64>> {
    let perlin = Perlin::new();
    perlin.set_seed(seed);

    let mut v: Vec<Vec<f64>> = Vec::new();
    for i in 0..height {
        v.push(Vec::new());
        for j in 0..width {
            let mut amplitude = 1.0;
            let mut frequency = 1.0;
            let mut depth = 0.0;
            for _ in 0..octaves {
                let x = i as f64 * frequency / scale;
                let y = j as f64 * frequency / scale;

                let value = perlin.get([x, y]);
                depth += value * amplitude;

                amplitude *= persistence;
                frequency *= lacunarity;
            }
            v[i].push(depth);
        }
    }
    v
}
