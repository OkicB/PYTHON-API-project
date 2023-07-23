import uvicorn
from typing import List
from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from models import Gender, Role, User, UpdateUser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "postgresql://bexpy:C0d1ng99@localhost:5432/firstdb"

# SQLALCHEMY ENGINE
engine = create_engine(DATABASE_URL)

# db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# fastapi application interface
app = FastAPI()

# db instance for async operations
database = Database(DATABASE_URL)

app = FastAPI()
db: List[User] = [
    User(
        id=uuid4(),
        first_name="John",
        last_name="doe",
        gender=Gender.male,
        roles=[Role.user],
    ),
    User(
        id=uuid4(),
        first_name="Jane",
        last_name="gabriel",
        gender=Gender.male,
        roles=[Role.user],
    ),
    User(
        id=uuid4(),
        first_name="bex",
        last_name="okan",
        gender=Gender.male,
        roles=[Role.user],
    ),
    User(
        id=uuid4(),
        first_name="Omer",
        last_name="okan",
        gender=Gender.male,
        roles=[Role.user],
    ),
]

#@app.get("/")
#async def read_root():
#    return {"Hello": "World"}

@app.get("/api/v1/users")
async def get_users():
    print("executing get users")
    await database.connect()

    session = SessionLocal()
    users = session.query(User).all()

    session.close()
    await database.disconnect()
    return users

@app.post("/api/v1/users")
async def create_user(user: User):
    db_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        roles=user.roles,
    )

    # connect to the db
    await database.connect()

    # creating a session and adding the user to the session
    session = SessionLocal()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # close the session and disconnect from the database
    session.close()
    await database.disconnect()

    return {"id": db_user.id}

#    db.append(user)
#    return {"id": user.id}

@app.delete("/api/v1/users/{id}")
async def delete_user(id: UUID):
    for user in db:
        if user.id == id:
            db.remove(user)
            return
        raise HTTPException(
            status_code=404, detail=f"Delete user failed, id {id} not found"
        )

@app.put("/api/v1/users/{id}")
async def update_user(user_update: UpdateUser, id:UUID):
    for user in db:
        if user.id == id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return user.id
        raise HTTPException(status_code=404, detail=f"Could not find user with id: {id}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
