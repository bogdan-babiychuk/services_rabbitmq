from src.database.database import Task
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.base_models import TaskaddSchema
from httpx import AsyncClient
from src.services.auth import AuthService
import datetime as dt
import pytest

@pytest.mark.usefixtures("session", "client", "setup_test_db")
class TestAPiTask:
    access_roles = ["simple_user",]
    @staticmethod
    def check_instance(obj, guess_type):
        assert isinstance(obj, guess_type) == True

    @pytest.mark.asyncio
    async def test_get_tasks(self, client: AsyncClient, session: AsyncSession):
        """Тест получения всех задач из тестовой БД"""
        self.check_instance(session, AsyncSession)
        count = 1
        async with session.begin():
            while count != 10:
                task = Task(name=f"Task {count}", description="Desc 1", status="in progress", date_creation=dt.datetime.utcnow().date())
                session.add(task)
                count += 1
        
        response = await client.get("/api/v1/tasks?skip=0&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Task 1"
        assert data[2]["name"] == "Task 3"

    @pytest.mark.asyncio
    async def test_get_one_task(self, client: AsyncClient, session: AsyncSession):
        """Тест получения одной задачи из тестовой БД"""
        self.check_instance(session, AsyncSession)
        async with session.begin():
            task = Task(name=f"Помыть посуду", description="Desc 1", status="in progress", date_creation=dt.datetime.utcnow().date())
            session.add(task)
        
        response = await client.get(f"api/v1/task/{task.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Помыть посуду"


    @pytest.mark.asyncio
    async def test_create_task(self, client:AsyncClient):
        """Тест создания записи и проверка авторизован ли Юзер"""

        task_data = TaskaddSchema(name="Покодить", description="пройти pytest", status="in progress")
        data_for_auth = {"email": "user@example.com",
                        "password": "string"}
        register_response = await client.post("/api/v1/register", json=data_for_auth)
        assert register_response.status_code == 200

        auth_response = await client.post("/api/v1/login", json=data_for_auth)
        token = auth_response.cookies.get("access_token")
        decode_token = AuthService().decode_token(token)
        assert decode_token["role"] in self.access_roles
        assert auth_response.status_code == 200, f"Ошибка авторизации, статус {auth_response.status_code}, ответ: {auth_response.text}"
        response = await client.post("/api/v1/tasks", json=task_data.dict(), cookies=auth_response.cookies)
        assert response.status_code == 201

