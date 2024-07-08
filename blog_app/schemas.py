from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    description:str

    class Config:
        orm_mode=True

class User(BaseModel):
    name:str
    email:str
    password:str

    class Config:
        orm_mode=True

class ResetPass(User):
    newpassword:str

class ShowUser(BaseModel):
    name:str
    email:str

    class Config:
        orm_mode=True

class ShowBlog(BaseModel):
    title:str
    description:str
    creator:ShowUser

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
   email: str | None = None