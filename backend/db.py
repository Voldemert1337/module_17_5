from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, String, Integer

engine = create_engine("sqlite:///taskmanager.db", echo = True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

def init_db():
    import app.models.user  # Импортируйте ваши модели здесь
    import app.models.task  # Убедитесь, что обе модели загружены
    Base.metadata.create_all(bind=engine)