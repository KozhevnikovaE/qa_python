import pytest

@pytest.fixture
def collector():
    return BooksCollector()