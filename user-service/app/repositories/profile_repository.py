from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.profile import UserProfile


class ProfileRepository:
    @staticmethod
    async def get_by_auth_user_id(
        db: AsyncSession, auth_user_id: int
    ) -> UserProfile | None:
        result = await db.execute(
            select(UserProfile).where(UserProfile.auth_user_id == auth_user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def upsert_from_registered_event(
        db: AsyncSession, user_id: int, email: str
    ) -> UserProfile:
        profile = await ProfileRepository.get_by_auth_user_id(db, user_id)
        if profile:
            return profile
        profile = UserProfile(auth_user_id=user_id, email=email, name=None)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile
