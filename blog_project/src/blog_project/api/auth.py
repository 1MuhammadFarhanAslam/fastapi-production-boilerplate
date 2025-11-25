from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from blog_project.db.session import get_db
from blog_project.models.models import User
from blog_project.schemas.schemas import Token, LoginRequest
from blog_project.core.security import verify_password, create_access_token

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Login attempt for email: {credentials.email}")
    
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        logger.warning(f"Failed login attempt for email: {credentials.email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    logger.info(f"User {user.email} logged in successfully")
    
    return {"access_token": access_token, "token_type": "bearer"}
