extern crate log;
extern crate pretty_env_logger;
extern crate rand;
extern crate sdl2;

mod board;
mod menu;
mod procedural;
mod utils;

use std::time::Duration;

use log::debug;
use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use sdl2::mouse::MouseButton;
use sdl2::render::Canvas;
use sdl2::video::Window;
use sdl2::EventPump;

fn init(height: u32, width: u32) -> (Canvas<Window>, EventPump) {
    let context = sdl2::init().unwrap();
    let video = context.video().unwrap();

    let window = video
        .window("game", width, height)
        .position_centered()
        .opengl()
        .build()
        .unwrap();

    let canvas = window.into_canvas().build().unwrap();
    let event_pump = context.event_pump().unwrap();

    (canvas, event_pump)
}

fn main() {
    pretty_env_logger::init();

    let height: u32 = 1080;
    let width: u32 = 820;
    let (mut canvas, mut event_pump) = init(height, width);

    let seed = String::from("prng seed");
    let mut board = board::Board::new(height as usize, width as usize, seed);

    'running: loop {
        for event in event_pump.poll_iter() {
            match event {
                Event::Quit { .. }
                | Event::KeyDown {
                    keycode: Some(Keycode::Q),
                    ..
                } => break 'running,
                Event::KeyDown {
                    keycode: Some(Keycode::R),
                    ..
                } => {
                    board.randomize_bg();
                }
                Event::MouseMotion { .. } => {}
                Event::MouseButtonDown { .. } => {}
                Event::MouseButtonUp {
                    mouse_btn: MouseButton::Left,
                    x,
                    y,
                    ..
                } => {
                    board.click(x as usize, y as usize);
                }
                Event::Window { .. } => {}
                _ => {
                    debug!("Unhandled keypress: {:?}", event);
                }
            }
        }

        board.render(&mut canvas);
        board.tick();

        ::std::thread::sleep(Duration::from_millis(50));
    }
}
