from pydantic import BaseModel, EmailStr


class ProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
