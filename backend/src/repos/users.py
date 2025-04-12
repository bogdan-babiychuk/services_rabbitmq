from src.database.database import UserModel
from src.repos.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserModel


