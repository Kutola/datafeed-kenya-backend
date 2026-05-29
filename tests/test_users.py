from app.schemas.user_schemas import FetchUser

def test_create_user(client):
    response = client.post("/users", json={
        "name": "Mike",
        "role": "Engineer",
        "email": "mike@test.com",
        "password": "mike123",
        "phone": "0703165143"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "mike@test.com"
    assert data["name"] == "Mike"
    assert "password" not in data #dont expose data in response


def test_create_user_duplicate_email(client):
    # Create first user
    client.post("/users", json={
        "name": "Brandon",
        "role": "Manager",
        "email": "brandon@test.com",
        "password": "password321",
        "phone": "0712345678"
    })   
    # Try creating second user with same email
    response = client.post("/users", json={
        "name": "Sophy",
        "role": "Manager",
        "email": "brandon@test.com",
        "password": "password321",
        "phone": "0712345671"
    })

    assert response.status_code == 409

def test_get_user_not_found(client):
    response = client.get("/users/364")
    assert response.status_code == 404

def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)    