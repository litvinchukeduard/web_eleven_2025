from sqlalchemy.orm import Session

from src.models import User, UserRole

def create_user(db: Session, username: str, hashed_password: str, role: UserRole) -> User:
    user = User(username=username, password=hashed_password, role=role.value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()
