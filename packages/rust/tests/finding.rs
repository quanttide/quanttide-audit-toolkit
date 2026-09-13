use chrono::{DateTime, Utc};
use quanttide_audit::criteria::AuditCriteria;
use quanttide_audit::evidence::AuditEvidence;
use quanttide_audit::finding::{AuditFinding, AuditSeverity};
use uuid::Uuid;

fn ts(text: &str) -> DateTime<Utc> {
    DateTime::parse_from_rfc3339(text).unwrap().into()
}

fn sample_criteria() -> AuditCriteria {
    AuditCriteria {
        id: Uuid::parse_str("0f0e0d0c-0b0a-0908-0706-050403020100").unwrap(),
        name: "line-length".into(),
        title: "行长度检查".into(),
        description: "每行不应超过 88 个字符".into(),
        created_at: ts("2026-01-01T00:00:00Z"),
        updated_at: ts("2026-01-01T00:00:00Z"),
    }
}

fn sample_evidence() -> AuditEvidence {
    AuditEvidence {
        id: Uuid::parse_str("1f1e1d1c-1b1a-1918-1716-151413121110").unwrap(),
        name: "ev-main.py-42".into(),
        title: "第 42 行超出长度限制".into(),
        description: "第 42 行 92 个字符，上限 88".into(),
        created_at: ts("2026-01-01T00:00:00Z"),
        updated_at: ts("2026-01-01T00:00:00Z"),
    }
}

fn sample() -> AuditFinding {
    AuditFinding {
        id: Uuid::parse_str("2f2e2d2c-2b2a-2928-2726-252423222120").unwrap(),
        name: "f-line-length-main.py-42".into(),
        title: "行过长（92 > 88）".into(),
        criterion: sample_criteria(),
        evidence: vec![sample_evidence()],
        description: Some("把第 42 行折到 88 字符以内".into()),
        severity: AuditSeverity::Major,
        created_at: ts("2026-01-01T00:00:00Z"),
        updated_at: ts("2026-01-01T00:00:00Z"),
    }
}

#[test]
fn construct() {
    let f = sample();
    assert_eq!(f.name, "f-line-length-main.py-42");
    assert_eq!(f.criterion.name, "line-length");
    assert_eq!(f.evidence.len(), 1);
}

#[test]
fn yaml_roundtrip() {
    let f = sample();
    let yaml = serde_yaml::to_string(&f).unwrap();
    let back: AuditFinding = serde_yaml::from_str(&yaml).unwrap();
    assert_eq!(f, back);
}

#[test]
fn severity_serializes_as_lowercase_name() {
    let json = serde_json::to_value(sample()).unwrap();
    assert_eq!(json["severity"], "major");
    assert_eq!(json["criterion"]["name"], "line-length");
    assert_eq!(json["evidence"][0]["name"], "ev-main.py-42");
}

#[test]
fn evidence_and_description_are_optional() {
    let yaml = r#"
id: 2f2e2d2c-2b2a-2928-2726-252423222120
name: f-line-length-main.py-42
title: 行过长（92 > 88）
criterion:
  id: 0f0e0d0c-0b0a-0908-0706-050403020100
  name: line-length
  title: 行长度检查
  description: 每行不应超过 88 个字符
  created_at: 2026-01-01T00:00:00Z
  updated_at: 2026-01-01T00:00:00Z
severity: minor
created_at: 2026-01-01T00:00:00Z
updated_at: 2026-01-01T00:00:00Z
"#;
    let f: AuditFinding = serde_yaml::from_str(yaml).unwrap();
    assert!(f.evidence.is_empty());
    assert_eq!(f.description, None);
    assert_eq!(f.severity, AuditSeverity::Minor);
}
