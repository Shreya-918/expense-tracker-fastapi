#all the apis of authentication 
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models.user_model import User
from ..schemas.user import UserCreate, UserResponse,UserLogin
from ..core.security import hash_password, verify_password
from ..core.JWT_helper import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post(
    "/register",
    response_model=UserResponse
)
def register(
    request: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = hash_password(
        request.password
    )

    new_user = User(
        username=request.username,
        email=request.email,
        password=hashed_password,
        firstname=request.firstname,
        lastname=request.lastname,
        city=request.city,
        age=request.age,
        active=request.active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@auth_router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_correct = verify_password(
        form_data.password,
        user.password
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
