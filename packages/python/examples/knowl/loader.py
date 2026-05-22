from dataclasses import dataclass
from pathlib import Path


@dataclass
class _Domain:
    id: str
    name: str


_SAMPLE_DOMAINS = [
    (_Domain(id="engineering", name="工程领域"), ["ontology-1"], ["instance-a"]),
    (_Domain(id="finance", name="金融领域"), ["ontology-2", "ontology-3"], ["instance-b", "instance-c"]),
]


def load_all_domains(data_dir: Path):
    """Yield (path, domain, ontologies, instances) tuples."""
    for domain, ontologies, instances in _SAMPLE_DOMAINS:
        yield data_dir / domain.id, domain, ontologies, instances
