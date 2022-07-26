extern crate log;
extern crate pretty_env_logger;
extern crate rand;
extern crate sdl2;

mod board;
mod utils;

use std::time::Duration;

use log::{debug,info};
use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use sdl2::render::Canvas;
use sdl2::video::Window;
use sdl2::EventPump;
use sdl2::Sdl;

fn init(height: u32, width: u32) -> (Sdl, Canvas<Window>, EventPump) {
    let context = sdl2::init().unwrap();
    let video = context.video().unwrap();

    let window = video
        .window("life", width, height)
        .position_centered()
        .opengl()
        .build()
        .unwrap();

    let canvas = window.into_canvas().build().unwrap();
    let event_pump = context.event_pump().unwrap();

    (context, canvas, event_pump)
}

fn main() {
    pretty_env_logger::init();

    let height: u32 = 600;
    let width: u32 = 400;
    let (context, mut canvas, mut event_pump) = init(height, width);

    let mut board = board::Board::new(height as usize, width as usize);

    'running: loop {
        for event in event_pump.poll_iter() {
            match event {
                Event::Quit { .. }
                | Event::KeyDown {
                    keycode: Some(Keycode::Q),
                    ..
                } => break 'running,
                _ => {
                    info!("Unhandled keypress: {:?}", event);
                }
            }
        }

        board.render(&mut canvas);
        board = board.tick();

        ::std::thread::sleep(Duration::from_millis(50));

        let focused = context.keyboard().focused_window_id().is_some();
        debug!("{:?}", focused);
        // TODO: why no kepresses captured when focused?
    }
}
