import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

url = os.getenv("DATABASE_URL", "sqlite:///receipts.db")

args = {}
if url.startswith("sqlite"):
    args["check_same_thread"] = False

engine = create_engine(url, connect_args=args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
