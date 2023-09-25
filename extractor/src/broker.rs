extern crate log;

use crate::config;

use futures_lite::stream::StreamExt;
use lapin::{
    options::*, publisher_confirm::Confirmation, types::FieldTable, BasicProperties, Connection,
    ConnectionProperties, Result, ExchangeKind, protocol::exchange,
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
        self.declare_all().await?;
        self.consume().await?;
        Ok(())
    }

    async fn declare_all(&self) -> Result<()> {
        self.declare(&self.exchange_in, &self.queue_in).await?;
        self.declare(&self.exchange_out, &self.queue_out).await?;
        Ok(())
    }

        async fn declare(&self, exchange: &str, queue: &str) -> Result<()> {
        self.channel
            .exchange_declare(
                exchange,
                ExchangeKind::Direct,
                ExchangeDeclareOptions::default(),
                FieldTable::default(),
            )
            .await?;
        self.channel
            .queue_declare(
                queue,
                QueueDeclareOptions::default(),
                FieldTable::default(),
            )
            .await?;
        self.channel
            .queue_bind(
                queue,
                exchange,
                queue,
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

        #[allow(dead_code)]
        async fn publish(&self, data: &[u8]) -> Result<()> {
        let confirm = self
            .channel
            .basic_publish(
                &self.exchange_out,
                &self.queue_out,
                BasicPublishOptions::default(),
                data,
                BasicProperties::default(),
            )
            .await?
            .await?;
        assert_eq!(confirm, Confirmation::NotRequested);
        Ok(())
    }
}