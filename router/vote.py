from fastapi import Depends,Response,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models
from oauth2 import get_current_user
from schemas import Vote

router = APIRouter()

@router.post('/vote',status_code=status.HTTP_201_CREATED)
def votes(vote : Vote,db:Session = Depends(get_db),current_user : int = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id : {vote.post_id} does not exist')
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == current_user.id)

    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Votes(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
                
        return{"message" : "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote Does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "successfully deleted message"}