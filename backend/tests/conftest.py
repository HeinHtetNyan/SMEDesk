import os

# Must run before any `app.*` import — app.core.database builds its engine
# from settings.database_url at import time.
os.environ["DATABASE_URL"] = "postgresql+asyncpg://smedesk:smedesk@localhost:5432/smedesk_test"

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from app import models  # noqa: F401  (registers models on Base.metadata)
from app.core.database import Base, async_session, engine, get_db
from app.main import app
from app.models.business import Business
from app.models.user import User


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def _clean_tables():
    async with async_session() as session:
        await session.execute(delete(User))
        await session.execute(delete(Business))
        await session.commit()


@pytest_asyncio.fixture
async def db_session():
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    async def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
