from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.schemas import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.auth.security import create_access_token
from app.auth.service import authenticate_user, create_user, get_user_by_email
from app.database import get_db
from app.users.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    existing_user = get_user_by_email(db, payload.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )

    user = create_user(
        db=db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = authenticate_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(subject=str(user.id))

    return TokenResponse(access_token=access_token)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user