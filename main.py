# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from sqlalchemy import create_engine, Column, Integer, String, Table
# from databases import Database
# from database import DATABASE_URL, metadata, database

# app = FastAPI()

# # Database initialization
# engine = create_engine(DATABASE_URL)

# # Определение таблицы SQLAlchemy
# users = Table(
#     'users',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('user_name', String(50)),
#     Column('email', String(50)),
# )

# metadata.create_all(engine)  # Create tables defined by metadata if they do not exist

# class UserIn(BaseModel):
#     name: str
#     email: str

# class UserOut(BaseModel):
#     id: int
#     user_name: str
#     email: str

# class UserUpdate(BaseModel):
#     name: str = None
#     email: str = None

# # Connect to the database when the app starts
# @app.on_event("startup")
# async def startup():
#     await database.connect()

# # Disconnect from the database when the app stops
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

# # Routes
# @app.post("/users/", response_model=UserOut)
# async def create_user(user: UserIn):
#     query = users.insert().values(user_name=user.name, email=user.email)
#     last_record_id = await database.execute(query)
#     return {**user.dict(), "id": last_record_id}

# @app.get("/users/{user_id}", response_model=UserOut)
# async def read_user(user_id: int):
#     query = users.select().where(users.c.id == user_id)
#     user = await database.fetch_one(query)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return UserOut(**user)

# @app.get("/users/", response_model=list[UserOut])
# async def read_users():
#     query = users.select()
#     results = await database.fetch_all(query)
#     return [UserOut(**user) for user in results]

# @app.put("/users/{user_id}", response_model=UserOut)
# async def update_user(user_id: int, user_update: UserUpdate):
#     query = users.select().where(users.c.id == user_id)
#     user = await database.fetch_one(query)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     update_data = user_update.dict(exclude_unset=True)
#     if update_data:
#         query = users.update().where(users.c.id == user_id).values(**update_data)
#         await database.execute(query)
#         user = {**user, **update_data}
#     return UserOut(**user)



# # Проверяется, что скрипт запущен напрямую (а не импортирован как модуль), и в таком случае запускается веб-сервер FastAPI с помощью Uvicorn на локальном хосте (127.0.0.1) и порту 8000.
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)










#############################################################################################
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Table
from databases import Database
from database import DATABASE_URL, metadata, database
import logging

app = FastAPI()

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database initialization
engine = create_engine(DATABASE_URL)

# Определение таблицы SQLAlchemy
users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', String(50)),
    Column('email', String(50)),
)

metadata.create_all(engine)  # Create tables defined by metadata if they do not exist

class UserIn(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    user_name: str
    email: str

class UserUpdate(BaseModel):
    name: str = None
    email: str = None

# Connect to the database when the app starts
@app.on_event("startup")
async def startup():
    logger.info("Connecting to the database...")
    await database.connect()
    logger.info("Connected to the database")

# Disconnect from the database when the app stops
@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnecting from the database...")
    await database.disconnect()
    logger.info("Disconnected from the database")

# Routes
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    logger.info(f"Creating user with name: {user.name} and email: {user.email}")
    query = users.insert().values(user_name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    logger.info(f"User created with ID: {last_record_id}")
    return {**user.dict(), "id": last_record_id}

@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    logger.info(f"Reading user with ID: {user_id}")
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        logger.warning(f"User with ID: {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User found: {user}")
    return UserOut(**user)

@app.get("/users/", response_model=list[UserOut])
async def read_users():
    logger.info("Reading all users")
    query = users.select()
    results = await database.fetch_all(query)
    logger.info(f"Users found: {results}")
    return [UserOut(**user) for user in results]

@app.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_update: UserUpdate):
    logger.info(f"Updating user with ID: {user_id}")
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        logger.warning(f"User with ID: {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        query = users.update().where(users.c.id == user_id).values(**update_data)
        await database.execute(query)
        user = {**user, **update_data}
        logger.info(f"User with ID: {user_id} updated to {user}")
    return UserOut(**user)



# Проверяется, что скрипт запущен напрямую (а не импортирован как модуль), и в таком случае запускается веб-сервер FastAPI с помощью Uvicorn на локальном хосте (127.0.0.1) и порту 8000.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
