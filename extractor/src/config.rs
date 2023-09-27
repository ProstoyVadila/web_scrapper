extern crate dotenv;

use envconfig::Envconfig;
use log;
use std::env;

#[derive(Debug, Envconfig, Clone)]
pub struct ConfigRabbitMQ {
    #[envconfig(from = "RABBITMQ_ADMIN_USER")]
    pub user: String,
    #[envconfig(from = "RABBITMQ_ADMIN_PASSWORD")]
    pub password: String,
    #[envconfig(from = "RABBITMQ_HOST")]
    pub host: String,
    #[envconfig(from = "RABBITMQ_VHOST")]
    pub vhost: String,
    #[envconfig(from = "RABBITMQ_PORT")]
    pub port: u16,
}

impl ConfigRabbitMQ {
    pub fn get_url(&self) -> String {
        format!(
            "amqp://{}:{}@{}:{}",
            self.user, self.password, self.host, self.port
        )
    }
}

#[derive(Debug, Envconfig, Clone)]
pub struct ConfigPostgres {
    #[envconfig(from = "POSTGRES_USER")]
    pub user: String,
    #[envconfig(from = "POSTGRES_PASSWORD")]
    pub password: String,
    #[envconfig(from = "POSTGRES_HOST")]
    pub host: String,
    #[envconfig(from = "POSTGRES_PORT")]
    pub port: u16,
    #[envconfig(from = "POSTGRES_DB")]
    pub db: String,
}

impl ConfigPostgres {
    pub fn get_url(&self) -> String {
        format!(
            "postgres://{}:{}@{}:{}/{}",
            self.user, self.password, self.host, self.port, self.db
        )
    }
}

#[derive(Debug, Envconfig, Clone)]
pub struct Config {
    #[envconfig(nested = true)]
    pub rabbit: ConfigRabbitMQ,
    #[envconfig(nested = true)]
    pub postgres: ConfigPostgres,
    #[envconfig(from = "LOG_LEVEL")]
    pub log_level: String,
}

pub fn get() -> Config {
    // If LOCAL_RUN is set, load .env file
    if !env::var("LOCAL_RUN").is_err() {
        use dotenv::dotenv;

        dotenv().ok();
        log::info!("Local Run mode enabled")
    }

    let config = match Config::init_from_env() {
        Ok(config) => config,
        Err(e) => panic!("Error loading config: {}", e),
    };
    log::debug!("rabbit url: {}", config.rabbit.get_url());
    config
}
