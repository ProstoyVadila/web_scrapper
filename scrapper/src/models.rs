extern crate log;

use chrono::prelude::*;
use std::collections::HashMap;
use strum_macros::Display;

const ERROR_NOT_ALL_BYTES_READ: &str = "Not all bytes read";


#[derive(Debug, Clone)]
pub struct Timestamp(DateTime<Utc>);

#[derive(Display, Debug, Clone)]
pub enum Status {
    Pending,
    ScrapperProcessing,
    ScrapperDone,
    ScrapperError,
    ParserProcessing,
    ParserError,
    ParserDone,
}

#[derive(Debug, Clone)]
pub struct PageMessage {
    // pub id: Uuid,
    pub url: String,
    pub status: Status,
    pub xpaths: HashMap<String, String>,
    pub created_at: Timestamp,
    pub updated_at: Timestamp,
    pub is_pagination: bool,
    pub refresh_interval: u64,
    pub refresh_at: Timestamp,
    pub last_refresh: Timestamp,
}
