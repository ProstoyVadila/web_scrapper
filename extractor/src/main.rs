
mod extractor;

fn main() {
    let data = r##"
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
        <TITLE>301 Moved</TITLE></HEAD><BODY>
        <H1>301 Moved</H1>
        The document has moved
        <A HREF="http://www.google.com/">here</A>.
    </BODY></HTML>
    "##;
    let xpath_extractor = extractor::XpathExtractor::new(data);
    let res = xpath_extractor.extract("//H1");
    println!("{}", res);
}
