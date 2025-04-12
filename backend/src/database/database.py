from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Date
from datetime import datetime, date
from config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(f"{settings.DB_URL}")

async_session = async_sessionmaker(engine, expire_on_commit=False)

#_________________________________________________________________________________________________________________
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=20))
    description: Mapped[str] = mapped_column(String(length=100))
    status: Mapped[str] = mapped_column(String(length=100), default="Ожидание")
    date_creation: Mapped[date] = mapped_column(Date, default=lambda: datetime.utcnow().date())
    date_of_edit: Mapped[date] = mapped_column(Date, nullable=True)

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=50))
    role: Mapped[str] = mapped_column(String(length=50))
#_________________________________________________________________________________________________________________

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

