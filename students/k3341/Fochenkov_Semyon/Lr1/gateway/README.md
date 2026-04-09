# Gateway — Personal Finance API

FastAPI-приложение: JWT-аутентификация, домен «личные финансы».

## Слои

- **`api/apps/`** — сборка `APIRouter` по доменам: `auth`, `finance`, `users`; HTTP-обработчики в `get_*_app.py`, `post_*_app.py` и т.д.
- **`core/`** — вызовы БД и правила для `auth`, `finance`, `users`.
- **`models/`** — SQLAlchemy-модели (`main_finance_*_model.py`).
- **`templates/`** — Pydantic-модели ответов/запросов, enums.
- **`migrations/`** — Alembic (применяются при старте в `main.py` lifespan).

## Точка входа

`uvicorn main:main_app` — роутер подключается из `api`, middleware: `PermissionMiddleware`, CORS.

## Конфигурация

Скопируйте `example.env` в `.env` в этом каталоге и задайте строку подключения к PostgreSQL и секреты JWT.
