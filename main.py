from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

# Initialize FastAPI
app = FastAPI()


engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Example SQLAlchemy table (replace with your actual table definition)
users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', String(50)),
    Column('email', String(50)),
)

# Models
class UserIn(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

# Routes
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
    return UserOut(**user)

# Run FastAPI with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
