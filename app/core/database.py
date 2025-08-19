from sqlalchemy import create_engine, MetaData
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT", 3306)

if password:
    DB_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
else:
    DB_URL = f"mysql+pymysql://{user}@{host}:{port}/{db_name}"

database = Database(DB_URL)
engine = create_engine(DB_URL,echo=True)
metadata = MetaData()
engine = create_engine(DB_URL)