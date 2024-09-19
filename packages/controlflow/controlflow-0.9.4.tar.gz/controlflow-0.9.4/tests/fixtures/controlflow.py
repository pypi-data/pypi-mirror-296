import pytest

import controlflow
from controlflow.llm.messages import BaseMessage
from controlflow.utilities.testing import FakeLLM


@pytest.fixture(autouse=True)
def restore_defaults(monkeypatch):
    """
    Monkeypatch defaults to themselves, which will automatically reset them after every test
    """
    for k, v in controlflow.defaults.__dict__.items():
        monkeypatch.setattr(controlflow.defaults, k, v)
    yield


@pytest.fixture()
def fake_llm() -> FakeLLM:
    return FakeLLM(responses=[])


@pytest.fixture()
def default_fake_llm(fake_llm) -> FakeLLM:
    controlflow.defaults.model = fake_llm
    return fake_llm
