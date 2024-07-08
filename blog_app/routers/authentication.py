from datetime import timedelta
from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blog_app.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from .. import schemas,models,hashing,database

router=APIRouter(
    tags=['Authentication']
)

get_db=database.get_db

@router.post('/login',status_code=status.HTTP_202_ACCEPTED)
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user_data=db.query(models.User).filter(models.User.email==request.username).first()
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {request.username} not found")
    if hashing.Hash.verify(user_data.password,request.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user_data.email})
        return {"access_token": access_token, "token_type": "bearer"}
    return {'result':'Invalid password'}


@router.post('/passwordreset',status_code=status.HTTP_202_ACCEPTED)
def resetPassword(user:schemas.ResetPass,db:Session=Depends(get_db)):
    user_data=db.query(models.User).filter(models.User.email==user.email).first()
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {user.email} not found")
    if hashing.Hash.verify(user_data.password,user.password):
        user_data.password=hashing.Hash.bcrypt(user.newpassword)
        db.commit()
        db.refresh(user_data)
        return {'result':'successfully reset'}
    return {'result':'Invalid password'}