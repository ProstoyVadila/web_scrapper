extern crate log;

use std::error::Error;

use tokio;

mod broker;
mod config;
mod extractor;
mod handlers;

#[tokio::main(flavor = "multi_thread", worker_threads = 8)]
async fn main() -> Result<(), Box<dyn Error>> {
    json_env_logger::init();

    log::info!("starting extractor");
    let conf = config::get();

    log::info!("Connecting to RabbitMQ");
    let broker = broker::Broker::new(conf.rabbit).await?;
    broker.start().await?;
    Ok(())
}
