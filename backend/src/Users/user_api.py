import sqlalchemy
from fastapi import HTTPException, APIRouter, Response
import json

from src.services.dependensies import SessionDep, UserIdDep
from src.repos.users import UsersRepository
from src.schemas.User.user_schemas import UserDataRequest, CreateUserRequestAdd
from src.services.auth import AuthService
from src.services.broker import ProduceMessageInRabbit
from config import settings
import logging

logging.basicConfig(level=logging.INFO)




user_router = APIRouter()

@user_router.post("/register",
                  summary="Регистрация")
async def register_user(request: UserDataRequest,
                        session: SessionDep):
    try:
        password = request.password
        data = CreateUserRequestAdd(email=request.email,
                                    hashed_password=AuthService().hash_password(password),
                                    role="simple_user")
        await UsersRepository(session).add(data=data)
        await session.commit()
        await ProduceMessageInRabbit(settings.RABBITMQ_URL,
                                     settings.RABBITMQ_LOGIN,
                                     settings.RABBITMQ_PASSWORD).publish_message(name_queue="register_queue",
                                                                                 name_exchange="register_exchange",
                                                                                 routing_key="register",
                                                                                 body=json.dumps(
                                                                                     {"email": request.email}
                                                                                 ))
        
        return {"status": "created"}
    
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/login",
                  summary="Авторизация")
async def login_user(request: UserDataRequest,
                     session: SessionDep,
                     response: Response):
    user = await UsersRepository(session).get_one_or_none(email=request.email)
    logging.info(f"user: {user}")
    if not AuthService().verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    else:
        token = AuthService().create_access_token({"user_id": user.id,
                                                   "role": user.role})
        response.set_cookie("access_token", token, httponly=True) #В продакшене secure=True, чтобы работал только с Https
        return {"token": token}


@user_router.get("/me")
async def get_me(user: UserIdDep):
    return user
