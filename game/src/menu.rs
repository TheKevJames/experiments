use sdl2::pixels::Color;
use sdl2::rect::Rect;
use sdl2::render::Canvas;
use sdl2::video::Window;

pub struct Button {
    active: bool,
    label: &'static str,
    height: usize,
}

impl Button {
    const BG_COLOR: Color = Color::RGB(200, 200, 200);
    const FG_COLOR_INACTIVE: Color = Color::RGB(255, 0, 0);
    const FG_COLOR_ACTIVE: Color = Color::RGB(0, 255, 0);
    const WIDTH: usize = 150;

    pub fn new(label: &'static str, height: usize) -> Button {
        Button {
            active: false,
            label: label,
            height: height,
        }
    }

    pub fn click(&mut self) {
        self.active = !self.active;
    }

    pub fn render(&self, c: &mut Canvas<Window>, x: i32, y: i32) {
        c.set_draw_color(Button::BG_COLOR);
        let rect = Rect::new(x, y, Button::WIDTH as u32, self.height as u32);
        c.fill_rect(rect).unwrap();

        let ttf_context = sdl2::ttf::init().unwrap();
        let texture_creator = c.texture_creator();

        let mut font = ttf_context.load_font("assets/arial.ttf", 128).unwrap();
        font.set_style(sdl2::ttf::FontStyle::BOLD);

        let color = if self.active {
            Button::FG_COLOR_ACTIVE
        } else {
            Button::FG_COLOR_INACTIVE
        };
        let surface = font.render(self.label).blended(color).unwrap();
        let texture = texture_creator
            .create_texture_from_surface(&surface)
            .unwrap();

        c.copy(&texture, None, Some(rect)).unwrap();
    }
}

pub struct Menu {
    buttons: [Button; 2],
    height: usize,
    width: usize,
}

impl Menu {
    const BG_COLOR: Color = Color::RGB(50, 50, 50);

    pub fn new(height: usize, width: usize) -> Menu {
        let buttons = [
            Button::new("Button 1", height),
            Button::new("Button 2", height),
        ];
        Menu {
            buttons: buttons,
            height: height,
            width: width,
        }
    }

    pub fn click(&mut self, x: usize, y: usize) {
        if x < Button::WIDTH {
            self.buttons[0].click();
        } else if x < 2 * Button::WIDTH {
            self.buttons[1].click();
        }
    }

    pub fn render(&self, c: &mut Canvas<Window>, x: usize, y: usize) {
        c.set_draw_color(Menu::BG_COLOR);
        let rect = Rect::new(x as i32, y as i32, self.width as u32, self.height as u32);
        c.fill_rect(rect).unwrap();

        for (i, button) in self.buttons.iter().enumerate() {
            button.render(c, (x + i * Button::WIDTH) as i32, y as i32);
        }
    }
}
