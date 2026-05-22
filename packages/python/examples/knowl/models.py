from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class AuditMode(Enum):
    SIMPLE = "simple"
    FULL = "full"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value == value:
                    return member
        return None


@dataclass(frozen=True)
class AuditIssue:
    category: str
    group: str
    label: str
    action: str = ""

    def issue_key(self) -> str:
        return f"{self.category}|{self.group}|{self.label}"


@dataclass(frozen=True)
class AuditDiff:
    fixed: frozenset
    new: frozenset
    pending: frozenset
    previous_timestamp: Optional[str] = None

    @classmethod
    def compute(cls, previous, current, prev_timestamp=None):
        prev_set = frozenset(i.issue_key() for i in previous)
        curr_set = frozenset(i.issue_key() for i in current)
        return cls(
            fixed=prev_set - curr_set,
            new=curr_set - prev_set,
            pending=prev_set & curr_set,
            previous_timestamp=prev_timestamp,
        )

    @property
    def has_changes(self) -> bool:
        return bool(self.fixed or self.new)

    @property
    def is_identical(self) -> bool:
        return not self.has_changes


@dataclass
class KnowledgeBaseStats:
    data_dir: Path
    domains: list
    ontology_count: int
    instance_count: int

    @property
    def domain_count(self) -> int:
        return len(self.domains)

    @property
    def has_domains(self) -> bool:
        return bool(self.domains)


@dataclass
class AuditIssues:
    need_confirm: list
    auto_fixable: list
    suggestions: list
    mode: AuditMode

    @classmethod
    def from_raw(cls, need_confirm, auto_fixable, suggestions, mode):
        if mode == AuditMode.SIMPLE:
            suggestions = need_confirm + suggestions
            need_confirm = auto_fixable
            auto_fixable = []
        return cls(need_confirm=need_confirm, auto_fixable=auto_fixable, suggestions=suggestions, mode=mode)
