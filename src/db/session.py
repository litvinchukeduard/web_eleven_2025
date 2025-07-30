from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config.app_config import app_settings

engine = create_engine(
    app_settings.DATABASE_CONNECT_URL
)

def open_session():
    with Session(engine) as session:
        yield session
