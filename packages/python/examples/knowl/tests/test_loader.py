from pathlib import Path

from examples.knowl.loader import load_all_domains


class TestLoadAllDomains:
    def test_yields_tuples(self):
        results = list(load_all_domains(Path("/data")))
        assert len(results) > 0
        for item in results:
            assert len(item) == 4

    def test_first_element_is_path(self):
        results = list(load_all_domains(Path("/base")))
        path, domain, ontologies, instances = results[0]
        assert isinstance(path, Path)
        assert str(path).startswith("/base")

    def test_domain_is_tuple_with_id_and_name(self):
        results = list(load_all_domains(Path("/data")))
        for _, domain, _, _ in results:
            assert isinstance(domain, tuple)
            assert len(domain) == 2
            assert isinstance(domain[0], str)
            assert isinstance(domain[1], str)

    def test_ontologies_and_instances_are_lists(self):
        results = list(load_all_domains(Path("/data")))
        for _, _, ontologies, instances in results:
            assert isinstance(ontologies, list)
            assert isinstance(instances, list)
