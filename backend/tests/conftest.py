"""Fixtures compartilhadas: banco de teste em memória e clientes HTTP da API."""

from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.cache import cache_clear
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(autouse=True)
def _reset_cache():
    """Garante que o cache em memória não vaze de um teste pro outro."""

    cache_clear()
    yield
    cache_clear()


@pytest_asyncio.fixture
async def async_session_maker():
    """Cria um banco SQLite em memória novo (com schema) para cada teste."""

    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        del connection_record
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    yield session_maker

    await engine.dispose()


def _override_get_db(async_session_maker):
    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    return override_get_db


@pytest_asyncio.fixture
async def client(async_session_maker) -> AsyncIterator[AsyncClient]:
    """Cliente HTTP já autenticado como admin (usado pela maioria dos testes)."""

    app.dependency_overrides[get_db] = _override_get_db(async_session_maker)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        settings = get_settings()
        login_response = await ac.post(
            "/api/v1/auth/login",
            json={"username": settings.admin_username, "password": settings.admin_password},
        )
        token = login_response.json()["access_token"]
        ac.headers["Authorization"] = f"Bearer {token}"
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def anon_client(async_session_maker) -> AsyncIterator[AsyncClient]:
    """Cliente sem token, para testar que rotas protegidas bloqueiam acesso."""

    app.dependency_overrides[get_db] = _override_get_db(async_session_maker)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()