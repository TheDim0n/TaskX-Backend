from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str
    description: str
    is_done: bool = None


class TaskCreate(TaskBase):
    pass


class TaskDB(TaskBase):
    id: int

    class Config:
        orm_mode = True
