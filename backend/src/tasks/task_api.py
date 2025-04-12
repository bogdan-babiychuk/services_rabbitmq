from src.schemas.base_models import TaskaddSchema, TaskResponseSchema, TaskEditSchema
from src.services.dependensies import SessionDep
from src.requests.base_requests import rq_create_task, rq_get_all_tasks, rq_edit_task, rq_get_task
from fastapi import Query, Path, status, HTTPException
from fastapi import APIRouter
from typing import List, Annotated
import logging

from src.services.dependensies import UserIdDep

task_router = APIRouter()


@task_router.get(
    "/tasks",
    summary="Получить все задачи",
    response_model=List[TaskResponseSchema]
)
async def get_tasks(
        session: SessionDep,
        skip: Annotated[int, Query(ge=0, description="Сколько записей пропустить")] = 0,
        limit: Annotated[int, Query(ge=2, description="Лимит записей", example="5")] = 10
) -> List[TaskResponseSchema]:
    tasks = await rq_get_all_tasks(session, skip=skip, limit=limit)
    return tasks


@task_router.get(
    "/task/{id}",
    summary="Получить задачу",
    response_model=TaskResponseSchema
)
async def get_task(
        id: Annotated[int, Path(ge=1, description="Введите id книги")],
        session: SessionDep
) -> TaskResponseSchema:
    task = await rq_get_task(session, id)
    return task


@task_router.post("/tasks",
                  status_code=status.HTTP_201_CREATED,
                  summary="Создать задачу"
                  )
async def create_task(data:TaskaddSchema,
                      _: UserIdDep,
                      session: SessionDep,
                      ):
    successfull = await rq_create_task(data.name, data.description, session)
    if successfull:
        return {"ok": True}
    else:
        raise HTTPException(status_code=400, detail="Failed to create task")



@task_router.patch(
    "/task/{id}",
    status_code=status.HTTP_200_OK,
    summary="Изменить задачу",
    response_model=TaskResponseSchema
)
async def edit_task(id: Annotated[int, Path(ge=1, description="Введите id задачи")],
                    data: TaskEditSchema,
                    session: SessionDep):
    try:
        logging.info(data.dict())
        if data.description is None and data.name is None:
            raise HTTPException(status_code=400, detail="Должно быть хотябы одно заполненное поле и проверьте id")
        edit_task = await rq_edit_task(session,
                                       id=id,
                                       name=data.name,
                                       description=data.description)
        if edit_task:
            return edit_task
        else:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    except HTTPException as e:
        logging.error(f"Ошибка в изменении задачи: {e}")


@task_router.delete("/task/{id}",
                    summary="Удалить задачу")
async def delete_task(id: int, session: SessionDep):
    pass




# @task_router.get("/users")
# async def get_users(users: Annotated[List[str], Query()]):
#     return {"people": users}
