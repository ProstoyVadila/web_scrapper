use crate::extractor::{Extractor, XpathExtractor};

use std::{collections::HashMap, error::Error};

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct MessageIn {
    pub html: String,
    pub xpaths: HashMap<String, String>,
}

#[derive(Serialize, Deserialize)]
pub struct MessageOut {
    pub html: String,
    pub values: HashMap<String, String>,
    pub invalid_xpaths: HashMap<String, String>,
}

pub async fn handle_parse_event(data: &str) -> Result<Vec<u8>, Box<dyn Error>> {
    let msg_in =
        serde_json::from_str::<MessageIn>(data).expect("deserialize error in handle_parse_event");
    let extractor = XpathExtractor::new(msg_in.html.clone(), msg_in.xpaths);
    let res = extractor.extract();
    let msg_out = MessageOut {
        html: msg_in.html,
        values: res,
        invalid_xpaths: extractor.invalid_exprs,
    };
    let out = serde_json::to_vec(&msg_out).expect("serialize error in handle_parse_event");
    Ok(out)
}