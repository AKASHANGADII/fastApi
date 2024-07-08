from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import database,models,schemas
from .. import hashing

router=APIRouter(
    prefix='/users',
    tags=['User']
)
get_db=database.get_db


@router.get('/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.ShowUser)
def getUser(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id={id} not found")
    return user

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def createUser(user:schemas.User,db:Session=Depends(get_db)):
    new_user=models.User(name=user.name,email=user.email,password=hashing.Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
