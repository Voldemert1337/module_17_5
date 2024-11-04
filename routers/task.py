from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.backend.db_depends import get_db
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from typing import Annotated

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task)
    result = db.scalars(stmt).all()
    return result

@router.get("/task_id")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task).where(Task.id == task_id)
    result = db.scalars(stmt).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return result

@router.post("/create")
async def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    stmt = insert(Task).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        user_id=user_id
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
async def update_task(task_id: int, task_data: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    stmt = update(Task).where(Task.id == task_id).values(
        title=task_data.title,
        content=task_data.content,
        priority=task_data.priority
    )
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful'}

@router.delete("/delete")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(Task).where(Task.id == task_id)
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deletion successful'}
