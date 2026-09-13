use chrono::{DateTime, Utc};
use quanttide_audit::evidence::AuditEvidence;
use uuid::Uuid;

fn ts(text: &str) -> DateTime<Utc> {
    DateTime::parse_from_rfc3339(text).unwrap().into()
}

fn sample() -> AuditEvidence {
    AuditEvidence {
        id: Uuid::parse_str("1f1e1d1c-1b1a-1918-1716-151413121110").unwrap(),
        name: "ev-main.py-42".into(),
        title: "第 42 行超出长度限制".into(),
        description: "第 42 行 92 个字符，上限 88".into(),
        created_at: ts("2026-01-01T00:00:00Z"),
        updated_at: ts("2026-01-01T00:00:00Z"),
    }
}

#[test]
fn construct() {
    let e = sample();
    assert_eq!(e.name, "ev-main.py-42");
    assert_eq!(e.title, "第 42 行超出长度限制");
}

#[test]
fn yaml_roundtrip() {
    let e = sample();
    let yaml = serde_yaml::to_string(&e).unwrap();
    let back: AuditEvidence = serde_yaml::from_str(&yaml).unwrap();
    assert_eq!(e, back);
}

#[test]
fn deserialize_gallery_format() {
    let yaml = r#"
id: 1f1e1d1c-1b1a-1918-1716-151413121110
name: ev-main.py-42
title: 第 42 行超出长度限制
description: 第 42 行 92 个字符，上限 88
created_at: 2026-01-01T00:00:00Z
updated_at: 2026-01-01T00:00:00Z
"#;
    let e: AuditEvidence = serde_yaml::from_str(yaml).unwrap();
    assert_eq!(e.name, "ev-main.py-42");
    assert_eq!(e.created_at.to_rfc3339(), "2026-01-01T00:00:00+00:00");
}
