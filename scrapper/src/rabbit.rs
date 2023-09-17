extern crate pretty_env_logger;

use crosstown_bus::{CrosstownBus, HandleError, MessageHandler, QueueProperties};

use crate::config::ConfigRabbitMQ;
use crate::models::PageMessage;

struct PageMessageHandler;

impl MessageHandler<PageMessage> for PageMessageHandler {
    fn handle(&self, message: Box<PageMessage>) -> Result<(), HandleError> {
        warn!("Received message: {:?}", message);
        Ok(())
    }

    fn get_handler_action(&self) -> String {
        todo!()
    }
}

pub async fn init_listener(config: ConfigRabbitMQ) {
    let bus = CrosstownBus::new_queue_listener(config.get_url()).unwrap();
    let queue_name = "urls_to_crawl";
    let queue_properties = QueueProperties {
        auto_delete: false,
        durable: true,
        use_dead_letter: false,
    };
    _ = bus.listen(queue_name.to_string(), PageMessageHandler{}, queue_properties);
}
