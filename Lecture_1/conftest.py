import pytest

@pytest.fixture()
def coord1():
    return "37.7891838", "-122.4033522"

@pytest.fixture()
def test1():
    return "One Montgomery Tower"