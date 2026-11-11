
from app.security import hash_password, verify_password


def test_password_is_hashed():
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$argon2id$")


def test_correct_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_incorrect_password():
    hashed = hash_password("CorrectPassword123!")

    assert verify_password("WrongPassword", hashed) is False


def test_same_password_different_hash():
    password = "SecurePassword123!"

    first = hash_password(password)
    second = hash_password(password)

    assert first != second
