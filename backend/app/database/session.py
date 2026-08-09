"""Database session management."""

from collections.abc import AsyncGenerator
import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import structlog

from app.config.settings import settings

log = structlog.get_logger()
from dotenv import load_dotenv

# Load all variables from the .env file into the environment
load_dotenv()
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(project_root, ".env.example"))

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

    # asyncpg does not accept sslmode/channel_binding; map to supported query params.
    parsed_url = urlsplit(DATABASE_URL)
    query_items = dict(parse_qsl(parsed_url.query, keep_blank_values=True))
    if "sslmode" in query_items:
        query_items["ssl"] = query_items.pop("sslmode")
    query_items.pop("channel_binding", None)
    DATABASE_URL = urlunsplit(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            urlencode(query_items),
            parsed_url.fragment,
        )
    )

try:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set.")

    print(f"Attempting to create database engine with URL: {DATABASE_URL.split('@')[-1]}")
    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
    AsyncSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )
    log.info("Database engine and session factory created successfully.")
except Exception as e:
    log.error("Failed to create database engine.", error=str(e))
    raise


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency function that yields an AsyncSession."""
    async with AsyncSessionLocal() as session:
        yield session
