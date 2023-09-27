extern crate log;

use std::error::Error;

use tokio;

mod app;
mod config;
mod broker;
mod database;
mod extractor;
mod models;

#[tokio::main(flavor = "multi_thread", worker_threads = 8)]
async fn main() -> Result<(), Box<dyn Error>> {
    json_env_logger::init();
    log::info!("Starting extractor");

    log::info!("Loading configuration");
    let conf = config::get();

    let app = app::App::new(conf).await;
    app.run().await;
    // log::info!("Connecting to Postgres");
    // let db = database::Database::new(conf.postgres).await?;

    // log::info!("Connecting to RabbitMQ");
    // let broker = broker::Broker::new(conf.rabbit).await?;
    // broker.start().await?;
    Ok(())
}
