
from pwdlib import PasswordHash

# Use the recommended password hashing algorithm (Argon2)
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plaintext password securely."""
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Check whether a password matches a stored hash."""
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )
