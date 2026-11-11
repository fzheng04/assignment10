# IS601 Module 10 — Secure User Model and CI/CD

This project extends my previous FastAPI calculator application by implementing secure user registration using SQLAlchemy, Pydantic, and PostgreSQL. It also incorporates password hashing, automated unit and integration tests, Docker containerization, and a GitHub Actions CI/CD pipeline.

## Features

- **FastAPI Calculator:** Supports addition, subtraction, multiplication, and division.
- **SQLAlchemy User Model:** Stores usernames, emails, password hashes, and account creation timestamps in PostgreSQL.
- **Pydantic Validation:** Validates registration information and prevents sensitive password data from appearing in API responses.
- **Password Security:** Uses Argon2 to securely hash and verify passwords.
- **Database Constraints:** Enforces unique usernames and email addresses.
- **Automated Testing:** Includes unit, integration, and end-to-end tests.
- **Docker Compose:** Runs FastAPI, PostgreSQL, and pgAdmin in separate containers.
- **CI/CD:** Uses GitHub Actions for automated testing, Trivy vulnerability scanning, and Docker Hub deployment.

## Technologies

Python, FastAPI, SQLAlchemy, Pydantic, PostgreSQL, Argon2, pytest, Playwright, Docker, Docker Compose, GitHub Actions, Trivy

## Running the Application

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.10+ for local development, with compatible dependencies installed

### Setup

Clone the repository:

```bash
git clone https://github.com/fzheng04/assignment10.git
cd assignment10
```

Build and start the containers:

```bash
docker compose up -d --build
```

The application will be accessible at:

| Service | URL |
|---|---|
| FastAPI Calculator | http://localhost:8000 |
| Swagger API Documentation | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |

The database tables are initialized automatically when the application starts.

Stop the containers with:

```bash
docker compose down
```

The PostgreSQL volume is preserved when stopping the containers normally.

## User Registration

The application provides a `POST /users` endpoint.

Example request:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePassword123!"
}
```

A successful request returns HTTP `201 Created` with the user's ID, username, email, and creation timestamp.

Passwords are hashed using Argon2 before being stored in PostgreSQL. The API response does not expose passwords or password hashes.

Duplicate usernames or emails return HTTP `409 Conflict`. Invalid registration data is rejected through Pydantic validation.

## Database Model

The SQLAlchemy `User` model includes:

| Column | Description |
|---|---|
| `id` | Primary key |
| `username` | Unique, required username |
| `email` | Unique, required email |
| `password_hash` | Securely hashed password |
| `created_at` | Automatically generated timestamp |

## Running Tests Locally

### Unit Tests

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Run unit tests:

```bash
python3 -m pytest tests/unit/ -v
```

### PostgreSQL Integration Tests

Start the application and database:

```bash
docker compose up -d --build
```

Run the integration tests inside the FastAPI container:

```bash
docker compose exec \
  -e COVERAGE_FILE=/tmp/module10-coverage \
  web python3 -m pytest tests/integration/ -v
```

Run unit and integration tests together:

```bash
docker compose exec \
  -e COVERAGE_FILE=/tmp/module10-coverage \
  web python3 -m pytest tests/unit/ tests/integration/ -v
```

The tests cover password hashing and verification, Pydantic validation, user registration, database persistence, duplicate usernames and emails, and safe API responses.

The project also retains end-to-end tests from the earlier calculator application.

## CI/CD Pipeline

GitHub Actions automatically runs when changes are pushed to the `main` branch.

The pipeline consists of three jobs:

1. **Test:** Installs dependencies, starts PostgreSQL, initializes database tables, and runs unit, integration, and end-to-end tests.
2. **Security:** Builds the Docker image and scans it with Trivy for high- and critical-severity vulnerabilities.
3. **Deploy:** Builds and pushes the Docker image to Docker Hub after successful testing and security scanning.

Docker Hub credentials are managed through GitHub Actions repository secrets.

## Docker Hub

**Docker Hub Repository:** https://hub.docker.com/r/fzheng04/601_module10

Pull the published image:

```bash
docker pull fzheng04/601_module10:latest
```

The application image requires a PostgreSQL database connection, configured through the `DATABASE_URL` environment variable.

## Security

- Passwords are never stored in plaintext.
- Argon2 is used for password hashing.
- Pydantic validates incoming registration data.
- SQLAlchemy enforces database constraints.
- API responses exclude password hashes.
- GitHub Actions secrets protect Docker Hub credentials.
- Trivy scans Docker images for known vulnerabilities.

## Project Development

This repository builds upon my Module 9 FastAPI calculator and PostgreSQL implementation. Module 10 introduces ORM-based database management, secure user registration, automated database testing, and additional deployment security.

The Git commit history documents the project's development, including implementation milestones, testing, bug fixes, and CI/CD improvements.

## Author

Feiyang Zheng  
NJIT — IS601  
Module 10 Assignment