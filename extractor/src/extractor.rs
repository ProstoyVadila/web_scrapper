use std::collections::HashMap;

use skyscraper::{xpath, html};


pub trait Extractor {
    fn extract(&self) -> HashMap<String, String>;
}

pub struct XpathExtractor {
    pub doc: html::HtmlDocument,
    pub exprs: HashMap<String, xpath::Xpath>,
    pub invalid_exprs: HashMap<String, String>,
}

impl Extractor for XpathExtractor {
    fn extract(&self) -> HashMap<String, String> {
        self.exprs
            .iter()
            .map(|(k, v)| (k.clone(), self.extract_one(v.clone()).unwrap_or("".to_string())))
            .collect()
    }
}

impl XpathExtractor {
    pub fn new(doc: &str, exprs: HashMap<&str, &str>) -> Self {
        // TODO validate doc and logs
        let doc = html::parse(doc).expect("parse error");
        let mut invalid_exprs = HashMap::new();
        let exprs = exprs
            .iter()
            .filter_map(|(k, v)| {
                match xpath::parse(v) {
                    Ok(expr) => Some((k.to_string(), expr)),
                    Err(e) => {
                        println!("invalid xpath: {}, err: {}", k, e);
                        invalid_exprs.insert(k.to_string(), e.to_string());
                        None
                    }
                }
            })
            .collect();
        XpathExtractor { doc, exprs, invalid_exprs }
    }

    fn extract_one(&self, expr: xpath::Xpath) -> Option<String> {
        let results = match expr.apply(&self.doc) {
            Ok(v) => v,
            Err(e) => {
                println!("apply error: {}", e);
                return None;
            }
        };
        if results.is_empty() {
            println!("no result found for xpath");
            return None;
        }
        results[0].get_text(&self.doc)
    }
}