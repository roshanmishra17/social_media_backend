from random import randrange
import time
from typing import List
from fastapi import Body, Depends, FastAPI, HTTPException, Response,status
from fastapi.security import OAuth2PasswordRequestForm
from router import auth, post, user, vote
from schemas import Post, PostOut, Token, UserCreate, UserOut
import psycopg2
from psycopg2.extras import RealDictCursor
from database import engine,get_db,SessionLocal
from sqlalchemy.orm import Session
import models
import utils





# my_posts = [
#             {"title" : "This is title","content" : "This is Content","id":1},
#             {"title" : "another title","content" : "another Content","id":2}
#         ]

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastAPI_Prac',user='postgres',password='roshan123',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection successful')
#         break
#     except Exception as error:
#         print('database connection failed')
#         print('Error',error)
#         time.sleep(2)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.get('/sqlalchemy')
# def root(db : Session = Depends(get_db)):
#     return {'message' : 'messsage is therre'}

# @app.post('/create_post',status_code = status.HTTP_201_CREATED)
# def create_post(post : Post,db : Session = Depends(get_db)):
#     # print(payLoad)
#     # return {"New_Post" : f"title : {payLoad['title']} Content : {payLoad['content']}"}

#     # post_dict = New_Post.dict()
#     # post_dict['id'] = randrange(0,1000000)
#     # my_posts.append(post_dict)
#     # return {"data" : post_dict}

#     # cursor.execute( """ INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
#     # newPost = cursor.fetchone()
#     # conn.commit()
#     # return newPost

#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {'data' : new_post}

# @app.get('/get_post',response_model=List[PostOut])
# def get_post(db : Session = Depends(get_db)):
#     # post = cursor.execute(""" SELECT * FROM posts """)
#     # post = cursor.fetchall()
#     # print(post)
#     # return {'data' : post}

#     post = db.query(models.Post).all()
#     print(post)

#     return post

# @app.get('/posts/{id}',response_model=PostOut)
# def get_one_post(id : int,response = Response,db : Session = Depends(get_db)):
#     # post = find_post(id)
#     # if not post:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')
#     # print(post)
#     # return {'post detail' : post}

#     # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,str(id))
#     # post = cursor.fetchone()
#     # if not post:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')
#     # print(post)
#     # return{'data': post}

#     post_query = db.query(models.Post).filter(models.Post.id == id).first()
#     # print(post_query)
#     if not post_query:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')
#     return post_query



# @app.put('/update/{id}')
# def update_post(id : int,up_post : Post,db : Session = Depends(get_db)):
#     # index = find_index(id)
#     # if index == None:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')
#     # post_dict = post.dict()
#     # post_dict['id'] = id
#     # my_posts[index] = post_dict
#     # return post_dict

#     # cursor.execute(""" UPDATE posts  SET title = %s,content = %s,published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
#     # post = cursor.fetchone()
#     # if post == None:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')
#     # conn.commit()
#     # return{'data' : post}

#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')

#     post_query.update(up_post.dict(),synchronize_session=False)
#     db.commit()
#     return {'data':post_query.first()}


# @app.delete('/delete/{id}')
# def delete_post(id : int,db : Session = Depends(get_db)):
# #     index = find_index(id)
# #     if index == None: 
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')

# #     my_posts.pop(index)
# #     return Response(status_code=status.HTTP_204_NO_CONTENT)

#     # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *   """,str(id))
#     # post = cursor.fetchone()
#     # if post == None:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')
#     # conn.commit()
#     # return Response(status_code=status.HTTP_204_NO_CONTENT)

#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     del_post = post_query.first()

#     if del_post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the post with id {id} was not found')
    
#     post_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.post('/user',status_code=status.HTTP_201_CREATED,response_model=UserOut)
# def create_user(user : UserCreate,db : Session = Depends(get_db)):

#     hash_pass = utils.hash(user.password)
#     user.password = hash_pass

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

# @app.get('/user/{id}',response_model=UserOut)
# def get_user(id : int,db : Session = Depends(get_db)):

#     user = db.query(models.User).filter(models.User.id == id).first()

#     if user is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'the user with id {id} was not found')
    
#     return user

# @app.get('/login',response_model=Token)
# def login(userCred : OAuth2PasswordRequestForm=Depends(),db : Session = Depends(get_db)):
    
#     user = db.query(models.User).filter(models.User.id == userCred.username).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    
#     if not utils.verify(userCred.password,user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    
    #return access
    #return bearer