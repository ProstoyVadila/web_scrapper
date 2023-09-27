use crate::{
    broker::Broker, config::Config, database::Database, extractor::XpathExtractor, models,
};

use std::sync::Arc;

use futures_lite::stream::StreamExt;
use lapin::message::Delivery;
use log;


pub struct App {
    pub database: Database,
    pub broker: Broker,
    pub config: Config,
}

impl App {
    pub async fn new(config: Config) -> Arc<Self> {
        let database = Database::new(config.postgres.clone())
            .await
            .expect("database error");
        let broker = Broker::new(config.rabbit.clone())
            .await
            .expect("broker error");

        let app = App {
            database,
            broker,
            config,
        };
        Arc::new(app)
    }

    pub async fn run(self: Arc<Self>) {
        log::info!("Declaring and binding queues");
        self.broker.declare_all().await.expect("declare error");
        log::info!("Starting consuming");
        self.start_consuming().await;
    }

    async fn start_consuming(self: Arc<Self>) {
        let mut consumer = self.broker.consumer().await;

        log::info!(" [*] Waiting for messages. To exit press CTRL+C");
        while let Some(delivery) = consumer.next().await {
            let app = Arc::clone(&self);
            match delivery {
                Ok(delivery) => {
                    app.handle_message(delivery).await;
                }
                Err(e) => {
                    log::error!("Error receiving message: {:?}", e);
                }
            }
        }
    }

    async fn handle_message(self: Arc<Self>, delivery: Delivery) {
        let msg_in = serde_json::from_slice::<models::MessageIn>(delivery.data.as_slice())
            .expect("deserialize error in handle_message");
        self.broker
            .ack(delivery.delivery_tag)
            .await
            .expect("ack error");
        log::info!("Received message: {}", msg_in);
    
        log::info!("Spawning task to parse and store");
        tokio::spawn(async move {
            let extractor = XpathExtractor::new(msg_in.html.clone(), msg_in.xpaths);
            let res = extractor.extract().await;
            let msg_out = models::MessageOut {
                html: msg_in.html,
                values: res,
                invalid_xpaths: extractor.invalid_exprs,
            };
            log::info!("Sending message: {}", msg_out);
            let out = serde_json::to_vec(&msg_out).expect("serialize error in handle_message");
            self.broker
                .publish(out.as_slice())
                .await
                .expect("send error");
        });
    }
}
