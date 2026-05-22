from pathlib import Path


_SAMPLE_DOMAINS = [
    (("engineering", "工程领域"), ["ontology-1"], ["instance-a"]),
    (("finance", "金融领域"), ["ontology-2", "ontology-3"], ["instance-b", "instance-c"]),
]


def load_all_domains(data_dir: Path):
    for (did, dname), ontologies, instances in _SAMPLE_DOMAINS:
        yield data_dir / did, (did, dname), ontologies, instances
