from mock import Mock
import pytest


@pytest.fixture()
def mock_run(monkeypatch):
    r = Mock()
    monkeypatch.setattr('utils.process.run', r)
    monkeypatch.setattr('ansible_hostmanager.run', r)
    return r
