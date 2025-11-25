# 1. Base Image
FROM python:3.11-slim

# 2. Set Environment Variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
# Add /app/src to PYTHONPATH so python can find your modules
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# 3. Set Work Directory
WORKDIR /app

# 4. Install System Dependencies
# (libpq-dev is required for psycopg2/asyncpg to build)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Poetry
RUN pip install --no-cache-dir poetry==1.8.2

# 6. Configure Poetry
RUN poetry config virtualenvs.create false

# 7. Copy dependency files
COPY pyproject.toml poetry.lock ./

# 8. Install dependencies
RUN poetry install --no-root --no-dev

# 9. Copy Application Code
COPY src ./src
COPY .env .

# 10. Install the project
RUN poetry install --only-root

# 11. Run the Application
CMD ["uvicorn", "src.blog_project.main:app", "--host", "0.0.0.0", "--port", "8000"]