from app.db_wrapper import DbWrapper

from fastapi import FastAPI, Request, Depends
from starlette.middleware.cors import CORSMiddleware

from bson.objectid import ObjectId

import pydantic

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

from app.models.main import User, Admin, as_form

# Create the FastAPI app
app = FastAPI()
db = DbWrapper(db_name="test_db")

# Add CORS middleware to allow cross-origin requests
origins = ["http://localhost:3000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(info: Request):
    """
    :return: a welcoming screen
    :return:
    """
    try:
        return "Welcome to the API"

    except Exception as e:
        return e


# Demo endpoint
@app.post("/create_user")
async def create_user(user: User = Depends(User.as_form)):
    """
    :param user: User model
    :return: a welcoming screen
    :return:
    """
    try:
        return user

    except Exception as e:
        return e
