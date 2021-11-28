from fastapi import APIRouter, Depends
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get('/', summary="Read list of tasks",
            response_model=List[schemas.TaskDB])
async def read_tasks(db=Depends(get_db)):
    return crud.get_tasks(db=db)


@router.post('/', status_code=201, summary="Create new task")
async def create_task(new_task: schemas.TaskCreate,
                      db=Depends(get_db)):
    return crud.create_task(db=db, new_task=new_task)


@router.put('/{id}/', status_code=204, summary="Update tasl by id")
async def update_task(id: int, values: schemas.TaskBase, db=Depends(get_db)):
    return crud.update_task_by_id(db=db, id=id, values=values)


@router.delete('/{id}/', status_code=204, summary="Delete task by id")
async def delete_task_by_id(id: int, db=Depends(get_db)):
    return crud.delete_task_by_id(db=db, id=id)
