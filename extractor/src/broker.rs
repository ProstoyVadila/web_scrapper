extern crate log;

use crate::config;

use futures_lite::stream::StreamExt;
use lapin::{
    options::*, publisher_confirm::Confirmation, types::FieldTable, BasicProperties, Connection,
    ConnectionProperties, Result, ExchangeKind,
};


pub struct Broker {
    conn: Connection,
    channel: lapin::Channel,
    queue_in: String,
    queue_out: String,
    exchange_in: String,
    exchange_out: String,
    routing_key: String,
}

impl Broker {
    pub async fn new(conf: config::ConfigRabbitMQ) -> Result<Broker> {
        let conn = Connection::connect(
            &conf.get_url(),
            ConnectionProperties::default(),
        )
        .await?;
        let channel = conn.create_channel().await?;

        let queue_in = "extractor_in".to_string();
        let queue_out = "extractor_out".to_string();
        let exchange_in = "extractor_in".to_string();
        let exchange_out = "extractor_out".to_string();
        let routing_key = "extractor_in".to_string();
        Ok(Broker {
            conn,
            channel,
            queue_in,
            queue_out,
            exchange_in,
            exchange_out,
            routing_key,
        })
    }


    pub async fn start(&self) -> Result<()> {
        self.declare().await?;
        self.consume().await?;
        Ok(())
    }

    // async fn connect(&self) -> Result<()> {
    //     let conn = Connection::connect(
    //         &conf.get_url(),
    //         ConnectionProperties::default(),
    //     )
    //     .await?;
    //     let channel = self.conn.create_channel().await?;
    //     Ok(())
    // }

    // async fn create_channel(&self) -> Result<()> {
    //     let channel = self.conn.create_channel().await?;
    //     Ok(())
    // }

    // fn retry(&self) {
    //     std::thread::sleep(std::time::Duration::from_secs(5));
    //     log::info!("Retrying connection");
    //     self.try_connect();
    // }

    // fn try_connect(&self) {
    //     async_global_executor::spawn(async move {
    //         if Err(e) = self.connect().await {
    //             log::error!("Error connecting to RabbitMQ: {}", e);
    //             self.retry();
    //         }
    //     })
    // }


    pub async fn declare(&self) -> Result<()> {
        self.channel
            .queue_declare(
                &self.queue_in,
                QueueDeclareOptions::default(),
                FieldTable::default(),
            )
            .await?;
        self.channel
            .queue_declare(
                &self.queue_out,
                QueueDeclareOptions::default(),
                FieldTable::default(),
            )
            .await?;
        self.channel
            .exchange_declare(
                &self.exchange_in,
                ExchangeKind::Direct,
                ExchangeDeclareOptions::default(),
                FieldTable::default(),
            )
            .await?;
        self.channel
            .exchange_declare(
                &self.exchange_out,
                ExchangeKind::Direct,
                ExchangeDeclareOptions::default(),
                FieldTable::default(),
            )
            .await?;
        self.channel
            .queue_bind(
                &self.queue_in,
                &self.exchange_in,
                &self.routing_key,
                QueueBindOptions::default(),
                FieldTable::default(),
            )
            .await?;
        self.channel
            .queue_bind(
                &self.queue_out,
                &self.exchange_out,
                &self.routing_key,
                QueueBindOptions::default(),
                FieldTable::default(),
            )
            .await?;
        Ok(())
    }

    pub async fn consume(&self) -> Result<()> {
        let mut consumer = self
            .channel
            .basic_consume(
                &self.queue_in,
                "extractor_in",
                BasicConsumeOptions::default(),
                FieldTable::default(),
            )
            .await?;
        log::info!(" [*] Waiting for messages. To exit press CTRL+C");
        while let Some(delivery) = consumer.next().await {
            match delivery {
                Ok(delivery) => {
                    log::info!(" [x] Received {}", std::str::from_utf8(&delivery.data).unwrap());
                    self.channel
                        .basic_ack(delivery.delivery_tag, BasicAckOptions::default())
                        .await?;
                },

                Err(error) => {
                    log::error!("Error caught in consumer: {}", error);
                    break;
                }
            }
        }
        Ok(())
    }
}