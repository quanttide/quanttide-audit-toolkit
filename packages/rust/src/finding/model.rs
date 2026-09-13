use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::criteria::AuditCriteria;
use crate::evidence::AuditEvidence;

/// 审计严重程度，遵循 ISO 19011:2018 审核管理指南。
///
/// 该指南把审核发现分为符合 / 不符合 / 改进机会；本枚举对应不符合的严重程度分级。
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AuditSeverity {
    #[serde(rename = "major")]
    Major,
    #[serde(rename = "minor")]
    Minor,
    #[serde(rename = "observation")]
    Observation,
}

/// 审计发现：由「证据匹配标准」产生。
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AuditFinding {
    /// 全局唯一标识。
    pub id: Uuid,
    /// 发现唯一名称，slug 风格，如 `f-line-length-main.py-42`。
    pub name: String,
    /// 发现概要标题，如「行过长（92 > 88）」。
    pub title: String,
    /// 被违反的审计标准。
    pub criterion: AuditCriteria,
    /// 触发该发现的证据列表。
    #[serde(default)]
    pub evidence: Vec<AuditEvidence>,
    /// 发现详细说明或修复建议。
    #[serde(default)]
    pub description: Option<String>,
    /// 严重程度。
    pub severity: AuditSeverity,
    /// 发现生成时间。
    pub created_at: DateTime<Utc>,
    /// 发现最后更新时间。
    pub updated_at: DateTime<Utc>,
}
