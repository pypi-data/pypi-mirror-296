use crate::settings::Settings;
use crate::violation;
use crate::{Method, Rule, Violation};
/// Defines rules that enforce widely accepted whitespace rules.

pub struct TrailingWhitespace {}

fn trailing_whitespace(source: &str, _: &Settings) -> Vec<Violation> {
    let mut violations = Vec::new();
    for (idx, line) in source.split('\n').enumerate() {
        if line.ends_with(&[' ', '\t']) {
            violations.push(violation!("trailing whitespace", idx + 1));
        }
    }
    violations
}

impl Rule for TrailingWhitespace {
    fn method(&self) -> Method {
        Method::Text(trailing_whitespace)
    }

    fn explain(&self) -> &str {
        "
        Trailing whitespace is difficult to spot, and as some editors will remove it
        automatically while others leave it, it can cause unwanted 'diff noise' in
        shared projects.
        "
    }

    fn entrypoints(&self) -> Vec<&str> {
        vec!["TEXT"]
    }
}
