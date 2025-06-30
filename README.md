Написати додаток, який буде менеджети Фільми.

Є можливість зайти на цей сайт та переглянути інформацію про фільм

(Потрібно буде додати можливість додати рейтинг до фільму)

FastAPI
SQLAlchemy (SQLite)
Pydantic


src/
 |- api
    |- movie_api.py
 |- config/
    |- app_config.py
 |- services/
    |- movie_service.py
 |- repositories/
    |- movie_repository.py
 |- schemas
    |- movie.py
 |- db/
    |- base.py
    |- session.py
 |- models/
    |- movie.py
main.py
pyproject.toml