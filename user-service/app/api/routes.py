from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.auth_client import AuthClient
from app.core.database import get_db
from app.repositories.profile_repository import ProfileRepository
from app.schemas.user import ProfileResponse

router = APIRouter()


@router.get("/profile", response_model=ProfileResponse)
async def profile(
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    auth_user = await AuthClient.validate(authorization)
    profile_obj = await ProfileRepository.get_by_auth_user_id(db, auth_user["user_id"])

    return {
        "id": auth_user["user_id"],
        "name": profile_obj.name if profile_obj and profile_obj.name else "New User",
        "email": auth_user["email"],
    }
