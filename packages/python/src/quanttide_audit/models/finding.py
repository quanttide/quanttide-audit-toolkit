from enum import Enum

from pydantic import BaseModel, Field
from quanttide import (
    CreatedAtField,
    DescriptionField,
    IdField,
    NameField,
    TitleField,
    UpdatedAtField,
)

from quanttide_audit.models.criteria import AuditCriteria
from quanttide_audit.models.evidence import AuditEvidence


class AuditSeverity(str, Enum):
    """审计严重程度，遵循 ISO 19011:2018 审核管理指南。

    ISO 19011:2018 第 6.4.6 节将审核发现分类为符合/不符合/改进机会，
    本枚举对应不符合的严重程度分级。
    """

    MAJOR = "major"
    MINOR = "minor"
    OBSERVATION = "observation"


class AuditFinding(BaseModel):
    """审计发现：由"证据匹配标准"产生。

    标识:
        id: 全局唯一标识（UUID）
        name: 发现唯一名称，slug 风格，如 "f-line-length-main.py-42"
        title: 发现概要标题，如 "行过长（92 > 88）"
    关联:
        criterion: 被违反的审计标准（直接对象引用）
        evidence: 触发该发现的证据列表（直接对象引用）
    审计数据:
        description: 发现详细说明或修复建议
        severity: 严重程度（MAJOR/MINOR/OBSERVATION）
    时间追踪:
        created_at: 发现生成时间
        updated_at: 发现最后更新时间
    """

    # 标识
    id: IdField
    name: NameField
    title: TitleField

    # 关联
    criterion: AuditCriteria
    evidence: list[AuditEvidence] = Field(default_factory=list)

    # 审计数据
    description: DescriptionField | None = None
    severity: AuditSeverity

    # 时间追踪
    created_at: CreatedAtField
    updated_at: UpdatedAtField
