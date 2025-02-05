import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  # Adjust the import path for your FastAPI app
from app.database import get_db, Base  # Adjust based on your project structure
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL_TEST"))
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Create a new database session for each test
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Create tables
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests

# Override the database dependency in FastAPI
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
