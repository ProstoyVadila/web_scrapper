// use futures_lite::stream::{self, StreamExt};
use futures::stream;
use reqwest::Client;

pub struct Requests {
    client: Client,
    // headers: Vec<String>,
}

impl Requests {
    pub fn new() -> Self {
        let client = Client::new();
        // let headers = vec![];
        Self {
            client,
            // headers,
        }
    }

    #[allow(dead_code)]
    pub async fn get(&self, url: &str) -> Result<String, reqwest::Error> {
        let resp = self.client.get(url).send().await?.text().await?;
        Ok(resp)
    }

    // pub async fn get_from_urls(&self, urls: Vec<&str>) -> Vec<Result<String, reqwest::Error>> {
    //     let bodies = stream::iter(urls)
    //         .map(|url| {
    //             let client = &self.client;
    //             async move {
    //                 let body = client.get(url).send().await?.text().await;
    //                 body
    //             }
    //         })
    //         .buffer_unordered(2);

    //     let bodies = bodies
    //         .collect::<Vec<Result<String, reqwest::Error>>>()
    //         .await;
    //     bodies
    // }
}
