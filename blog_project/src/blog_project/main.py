from fastapi import FastAPI
from contextlib import asynccontextmanager
from blog_project.core.config import settings
from blog_project.db.session import engine
from blog_project.db.base import Base
from blog_project.api import routes

# Auto-create tables on startup (For Dev only)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Import models to ensure they are registered
    from blog_project.models import models
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(routes.router, prefix=f"{settings.API_V1_STR}/posts", tags=["Posts"])

@app.get("/")
def root():
    return {"message": "Welcome to the Blog API"}