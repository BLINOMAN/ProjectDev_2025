import pytest


@pytest.mark.asyncio
def test_create_user(client):
    user_data = {
        "username": "Test User",
        "email": "test@example.com"
    }

    response = client.post("/users/create_user", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == "Test User"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
def test_get_user_by_id(client):
    user_data = {
        "username": "Test User",
        "email": "test@example.com"
    }
    user_response = client.post("/users/create_user", json=user_data)
    assert user_response.status_code == 201
    created_user = user_response.json()
    
    response = client.get(f"/users/{created_user['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_user["id"]
    assert data["username"] == "Test User"


@pytest.mark.asyncio
def test_get_users_list(client):
    response = client.get("/users")

    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert isinstance(data["users"], list)


@pytest.mark.asyncio
def test_update_user(client):  
    user_data = {
        "username": "Original User",
        "email": "original@example.com"
    }
    user_response = client.post("/users/create_user", json=user_data)
    assert user_response.status_code == 201
    created_user = user_response.json()

    
    update_data = {
        "username": "Updated User",
     
    }
    response = client.put(f"/users/{created_user['id']}", json=update_data)

    
    print("Response status:", response.status_code)
    print("Response body:", response.text)

    assert response.status_code == 200  
    data = response.json()
    assert data["username"] == "Updated User"


@pytest.mark.asyncio
def test_delete_user(client):
    user_data = {
        "username": "To Delete",
        "email": "delete@example.com"
    }
    user_response = client.post("/users/create_user", json=user_data)
    assert user_response.status_code == 201
    created_user = user_response.json()

    
    response = client.delete(f"/users/{created_user['id']}")

    assert response.status_code == 204  

    
    get_response = client.get(f"/users/{created_user['id']}")
    assert get_response.status_code == 404