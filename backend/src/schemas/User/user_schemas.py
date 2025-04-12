from pydantic import BaseModel, EmailStr, field_validator
class UserDataRequest(BaseModel):
    email: EmailStr
    password: str


class CreateUserRequestAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    role: str

    @field_validator('email')
    def validate_email(cls, value):
        # Логика проверки домена email
        domen = value.split("@")[-1]
        if domen not in ["mail.ru", "gmail.com", "yandex.ru"]:
            raise ValueError('Email domain must be mail.ru, gmail.com, or yandex.ru')
        return value
