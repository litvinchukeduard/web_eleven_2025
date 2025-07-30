from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session
from authlib.jose import jwt, JoseError
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.models import User, UserRole
from src.config.app_config import app_settings
from src.repositories import user_repository
from src.db.session import open_session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict) -> str:
    issue_date_time = datetime.now(timezone.utc)
    expire_date_time = issue_date_time + timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRES_IN_MINUTES)
    header = {'alg': app_settings.JWT_ALGORITHM}
    payload = {**data, "iat": issue_date_time, "exp": expire_date_time}
    return jwt.encode(header, payload, app_settings.JWT_SECURE_KEY).decode('utf-8')

'''
Token
{
    "sub": "username",
    "iat": 1243254543,
    "exp": 1423546554
}
'''
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(open_session)) -> User:
    jwt_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        claims = jwt.decode(token, app_settings.JWT_SECURE_KEY)
        claims.validate()
        username = claims.get('sub')
        if not username:
            raise jwt_exception
        user = user_repository.get_user_by_username(db, username)
        if not user:
            raise jwt_exception
        return user
    except JoseError as exc:
        raise jwt_exception from exc
    
def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    return user
    
def get_current_active_admin(user: User = Depends(get_current_active_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not allowed to do this action")
    return user
