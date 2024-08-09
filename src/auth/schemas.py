from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr | None
    name: str = Field(max_length=32, min_length=3)


class UserCreateSchema(UserBase):
    password: str | None = Field(default=None, min_length=8)


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class JwtPayloadSchema(BaseModel):
    id: int
    name: str
