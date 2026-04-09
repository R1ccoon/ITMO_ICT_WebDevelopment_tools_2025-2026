## Personal Finance Service

FastAPI сервис для управления личными финансами с поддержкой JWT-аутентификации.

### Реализовано по заданию

- регистрация и авторизация пользователей;
- генерация JWT токена;
- аутентификация по JWT;
- хэширование пароля;
- API: `me`, список пользователей, смена пароля;
- учет доходов/расходов, категорий, бюджетов, целей и отчетов.

### Модель данных

- `users`
- `categories`
- `transactions`
- `budgets`
- `goals`
- `tags`
- `transaction_tags` (associative many-to-many с дополнительным полем `weight`)

### Запуск

```bash
cd gateway
pip install -r requirements.txt
uvicorn main:main_app --reload
```
