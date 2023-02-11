import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

userDB = os.getenv("DB_USER")
passwdDB = os.getenv("DB_PASSWORD")
hostDB = os.getenv("DB_HOST")
portDB = os.getenv("DB_PORT")
nameDB = os.getenv("DB_NAME")
serviceDB = os.getenv("DB_SERVICE")

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:secretpassword@localhost:3306/DB-Receipt"
SQLALCHEMY_DATABASE_URL = f"{serviceDB}://{userDB}:{passwdDB}@{hostDB}:{portDB}/{nameDB}"
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # connect_args={"init_command": "SET SESSION time_zone='+07:00'"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()