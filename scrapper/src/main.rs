extern crate log;

use std::error::Error;
use tokio;

mod config;
mod models;
mod rabbit;
mod requests;
mod handlers;

#[tokio::main(flavor = "multi_thread", worker_threads = 8)]
async fn main() -> Result<(), Box<dyn Error>> {
    json_env_logger::init();
    log::info!("Starting scrapper");

    log::info!("Loading config");
    let config = config::get();
    log::debug!("Config loaded: {:?}", config);

    log::info!("Initializing rabbit listener");
    let broker = rabbit::Broker::new(config.rabbit).await?;
    broker.start().await?;
    Ok(())
}
