from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cfg import settings
from src.database.models import Base

# Create the SQLAlchemy engine using the database URL from settings
engine = create_engine(settings.database_url)


# Create all tables defined in Base (only if they don't exist)
# This is used to initialize the DB, not for complex migrations
def create_db_and_tables():
    Base.metadata.create_all(engine)


# Configure the session to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
