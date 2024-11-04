from fastapi import FastAPI
import logging
from app.routers import task, user

import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

logger.debug("Добавление роутеров")
app.include_router(task.router)
app.include_router(user.router)
logger.debug("Приложение запущено")
