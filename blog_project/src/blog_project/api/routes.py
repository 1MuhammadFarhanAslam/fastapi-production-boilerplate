from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from blog_project.db.session import get_db
from blog_project.models.models import Post
from blog_project.schemas.schemas import PostCreate, PostResponse

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
async def read_posts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Post).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    # Hardcoded author_id=1 for prototype until Auth is built
    new_post = Post(**post.model_dump(), author_id=1)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post