# get username and password from .env file
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base  # type: ignore[import]

load_dotenv()

username = os.getenv("user")
port = os.getenv("port")
password = os.getenv("password")
server = os.getenv("server")
database = os.getenv("database")

# create the database url using the username and password from the .env file
DATABASE_URL = (
    f"mysql+mysqlconnector://{username}:{password}"
    f"@{server}:{port}/{database}"
)

# create the database engine and session
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
