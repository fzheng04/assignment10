
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.database import Base, engine, get_db
from app.models import User
from app.security import verify_password


@pytest.fixture
def client_and_db():
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()

    db = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client, db
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        transaction.rollback()
        connection.close()


def new_user():
    suffix = uuid4().hex[:10]

    return {
        "username": f"user_{suffix}",
        "email": f"{suffix}@example.com",
        "password": "SecurePassword123!",
    }


def test_create_user(client_and_db):
    client, db = client_and_db
    payload = new_user()

    response = client.post("/users", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert data["created_at"] is not None
    assert "password" not in data
    assert "password_hash" not in data

    saved_user = db.query(User).filter_by(
        username=payload["username"]
    ).one()

    assert saved_user.password_hash != payload["password"]
    assert verify_password(
        payload["password"],
        saved_user.password_hash,
    )


def test_duplicate_username(client_and_db):
    client, _ = client_and_db

    original = new_user()
    assert client.post("/users", json=original).status_code == 201

    duplicate = new_user()
    duplicate["username"] = original["username"]

    response = client.post("/users", json=duplicate)

    assert response.status_code == 409


def test_duplicate_email(client_and_db):
    client, _ = client_and_db

    original = new_user()
    assert client.post("/users", json=original).status_code == 201

    duplicate = new_user()
    duplicate["email"] = original["email"]

    response = client.post("/users", json=duplicate)

    assert response.status_code == 409


def test_invalid_email(client_and_db):
    client, _ = client_and_db

    payload = new_user()
    payload["email"] = "not-an-email"

    response = client.post("/users", json=payload)

    # Your existing custom validation handler returns 400.
    assert response.status_code == 400
