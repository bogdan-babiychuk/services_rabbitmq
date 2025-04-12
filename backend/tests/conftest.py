from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database.database import Base
from main import app
from config import settings


test_engine = create_async_engine(settings.DB_URL, echo=True)

TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)



@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    # Создаём таблицы в БД
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Удаляем таблицы после тестов
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




@pytest_asyncio.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session


# Фикстура для клиента FastAPI
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app) #Мы не поднимаем реальный сервер, а создаём экземпляр ASGI и передаём туда FASTAPI app
    async with AsyncClient(transport=transport, base_url="http://test") as ac: #Можно написать и localhost
        yield ac



