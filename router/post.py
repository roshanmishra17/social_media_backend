from unittest import skip

from fastapi import APIRouter
from oauth2 import get_current_user
from schemas import Out, Post, PostOut
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends,Response,status,HTTPException,APIRouter
import models
from database import get_db

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])

@router.post('/',status_code = status.HTTP_201_CREATED,response_model=PostOut)
def create_post(
    post : Post, 
    db : Session = Depends(get_db),
    curr_user : models.User = Depends(get_current_user)
):
    new_post = models.Post(owner_id = curr_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/',response_model=List[PostOut])
def get_post(
    db : Session = Depends(get_db),
    curr_user : models.User = Depends(get_current_user),
    limit : int = 10,
    skip : int = 0
):
    posts = (
        db.query(models.Post)
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts

@router.get('/{id}',response_model=PostOut)
def get_one_post(
    id : int,
    db : Session = Depends(get_db),
    curr_user : models.User = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return post


@router.put('/{id}')
def update_post(
    id : int,
    up_post : Post,
    db : Session = Depends(get_db),
    curr_user : models.User = Depends(get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post :
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {id} not found'
        )
    
    if post.owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.update(up_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete('/{id}')
def delete_post(
    id : int,
    db : Session = Depends(get_db),
    curr_user : models.User = Depends(get_current_user)
):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {id} not found'
        )

    if post.owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
