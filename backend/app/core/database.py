import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

logger = logging.getLogger("agroscan.database")

db_url = settings.DATABASE_URL

# Fallback to SQLite if PostgreSQL driver is missing or specified as fallback
import importlib.util
if db_url.startswith("postgresql"):
    if importlib.util.find_spec("psycopg2") is None:
        logger.warning("psycopg2 module not found. Falling back to SQLite database at sqlite:///./agroscan.db")
        db_url = "sqlite:///./agroscan.db"

connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
