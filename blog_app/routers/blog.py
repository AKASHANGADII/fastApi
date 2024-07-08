from typing import List
from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import database,models,schemas,oauth2

router=APIRouter(
    prefix='/blogs',
    tags=['Blog']
)

get_db=database.get_db

@router.get('/',status_code=status.HTTP_302_FOUND,response_model=List[schemas.ShowBlog])
def allBlogs(db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    blogs=db.query(models.Blog).all()
    return blogs

@router.get('/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.ShowBlog)
def specificBlog(id:int,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    return blog

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def createBlog(blog:schemas.Blog,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_model=models.Blog(title=blog.title,description=blog.description,user_id=1)
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model

@router.put('/',status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id:int,blog:schemas.Blog,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    old_blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if old_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    old_blog.title=blog.title
    old_blog.description=blog.description
    db.commit()
    db.refresh(old_blog)
    return {'result':'updated','blogs':old_blog}

@router.delete('/{id}',status_code=status.HTTP_200_OK)
def deleteBlog(id:int,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()
    return {'result':'deleted'}
