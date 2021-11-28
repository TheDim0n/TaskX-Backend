from sqlalchemy.orm import Session
from typing import List

from . import models, schemas


def create_task(db: Session, new_task: schemas.TaskCreate) -> None:
    db_task = models.Task(**new_task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return


def get_tasks(db: Session) -> List[schemas.TaskDB]:
    return db.query(models.Task).all()


def delete_task_by_id(db: Session, id: int) -> None:
    _ = db.query(models.Task).filter(models.Task.id == id).delete()
    db.commit()
    return


def update_task_by_id(db: Session, id: int, values: schemas.TaskBase) -> None:
    _ = db.query(models.Task).filter(models.Task.id == id).\
        update(values.dict())
    db.commit()
    return
