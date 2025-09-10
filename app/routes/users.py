from fastapi import APIRouter, HTTPException, Depends
from app.models import User, UserOut, Token
from app.auth import hash_password, verify_password, create_access_token
from app.db import users_collection
from fastapi.security import OAuth2PasswordRequestForm

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
async def register(user: User):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    await users_collection.insert_one({"email": user.email, "password": hashed_pw})
    return {"email": user.email}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
