import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from quanttide_audit import AuditReport


JSON_FILE = "audit.json"


class ReportRepository:
    def __init__(self, state_home: Path):
        self._path = state_home / JSON_FILE

    def load_previous_state(self, mode: Optional[str] = None) -> Optional[tuple]:
        if not self._path.exists():
            return None
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            if mode and data.get("mode") != mode:
                return None
            keys = frozenset(
                f"{s['severity']}|{s['criterion']}|{s['title']}|{s.get('description', '')}"
                for s in data.get("findings", [])
            )
            return (keys, data.get("timestamp", ""))
        except Exception:
            return None

    def save_report(self, report: AuditReport, mode: str) -> None:
        data = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "findings": [
                {"severity": f.severity.value, "criterion": f.criterion.name, "title": f.title, "description": f.description or ""}
                for f in report.findings
            ],
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
