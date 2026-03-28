```markdown
# TaskManager

Backend для управления задачами на **FastAPI** + **SQLAlchemy** (async SQLite).

## 🚀 Быстрый старт

```bash
# Клонирование
git clone https://github.com/Levletsplay0/TaskManager.git
cd TaskManager

# Установка зависимостей
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic[email] werkzeug

# Запуск
uvicorn main:app --reload
```

🔗 API: `http://127.0.0.1:8000`  
📚 Docs: `http://127.0.0.1:8000/docs`

## 📦 Основные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/register` | Регистрация |
| `POST` | `/login` | Вход (возвращает токен) |
| `POST` | `/create_project` | Создать проект |
| `POST` | `/add_task` | Добавить задачу |
| `POST` | `/set_task` | Изменить статус задачи |

## 🗄️ Структура

```
├── main.py      # Эндпоинты API
├── models.py    # SQLAlchemy модели
├── schemas.py   # Pydantic схемы
├── database.py  # Логика БД и авторизации
```

> Все запросы, кроме `/register` и `/login`, требуют поле `token` в теле запроса.

---
*Made with ❤️ by [Levletsplay0](https://github.com/Levletsplay0)*
```