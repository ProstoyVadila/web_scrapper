extern crate pretty_env_logger;

use amqprs::{
    callbacks::{DefaultChannelCallback, DefaultConnectionCallback},
    channel::{BasicConsumeArguments, QueueBindArguments, QueueDeclareArguments, ExchangeDeclareArguments, BasicAckArguments},
    connection::{Connection, OpenConnectionArguments},
};
use std::error::Error;
use tokio::sync::Notify;

use crate::config::Config;

pub async fn consume(config: &Config) -> Result<(), Box<dyn Error>> {
    let connection = Connection::open(&OpenConnectionArguments::new(
        &config.rabbit.host.clone(),
        config.rabbit.port.clone(),
        &config.rabbit.user.clone(),
        &config.rabbit.password.clone(),
    ))
    .await
    .unwrap();

    connection
        .register_callback(DefaultConnectionCallback)
        .await
        .unwrap();

    let channel = connection.open_channel(None).await.unwrap();
    channel
        .register_callback(DefaultChannelCallback)
        .await
        .unwrap();

        // declare a server-named transient queue
    let queue_name = "urls_to_crawl_queue";
    let queue_declare_arguments = QueueDeclareArguments::new(queue_name.clone())
        .durable(true)
        .finish();
    channel.queue_declare(queue_declare_arguments).await.unwrap();

    let exchange_name = "urls_to_crawl_exchange";
    let exchange_declare_arguments = ExchangeDeclareArguments::new(exchange_name.clone(), "direct");
    channel.exchange_declare(exchange_declare_arguments).await.unwrap();

    let routing_key = queue_name.clone();
    let queue_bind_arguments = QueueBindArguments::new(queue_name, exchange_name, routing_key);
    channel.queue_bind(queue_bind_arguments).await.unwrap();

    let args = BasicConsumeArguments::new(queue_name, "basic consumer tag")
        .manual_ack(false)
        .finish();

    let (_ctag, mut rx) = channel
        .basic_consume_rx(args)
        .await
        .unwrap();

    tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            if let Some(payload) = msg.content {
                println!("Received message: {:?}", payload);
                let basic_ack_args = BasicAckArguments::new(
                    msg.deliver.unwrap().delivery_tag(), 
                    false
                );
                channel.basic_ack(basic_ack_args).await.unwrap();
            }
        }
    });

    ("consume forever..., ctrl+c to exit");
    let guard = Notify::new();
    guard.notified().await;
    Ok(())
}
