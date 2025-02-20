from fastapi import Depends, FastAPI
from . import models,database
from .routers import blog,user,authentication

app=FastAPI()

models.Base.metadata.create_all(database.engine)
@app.get('/')
def index():
    return {'reuslt':'index'}

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
