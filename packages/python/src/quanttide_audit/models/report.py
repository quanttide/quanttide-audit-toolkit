from __future__ import annotations

from pydantic import BaseModel, Field
from quanttide import (
    CreatedAtField,
    DescriptionField,
    IdField,
    NameField,
    TitleField,
    UpdatedAtField,
)

from quanttide_audit.models.finding import AuditFinding


class AuditReport(BaseModel):
    """审计报告：聚合审计发现。

    标识:
        id: 全局唯一标识（UUID）
        name: 报告唯一名称，slug 风格
        title: 报告可读标题
    说明:
        description: 报告补充说明，如审计范围、运行环境
    审计数据:
        findings: 审计发现列表，每条自包含 criterion 和 evidence
    时间追踪:
        created_at: 报告创建时间
        updated_at: 报告最后更新时间

    Usage:
        >>> from uuid import uuid4
        >>> now = "2026-01-01T00:00:00"
        >>> r = AuditReport(
        ...     id=uuid4(), name="rep-1", title="Audit #1",
        ...     findings=[], created_at=now, updated_at=now,
        ... )
        >>> r.name == "rep-1"
        True
    """

    # 标识
    id: IdField
    name: NameField
    title: TitleField

    # 说明
    description: DescriptionField | None = None

    # 审计数据
    findings: list[AuditFinding] = Field(default_factory=list)

    # 时间追踪
    created_at: CreatedAtField
    updated_at: UpdatedAtField
