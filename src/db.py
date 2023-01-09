from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@10.100.1.180:5432/nv"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, max_overflow=50, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
        