extern crate pretty_env_logger;

use borsh::{BorshDeserialize, BorshSerialize};
use chrono::prelude::*;
use std::{io::{Error as IoError, ErrorKind}, collections::HashMap};
use strum_macros::Display;
use uuid::Uuid as DefaultUuid;

const ERROR_NOT_ALL_BYTES_READ: &str = "Not all bytes read";

#[derive(Debug, Clone)]
pub struct Uuid(DefaultUuid);

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

#[derive(BorshSerialize, BorshDeserialize, Debug, Clone)]
pub struct PageMessage {
    pub id: Uuid,
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

impl Default for Status {
    fn default() -> Self {
        Status::ScrapperProcessing
    }
}

impl Default for Timestamp {
    fn default() -> Self {
        Timestamp(Utc::now())
    }
}

impl Default for Uuid {
    fn default() -> Self {
        Uuid(DefaultUuid::new_v4())
    }
}

impl BorshDeserialize for Uuid {
    fn deserialize(buf: &mut &[u8]) -> Result<Self, IoError> {
        let bytes = buf
            .get(..16)
            .ok_or_else(|| IoError::new(ErrorKind::UnexpectedEof, ERROR_NOT_ALL_BYTES_READ))?;
        *buf = &buf[16..];
        Ok(Uuid(DefaultUuid::from_slice(bytes).unwrap()))
    }
}

impl BorshSerialize for Uuid {
    fn serialize<W: std::io::Write>(&self, writer: &mut W) -> Result<(), IoError> {
        writer.write_all(self.0.as_bytes())?;
        Ok(())
    }
}

impl BorshDeserialize for Timestamp {
    fn deserialize(buf: &mut &[u8]) -> Result<Self, IoError> {
        let bytes = buf
            .get(..8)
            .ok_or_else(|| IoError::new(ErrorKind::UnexpectedEof, ERROR_NOT_ALL_BYTES_READ))?;
        *buf = &buf[8..];
        let timestamp = i64::from_be_bytes(bytes.try_into().unwrap());
        Ok(Timestamp(Utc.timestamp_opt(timestamp, 0).single().unwrap()))
    }
}

impl BorshSerialize for Timestamp {
    fn serialize<W: std::io::Write>(&self, writer: &mut W) -> Result<(), IoError> {
        let timestamp = self.0.timestamp();
        writer.write_all(&timestamp.to_be_bytes())?;
        Ok(())
    }
}

impl BorshDeserialize for Status {
    fn deserialize(buf: &mut &[u8]) -> Result<Self, IoError> {
        let value = String::deserialize(buf)?;
        let status = match value.as_str() {
            "pending" => Status::Pending,
            "scrapper_processing" => Status::ScrapperProcessing,
            "scrapper_done" => Status::ScrapperDone,
            "scrapper_error" => Status::ScrapperError,
            "parser_processing" => Status::ParserProcessing,
            "parser_error" => Status::ParserError,
            "parser_done" => Status::ParserDone,
            _ => panic!("Invalid status value"),
        };
        Ok(status)
    }
}

impl BorshSerialize for Status {
    fn serialize<W: std::io::Write>(&self, writer: &mut W) -> std::io::Result<()> {
        let status = match self {
            Status::Pending => "pending",
            Status::ScrapperProcessing => "scrapper_processing",
            Status::ScrapperDone => "scrapper_done",
            Status::ScrapperError => "scrapper_error",
            Status::ParserProcessing => "parser_processing",
            Status::ParserError => "parser_error",
            Status::ParserDone => "parser_done",
        };
        writer.write_all(status.as_bytes())?;
        Ok(())
    }
}