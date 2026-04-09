## ЛР 1 — Personal Finance Service

FastAPI-сервис учёта личных финансов: JWT, PostgreSQL, миграции Alembic, reverse proxy Nginx. Код разнесён по слоям **api** (роутеры и HTTP), **core** (бизнес-логика), **models** (SQLAlchemy), **middlewares**, **utils**.

### Структура репозитория

```
Lr1/
├── docker-compose.yml      # nginx, gateway, gateway-db
├── Makefile                # сборка и docker compose
├── example.env             # (опционально) старый шаблон; для gateway см. gateway/example.env
├── nginx/                  # образ и конфиг прокси
├── gateway/                # приложение FastAPI
│   ├── main.py             # точка входа, lifespan (Alembic, init)
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py     # api_router
│   │   └── apps/           # доменные роутеры
│   │       ├── auth/       # _auth_router + get/post_*_app
│   │       ├── finance/    # CRUD по сущностям финансов
│   │       └── users/      # публичные эндпоинты пользователей
│   ├── core/               # реализация сценариев (auth, finance, users)
│   ├── models/             # main_finance_*_model.py
│   ├── migrations/         # Alembic
│   ├── middlewares/        # PermissionMiddleware
│   ├── templates/          # Pydantic-схемы, enums, responses
│   └── utils/              # БД, Redis, auth worker, логирование
└── observability/          # конфиги Grafana / Loki / Prometheus (в compose закомментированы)
```

### Реализовано по заданию

- регистрация и вход (`OAuth2PasswordRequestForm` на логине);
- JWT и проверка токена;
- хэширование паролей;
- эндпоинты профиля и пользователей;
- учёт счетов, категорий, транзакций, бюджетов, целей, тегов и связей транзакция–тег.

### Модель данных (основные сущности)

- пользователи (`users`);
- категории, счета, транзакции, бюджеты, цели;
- теги и связь транзакций с тегами (many-to-many с дополнительными полями при необходимости).

Точная схема — в миграции `gateway/migrations/versions/` и моделях `gateway/models/main_finance_*_model.py`.

### HTTP API (кратко)

Префиксы задаются в `gateway/api/apps/__init__.py`.

| Группа   | Префикс  | Примеры |
|----------|----------|---------|
| Auth     | `/auth`  | `POST /auth/login`, `POST /auth/register`, `POST /auth/change-password`, `GET /auth/me`, `GET /auth/users` |
| Users    | корень   | `GET /users`, `GET /users/{id}`, `GET /users/{id}/details` |
| Finance  | корень   | `GET|POST|PUT|DELETE` для `/accounts`, `/categories`, `/transactions`, `/budgets`, `/goals`, `/tags` и связанных путей |

Интерактивная документация: `GET /docs` (Scalar).

### Запуск

**Локально (разработка):**

```bash
cd gateway
pip install -r requirements.txt
# настроить .env по образцу example.env, поднять PostgreSQL
uvicorn main:main_app --reload --host 0.0.0.0 --port 8000
```

**Docker Compose** (из каталога `Lr1`):

```bash
cp gateway/example.env gateway/.env   # при необходимости отредактировать
docker compose up -d --build
```

- API gateway: порт **8000**  
- Nginx (если сервис включён в compose): **1080** → прокси на gateway  
- PostgreSQL: **5432** (см. `gateway/.env`)

Команды `make build`, `make start`, `make stop` используют текущий `docker-compose.yml`.
