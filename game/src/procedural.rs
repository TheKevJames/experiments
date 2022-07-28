use noise::NoiseFn;
use noise::Perlin;
use noise::Seedable;

// fn lerp(min: f64, max: f64, fraction: f64) -> f64 {
//     min + fraction * (max - min)
// }

fn inverse_lerp(min: f64, max: f64, value: f64) -> f64 {
    (value - min) / (max - min)
}

pub fn generate_map(
    height: usize,
    width: usize,
    seed: u32,
    scale: f64,
    octaves: u8,
    persistence: f64,
    lacunarity: f64,
) -> Vec<Vec<f64>> {
    let perlin = Perlin::new().set_seed(seed);

    let mut min = std::f64::MAX;
    let mut max = std::f64::MIN;

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

                depth += perlin.get([x, y]) * amplitude;

                amplitude *= persistence;
                frequency *= lacunarity;
            }
            v[i].push(depth);

            if depth < min {
                min = depth;
            } else if depth > max {
                max = depth;
            }
        }
    }

    for i in 0..height {
        for j in 0..width {
            v[i][j] = inverse_lerp(min, max, v[i][j]);
        }
    }

    v
}
