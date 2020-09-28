from glob import glob
import pytest
from run import app as flask_app

def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

