from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os


DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./techwear.db')

engine = create_engine(
    DATABASE_URL,
    connect_args = {'check_same_thread': False} if 'sqlite' in DATABASE_URL else {},
    pool_pre_ping = True,                                                               #пересоздаем соединение, если оно истекло
    echo = False                                                                        #чтобы логи не засорять
)

SessionLocal = sessionmaker (autocommit = False, autoflash = False, bind = engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind = engine)                                              #создает таблицы если их еще нет


