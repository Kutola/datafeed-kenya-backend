import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Separate test database
TEST_DATABASE_URL = "postgresql://postgres:750369@localhost:5432/newsfeed_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

# Create all tables before tests, drop after
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Override get_db with test session
@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()   
        # Clean all tables after every test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine) 

@pytest.fixture()
def client(db_session):
    def overide_get_db():
        try:
            yield db_session
        finally:
            db_session.close()            

    app.dependency_overrides[get_db] = overide_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()  


@pytest.fixture()
def authorized_client(client):
    # Create user
    client.post("/users", json={
        "name": "James",
        "role": "Manager",
        "email": "james@test.com",
        "password": "james123",
        "phone": "0712345678"
    })          

    # Login
    login_response = client.post("/auth/login", data={
        "username": "james@test.com",
        "password": "james123"
    })
    token = login_response.json()["access_token"]

    # Attach token to all requests from this client
    client.headers.update({"Authorization": f"Bearer {token}"})

    return client