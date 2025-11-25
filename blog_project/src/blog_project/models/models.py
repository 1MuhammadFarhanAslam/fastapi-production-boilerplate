from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from blog_project.db.base import Base
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Boolean

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationship to Post
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("blog_project.models.user.User", back_populates="posts")