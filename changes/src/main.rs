#[macro_use]
extern crate clap;
extern crate hyper;
extern crate hyper_tls;
// extern crate pulldown_cmark;
extern crate serde_json;
extern crate tokio_core;

mod changelog;
mod http;
mod python;

fn main() {
    let args = clap::App::new("changes")
        .version(crate_version!())
        .arg(
            clap::Arg::with_name("source")
                .short("s")
                .long("source")
                .value_name("SOURCE")
                .help("Provides a source restriction.")
                .takes_value(true),
        )
        .arg(
            clap::Arg::with_name("NAME")
                .help("Sets the name to search")
                .required(true)
                .index(1),
        )
        .get_matches();

    let name = args.value_of("NAME").unwrap();

    if let Some(source) = args.value_of("source") {
        if python::SOURCES.contains(&source) {
            if let Some(changelog_url) = python::find_url(&name) {
                let mut clog = changelog::Changelog::new(name, &changelog_url);
                clog.retrieve();
                clog.print();
                std::process::exit(0);
            }
            eprintln!("could not find changelog for package {}", name);
            std::process::exit(1);
        }

        // TODO: implement
        // println!("Values: {} {}", source, name);
    }

    // TODO: implement
    // println!("Value: {}", name);
    std::process::exit(1);
}
