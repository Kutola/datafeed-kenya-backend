def test_create_article(authorized_client):
    response = authorized_client.post("/articles/", json={
        "title": "Crazy",
        "content": "We are leaving in a crazy world"
    })
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == "Crazy"
    #assert "id" in data

def test_create_article_unauthenticated(client):
    response = client.post("/articles/", json={
        "title": "Article",
        "content": "This is my first article"
    })    
    assert response.status_code == 401

def test_get_all_articles(client): # Public - no auth needed
    response = client.get("/articles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_article(authorized_client):
    create_response = authorized_client.post("/articles/", json={
        "title": "Test Article",
        "content": "Some content"
    })
    article_id = create_response.json()["id"]
    response = authorized_client.get(f"/articles/{article_id}")
    assert response.status_code == 200

def test_get_article_not_found(client):
    response = client.get("/articles/1234") 
    assert response.status_code == 404   

def test_update_article(authorized_client):
    # Create an article as James
    create_response = authorized_client.post("/articles/", json={
        "title": "Original",
        "content": "This is the original article"
    }) 
    article_id = create_response.json()["id"]

    # Update it
    response = authorized_client.put(f"/articles/{article_id}", json={
        "title": "Updated",
        "content": "This is the updated article"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

def test_update_article_unauthenticated(client):
    response = client.put("/articles/1", json={
        "title": "Unauthenticated",
        "content": "You are unauthenticated"
    })    
    assert response.status_code == 401

def test_delete_article_unauthenticated(client):
    response = client.delete("/articles/1")
    assert response.status_code == 401    

def test_delete_other_users_articles(client):
    # Create user A and their article
    client.post("/users", json={
        "name": "User A",
        "role": "author",
        "email": "usera@test.com",
        "password": "usera123",
        "phone": "0712345678"
    })
    login_a = client.post("auth/login", data={
        "username": "usera@test.com",
        "password": "usera123"
    })
    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    create_response = client.post("/articles/", json={
        "title": "User A article",
        "content": "The article belongs to user A"
    }, headers=headers_a)
    article_id = create_response.json()["id"]

    # Create user B and try to delete user A's article
    client.post("/users", json={
        "name": "User B",
        "role": "Writer",
        "email": "userb@test.com",
        "password": "password123",
        "phone": "0712345679"
    })
    login_b = client.post("/auth/login", data={
        "username": "userb@test.com",
        "password": "password123"
    })
    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    #User B attempts to delete user A's article
    response = client.delete(f"/articles/{article_id}", headers=headers_b)
    assert response.status_code == 403
