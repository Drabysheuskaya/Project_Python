from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseManager:
    _engine: Engine | None = None
    _connection: Connection | None = None
    _sessionmaker: sessionmaker | None = None

    @classmethod
    def connect(cls, db_url: str) -> None:
        cls._engine = create_engine(db_url, connect_args={"check_same_thread": False})
        cls._sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=cls._engine
        )
        cls._connection = cls._engine.connect()

    @classmethod
    def disconnect(cls) -> None:
        if cls._connection:
            cls._connection.close()
            cls._connection = None

    @classmethod
    def get_db(cls) -> Iterable[Session]:
        if cls._sessionmaker is not None:
            with cls._sessionmaker() as db:
                yield db
