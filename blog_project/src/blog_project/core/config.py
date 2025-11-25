from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str = "Blog API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    model_config = ConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    @property
    def DATABASE_URL(self) -> str:
        # Build the Async Postgres Connection String
        user = quote_plus(str(self.POSTGRES_USER))
        password = quote_plus(str(self.POSTGRES_PASSWORD))
        return f"postgresql+asyncpg://{user}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()  # type: ignore[call-arg]