from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from dotenv import dotenv_values, find_dotenv


settings = dotenv_values(find_dotenv())
driver_path: str = "postgresql://{}:{}@{}:5432/{}".format(
    settings["DB_LOGIN"],
    settings["DB_PASSWORD"],
    settings["DB_HOST"],
    settings["DB_NAME"])

engine = create_engine(url=driver_path)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False)
Base = declarative_base()
