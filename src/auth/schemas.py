from pydantic import BaseModel, EmailStr, Field

from src.schemas import UserBase


class UserCreateSchema(UserBase):
    password: str | None = Field(default=None, min_length=8)


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class JwtPayloadSchema(BaseModel):
    id: int
    name: str
