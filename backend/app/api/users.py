from fastapi import APIRouter, Path, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from schemas.users import *
from model.users import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import secrets
from auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)

router = APIRouter(prefix="/profile", tags=["Users"])


def generate_token(length=32):
    return secrets.token_hex(length)


@router.post("/login")
async def retrieve_tasks_detail(
    request: UserLoginSchema, db: Session = Depends(get_db)
):
    user_obj = db.query(UserModel).filter_by(username=request.username).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user or password"
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user or password"
        )

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(
        content={
            "detail": "logged in succsessfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/register")
async def retrieve_tasks_detail(
    request: UserRegisterSchema, db: Session = Depends(get_db)
):
    if db.query(UserModel).filter_by(username=request.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="username already exist"
        )

    user_obj = UserModel(username=request.username,firstname=request.firstname,lastname=request.lastname)
    user_obj.set_password(request.password) #TODO Confirm passwords
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"details": "user registered successfully"})


@router.post("/refresh_token")
async def retrieve_tasks_detail(
    request: UserRefreshTokenSchema, db: Session = Depends(get_db)
):
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id)
    return JSONResponse(content={"access_token": access_token})