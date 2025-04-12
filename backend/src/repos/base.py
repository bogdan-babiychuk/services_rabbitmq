from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.mysql import insert


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        hotels = result.scalars().all()

        return hotels

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset)).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
