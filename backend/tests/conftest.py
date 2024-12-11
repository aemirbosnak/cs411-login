import pytest
import mongomock
from config import Config
from app import app as flask_app

@pytest.fixture(scope="function")
def mock_db():
    # Replace the mongo_db with a mongomock instance for testing
    Config.mongo_db = mongomock.MongoClient().mydb
    yield
    # After tests complete, no cleanup needed

@pytest.fixture(scope="function")
def test_client(mock_db):
    with flask_app.test_client() as client:
        yield client
