
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
import models
from oauth2 import get_current_user
import schemas
import utils

router = APIRouter(prefix="/api/v1/users", tags=["User"])


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(
    user : schemas.UserCreate,
    db : Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = models.User(
        email=user.email,
        password=utils.hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(
    id : int,
    db : Session = Depends(get_db),
    curr_user: models.User = Depends(get_current_user)
):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found')
    if user.id != curr_user.id:
           raise HTTPException(status_code=403, detail="Not authorized")
    
    return user

