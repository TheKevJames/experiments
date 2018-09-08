use http::fetch_json;
use hyper::rt::Future;
use tokio_core;

pub static SOURCES: &'static [&str] = &["pip", "pypi", "py", "python"];

pub fn find_url(name: &str) -> Option<String> {
    let uri = format!("https://pypi.org/pypi/{}/json", name)
        .parse()
        .unwrap();

    let fut = fetch_json(uri).and_then(|results| {
        let info = &results["info"];

        if info["project_urls"].is_object() {
            let urls = info["project_urls"].as_object().unwrap();
            if urls.contains_key("Changelog") {
                return Ok(urls["Changelog"].as_str().unwrap().to_string());
            } else if urls.contains_key("changelog") {
                return Ok(urls["changelog"].as_str().unwrap().to_string());
            }
        };
        // TODO: /[sS]ource/ -> return GitHub root, find changelog there

        let homepage = info["home_page"].as_str().unwrap();
        if homepage.contains("github.com") {
            // TODO: return GitHub root, find changelog there
        }

        eprintln!("no changelog found");
        Err(())
    });

    match tokio_core::reactor::Core::new() {
        Ok(mut core) => match core.run(fut) {
            Ok(url) => Some(url),
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
