from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from blog_project.db.session import get_db
from blog_project.models.models import Post, User
from blog_project.schemas.schemas import PostCreate, PostResponse
from blog_project.core.deps import get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
async def read_posts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Post).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"User {current_user.email} creating post")
    
    # Use authenticated user as author
    new_post = Post(title=post.title, content=post.content, published=post.published, author_id=current_user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    logger.info(f"Post created successfully with id: {new_post.id}")
    return new_post