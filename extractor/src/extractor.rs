use std::{collections::HashMap, sync::Arc};

use log;
use skyscraper::{html, xpath};
use tokio::sync::mpsc;

pub struct XpathExtractor {
    pub doc: html::HtmlDocument,
    pub exprs: HashMap<String, xpath::Xpath>,
    pub invalid_exprs: HashMap<String, String>,
}

impl XpathExtractor {
    pub fn new(doc: String, exprs: HashMap<String, String>) -> Self {
        // TODO validate doc and logs
        let doc = html::parse(&doc).expect("parse error");
        let mut invalid_exprs = HashMap::new();
        let exprs = exprs
            .iter()
            .filter_map(|(k, v)| match xpath::parse(v) {
                Ok(expr) => Some((k.to_string(), expr)),
                Err(e) => {
                    log::error!("invalid xpath: {}, err: {}", k, e);
                    invalid_exprs.insert(k.to_string(), e.to_string());
                    None
                }
            })
            .collect();
        XpathExtractor {
            doc,
            exprs,
            invalid_exprs,
        }
    }

    pub async fn extract(&self) -> HashMap<String, String> {
        let mut values = HashMap::new();
        let doc = Arc::new(self.doc.clone());

        let (tx, mut rx) = mpsc::channel(self.exprs.len());

        for (field, expr) in self.exprs.clone() {
            let tx = tx.clone();
            let doc = Arc::clone(&doc);
            tokio::spawn(async move {
                let res = parse(&doc, expr.clone()).unwrap_or("".to_string());
                tx.send((field, res)).await.unwrap();
            });
        }
        drop(tx);

        while let Some((field, res)) = rx.recv().await {
            values.insert(field.to_string(), res);
        }
        values
    }

    #[allow(dead_code)]
    pub async fn extract_one(&self, expr: xpath::Xpath) -> Option<String> {
        parse(&self.doc, expr)
    }
}

fn parse(doc: &html::HtmlDocument, expr: xpath::Xpath) -> Option<String> {
    let results = match expr.apply(doc) {
        Ok(v) => v,
        Err(e) => {
            log::error!("apply error: {}", e);
            return None;
        }
    };
    if results.is_empty() {
        log::error!("no result found for xpath");
        return None;
    }
    results[0].get_text(doc)
}
