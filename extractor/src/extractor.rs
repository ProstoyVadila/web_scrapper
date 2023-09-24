use skyscraper::{xpath, html};


pub struct XpathExtractor {
    pub doc: html::HtmlDocument,
}

impl XpathExtractor {
    pub fn new(doc: &str) -> Self {
        let doc = html::parse(doc).expect("parse error");
        XpathExtractor { doc }
    }

    pub fn extract(&self, expr: &str) -> String {
        let expr = self.get_xpath(expr);
        let res = expr.apply(&self.doc).expect("apply error");
        let attr = res[0].get_text(&self.doc).expect("get_text error");
        attr.to_string()
    }

    #[allow(dead_code)]
    pub fn extract_all(&self, expr: &str) -> Vec<String> {
        let expr = self.get_xpath(expr);
        let mut attrs = Vec::new();
        let res = expr.apply(&self.doc).expect("apply error");
        for node in res {
            let attr = node.get_text(&self.doc).expect("get_text error");
            attrs.push(attr.to_string());
        }
        attrs
    }

    fn get_xpath(&self, expr: &str) -> xpath::Xpath {
        xpath::parse(expr).expect("parse error")
    }

    #[allow(dead_code)]
    fn get_xpaths(&self, exprs: Vec<&str>) -> Vec<xpath::Xpath> {
        let mut xpaths = Vec::new();
        for expr in exprs {
            let xpath = self.get_xpath(expr);
            xpaths.push(xpath);
        }
        xpaths
    }
}