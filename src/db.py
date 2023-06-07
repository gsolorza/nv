from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/nv"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, poolclass=NullPool)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()