import inspect
from typing import Type, Optional
from fastapi import Form
from pydantic import BaseModel


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


@as_form
class User(BaseModel):
    publicAddress: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    discordId: Optional[str] = None
    opensea: Optional[str] = None
    profileImage: Optional[str] = None
    bio: Optional[str] = None
    points: Optional[int] = None
    token: Optional[str] = None


@as_form
class Admin(BaseModel):
    publicAddress: Optional[str] = None
    token: Optional[str] = None
