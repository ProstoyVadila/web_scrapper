use skyscraper::{xpath, html};

fn main() {
    let data = r##"
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
        <TITLE>301 Moved</TITLE></HEAD><BODY>
        <H1>301 Moved</H1>
        The document has moved
        <A HREF="http://www.google.com/">here</A>.
    </BODY></HTML>
    "##;
    let document = html::parse(data).expect("parse error");
    let expr = xpath::parse("//H1").expect("parse error");
    let res = expr.apply(&document).expect("apply error");
    assert_eq!(res.len(), 1);
    let text = res[0].get_text(&document).expect("get_text error");
    assert_eq!(text, "301 Moved");
    println!("text: {}", text);
}
