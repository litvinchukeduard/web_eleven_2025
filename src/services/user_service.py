from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi import status

from src.models import User, UserRole
from src.security import passwords
from src.repositories import user_repository


def create_user(db: Session, username: str, password: str, role: UserRole) -> User:
    existing = user_repository.get_user_by_username(db, username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    hashed_password = passwords.get_password_hash(password)
    return user_repository.create_user(db, username, hashed_password, role)

def get_user_by_username(db: Session, username: str) -> User | None:
    return user_repository.get_user_by_username(db, username)

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if passwords.verify_password(password, user.password):
        return None
    return user
