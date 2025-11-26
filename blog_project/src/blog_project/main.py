from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from blog_project.core.config import settings
from blog_project.db.session import engine
from blog_project.db.base import Base
from blog_project.api import routes, users, auth, admin, user_profile
from blog_project.core.exceptions import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
from blog_project.core.security_headers import SecurityHeadersMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Auto-create tables on startup (For Dev only)
@asynccontextmanager
async def lifespan(app: FastAPI):
    from blog_project.models.models import User, UserRole
    from blog_project.core.security import get_password_hash
    from blog_project.db.session import AsyncSessionLocal
    from sqlalchemy import select
    
    logger.info("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create default admin if not exists
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
        if not result.scalar_one_or_none():
            admin = User(
                email=settings.ADMIN_EMAIL,
                password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                is_active=True,
                role=UserRole.ADMIN
            )
            session.add(admin)
            await session.commit()
            logger.info(f"Default admin created: {settings.ADMIN_EMAIL}")
    
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Security Headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(user_profile.router, prefix=f"{settings.API_V1_STR}/profile", tags=["User Profile"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(routes.router, prefix=f"{settings.API_V1_STR}/posts", tags=["Posts"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Blog API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION
    }