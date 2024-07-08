from typing import Annotated
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import jwt
from blog_app.token import ALGORITHM, SECRET_KEY
from . import schemas,token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verifyToken(data,credentials_exception)
    
    

