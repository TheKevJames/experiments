use crate::utils;

use rand::Rng;
use sdl2::pixels::Color;
use sdl2::rect::Rect;
use sdl2::render::Canvas;
use sdl2::video::Window;

pub struct Board {
    state: Vec<Vec<bool>>,
    height: usize,
    width: usize,
}

impl Board {
    const BG_COLOR: Color = Color::RGB(255, 255, 255);

    const CELL_COLOR: Color = Color::RGB(0, 0, 0);
    const CELL_SIZE: usize = 5;

    pub fn new(height: usize, width: usize) -> Board {
        let mut rng = rand::thread_rng();

        let cols = width / Board::CELL_SIZE;
        let rows = height / Board::CELL_SIZE;

        let mut v: Vec<Vec<bool>> = Vec::new();
        for i in 0..rows {
            v.push(Vec::new());
            for _ in 0..cols {
                v[i].push(rng.gen());
            }
        }

        Board {
            state: v,
            height: rows,
            width: cols,
        }
    }

    fn count_neighbours(&self, i: usize, j: usize) -> u8 {
        self.state[utils::dec(i, self.height)][j] as u8
            + self.state[utils::inc(i, self.height)][j] as u8
            + self.state[i][utils::dec(j, self.width)] as u8
            + self.state[i][utils::inc(j, self.width)] as u8
            + self.state[utils::dec(i, self.height)][utils::dec(j, self.width)] as u8
            + self.state[utils::dec(i, self.height)][utils::inc(j, self.width)] as u8
            + self.state[utils::inc(i, self.height)][utils::dec(j, self.width)] as u8
            + self.state[utils::inc(i, self.height)][utils::inc(j, self.width)] as u8
    }

    fn tick_cell(&self, i: usize, j: usize) -> bool {
        let n = self.count_neighbours(i, j);
        match (self.state[i][j], n) {
            (true, 0..=1) => false,
            (true, 2..=3) => true,
            (true, 4..=8) => false,
            (false, 0..=2) => false,
            (false, 3) => true,
            (false, 4..=8) => false,
            _ => panic!("invalid match"),
        }
    }

    pub fn click(self, x: usize, y: usize) -> Board {
        let col = x / Board::CELL_SIZE;
        let row = y / Board::CELL_SIZE;

        let mut v = self.state;
        v[row][col] = true;
        Board {
            state: v,
            height: self.height,
            width: self.width,
        }
    }

    pub fn tick(&self) -> Board {
        let mut v: Vec<Vec<bool>> = Vec::new();

        for i in 0..self.height {
            v.push(Vec::new());
            for j in 0..self.width {
                v[i].push(self.tick_cell(i, j));
            }
        }

        Board {
            state: v,
            height: self.height,
            width: self.width,
        }
    }

    pub fn render(&self, c: &mut Canvas<Window>) {
        c.set_draw_color(Board::BG_COLOR);
        c.clear();

        c.set_draw_color(Board::CELL_COLOR);
        for i in 0..self.height {
            for j in 0..self.width {
                if self.state[i][j] {
                    c.fill_rect(Rect::new(
                        (j * Board::CELL_SIZE) as i32,
                        (i * Board::CELL_SIZE) as i32,
                        Board::CELL_SIZE as u32,
                        Board::CELL_SIZE as u32,
                    ))
                    .unwrap();
                }
            }
        }

        c.present();
    }
}
