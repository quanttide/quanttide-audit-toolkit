from pathlib import Path

from examples.knowl.config import _Settings


class TestSettings:
    def test_data_home_default(self):
        s = _Settings()
        assert isinstance(s.data_home, Path)

    def test_state_home_default(self):
        s = _Settings()
        assert isinstance(s.state_home, Path)
