from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserLogin(BaseModel):

    username: str

    password: str

class UserCreate(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=100
    )

    firstname: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    lastname: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ...,
        ge=18,
        le=100
    )

    active: bool = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    city: str
    age: int
    active: bool

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):

    username: Optional[str] = None

    email: Optional[EmailStr] = None

    firstname: Optional[str] = None

    lastname: Optional[str] = None

    city: Optional[str] = None

    age: Optional[int] = Field(
        default=None,
        ge=18,
        le=100
    )

    active: Optional[bool] = None
