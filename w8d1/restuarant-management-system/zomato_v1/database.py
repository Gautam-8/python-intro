# Import required modules for async SQLAlchemy and database setup
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Set the database URL for SQLite (async)
DATABASE_URL = "sqlite+aiosqlite:///./restaurants.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a sessionmaker factory for async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get DB session for FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
