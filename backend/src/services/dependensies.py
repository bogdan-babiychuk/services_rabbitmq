from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.repos.users import UsersRepository
from src.database.database import async_session
from src.services.auth import AuthService


async def get_session():
    async with async_session() as session:
        yield session

async def get_token(request: Request)-> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен")
    return token


async def is_current_user(token:str = Depends(get_token),
                          session: AsyncSession = Depends(get_session)):
    data = AuthService().decode_token(token)
    user = await UsersRepository(session).get_one_or_none(id=data["user_id"])
    return user

SessionDep = Annotated[AsyncSession, Depends(get_session)]
UserIdDep = Annotated[dict, Depends(is_current_user)]




