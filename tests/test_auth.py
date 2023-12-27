from fastapi import status
from fastapi.testclient import TestClient
import pytest

from app.utils.setup import config as cg
from app.main import app
from .conftest import TestConfig


client = TestClient(app)

def test_create_user(config: TestConfig):
    data = {
        "email": config.username,
        "password": config.password,
    }
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/sign-up', json=data)
    schema = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(schema["data"], dict)
    assert isinstance(schema["data"]["user_id"], str)
    assert isinstance(schema["data"]["token"], str)

def test_create_user_twice(config: TestConfig):
    data = {
        "email": config.username,
        "password": config.password,
    }
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/sign-up', json=data)
    schema = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(schema["detail"], str)
    assert schema["detail"] == "Email already registered"

def test_token(config: TestConfig):
    data = {
        "username": config.username,
        "password": config.password,
    }
    
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/token', data=data)
    schema = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert schema["token_type"] == "bearer"
    assert isinstance(schema["access_token"], str)


def test_login(config: TestConfig):
    data = {
        "email": config.username,
        "password": config.password,
    }
    
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/login', json=data)
    schema = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(schema["data"], dict)
    assert isinstance(schema["data"]["user_id"], str)
    assert isinstance(schema["data"]["token"], str)

def test_login_incorrect_password(config: TestConfig):
    data = {
        "email": config.username,
        "password": "config.password",
    }
    
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/login', json=data)
    schema = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(schema["detail"], str)
    assert schema["detail"] == "Couldn't not log in user"

def test_social_auth_invalid_token():
    data = {
        "token": "",
    }
    
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/social-auth', json=data)
    schema = response.json()

    print("Schema: ", schema)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert isinstance(schema["detail"], dict)
    assert schema["detail"]["message"] == "invalid_claims"
    assert schema["detail"]["description"] == "Incorrect claims. Please, check the audience and issuer."

def test_user_subscription(config: TestConfig):
    data = {
        "email": config.username,
    }
    
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/subscribe', json=data)
    schema = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(schema["message"], str)
    assert schema["message"] == "Successfully Subscribed"

def test_user_subscription_already(config: TestConfig):
    data = {
        "email": config.username,
    }
    
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/subscribe', json=data)
    schema = response.json()

    print("Schema: ", schema)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(schema["message"], str)
    assert schema["message"] == "Already Subscribed"

@pytest.mark.parametrize("authorized", [
    (True),
    (False),
])
def test_user_settings(headers, authorized):
    data = {
        "ninety_days_chat_limit": True,
    }

    if authorized:
        response = client.patch(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/setting', headers=headers, json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successfully updated settings"
    else:
        response = client.patch(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/setting', json=data)
        schema = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"

@pytest.mark.parametrize("authorized", [
    (True),
    (False),
])
def test_user_settings_get(headers, authorized):
    if authorized:
        response = client.get(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/setting', headers=headers)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successful"
    else:
        response = client.get(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/setting')
        schema = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"

@pytest.mark.parametrize("user_exists", [
    (False),
    (True),
])
def test_user_request_password_reset(config: TestConfig, user_exists):
    if user_exists:
        data = {
            "email": config.username,
        }

        response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/password/request-reset', json=data)
        schema = response.json()

        print("Schema: ", schema)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successful"
    else:
        data = {
            "email": "username@gmail.com",
        }
        response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/password/request-reset', json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "user not found"

@pytest.mark.parametrize("request_type", [
    (1),
    (2),
    (3)
])
def test_user_password_reset(config: TestConfig, request_type, password_reset_token):
    if request_type == 1:
        data = {
            "email": "username@gmail.com",
            "token": config.password,
            "new_password": config.password
        }
        
        response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/password/reset', json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "user not found"

    elif request_type == 2:
        data = {
            "email": config.username,
            "token": config.password,
            "new_password": config.password
        }

        response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/password/reset', json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "invalid token"
    elif request_type == 3:
        data = {
            "email": config.username,
            "token": password_reset_token,
            "new_password": config.password
        }

        response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/password/reset', json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "password reset successful"


def test_delete_user_incorrect_password(headers):
    data = {
        "password": "config.password",
    }
    
    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/delete', headers=headers, json=data)
    schema = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(schema["detail"], str)
    assert schema["detail"] == "incorrect password"

@pytest.mark.parametrize("authorized", [
    (False),
    (True),
])
def test_delete_user(config: TestConfig, headers, authorized):
    data = {
        "password": config.password,
    }

    if authorized:
        response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/delete', headers=headers, json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successfully deleted account"
    else:
        response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/user/delete', json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"