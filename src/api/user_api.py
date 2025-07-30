from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

from src.db.session import open_session
from src.services import user_service
from src.security import oauth

from src.schemas.user import UserCreate, UserRead

from src.models import UserRole

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(open_session)):
    user = user_service.get_user_by_username(session, form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token = oauth.create_access_token({'sub': user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users", response_model=UserRead)
def create_user(user_create: UserCreate, session: Session = Depends(open_session)):
    return user_service.create_user(session, user_create.username, user_create.password, role=UserRole.USER)
