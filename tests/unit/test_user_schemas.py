
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.schemas import UserCreate, UserRead


def test_valid_user():
    user = UserCreate(
        username="feiyang",
        email="fei@example.com",
        password="SecurePassword123!",
    )

    assert user.username == "feiyang"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="feiyang",
            email="invalid-email",
            password="SecurePassword123!",
        )


def test_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="feiyang",
            email="fei@example.com",
            password="short",
        )


def test_invalid_username():
    with pytest.raises(ValidationError):
        UserCreate(
            username="invalid username!",
            email="fei@example.com",
            password="SecurePassword123!",
        )


def test_user_read_excludes_password():
    db_user = SimpleNamespace(
        id=1,
        username="feiyang",
        email="fei@example.com",
        password_hash="some_hash",
        created_at=datetime.now(timezone.utc),
    )

    response = UserRead.model_validate(db_user)
    data = response.model_dump()

    assert "password" not in data
    assert "password_hash" not in data
