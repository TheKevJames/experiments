use hyper::rt::{Future, Stream};
use hyper::{self, Client};
use hyper_tls::HttpsConnector;
use serde_json;

pub enum FetchError {
    Http(hyper::Error),
    Json(serde_json::Error),
}

impl From<hyper::Error> for FetchError {
    fn from(err: hyper::Error) -> FetchError {
        FetchError::Http(err)
    }
}

impl From<serde_json::Error> for FetchError {
    fn from(err: serde_json::Error) -> FetchError {
        FetchError::Json(err)
    }
}

fn fetch(url: hyper::Uri) -> impl Future<Item = hyper::Chunk, Error = FetchError> {
    let https = HttpsConnector::new(4).expect("TLS initialization failed");
    let client = Client::builder().build::<_, hyper::Body>(https);

    client
        .get(url)
        .and_then(|res| {
            if res.status().is_success() {
                res.into_body().concat2()
            } else {
                // TODO: return error code as FetchError
                panic!("http error code: {}", res.status().as_u16())
            }
        })
        .from_err::<FetchError>()
}

pub fn fetch_json(url: hyper::Uri) -> impl Future<Item = serde_json::Value, Error = ()> {
    fetch(url)
        .and_then(|body| {
            let payload: serde_json::Value = serde_json::from_slice(&body)?;
            Ok(payload)
        })
        .from_err()
        .map_err(|e| match e {
            FetchError::Http(e) => eprintln!("http error: {}", e),
            FetchError::Json(e) => eprintln!("json parsing error: {}", e),
        })
}

pub fn fetch_text(url: hyper::Uri) -> impl Future<Item = String, Error = ()> {
    fetch(url)
        .and_then(|body| {
            let v = body.to_vec();
            Ok(String::from_utf8_lossy(&v).to_string())
        })
        .from_err()
        .map_err(|e| match e {
            FetchError::Http(e) => eprintln!("http error: {}", e),
            FetchError::Json(e) => eprintln!("json parsing error: {}", e),
        })
}
