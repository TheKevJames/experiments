use noise::NoiseFn;
use noise::Perlin;

pub fn generate_map(height: usize, width: usize, scale: f64) -> Vec<Vec<f64>> {
    let perlin = Perlin::new();

    let mut v: Vec<Vec<f64>> = Vec::new();
    for i in 0..height {
        v.push(Vec::new());
        for j in 0..width {
            let x = i as f64 / scale;
            let y = j as f64 / scale;

            v[i].push(perlin.get([x, y]));
        }
    }
    v
}
