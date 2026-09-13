use chrono::{DateTime, Utc};
use quanttide_audit::criteria::AuditCriteria;
use quanttide_audit::evidence::AuditEvidence;
use quanttide_audit::finding::{AuditFinding, AuditSeverity};
use quanttide_audit::report::AuditReport;
use uuid::Uuid;

fn ts(text: &str) -> DateTime<Utc> {
    DateTime::parse_from_rfc3339(text).unwrap().into()
}

fn sample_finding() -> AuditFinding {
    AuditFinding {
        id: Uuid::parse_str("2f2e2d2c-2b2a-2928-2726-252423222120").unwrap(),
        name: "f-line-length-main.py-42".into(),
        title: "行过长（92 > 88）".into(),
        criterion: AuditCriteria {
            id: Uuid::parse_str("0f0e0d0c-0b0a-0908-0706-050403020100").unwrap(),
            name: "line-length".into(),
            title: "行长度检查".into(),
            description: "每行不应超过 88 个字符".into(),
            created_at: ts("2026-01-01T00:00:00Z"),
            updated_at: ts("2026-01-01T00:00:00Z"),
        },
        evidence: vec![AuditEvidence {
            id: Uuid::parse_str("1f1e1d1c-1b1a-1918-1716-151413121110").unwrap(),
            name: "ev-main.py-42".into(),
            title: "第 42 行超出长度限制".into(),
            description: "第 42 行 92 个字符，上限 88".into(),
            created_at: ts("2026-01-01T00:00:00Z"),
            updated_at: ts("2026-01-01T00:00:00Z"),
        }],
        description: Some("把第 42 行折到 88 字符以内".into()),
        severity: AuditSeverity::Major,
        created_at: ts("2026-01-01T00:00:00Z"),
        updated_at: ts("2026-01-01T00:00:00Z"),
    }
}

fn sample() -> AuditReport {
    AuditReport {
        id: Uuid::parse_str("3f3e3d3c-3b3a-3938-3736-353433323130").unwrap(),
        name: "rep-1".into(),
        title: "代码审计 #1".into(),
        description: Some("审计范围：src/".into()),
        findings: vec![sample_finding()],
        created_at: ts("2026-01-01T00:00:00Z"),
        updated_at: ts("2026-01-01T00:00:00Z"),
    }
}

#[test]
fn construct() {
    let r = sample();
    assert_eq!(r.name, "rep-1");
    assert_eq!(r.findings.len(), 1);
    assert_eq!(r.findings[0].criterion.name, "line-length");
}

#[test]
fn yaml_roundtrip() {
    let r = sample();
    let yaml = serde_yaml::to_string(&r).unwrap();
    let back: AuditReport = serde_yaml::from_str(&yaml).unwrap();
    assert_eq!(r, back);
}

#[test]
fn findings_and_description_are_optional() {
    let yaml = r#"
id: 3f3e3d3c-3b3a-3938-3736-353433323130
name: rep-1
title: 代码审计 #1
created_at: 2026-01-01T00:00:00Z
updated_at: 2026-01-01T00:00:00Z
"#;
    let r: AuditReport = serde_yaml::from_str(yaml).unwrap();
    assert!(r.findings.is_empty());
    assert_eq!(r.description, None);
}
