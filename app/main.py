from app.db_wrapper import DbWrapper

from fastapi import FastAPI, Request, Depends, Form
from starlette.middleware.cors import CORSMiddleware
from typing import Type, Optional

from bson.objectid import ObjectId

import pydantic

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str  # Convert ObjectId to string to fix
# the MongoDB error: "TypeError: Object of type ObjectId is not JSON serializable"

from app.models.main import User, Admin

# Create the FastAPI app
app = FastAPI()
db = DbWrapper(db_name="test_db")

# Add CORS middleware to allow cross-origin requests
origins = ["http://127.0.0.1:3000", "http://127.0.0.1:8000"]

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


# Access: Admin
@app.post("/user_exists")
async def user_exists(
    admin: Admin = Depends(Admin.as_form), public_address: Optional[str] = Form("")
):
    """
    :param admin: Admin object
    :param public_address: public address of the user
    :return: True if user exists, False otherwise
    """
    try:
        if public_address:
            return db.user_exists(public_address)
        else:
            return False

    except Exception as e:
        return e


# Access: Admin
@app.post("/get_users")
async def get_users(admin: Admin = Depends(Admin.as_form)):
    """
    :param admin: Admin object
    :return: List of users
    """
    try:
        return db.get_users()

    except Exception as e:
        return e


# Everybody can post a request. JWT authentication is checked in the backend
# and the user is added to the database if it doesn't exist and if the signature
# is valid for the public address
# Access: Admin
@app.post("/set_user")
async def set_user(user: User = Depends(User.as_form)) -> str:
    """
    :param user: User object
    :return: True if user was set, False otherwise
    """
    try:
        return db.set_user(dict(user))

    except Exception as e:
        return e


# Every registered user if free to update their profile with their token passed
# as an argument as well in the form or the user should be admin.
# Access: Admin + Registered User
@app.post("/update_user")
async def update_user(user: User = Depends(User.as_form)) -> bool:
    """
    :param user: User object
    :return: True if user was updated, False otherwise
    """
    try:
        return db.update_user(dict(user))

    except Exception as e:
        return e


@app.post("/get_user")  # A specific user data registered in the database by
# public address
# Access: Admin + Registered User
async def get_user(
    admin: Admin = Depends(Admin.as_form), public_address: Optional[str] = Form("")
) -> str:
    """
    :param admin: Admin object
    :param public_address: public address of the user
    :return: User object
    """
    try:
        if public_address:
            return db.get_user_by_public_address(public_address)
        else:
            return False

    except Exception as e:
        return e


# Everybody is allowed to post to this endpoint
# Access: Admin + Registered User + Unregistered User
@app.post("/user/signature")
async def user_signature(
    user: User = Depends(User.as_form), signature: Optional[str] = Form("")
) -> dict:
    """
    :param user: User object
    :param signature: signature of the user
    :return: True if signature is valid, False otherwise
    """
    try:
        if user.publicAddress and signature:
            return db.signature(user.publicAddress, signature)
        else:
            return False

    except Exception as e:
        return e


# Everybody is allowed to use this endpoint because you can not really hack blockchain
# yet.
# Access: Admin + Registered User + Unregistered User
@app.post("/user/verify")
async def user_verify(
    user: User = Depends(User.as_form), token: Optional[str] = Form("")
) -> dict:
    """
    :param user: User object
    :param token: JWT token of the user
    :return: True if signature is valid, False otherwise
    """
    try:
        if user.publicAddress and token:
            return db.verify(user.publicAddress, token)
        else:
            return False

    except Exception as e:
        return e


# Everybody is allowed to use this endpoint because you can not really hack blockchain
# yet, so only Admin will be allowed after the backend check in the end.
# Access: Admin + Registered User + Unregistered User
@app.post("/admin/signature")
async def admin_signature(
    admin: Admin = Depends(Admin.as_form), signature: Optional[str] = Form("")
) -> dict:
    """
    :param admin: Admin object
    :param signature: signature of the user
    :return: True if signature is valid, False otherwise
    """
    try:
        if admin.publicAddress and signature:
            return db.admin_signature(admin.publicAddress, signature)
        else:
            return False

    except Exception as e:
        return e


# Everybody is allowed to use this endpoint because you can not really hack blockchain
# yet, so only Admin will be allowed after the backend check in the end.
# Access: Admin + Registered User + Unregistered User
@app.post("/admin/verify")
async def admin_verify(
    admin: Admin = Depends(Admin.as_form), token: Optional[str] = Form("")
) -> dict:
    """
    :param admin: Admin object
    :param token: JWT token of the user
    :return: True if signature is valid, False otherwise
    """
    try:
        if admin.publicAddress and token:
            return db.admin_verify(admin.publicAddress, token)
        else:
            return False

    except Exception as e:
        return e


################################################
############  E-Mail Set/Get  ##################
################################################
# Access: Admin
@app.post("/get_emails")
async def get_emails(admin: Admin = Depends(Admin.as_form)):
    """
    :param admin: Admin object
    :return: List of emails
    """
    try:
        return db.get_emails()

    except Exception as e:
        return e


# To be modified
# Access: Admin + Registered User
@app.post("/set_email")
async def set_email(user: User = Depends(User.as_form)):
    """
    :param user: User object
    :return: True if email was set, False otherwise
    """
    try:
        return db.set_email(user.email)

    except Exception as e:
        return e
