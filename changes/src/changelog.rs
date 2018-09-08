use std;
use std::ffi::OsStr;
use std::io::Write;
use std::path::Path;

use http::fetch_text;
use hyper::rt::Future;
// use pulldown_cmark::{Parser, html};
use tokio_core;

pub struct Changelog<'a, 'b> {
    pub name: &'a str,
    pub url: &'b str,

    pub raw: Option<String>,
    pub ext: &'static str,
}

impl<'a, 'b> Changelog<'a, 'b> {
    pub fn new(name: &'a str, url: &'b str) -> Changelog<'a, 'b> {
        Changelog {
            name: name,
            url: url,
            raw: None,
            ext: match Path::new(&name).extension().and_then(OsStr::to_str) {
                Some(".md") => "markdown",
                Some(".rst") => "restructuredtext",
                Some(x) => {
                    eprintln!("unsupported changelog extension: {}", x);
                    std::process::exit(1);
                }
                None => "markdown",
            },
        }
    }

    pub fn retrieve(&mut self) {
        // TODO: do this render->raw replacement in github.rs
        let uri = self
            .url
            .replace("github.com", "raw.githubusercontent.com")
            .replace("/blob", "")
            .parse()
            .unwrap();
        let fut = fetch_text(uri).and_then(|result| Ok(result));
        self.raw = match tokio_core::reactor::Core::new() {
            Ok(mut core) => match core.run(fut) {
                Ok(r) => Some(r),
                _ => {
                    eprintln!("error running future");
                    None
                }
            },
            Err(e) => {
                eprintln!("error starting tokio core: {}", e);
                None
            }
        }
    }

    pub fn print(self) {
        if let Some(raw) = self.raw {
            for line in raw.split("\n") {
                // https://github.com/rust-lang/rust/issues/46016
                writeln!(&mut std::io::stdout(), "{}", line).ok();
            }

            // let mut converted = String::new();
            // let parser = Parser::new(&raw);
            // html::push_html(&mut converted, parser);
            // println!("{}", converted);
        }
    }
}
