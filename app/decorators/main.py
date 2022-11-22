from functools import wraps

from app.models.main import User, Admin


def jwt_admin_control(self, func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        req = await kwargs["User"].token

        user_token = req["token"]
        response = self.admin_verify(user_token)

        if response:
            return await func(*args, **kwargs)
        else:
            return "Admin Access Required! You are not authorized to access this page!"

    return wrapper


def jwt_user_control(self, func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        req = await kwargs["info"].json()

        user_token = req["token"]
        response = self.admin_verify(user_token)

        if response:
            return await func(*args, **kwargs)
        else:
            return "Admin Access Required! You are not authorized to access this page!"

    return wrapper
