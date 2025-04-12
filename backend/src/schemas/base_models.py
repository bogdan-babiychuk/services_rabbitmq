from pydantic import BaseModel
from datetime import date
from typing import Union

class TaskaddSchema(BaseModel):
    name: str
    description: str
    status: str

class TaskEditSchema(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None


class TaskResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    date_creation: date
    date_of_edit: Union[date, None]

