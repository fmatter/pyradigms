import pytest
from pathlib import Path


@pytest.fixture
def data():
    return Path(__file__).parent / "data"
