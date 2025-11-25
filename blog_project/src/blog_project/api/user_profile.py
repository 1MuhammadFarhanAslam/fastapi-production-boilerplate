from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from blog_project.db.session import get_db
from blog_project.models.models import User
from blog_project.schemas.schemas import UserResponse, PasswordChange
from blog_project.core.deps import get_current_active_user
from blog_project.core.security import verify_password, get_password_hash

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    logger.info(f"User {current_user.email} fetching profile")
    return current_user

@router.put("/change-password")
async def change_password(
    password_data: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"User {current_user.email} changing password")
    
    if not verify_password(password_data.old_password, current_user.password_hash):
        logger.warning(f"Failed password change for {current_user.email}: incorrect old password")
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    current_user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()
    logger.info(f"Password changed successfully for {current_user.email}")
    
    return {"message": "Password changed successfully"}
