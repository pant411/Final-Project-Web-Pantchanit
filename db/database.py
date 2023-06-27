import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes

# load env vars
load_dotenv()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:secretpassword@localhost:3608/DB-Receipt"
# SQLALCHEMY_DATABASE_URL = os.getenv("DB_SERVICE")
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # creator=getconn
    # connect_args={"init_command": "SET SESSION time_zone='+07:00'"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()