from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from blog_project.core.config import settings
from blog_project.db.session import engine
from blog_project.db.base import Base
from blog_project.api import routes, users, auth, admin, user_profile

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Auto-create tables on startup (For Dev only)
@asynccontextmanager
async def lifespan(app: FastAPI):
    from blog_project.models import models
    logger.info("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(user_profile.router, prefix=f"{settings.API_V1_STR}/profile", tags=["User Profile"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(routes.router, prefix=f"{settings.API_V1_STR}/posts", tags=["Posts"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Blog API"}