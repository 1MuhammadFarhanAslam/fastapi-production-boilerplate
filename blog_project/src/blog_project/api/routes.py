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

@router.get("/")
async def read_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import func
    
    # Get total count
    count_query = select(func.count(Post.id))
    total = await db.scalar(count_query)
    
    # Get paginated posts
    query = select(Post).offset(skip).limit(limit)
    result = await db.execute(query)
    posts = result.scalars().all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": posts
    }

@router.get("/{post_id}", response_model=PostResponse) 
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"User {current_user.email} creating post")
    new_post = Post(title=post.title, content=post.content, published=post.published, author_id=current_user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    logger.info(f"Post created successfully with id: {new_post.id}")
    return new_post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    post.title = post_update.title
    post.content = post_update.content
    post.published = post_update.published
    await db.commit()
    await db.refresh(post)
    logger.info(f"Post {post_id} updated by {current_user.email}")
    return post

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    await db.delete(post)
    await db.commit()
    logger.info(f"Post {post_id} deleted by {current_user.email}")
    return {"message": "Post deleted successfully"}