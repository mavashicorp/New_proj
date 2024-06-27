from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String
from database import metadata

users = Table(
    "users_info",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_name", String(100)),
    Column("email", String(100)),
)

class UserOut(BaseModel):
    id: int
    user_name: str
    email: str
