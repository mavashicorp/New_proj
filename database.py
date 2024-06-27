# database.py
from sqlalchemy import create_engine, MetaData
from databases import Database
import mysql.connector

DATABASE_URL = "mysql+pymysql://root:1488@localhost/users"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)

