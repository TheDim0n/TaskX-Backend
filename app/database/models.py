from sqlalchemy import Boolean, Column, Integer, String

from .database import DataBase


class Task(DataBase):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    description = Column(String(), nullable=True)
    is_done = Column(Boolean, default=False)
