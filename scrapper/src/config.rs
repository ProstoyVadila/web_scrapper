extern crate dotenv;
extern crate pretty_env_logger;

use envconfig::Envconfig;
use std::env;

#[derive(Debug, Envconfig)]
pub struct RabbitMQ {
    #[envconfig(from = "RABBITMQ_USER")]
    pub address: String,
    #[envconfig(from = "RABBITMQ_PASSWORD")]
    pub password: String,
    #[envconfig(from = "RABBITMQ_HOST")]
    pub host: String,
    #[envconfig(from = "RABBITMQ_PORT")]
    pub port: u16,
}

impl RabbitMQ {
    pub fn get_url(&self) -> String {
        format!(
            "amqp://{}:{}@{}:{}",
            self.address, self.password, self.host, self.port
        )
    }
}

#[derive(Debug, Envconfig)]
pub struct Config {
    #[envconfig(nested = true)]
    pub rabbit: RabbitMQ,
    #[envconfig(from = "LOG_LEVEL")]
    pub log_level: String,
}

pub fn get() -> Config {
    // If LOCAL_RUN is set, load .env file
    if !env::var("LOCAL_RUN").is_err() {
        use dotenv::dotenv;

        dotenv().ok();
        info!("Local Run mode enabled")
    }

    let config = match Config::init_from_env() {
        Ok(config) => config,
        Err(e) => panic!("Error loading config: {}", e),
    };
    debug!("rabbit url: {}", config.rabbit.get_url());
    config
}
