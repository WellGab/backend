from fastapi import status
from fastapi.testclient import TestClient
import pytest

from app.utils.setup import config as cg
from app.main import app
from .conftest import TestConfig


client = TestClient(app)

@pytest.mark.parametrize("authorized", [
    (True),
    (False),
])
def test_create_chat(test_user, authorized):
    data = {
        "topic": "new chat",
    }
    
    if (authorized):
        headers = {"Authorization": f'Bearer {test_user["token"]}'}

        response = client.post(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats', headers=headers, json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successful"
        assert isinstance(schema["data"], dict)
        assert isinstance(schema["data"]["id"], str)
        assert isinstance(schema["data"]["topic"], str)
        assert schema["data"]["topic"] == data["topic"]
    else:   
        response = client.post(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats', json=data)
        schema = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"


@pytest.mark.parametrize("authorized", [
    (True),
    (False),
])
def test_get_chats(test_user, authorized):
    if (authorized):
        headers = {"Authorization": f'Bearer {test_user["token"]}'}

        response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats', headers=headers)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successful"
        assert isinstance(schema["data"], list)
    else: 
        response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats')
        schema = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"


@pytest.mark.parametrize("authorized", [
    (True),
    (False),
])
def test_create_anon_chat(config: TestConfig, authorized):
    data = {
        "uid": config.uid,
        "topic": "new chat",
    }

    if (authorized):
        response = client.post(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats-anon', json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successful"
        assert isinstance(schema["data"], dict)
        assert isinstance(schema["data"]["id"], str)
        assert isinstance(schema["data"]["topic"], str)
        assert schema["data"]["topic"] == data["topic"]
    else:
        response = client.post(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats-anon', json=data)
        schema = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "sign up to create more chats"


@pytest.mark.parametrize("valid_chat", [
    (True),
    (False),
])
def test_get_chat(test_user, valid_chat):
    headers = {"Authorization": f'Bearer {test_user["token"]}'}
    if (valid_chat):
        response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats', headers=headers)
        schema = response.json()
        chat_id = schema["data"][0]["id"]

        response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/{chat_id}', headers=headers)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Successful"
        assert isinstance(schema["data"], dict)
    else:
        response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/6565089f2ed90d8e1d392b55', headers=headers)
        schema = response.json()
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "chat not found"



@pytest.mark.parametrize("authorized, valid_chat", [
    (True, True),
    (True, False),
    (False, False)
])
def test_update_chat(test_user, authorized, valid_chat):
    data = {
        "topic": "malaria",
    }
    if (authorized):
        headers = {"Authorization": f'Bearer {test_user["token"]}'}
        print("Test token: ", test_user)
        if (valid_chat):
            response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats', headers=headers)
            schema = response.json()
            chat_id = schema["data"][0]["id"]

            response = client.patch(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/{chat_id}', headers=headers, json=data)
            schema = response.json()

            assert response.status_code == status.HTTP_200_OK
            assert isinstance(schema["message"], str)
            assert schema["message"] == "Successful"
            assert isinstance(schema["data"], dict)
        else:
            response = client.patch(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/6565089f2ed90d8e1d392b55', headers=headers, json=data)
            schema = response.json()
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert isinstance(schema["detail"], str)
            assert schema["detail"] == "chat not found"
    else:
        response = client.patch(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/6565089f2ed90d8e1d392b55', json=data)    
        schema = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"


@pytest.mark.parametrize("authorized, valid_chat", [
    (True, True),
    (True, False),
    (False, False)
])
def test_delete_chat(test_user, authorized, valid_chat):
    if (authorized):
        headers = {"Authorization": f'Bearer {test_user["token"]}'}
        print("Test token: ", test_user)
        if (valid_chat):
            response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats', headers=headers)
            schema = response.json()
            chat_id = schema["data"][0]["id"]

            response = client.delete(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/{chat_id}', headers=headers)
            schema = response.json()

            assert response.status_code == status.HTTP_200_OK
            assert isinstance(schema["message"], str)
            assert schema["message"] == "Successful"
        else:
            response = client.delete(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/6565089f2ed90d8e1d392b55', headers=headers)
            schema = response.json()
            print("Schema-2: ", schema)
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert isinstance(schema["detail"], str)
            assert schema["detail"] == "chat not found"
    else:
        response = client.delete(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/6565089f2ed90d8e1d392b55')    
        schema = response.json()
        print("Schema-3: ", schema)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"


@pytest.mark.parametrize("authorized", [
    (True),
    (False)
])
def test_send_message(test_user, authorized):
    data = {
        "message": "Hello"
    }

    if (authorized):
        headers = {"Authorization": f'Bearer {test_user["token"]}'}
        print("Test token: ", test_user)
            
        response = client.get(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats', headers=headers)
        schema = response.json()
        chat_id = schema["data"][0]["id"]

        response = client.post(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/{chat_id}/messages', headers=headers, json=data)
        schema = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(schema["message"], str)
        assert schema["message"] == "Received"
        assert isinstance(schema["data"], str)
    else:
        response = client.post(f'{cg.ROOT_PATH}{cg.CHAT_URL}/chats/6565089f2ed90d8e1d392b55/messages', json=data)    
        schema = response.json()
        print("Schema-3: ", schema)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert isinstance(schema["detail"], str)
        assert schema["detail"] == "Not authenticated"