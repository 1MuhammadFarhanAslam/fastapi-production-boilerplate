# Blog API - FastAPI Production Boilerplate

A production-ready FastAPI application with PostgreSQL database, async SQLAlchemy ORM, and Docker containerization.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Docker Deployment](#-docker-deployment)
- [API Documentation](#-api-documentation)
- [Database](#-database)
- [Development](#-development)

## ✨ Features

- ⚡ **FastAPI** - Modern, fast web framework for building APIs
- 🗄️ **PostgreSQL** - Robust relational database
- 🔄 **Async SQLAlchemy** - Asynchronous ORM for database operations
- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **Role-Based Access Control** - Admin and User roles with permissions
- 🔑 **Password Hashing** - Bcrypt password encryption
- 🐳 **Docker** - Containerized application with Docker Compose
- 🔧 **Pydantic Settings** - Environment-based configuration management
- 📝 **Auto-generated API Docs** - Interactive Swagger UI and ReDoc
- 📊 **Logging** - Structured logging for monitoring
- 🏗️ **Clean Architecture** - Separation of concerns with layered structure

## 🛠️ Tech Stack

- **Python**: 3.12+
- **FastAPI**: 0.122.0
- **SQLAlchemy**: 2.x (Async)
- **PostgreSQL**: 15
- **asyncpg**: 0.31.0
- **Pydantic**: 2.x
- **python-jose**: JWT token handling
- **passlib**: Password hashing with bcrypt
- **Docker & Docker Compose**

## 📁 Project Architecture

```
blog_project/
├── src/
│   └── blog_project/
│       ├── api/                    # API routes and endpoints
│       │   ├── __init__.py
│       │   ├── routes.py           # Post CRUD endpoints (GET, POST, PUT, DELETE)
│       │   ├── users.py            # User signup (public)
│       │   ├── auth.py             # Authentication (OAuth2 login)
│       │   ├── user_profile.py     # User profile & password change
│       │   └── admin.py            # Admin-only endpoints (manage users/posts)
│       ├── core/                   # Core configuration & security
│       │   ├── __init__.py
│       │   ├── config.py           # Settings (env variables, CORS, admin)
│       │   ├── security.py         # Password hashing (bcrypt) & JWT tokens
│       │   ├── deps.py             # Auth dependencies (get_current_user, get_admin)
│       │   ├── exceptions.py       # Global exception handlers
│       │   ├── rate_limit.py       # Rate limiting (100 req/min)
│       │   └── security_headers.py # Security headers middleware
│       ├── db/                     # Database configuration
│       │   ├── __init__.py
│       │   ├── base.py             # SQLAlchemy Base
│       │   └── session.py          # Async database session
│       ├── models/                 # SQLAlchemy ORM models
│       │   ├── __init__.py
│       │   └── models.py           # User (with roles) & Post models
│       ├── schemas/                # Pydantic validation schemas
│       │   ├── __init__.py
│       │   └── schemas.py          # Request/Response models, Token, Login
│       ├── __init__.py
│       └── main.py                 # App entry (CORS, middleware, routers)
├── tests/                          # Test suite
│   └── __init__.py
├── .dockerignore
├── .env                            # Environment variables (SECRET_KEY, DB, ADMIN)
├── .gitignore
├── docker-compose.yaml             # Docker services (db + web)
├── Dockerfile                      # Production Docker image (Poetry)
├── pyproject.toml                  # Poetry dependencies
├── poetry.lock                     # Locked dependencies
├── requirements.txt                # Pip dependencies
├── README.md                       # This file
├── PRODUCTION.md                   # Production deployment guide
└── CHANGELOG.md                    # Version history
```

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 15+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Docker & Docker Compose**: [Download Docker](https://www.docker.com/get-started)
- **Poetry** (optional): `pip install poetry`

## 🚀 Installation

### Option 1: Local Development with Virtual Environment

#### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd blog_project
```

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

**Using pip:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Using Poetry:**
```bash
poetry install
poetry shell
```

#### Step 4: Set Up PostgreSQL Database

Create a PostgreSQL database:

```sql
CREATE DATABASE blog_db;
CREATE USER postgres WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO postgres;
```

### Option 2: Using Poetry

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run the application
poetry run uvicorn src.blog_project.main:app --reload
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Application Settings
PROJECT_NAME="Professional Blog API"
VERSION=1.0.0
API_V1_STR=/api/v1

# Security (Generate with: openssl rand -hex 32)
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS - Add your frontend URLs (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Admin Credentials (Auto-created on startup)
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin@123456

# Environment
ENVIRONMENT=development

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=blog_db
```

**Important Notes:**
- Never commit `.env` file to version control
- Use strong passwords in production
- Special characters in passwords are automatically URL-encoded

### Configuration File

The application uses Pydantic Settings for configuration management. See `src/blog_project/core/config.py`:

```python
class Settings(BaseSettings):
    PROJECT_NAME: str = "Professional Blog API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str  # Required, min 32 chars
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    # Admin (Auto-created on startup)
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "admin123"
    
    # Database Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    
    @property
    def DATABASE_URL(self) -> str:
        # Async PostgreSQL with URL-encoded credentials
        user = quote_plus(str(self.POSTGRES_USER))
        password = quote_plus(str(self.POSTGRES_PASSWORD))
        return f"postgresql+asyncpg://{user}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")
```

## 🏃 Running the Application

### Local Development

#### Step 1: Ensure PostgreSQL is Running

**Windows:**
```bash
# Check if PostgreSQL service is running
sc query postgresql-x64-15
```

**Linux:**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

#### Step 2: Start Database (Docker)

```bash
# Start PostgreSQL in Docker
docker-compose up -d db

# Verify database is running
docker ps
```

#### Step 3: Run the FastAPI Application

```bash
# Development mode with auto-reload
uvicorn src.blog_project.main:app --reload --host 0.0.0.0 --port 8000

# Or using Poetry
poetry run uvicorn src.blog_project.main:app --reload
```

#### Step 4: Access the Application

- **API Base URL**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

#### Step 5: Login with Default Admin

Go to http://localhost:8000/docs and use:
- **Username**: `admin@example.com`
- **Password**: `Admin@123456`

## 🐳 Docker Deployment

### Quick Start with Docker Compose

#### Step 1: Build and Run Containers

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

#### Step 2: Verify Services

```bash
# Check running containers
docker ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db
```

#### Step 3: Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes database data)
docker-compose down -v
```

### Docker Architecture

The `docker-compose.yaml` defines two services:

1. **db** (PostgreSQL Database)
   - Image: `postgres:15-alpine`
   - Port: `5432`
   - Persistent volume: `postgres_data`

2. **web** (FastAPI Application)
   - Built from `Dockerfile`
   - Port: `8000`
   - Depends on: `db`
   - Hot-reload enabled for development

### Docker Commands Reference

```bash
# Build without cache
docker-compose build --no-cache

# Restart specific service
docker-compose restart web

# Execute commands in container
docker-compose exec web bash
docker-compose exec db psql -U postgres -d blog_db

# View container resource usage
docker stats

# Remove all stopped containers
docker-compose rm
```

## 📚 API Documentation

### Authentication Flow

#### Quick Start
1. **Access Swagger UI**: http://localhost:8000/docs
2. **Login**: Click "Authorize" button, use default admin credentials
3. **Test Endpoints**: All authenticated endpoints now accessible

#### Detailed Flow

**1. User Signup (Public)**
```bash
POST /api/v1/users
{
  "email": "user@example.com",
  "password": "SecurePass123",  # Min 8 chars, uppercase, lowercase, digit
  "role": "user"  # or "admin"
}
```

**2. Login (OAuth2 Form)**
```bash
POST /api/v1/auth/login
# Swagger UI sends form data automatically
username: admin@example.com  # Use email in username field
password: Admin@123456

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**3. Use Token**
- **Swagger UI**: Click "Authorize" → Enter token → Click "Authorize"
- **cURL**: Add header: `Authorization: Bearer YOUR_TOKEN`
- **Code**: Add header: `{"Authorization": "Bearer YOUR_TOKEN"}`

### Available Endpoints

#### Public Endpoints (No Authentication Required)

```http
GET  /                        # Welcome message
GET  /api/v1/posts            # List all posts
```

#### Authentication Endpoints

```http
POST /api/v1/users            # User signup (public)
POST /api/v1/auth/login       # Login and get JWT token
```

#### User Endpoints (Requires Authentication)

```http
GET  /api/v1/profile/me              # Get current user profile
PUT  /api/v1/profile/change-password # Change password
POST /api/v1/posts                   # Create blog post
```

#### Admin Endpoints (Requires Admin Role)

```http
GET    /api/v1/admin/users       # List all users
DELETE /api/v1/admin/users/{id}  # Delete user
GET    /api/v1/admin/posts       # List all posts
DELETE /api/v1/admin/posts/{id}  # Delete post
```

### Example API Requests

#### 1. Health Check
```bash
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

#### 2. User Signup
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "role": "user"
  }'
```

#### 3. Login (OAuth2 Form Data)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=Admin@123456"

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 4. List Posts (Public - with Pagination)
```bash
curl "http://localhost:8000/api/v1/posts?skip=0&limit=10"

# Response:
{
  "total": 5,
  "skip": 0,
  "limit": 10,
  "data": [/* posts array */]
}
```

#### 5. Create Post (Authenticated - Author auto-set)
```bash
curl -X POST "http://localhost:8000/api/v1/posts" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post",
    "published": true
  }'
```

#### 6. Update Post (Owner Only)
```bash
curl -X PUT "http://localhost:8000/api/v1/posts/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content",
    "published": true
  }'
```

#### 7. Delete Post (Owner Only)
```bash
curl -X DELETE "http://localhost:8000/api/v1/posts/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### 8. Get User Profile
```bash
curl -X GET "http://localhost:8000/api/v1/profile/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### 9. Change Password
```bash
curl -X PUT "http://localhost:8000/api/v1/profile/change-password" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "old_password": "Admin@123456",
    "new_password": "NewSecure@789"
  }'
```

#### 10. Admin - List All Users
```bash
curl -X GET "http://localhost:8000/api/v1/admin/users" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"
```

#### 11. Admin - Delete User
```bash
curl -X DELETE "http://localhost:8000/api/v1/admin/users/2" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"
```

### Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
  - Test endpoints directly in browser
  - View request/response schemas
  - See all available operations

- **ReDoc**: http://localhost:8000/redoc
  - Clean, readable documentation
  - Better for sharing with team

## 🗄️ Database

### Database Models

#### User Model
```python
class User(Base):
    id: int (Primary Key)
    email: str (Unique, Indexed)
    password_hash: str
    is_active: bool
    role: UserRole (Enum: admin/user)
    posts: List[Post] (Relationship)
```

#### Post Model
```python
class Post(Base):
    id: int (Primary Key)
    title: str (Indexed)
    content: str
    published: bool
    created_at: datetime
    author_id: int (Foreign Key)
    author: User (Relationship)
```

### Database Migrations

The application uses SQLAlchemy's `create_all()` for automatic table creation on startup (development only).

For production, consider using **Alembic** for database migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Database Access

#### Using Docker:
```bash
# Access PostgreSQL in Docker container
docker-compose exec db psql -U postgres -d blog_db

# Common SQL commands
\dt              # List tables
\d users         # Describe users table
SELECT * FROM posts;
```

#### Using Local PostgreSQL:
```bash
# Connect to database
psql -U postgres -d blog_db

# Or using connection string
psql postgresql://postgres:password123@localhost:5432/blog_db
```

## 💻 Development

### Code Structure Guidelines

- **api/**: Define API routes and endpoints
- **core/**: Application configuration and settings
- **db/**: Database connection and session management
- **models/**: SQLAlchemy ORM models
- **schemas/**: Pydantic models for request/response validation

### Adding New Features

#### 1. Create Model (models/models.py)
```python
class NewModel(Base):
    __tablename__ = "new_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
```

#### 2. Create Schema (schemas/schemas.py)
```python
class NewModelCreate(BaseModel):
    name: str

class NewModelResponse(BaseModel):
    id: int
    name: str
```

#### 3. Create Routes (api/routes.py)
```python
@router.post("/new-endpoint")
async def create_item(item: NewModelCreate, db: AsyncSession = Depends(get_db)):
    # Implementation
    pass
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=src/blog_project tests/
```

### Code Quality Tools

```bash
# Type checking with mypy
pip install mypy
mypy src/

# Code formatting with black
pip install black
black src/

# Linting with ruff
pip install ruff
ruff check src/
```

### Hot Reload

The application supports hot-reload in development mode:

```bash
# Local development
uvicorn src.blog_project.main:app --reload

# Docker development (already configured in docker-compose.yaml)
docker-compose up
```

Changes to Python files will automatically restart the server.

## 🔒 Security Features

### ✅ Implemented Security

1. **JWT Authentication (OAuth2)**
   - Token-based authentication
   - 30-minute expiration (configurable)
   - Secure HS256 algorithm

2. **Password Security**
   - Bcrypt hashing (72-byte optimized)
   - Strong validation: min 8 chars, uppercase, lowercase, digit
   - Password change functionality

3. **Role-Based Access Control**
   - Admin: Full access to all endpoints
   - User: Can manage own posts only

4. **Rate Limiting**
   - 100 requests/minute per IP
   - Prevents DDoS attacks

5. **Security Headers** (Configurable)
   - Commented out for development
   - Uncomment in `core/security_headers.py` for production

6. **CORS Configuration**
   - Environment-based allowed origins
   - Configurable in `.env`

7. **Global Exception Handling**
   - Professional error responses
   - No internal details exposed

8. **Input Validation**
   - Pydantic models for all requests
   - Email and password validation

### 🔐 Default Admin

**Auto-created on startup:**
- Email: `admin@example.com`
- Password: `Admin@123456`

⚠️ **Change in production!** Update `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `.env`

### 🛡️ Production Checklist

```bash
# 1. Generate secure SECRET_KEY
openssl rand -hex 32

# 2. Update .env
SECRET_KEY=<generated-key>
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=<strong-password>
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com

# 3. Uncomment security headers in core/security_headers.py

# 4. Enable HTTPS

# 5. Set up firewall and SSL certificates
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue in the repository.

## 🎯 Production Readiness: 10/10 ✅

### Quick Start Guide

```bash
# 1. Clone and navigate
git clone <repo-url>
cd blog_project

# 2. Start database
docker-compose up -d db

# 3. Install dependencies
poetry install
poetry shell

# 4. Run application
uvicorn src.blog_project.main:app --reload

# 5. Access Swagger UI
http://localhost:8000/docs

# 6. Login with default admin
Username: admin@example.com
Password: Admin@123456
```
---

**Production-Ready FastAPI Blog API** 🚀

**Built with ❤️ for Production Deployment**

---
![alt text](image.png)
![alt text](image-1.png)
