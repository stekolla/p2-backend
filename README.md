# Pier 2 Imports Backend API

## Overview
This is a FastAPI-based backend system for managing customer orders, billing, and shipping information for Pier 2 Imports. It includes API endpoints for retrieving order history, performing analytics, and ensuring no duplicate customer records.

## Requirements
- Docker & Docker Compose
- Python 3.8+

## Setup Instructions
### 1. Clone the Repository
```sh
git clone https://github.com/stekolla/p2-backend.git
cd p2-backend
```

### 2. Create a `.env` File
Create a `.env` file in the root directory of the project using `.env.local` as an example.

### 3. Build and Run with Docker Compose
```sh
docker-compose up --build
```
This will start the FastAPI backend and a PostgreSQL database container.

### 4. Access the API
Once running, the API will be available at:

- Docs: http://localhost:8000/doc
- Redoc: http://localhost:8000/redoc

## Other Tasks
### 1. Run Tests
To run unit tests inside the container:
```sh
docker-compose exec api pytest
```

### 2. Apply Migrations
To apply any new database migrations:
```sh
docker-compose exec api alembic upgrade head
```

### 3. Seed the Database
```sh
docker-compose exec api python tests/db_seed.py
```

### 4. Create a DB Migration
To create a new DB migration:
```sh
docker-compose exec api alembic revision --autogenerate -m "Your message here"
```

Migrations will be applied automatically when the API container starts.

### 5. Access the Database
To access the PostgreSQL database directly:
```sh
docker-compose exec db psql -U <user> -d <database>
```
