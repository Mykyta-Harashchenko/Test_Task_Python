from fastapi import APIRouter, HTTPException, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from fastapi.routing import APIRoute

from Project.src.database.db import get_db
from Project.src.schemas.user import UserResponse, UserSignin, UserSignup
from Project.src.services.auth_service import signout, signin, signup, authenticate_user, create_access_token, \
    create_refresh_token
from Project.src.entity.models import User
from Project.src.services.dependencies import get_current_user

router = APIRouter()

@router.post("/signup",
             status_code=status.HTTP_201_CREATED)
async def register(user: UserSignup, db: AsyncSession = Depends(get_db)):
    return await signup(user, db)

@router.post("/signin",
             status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):
    user_signin = UserSignin(email=form_data.username, password=form_data.password)
    return await signin(user_signin, db)


@router.post("/signout",
             status_code=status.HTTP_201_CREATED)
async def logout(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await signout(current_user, db)
