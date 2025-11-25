from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from blog_project.db.session import get_db
from blog_project.models.models import User
from blog_project.schemas.schemas import UserCreate, UserResponse
from blog_project.core.security import get_password_hash

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating user with email: {user.email}")
    
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        logger.warning(f"User with email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password),
        is_active=True,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.info(f"User created successfully with id: {new_user.id}")
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
