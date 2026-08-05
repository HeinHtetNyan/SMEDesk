from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.business import Business
from app.models.user import User, UserRole
from app.schemas.auth import BusinessSignup, LoginRequest, Token, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token)
async def signup(payload: BusinessSignup, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(User).where(User.email == payload.owner_email))
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    business = Business(name=payload.business_name)
    db.add(business)
    await db.flush()

    owner = User(
        business_id=business.id,
        email=payload.owner_email,
        hashed_password=hash_password(payload.owner_password),
        full_name=payload.owner_full_name,
        role=UserRole.OWNER,
    )
    db.add(owner)
    await db.commit()

    token = create_access_token(str(owner.id), str(business.id), owner.role.value)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user or not user.is_active or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(str(user.id), str(user.business_id), user.role.value)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
