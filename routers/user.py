from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify



router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    try:
        stmt = select(User)
        result = db.scalars(stmt).all()
        print(f"Пользователи получены: {result}")  # Отладочный принт
        return result
    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")  # Логирование ошибки
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка при получении пользователей: {e}")


@router.get('/user_id')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.id == user_id)
    result = db.scalars(stmt).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return result


@router.post('/create')
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    try:
        print("Запрос получен")  # Отладочный принт
        print(f"Создание пользователя: {user}")  # Отладочный принт
        stmt = insert(User).values(
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            age=user.age
        )
        db.execute(stmt)
        db.commit()
        print("Пользователь успешно создан")  # Отладочный принт
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")  # Логирование ошибки
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка при создании пользователя: {e}")



@router.put('/update')
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = update(User).where(User.id == user_id).values(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age
    )
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted is successfully!'}