from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from blog_project.db.session import get_db
from blog_project.models.models import User, Post
from blog_project.schemas.schemas import UserResponse, PostResponse
from blog_project.core.deps import get_current_admin

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    logger.info(f"Admin {admin.email} fetching all users")
    result = await db.execute(select(User))
    return result.scalars().all()

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    logger.info(f"Admin {admin.email} deleting user {user_id}")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}

@router.get("/posts", response_model=List[PostResponse])
async def get_all_posts(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    logger.info(f"Admin {admin.email} fetching all posts")
    result = await db.execute(select(Post))
    return result.scalars().all()

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    logger.info(f"Admin {admin.email} deleting post {post_id}")
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted successfully"}
