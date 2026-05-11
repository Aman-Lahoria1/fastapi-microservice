from fastapi import APIRouter, Header

from app.clients.auth_client import AuthClient
from app.schemas.user import ProfileResponse


router = APIRouter()


@router.get(
    "/profile",
    response_model=ProfileResponse,
)
async def profile(
    authorization: str | None = Header(default=None),
):
    auth_user = await AuthClient.validate(authorization)

    return {
        "id": auth_user["user_id"],
        "name": "Aman",
        "email": auth_user["email"],
    }
