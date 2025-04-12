from src.services.dependensies import SessionDep
from src.database.database import Task
from sqlalchemy import select
from datetime import datetime
import logging


async def rq_create_task(name, description, session: SessionDep):
    new_book = Task(name=name, description=description)
    if new_book:
        session.add(new_book)
        await session.commit()
        return True
    return False


async def rq_get_all_tasks(session: SessionDep,
                            skip:int=0,
                              limit:int=10):
    query = await session.scalars(select(Task).offset(skip).limit(limit))
    return query.all()


async def rq_get_task(session: SessionDep, id):
    task = await session.scalar(select(Task).where(Task.id == id))
    return task


async def rq_edit_task(session: SessionDep,
                       **kwargs):
    logging.info(kwargs)
    id = kwargs["id"]
    name = kwargs.get("name")
    description = kwargs.get("description")
    task = await session.scalar(select(Task).where(Task.id == id))
    if task:
        if name:
            task.name = name
        if description:
            task.description = description
        
        task.date_of_edit = datetime.utcnow().date()
        await session.commit()
        return task
    return False
    


