# FastAPI Microservices — Phase 1 + Phase 2 Job Ready Project

This is your original microservices project upgraded into Phase 2.

## What Phase 1 Had

- FastAPI auth-service
- FastAPI user-service
- NGINX gateway
- Docker Compose
- In-memory fake user list
- Basic JWT token generation

## What Phase 2 Adds

- PostgreSQL as the real database
- Redis for token validation cache
- SQLAlchemy Async ORM
- Alembic migrations
- Repository layer
- Service layer
- Proper async DB sessions
- Better JWT validation flow between services

## Architecture Flow

```text
Client
  ↓
NGINX
  ↓
/auth/*  → Auth Service
/users/* → User Service
  ↓
Auth Service → PostgreSQL
Auth Service → Redis
User Service → Auth Service /auth/validate
```

## Folder Structure

```text
fastapi_microservices_phase2_job_ready/
├── docker-compose.yml
├── nginx/
│   └── nginx.conf
├── auth-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_create_users_table.py
│   └── app/
│       ├── main.py
│       ├── api/routes.py
│       ├── core/config.py
│       ├── core/database.py
│       ├── core/redis_client.py
│       ├── core/security.py
│       ├── models/user.py
│       ├── repositories/user_repository.py
│       ├── schemas/auth.py
│       ├── services/auth_service.py
│       └── utils/jwt_handler.py
└── user-service/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py
        ├── api/routes.py
        ├── clients/auth_client.py
        ├── core_config.py
        └── schemas/user.py
```

## Run the Project

From the root folder:

```bash
docker compose build --no-cache
docker compose up
```

## Apply Alembic Migration

Open another terminal:

```bash
docker compose exec auth-service alembic upgrade head
```

This creates the `users` table in PostgreSQL.

## Test Register

```bash
curl -X POST http://localhost/auth/register \
-H "Content-Type: application/json" \
-d '{
  "email": "aman@example.com",
  "password": "password123"
}'
```

## Test Login

```bash
curl -X POST http://localhost/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "aman@example.com",
  "password": "password123"
}'
```

Copy the `access_token`.

## Test Auth Validate

```bash
curl http://localhost/auth/validate \
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Test User Profile Through User Service

```bash
curl http://localhost/users/profile \
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Important Flow Explanation

### Register Flow

```text
POST /auth/register
  ↓
routes.py
  ↓
AuthService.register()
  ↓
UserRepository.get_by_email()
  ↓
PostgreSQL check existing user
  ↓
hash password using Argon2
  ↓
UserRepository.create()
  ↓
Save user in PostgreSQL
```

### Login Flow

```text
POST /auth/login
  ↓
routes.py
  ↓
AuthService.login()
  ↓
Find user from PostgreSQL
  ↓
Verify password
  ↓
Generate JWT token
  ↓
Store token in Redis
  ↓
Return access_token
```

### User Profile Flow

```text
GET /users/profile
  ↓
User Service receives request
  ↓
User Service calls Auth Service /auth/validate
  ↓
Auth Service validates JWT
  ↓
Auth Service first checks Redis
  ↓
If not found in Redis, checks PostgreSQL
  ↓
User Service returns profile
```

## Why PostgreSQL?

In Phase 1, users were stored in memory:

```python
fake_users = []
```

Problem:

- Data is lost after restart
- Not production ready
- Not shared across containers
- Cannot query properly

PostgreSQL solves this by giving durable relational storage.

## Why Redis?

Redis is used for fast token/session lookup.

Instead of always going to PostgreSQL for validation, Auth Service can quickly check Redis.

This improves latency and reduces DB load.

## Why SQLAlchemy Async?

FastAPI supports async request handling.

Async SQLAlchemy allows the DB call to avoid blocking the event loop while waiting for I/O.

This helps with high concurrency.

## Why Alembic?

Alembic manages database schema changes.

For example:

- Create users table
- Add new column
- Rollback migration
- Keep DB schema version-controlled

## Interview Explanation

You can explain this project like this:

> In Phase 1, I had simple FastAPI microservices with NGINX and Docker. In Phase 2, I made it production-oriented by replacing in-memory storage with PostgreSQL, using async SQLAlchemy for non-blocking DB operations, Redis for token caching, and Alembic for database migrations. The Auth Service owns authentication and user persistence, while User Service depends on Auth Service for token validation. This follows microservice separation and clean architecture principles.

## Useful Commands

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f auth-service
```

Enter auth container:

```bash
docker compose exec auth-service bash
```

Run migration:

```bash
docker compose exec auth-service alembic upgrade head
```

Rollback migration:

```bash
docker compose exec auth-service alembic downgrade -1
```

Connect PostgreSQL:

```bash
docker compose exec postgres psql -U postgres -d authdb
```

Check users table:

```sql
select * from users;
```

Connect Redis:

```bash
docker compose exec redis redis-cli
```

Check token keys:

```bash
keys auth_token:*
```
