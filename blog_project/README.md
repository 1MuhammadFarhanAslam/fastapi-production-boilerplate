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
│       ├── api/              # API routes and endpoints
│       │   ├── __init__.py
│       │   ├── routes.py     # Post endpoints
│       │   ├── users.py      # User signup
│       │   ├── auth.py       # Authentication (login)
│       │   ├── user_profile.py  # User profile & password change
│       │   └── admin.py      # Admin-only endpoints
│       ├── core/             # Core configuration
│       │   ├── __init__.py
│       │   ├── config.py     # Settings and environment variables
│       │   ├── security.py   # Password hashing & JWT
│       │   └── deps.py       # Authentication dependencies
│       ├── db/               # Database configuration
│       │   ├── __init__.py
│       │   ├── base.py       # SQLAlchemy Base
│       │   └── session.py    # Database session management
│       ├── models/           # SQLAlchemy models
│       │   ├── __init__.py
│       │   └── models.py     # User and Post models with roles
│       ├── schemas/          # Pydantic schemas
│       │   ├── __init__.py
│       │   └── schemas.py    # Request/Response schemas
│       ├── __init__.py
│       └── main.py           # Application entry point
├── tests/                    # Test suite
│   └── __init__.py
├── .dockerignore
├── .env                      # Environment variables
├── .gitignore
├── docker-compose.yaml       # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── pyproject.toml            # Project dependencies
├── poetry.lock
├── requirements.txt
└── README.md
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
PROJECT_NAME=Blog API
VERSION=1.0.0
API_V1_STR=/api/v1

# Security
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
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
    PROJECT_NAME: str = "Blog API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    
    @property
    def DATABASE_URL(self) -> str:
        # Async PostgreSQL connection string
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"
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

#### Step 2: Run the FastAPI Application

```bash
# Development mode with auto-reload
uvicorn src.blog_project.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 3: Access the Application

- **API Base URL**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

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

1. **Signup**: Create a new user account
2. **Login**: Get JWT access token
3. **Use Token**: Include token in Authorization header for protected endpoints

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

#### 1. User Signup
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "role": "user"
  }'
```

#### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Create Post (Authenticated)
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

#### 4. Change Password
```bash
curl -X PUT "http://localhost:8000/api/v1/profile/change-password" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "old_password": "securepassword123",
    "new_password": "newsecurepassword456"
  }'
```

#### 5. Admin - List All Users
```bash
curl -X GET "http://localhost:8000/api/v1/admin/users" \
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

## 🔒 Security Best Practices

- ✅ **JWT Authentication** - Implemented with secure token-based auth
- ✅ **Password Hashing** - Bcrypt encryption for passwords
- ✅ **Role-Based Access Control** - Admin and User roles
- Store sensitive data in `.env` file (never commit to Git)
- Use strong SECRET_KEY (generate with `openssl rand -hex 32`)
- Use strong passwords for database
- Enable CORS only for trusted origins
- Use HTTPS in production
- Regularly update dependencies
- Implement rate limiting
- Validate and sanitize all inputs

### Creating Admin User

To create an admin user, signup with role="admin":

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "adminpassword",
    "role": "admin"
  }'
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

---

**Happy Coding! 🚀**
