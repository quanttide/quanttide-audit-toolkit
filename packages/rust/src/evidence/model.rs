use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// 审计证据：描述性证据。
///
/// 独立收集，不引用标准或发现，作为素材等待被标准检验。
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AuditEvidence {
    /// 全局唯一标识。
    pub id: Uuid,
    /// 证据唯一名称，slug 风格，如 `ev-main.py-42`。
    pub name: String,
    /// 证据概要标题，如「第 42 行超出长度限制」。
    pub title: String,
    /// 证据详细内容，如违规行原文或具体度量值。
    pub description: String,
    /// 证据收集时间。
    pub created_at: DateTime<Utc>,
    /// 证据最后更新时间。
    pub updated_at: DateTime<Utc>,
}
