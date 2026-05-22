from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class _Settings:
    data_home: Path = field(default_factory=lambda: Path.cwd() / "data")
    state_home: Path = field(default_factory=lambda: Path.home() / ".quanttide" / "audit")


settings = _Settings()
