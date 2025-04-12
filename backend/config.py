from pydantic_settings import BaseSettings, SettingsConfigDict

class ProjectSettings(BaseSettings):
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MODE: str
    RABBITMQ_URL: str
    RABBITMQ_LOGIN:str
    RABBITMQ_PASSWORD: str

    @property
    def DB_URL(self):
        return f"sqlite+aiosqlite:///{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = ProjectSettings()

