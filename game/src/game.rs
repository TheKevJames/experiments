use crate::menu;
use crate::procedural;
use crate::utils;

use rand::rngs::StdRng;
use rand::Rng;
use rand_seeder::Seeder;
use sdl2::pixels::Color;
use sdl2::rect::Rect;
use sdl2::render::Canvas;
use sdl2::video::Window;

pub struct Terrain {
    color: Color,
    _label: &'static str,
    height: f64,
}

const REGIONS: [Terrain; 8] = [
    Terrain {
        color: Color::RGB(0, 71, 171),
        _label: "deep water",
        height: 0.3,
    },
    Terrain {
        color: Color::RGB(100, 149, 237),
        _label: "shallow water",
        height: 0.4,
    },
    Terrain {
        color: Color::RGB(194, 178, 128),
        _label: "sand",
        height: 0.45,
    },
    Terrain {
        color: Color::RGB(126, 200, 80),
        _label: "grass",
        height: 0.55,
    },
    Terrain {
        color: Color::RGB(1, 68, 33),
        _label: "forest",
        height: 0.6,
    },
    Terrain {
        color: Color::RGB(105, 70, 5),
        _label: "rock",
        height: 0.7,
    },
    Terrain {
        color: Color::RGB(75, 44, 13),
        _label: "mountain",
        height: 0.9,
    },
    Terrain {
        color: Color::RGB(255, 255, 255),
        _label: "snow",
        height: 1.0,
    },
];

pub struct Map {
    bg: Vec<Vec<f64>>,
    state: Vec<Vec<bool>>,
    height: usize,
    width: usize,
}

impl Map {
    const CELL_COLOR: Color = Color::RGB(0, 0, 0);
    const CELL_SIZE: usize = 10;

    pub fn new(height: usize, width: usize, rng: &mut StdRng) -> Map {
        let cols = width / Map::CELL_SIZE;
        let rows = height / Map::CELL_SIZE;

        let bg = procedural::generate_map(height, width, rng.gen(), 25.0, 4, 0.5, 2.0);

        let mut v: Vec<Vec<bool>> = Vec::new();
        for i in 0..rows {
            v.push(Vec::new());
            for _ in 0..cols {
                v[i].push(rng.gen());
            }
        }

        Map {
            bg: bg,
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

    pub fn click(&self, x: usize, y: usize) -> Map {
        let col = x / Map::CELL_SIZE;
        let row = y / Map::CELL_SIZE;

        let mut v = self.state.to_vec();
        v[row][col] = true;
        Map {
            bg: self.bg.to_vec(),
            state: v,
            height: self.height,
            width: self.width,
        }
    }

    pub fn randomize_bg(&self, seed: u32) -> Map {
        let bg = procedural::generate_map(self.height, self.width, seed, 25.0, 4, 0.5, 2.0);
        Map {
            bg: bg,
            state: self.state.to_vec(),
            height: self.height,
            width: self.width,
        }
    }

    pub fn render(&self, c: &mut Canvas<Window>, x: usize, y: usize, draw_perlin: bool) {
        let x_offset = x / Map::CELL_SIZE;
        let y_offset = y / Map::CELL_SIZE;

        for i in 0..self.height {
            for j in 0..self.width {
                if self.state[i][j] {
                    c.set_draw_color(Map::CELL_COLOR);
                    c.fill_rect(Rect::new(
                        ((j + x_offset) * Map::CELL_SIZE) as i32,
                        ((i + y_offset) * Map::CELL_SIZE) as i32,
                        Map::CELL_SIZE as u32,
                        Map::CELL_SIZE as u32,
                    ))
                    .unwrap();
                    continue;
                }

                if draw_perlin {
                    let value = (self.bg[i][j] * 200.0) as u8;
                    c.set_draw_color(Color::RGB(value, value, value));
                } else {
                    for region in REGIONS {
                        if self.bg[i][j] <= region.height {
                            c.set_draw_color(region.color);
                            break;
                        }
                    }
                }

                c.fill_rect(Rect::new(
                    ((j + x_offset) * Map::CELL_SIZE) as i32,
                    ((i + y_offset) * Map::CELL_SIZE) as i32,
                    Map::CELL_SIZE as u32,
                    Map::CELL_SIZE as u32,
                ))
                .unwrap();
            }
        }
    }

    pub fn tick(&self) -> Map {
        let mut v: Vec<Vec<bool>> = Vec::new();
        for i in 0..self.height {
            v.push(Vec::new());
            for j in 0..self.width {
                v[i].push(self.tick_cell(i, j));
            }
        }

        Map {
            bg: self.bg.to_vec(),
            state: v,
            height: self.height,
            width: self.width,
        }
    }
}

pub struct Game {
    map: Map,
    menu: menu::Menu,
    rng: StdRng,
    _height: usize,
    _width: usize,
}

impl Game {
    pub fn new(height: usize, width: usize, seed: String) -> Game {
        let mut rng: StdRng = Seeder::from(seed).make_rng();

        let menu = menu::Menu::new(50, width);
        let map = Map::new(height - 50, width, &mut rng);

        Game {
            map: map,
            menu: menu,
            rng: rng,
            _height: height,
            _width: width,
        }
    }

    pub fn click(&mut self, x: usize, y: usize) {
        if y < 50 {
            self.menu.click(x, y);
        } else {
            self.map = self.map.click(x, y - 50);
        }

        if self.menu.buttons[1].active {
            self.map = self.map.randomize_bg(self.rng.gen());
            self.menu.buttons[1].active = false;
        }
    }

    pub fn tick(&mut self) {
        self.map = self.map.tick();
    }

    pub fn render(&self, c: &mut Canvas<Window>) {
        // TODO: the x/y offset is probably a bad method -- can I nest Canvas's?

        // TODO: clear before renders?
        self.menu.render(c, 0, 0);
        self.map.render(c, 0, 50, self.menu.buttons[0].active);

        c.present();
    }
}
