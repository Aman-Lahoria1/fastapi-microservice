from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_client import redis_client
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.jwt_handler import create_access_token, decode_access_token
from app.events.kafka import kafka_producer


class AuthService:

    @staticmethod
    async def register(db: AsyncSession, payload):
        existing_user = await UserRepository.get_by_email(db, payload.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

        user = User(
            email=payload.email,
            password=hash_password(payload.password),
        )

        created_user = await UserRepository.create(db, user)

        await kafka_producer.publish(
            topic="user.registered",
            key=str(created_user.id),
            event={
                "event_type": "user.registered",
                "user_id": created_user.id,
                "email": created_user.email,
            },
        )

        return created_user

    @staticmethod
    async def login(db: AsyncSession, payload):
        user = await UserRepository.get_by_email(db, payload.email)

        if not user or not verify_password(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
            }
        )

        # Redis stores token -> user id for quick validation.
        # In real production, you can also use this for logout/token blacklist.
        await redis_client.setex(
            f"auth_token:{token}",
            3600,
            str(user.id),
        )

        return token

    @staticmethod
    async def validate_token(db: AsyncSession, token: str):
        cached_user_id = await redis_client.get(f"auth_token:{token}")

        payload = decode_access_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        user_id = int(payload["user_id"])

        if cached_user_id:
            return {
                "valid": True,
                "source": "redis",
                "user_id": user_id,
                "email": payload["email"],
            }

        user = await UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        await redis_client.setex(
            f"auth_token:{token}",
            3600,
            str(user.id),
        )

        return {
            "valid": True,
            "source": "postgres",
            "user_id": user.id,
            "email": user.email,
        }
