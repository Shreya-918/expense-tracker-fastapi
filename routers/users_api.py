from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.user import UserResponse, UserUpdate
from ..models.user_model import User
from ..core.db import get_db
from ..core.dependencies import get_current_user


user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)


# GET MY PROFILE
@user_router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# UPDATE MY PROFILE
@user_router.patch("/me", response_model=UserResponse)
def update_my_profile(
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if request.username is not None:
        current_user.username = request.username

    if request.email is not None:
        current_user.email = request.email

    if request.firstname is not None:
        current_user.firstname = request.firstname

    if request.lastname is not None:
        current_user.lastname = request.lastname

    if request.city is not None:
        current_user.city = request.city

    if request.age is not None:
        current_user.age = request.age

    if request.active is not None:
        current_user.active = request.active

    db.commit()
    db.refresh(current_user)

    return current_user


# DELETE MY ACCOUNT
@user_router.delete("/me")
def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db.delete(current_user)
    db.commit()

    return {
        "status": "success",
        "message": "Your account has been deleted successfully"
    }
