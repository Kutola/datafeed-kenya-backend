# Newsfeed Kenya API

A RESTful API powering a news platform that gives journalists the ability to create, manage, and publish news articles. Built with FastAPI and PostgreSQL.


## Features

- JWT authentication — secure login and token-based access control
- Article management — create, read, update, and delete news articles
- User management — journalist accounts with role-based ownership
- Schema migrations — Alembic-managed database versioning
- Automated tests — 16 pytest tests covering all endpoints and edge cases


## Tech Stack

language: Python
Framework: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
Migrations: Alembic
Authentication: JWT (python-jose) + bcrypt
Validation: Pydantic v2 
Testing: Pytest + TestClient
Server: Uvicorn


## Project Structure

```
newsfeed_crud/
├── app/
│   ├── routers/
│   │   ├── article.py       # Article CRUD endpoints
│   │   ├── users.py         # User registration and retrieval
│   │   └── auth.py          # Login and token generation
│   ├── models/
│   │   └── models.py        # SQLAlchemy models
│   ├── schemas/
│   │   ├── article_schemas.py
│   │   └── user_schemas.py
│   ├── utils/
│   │   └── auth.py          # Password hashing and JWT utilities
│   ├── dependencies/
│   │   └── oauth2.py        # OAuth2 token scheme
│   ├── database.py          # Database connection and session
│   ├── config.py            # Environment settings via Pydantic
│   └── main.py              # App entry point
├── alembic/
│   └── versions/            # Migration history
├── tests/
│   ├── conftest.py          # Fixtures and test database setup
│   ├── test_articles.py
│   ├── test_auth.py
│   └── test_users.py
├── alembic.ini
├── requirements.txt
└── .env
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

Step 1. Clone the repository**

git clone https://github.com/your-username/newsfeed_crud.git
cd newsfeed_crud


Step 2. Create and activate a virtual environment
bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

Step 3. Install dependencies
pip install -r requirements.txt


Step 4. Set up environment variables
Create a `.env` file in the project root:

env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/newsfeed
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


Step 5. Run database migrations
alembic upgrade head

Step 6. Start the server
uvicorn app.main:app --reload

The API will be available at `http://localhost:8000`

Interactive docs at `http://localhost:8000/docs`


## API Endpoints

### Authentication
Method: POST 
Endpoint:  `/auth/login`
Description: Login and receive JWT token
Auth Required: No


### Users

Method: POST  GET  GET 
Endpoint: `/users/`   `/users/`  `/users/{id}`  
Description: Register a new USER account,  List all users,  Get a user by ID 
Auth Required: No  No  No


### Articles

Method | Endpoint         | Description           | Auth Required 
POST   | `/articles/`     | Create a new article  | Yes 
GET    | `/articles/`     | List all articles     | No 
GET    | `/articles/{id}` | Get an article by ID  | No 
PUT    | `/articles/{id}` | Update an article     | Yes (owner only) 
DELETE | `/articles/{id}` | Delete an article     | Yes (owner only) 

---

## Running Tests

Create a test database first:

```sql
CREATE DATABASE newsfeed_test;
```

Then run the full test suite:

```bash
pytest tests/ -v
```

Expected output: **16 passed**

---

## Environment Variables

| Variable                      | Description 

| `DATABASE_URL`                | PostgreSQL connection string 
| `SECRET_KEY`                  | Secret key for JWT signing 
| `ALGORITHM`                   | JWT algorithm (use `HS256`) 
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry duration in minutes 

---

## Author

Built by Mike Kutola

X: [@Mike_kutola](https://x.com/Mike_kutola)