import uuid

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole

# bcrypt silently ignores/truncates input past 72 bytes, so the cap must be enforced here.
PASSWORD_MAX_LENGTH = 72


class BusinessSignup(BaseModel):
    business_name: str
    owner_email: EmailStr
    owner_password: str = Field(min_length=8, max_length=PASSWORD_MAX_LENGTH)
    owner_full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=PASSWORD_MAX_LENGTH)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}
