# Assignment 9: Raw SQL in pgAdmin with Docker Compose

A FastAPI calculator app running with PostgreSQL and pgAdmin in Docker Compose. The assignment practices raw SQL: creating tables, inserting, querying, updating and deleting records, and working with a one-to-many relationship.

## What's in this repo

| File | Purpose |
|---|---|
| `docker-compose.yml` | Runs FastAPI, PostgreSQL and pgAdmin |
| `assignment9.sql` | All SQL commands from the assignment |
| `Assignment9_Screenshots.docx` | Screenshots of every step with captions |
| `.trivyignore` | Known issues in pinned dependencies, skipped by the security scan |
| `.github/workflows/test.yml` | CI/CD: tests, Trivy scan, Docker Hub deploy |

## Run it

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| FastAPI app | http://localhost:8000 |
| pgAdmin | http://localhost:5050 |

Stop it with `Ctrl+C`. Use `docker compose down -v` only if you want to delete the database data.

## Connect pgAdmin to Postgres

1. Log in to pgAdmin with `admin@example.com` and `admin`.
2. Right-click **Servers**, then **Register**, then **Server**.
3. On the **Connection** tab, enter:
   - Host: `db`
   - Port: `5432`
   - Database: `fastapi_db`
   - Username: `postgres`
   - Password: `postgres`
4. Open the **Query Tool** on `fastapi_db` and run the commands from `assignment9.sql`.

Use `db` as the host, not `localhost`, because pgAdmin runs inside Docker and reaches Postgres by its service name.

## Database design

- `users`: `id`, `username`, `email`, `created_at`
- `calculations`: `id`, `operation`, `operand_a`, `operand_b`, `result`, `timestamp`, `user_id`
- One user can have many calculations. `calculations.user_id` is a foreign key to `users.id` with `ON DELETE CASCADE`, so deleting a user also deletes their calculations.

## SQL steps covered

1. Create both tables
2. Insert two users and three calculations
3. Select all users, all calculations, and a JOIN of the two
4. Update the result of calculation 1 to 6
5. Delete calculation 2

Screenshots of each step are in `Assignment9_Screenshots.docx`.

## Troubleshooting

**Postgres container exits with a "in 18+" data directory error.**
Newer Postgres images need the volume mounted at `/var/lib/postgresql`, not `/var/lib/postgresql/data`. This repo already uses the correct path. If you see the error on an older copy, change the mount and run `docker compose down -v`.

**"relation users already exists" in pgAdmin.**
The app created the table on startup. Run `DROP TABLE IF EXISTS calculations CASCADE;` and `DROP TABLE IF EXISTS users CASCADE;`, then run the create statements again.

## CI/CD

GitHub Actions runs the unit, integration and end-to-end tests, scans the Docker image with Trivy, then builds and pushes the image to Docker Hub as `fzheng04/601_module9`. Vulnerabilities in pinned course dependencies are listed in `.trivyignore`.