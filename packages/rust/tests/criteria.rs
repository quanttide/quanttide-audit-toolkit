use chrono::{DateTime, Utc};
use quanttide_audit::criteria::AuditCriteria;
use uuid::Uuid;

fn ts(text: &str) -> DateTime<Utc> {
    DateTime::parse_from_rfc3339(text).unwrap().into()
}

fn sample() -> AuditCriteria {
    AuditCriteria {
        id: Uuid::parse_str("0f0e0d0c-0b0a-0908-0706-050403020100").unwrap(),
        name: "line-length".into(),
        title: "行长度检查".into(),
        description: "每行不应超过 88 个字符".into(),
        created_at: ts("2026-01-01T00:00:00Z"),
        updated_at: ts("2026-01-01T00:00:00Z"),
    }
}

#[test]
fn construct() {
    let c = sample();
    assert_eq!(c.name, "line-length");
    assert_eq!(c.description, "每行不应超过 88 个字符");
}

#[test]
fn yaml_roundtrip() {
    let c = sample();
    let yaml = serde_yaml::to_string(&c).unwrap();
    let back: AuditCriteria = serde_yaml::from_str(&yaml).unwrap();
    assert_eq!(c, back);
}

#[test]
fn deserialize_gallery_format() {
    let yaml = r#"
id: 0f0e0d0c-0b0a-0908-0706-050403020100
name: line-length
title: 行长度检查
description: 每行不应超过 88 个字符
created_at: 2026-01-01T00:00:00Z
updated_at: 2026-01-01T00:00:00Z
"#;
    let c: AuditCriteria = serde_yaml::from_str(yaml).unwrap();
    assert_eq!(c.name, "line-length");
    assert_eq!(c.created_at.to_rfc3339(), "2026-01-01T00:00:00+00:00");
}
