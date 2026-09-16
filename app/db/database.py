from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

#engine connects database with backend
# echo=True will show the SQL queries in the terminal
engine = create_engine(settings.DATABASE_URL, echo=True)

#session manages the database connection, transactions, and provides ORM
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class for all models
#all models will inherit from this class
class Base(DeclarativeBase):
    pass

def init_db():
    """Creates all tables in the database"""
    Base.metadata.create_all(bind=engine)
    
#dependency to get the db session in routes
#yield is like return but for generator functions
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
