import select
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.database import UserModel
from src.services.auth import AuthService

class TestUserApi:
    data_for_reg = {"email": "simple_user@example.com", "password": "string"}
    access_roles = ["simple_user"] #здесь типо много ролей может быть

    @pytest.mark.asyncio
    async def test_register_user(self, client: AsyncClient, session: AsyncSession):

        register_response = await client.post("api/v1/register", json=self.data_for_reg)
        register_response_again = await client.post("api/v1/register", json=self.data_for_reg)

        data = register_response.json()

        async with session.begin():
            query = select(UserModel).where(UserModel.email == self.data_for_reg["email"])
            user = await session.scalar(query)
        
        # Проверка данных
        assert user  
        assert register_response_again.status_code == 400
        assert data["status"] == "ok"
    
    @pytest.mark.asyncio
    async def test_auth_user(self, client: AsyncClient):
        auth_response = await client.post("api/v1/login", json=self.data_for_reg)
        access_token = auth_response.json()["token"]
        decode_token = AuthService().decode_token(access_token)
        assert decode_token["role"] in self.access_roles
        assert auth_response.status_code == 200
        assert access_token
        
