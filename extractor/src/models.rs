use std::{collections::HashMap, fmt::Display};

use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct MessageIn {
    pub event_id: String,
    pub user_id: String,
    pub html: String,
    pub xpaths: HashMap<String, String>,
    pub is_pagination: bool,
    pub refresh_interval: u64,
}

impl Display for MessageIn {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{{ event_id: {}, user_id: {}, xpaths: {:?}, is_pagination: {}, refresh_interval: {} }}",
            self.event_id, self.user_id, self.xpaths, self.is_pagination, self.refresh_interval
        )
    }
}

#[derive(Serialize, Deserialize)]
pub struct MessageOut {
    pub html: String,
    pub values: HashMap<String, String>,
    pub invalid_xpaths: HashMap<String, String>,
}

impl Display for MessageOut {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{{ values: {:?}, invalid_xpaths: {:?} }}",
            self.values, self.invalid_xpaths
        )
    }
}
