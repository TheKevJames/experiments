pub fn dec(x: usize, max: usize) -> usize {
    if x == 0 {
        max - 1
    } else {
        x - 1
    }
}

pub fn inc(x: usize, max: usize) -> usize {
    (x + 1) % max
}
