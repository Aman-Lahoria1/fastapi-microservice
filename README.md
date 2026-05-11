# FastAPI Microservices

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
