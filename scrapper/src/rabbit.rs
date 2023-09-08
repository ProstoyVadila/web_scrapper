use amqprs::{
    callbacks::{DefaultChannelCallback, DefaultConnectionCallback},
    channel::{BasicConsumeArguments, QueueBindArguments, QueueDeclareArguments},
    connection::{Connection, OpenConnectionArguments},
    consumer::DefaultConsumer,
};
use tokio::sync::Notify;

use tracing_subscriber::{fmt, prelude::*, EnvFilter};


struct RabbitMQ {
    consumer: Consumer,
}

pub async fn consume(config: &Config) -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::registry()
        .with(fmt::layer())
        .with(EnvFilter::from_default_env())
        .try_init()
        .ok();

    let connection = Connection::open(
        &OpenConnectionArguments::new(
            config.rabbitmq_host.clone(),
            config.rabbitmq_port.clone(),
            config.rabbitmq_username.clone(),
            config.rabbitmq_password.clone(),
        )
    ).await.unwrap();

    connection.register_callback(DefaultConnectionCallback).await.unwrap();

    let channel = connection.open_channel().await.unwrap();
    channel
        .register_callback(DefaultChannelCallback)
        .await
        .unwrap();


}
