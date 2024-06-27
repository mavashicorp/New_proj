# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import database
from models import users, UserOut

app = FastAPI()

class UserIn(BaseModel):
    name: str
    email: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    query = users.insert().values(user_name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


