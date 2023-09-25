extern crate log;

use crate::extractor::Extractor;
use std::collections::HashMap;
use std::error::Error;

use tokio;


mod extractor;
mod config;
mod broker;


#[tokio::main(flavor = "multi_thread", worker_threads = 2)]
async fn main() -> Result<(), Box<dyn Error>>{
    json_env_logger::init();


    log::info!("starting extractor");
    let conf = config::get();
    
    log::info!("Connecting to RabbitMQ");
    let broker = broker::Broker::new(conf.rabbit).await?;
    broker.start().await?;

    let data = r##"
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
        <TITLE>301 Moved</TITLE></HEAD><BODY>
        <H1>301 Moved</H1>
        The document has moved
        <A HREF="http://www.google.com/">here</A>.
    </BODY></HTML>
    "##;
    let exprs = HashMap::<&str, &str>::from([
        ("title", "//TITLE"),
        ("a", "//A/text()"),
        ("h1", "//H1"),
    ]);
    let xpath_extractor = extractor::XpathExtractor::new(data, exprs);
    let res = xpath_extractor.extract();
    log::info!("res: {:?}", res);
    Ok(())
}
