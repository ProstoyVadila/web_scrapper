extern crate pretty_env_logger;
#[macro_use]
extern crate log;

use std::error::Error;
use tokio;

mod config;
mod rabbit;
mod requests;

#[tokio::main(flavor = "multi_thread", worker_threads = 2)]
async fn main() -> Result<(), Box<dyn Error>> {
    pretty_env_logger::init();
    info!("Starting scrapper");

    info!("Loading config");
    let config = config::get();
    debug!("Config loaded: {:?}", config);

    // info!("Creating requests client");
    // let client = requests::Requests::new();

    // let urls = vec!["https://www.rust-lang.org/"; 2];

    // let bodies = client.get_from_urls(urls).await;
    // println!("{:?}", bodies);
    rabbit::consume(&config).await?;
    Ok(())
}
