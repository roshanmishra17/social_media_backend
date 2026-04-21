from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,status,HTTPException,APIRouter
from database import get_db
import models
from oauth2 import create_access_token
from schemas import Token
from sqlalchemy.orm import Session
import utils


router = APIRouter()

@router.post('/login',response_model=Token)
def login(userCred :OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    # OAuth2PasswordRequestForm : This is a dependency class to collect the username and password as form data for an OAuth2 password flow.
    user = db.query(models.User).filter(models.User.email == userCred.username).first()

    if not user :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail = f"Invaild Credentials"
        )
    if not utils.verify(userCred.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail = f"Invaild Credentials"
        )
    
    access_token = create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token,"token_type" : "bearer"}
    

