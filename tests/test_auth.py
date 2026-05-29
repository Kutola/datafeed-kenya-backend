def test_login_success(client):
    # Create user first
    client.post("/users", json={
        "name": "Ken",
        "role": "CTO",
        "email": "ken@test.com",
        "password": "ken123",
        "phone": "0712345678"
    })

    # Login the user
    response = client.post("auth/login", data={
        "username": "ken@test.com",
        "password": "ken123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/users", json={
        "name": "Ken",
        "role": "CTO",
        "email": "ken@test.com",
        "password": "ken123",
        "phone": "0712345678"
    })

    # Login the user
    response = client.post("auth/login", data={
        "username": "ken@test.com",
        "password": "123"
    })
    assert response.status_code == 403   


def test_login_nonexistent_user(client):
    response = client.post("auth/login", data={
        "username": "nancy@test.com",
        "password": "password123"
    })    
    assert response.status_code == 403
