from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import find_dotenv, load_dotenv


import os

load_dotenv(find_dotenv(raise_error_if_not_found=True))

db_host = os.getenv("DB_HOST")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")
db_port = os.getenv("DB_PORT")


engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}")

DBSession = sessionmaker(bind=engine)

Base = declarative_base()