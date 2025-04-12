from fastapi import FastAPI
import uvicorn

from src.Users.users_api import user_router
from src.database.database import async_main
from src.tasks.task_api import task_router

app = FastAPI(title="TaskiProject", summary="Позволяет создавать задачи и отслеживать их!", openapi_url="/api/v1/openapi.json")
app.include_router(task_router, prefix="/api/v1", tags=["Tasks"])
app.include_router(user_router, prefix="/api/v1", tags=["Users"])


@app.on_event("startup")
async def on_start_up():
    await async_main()




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0")
