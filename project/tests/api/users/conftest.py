import os
os.environ["DB_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from src.api import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as client:
        return client
