from datetime import timedelta, datetime
from fastapi import HTTPException

from passlib.context import CryptContext
import jwt

from config import  settings

class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def decode_token(self, token):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except Exception:
            raise HTTPException(status_code=401, detail="Could not validate credentials")



