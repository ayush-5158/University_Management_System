from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:Ayush%401927@localhost:5432/student_db"

#Connection
engine = create_engine(DATABASE_URL)

#Session 
SessionLocal = sessionmaker(autoflush=False,bind=engine,autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Base
Base = declarative_base()