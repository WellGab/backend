from fastapi import status
from fastapi.testclient import TestClient

from app.utils.const import (
    AUTH_URL,
)
from app.main import app


client = TestClient(app)


def test_login(config):
    response = client.post(f'/{AUTH_URL}/login')

    assert response.status_code == status.HTTP_200_OK