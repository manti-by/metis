import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, declared_attr

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/metis"
)

engine = None
SessionLocal = None
Base = declarative_base()


def get_engine():
    global engine
    if engine is None:
        engine = create_engine(DATABASE_URL)
    return engine


def get_session_local():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return SessionLocal


def get_db():
    Session = get_session_local()
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=get_engine())
