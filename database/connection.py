# database/supabase_connection.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("user", "postgres")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = int(os.getenv("port", "5432"))
DBNAME = os.getenv("dbname", "postgres")

# 👇 psycopg v3 + SSL + forçar IPv4 (gai_family=inet)
DATABASE_URL = (
    f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    f"?sslmode=require&gai_family=inet"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
