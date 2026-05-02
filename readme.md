# TaskManager

Backend для управления задачами на **FastAPI** + **SQLAlchemy** (async SQLite).

## 🚀 Быстрый старт

```bash
git clone https://github.com/Levletsplay0/TaskManager.git
cd TaskManager

pip install -r requirements.txt

uvicorn main:app --reload
```

📚 Docs: `http://127.0.0.1:8000/docs`  

---



## 📦 Основные эндпоинты

### 👤 Пользователь

| Метод | Путь | Описание | Тело запроса |
|-------|------|----------|--------------|
| `POST` | `/register` | Регистрация нового пользователя | `{"username": str, "password": str, "email": str}` |
| `POST` | `/login` | Вход в систему | `{"username": str, "password": str}` |
| `GET` | `/users/me` | Получение данных текущего пользователя | Header: `auth_token` |

### 📁 Проекты

| Метод | Путь | Описание | Параметры |
|-------|------|----------|-----------|
| `GET` | `/projects` | Список всех проектов пользователя | Header: `auth_token` |
| `POST` | `/projects` | Создать новый проект | Header: `auth_token`, Body: `{"name": str}` |
| `GET` | `/projects/{project_id}` | Получение проекта по ID | Header: `auth_token`, Path: `project_id` |

### ✅ Задачи

| Метод | Путь | Описание | Параметры |
|-------|------|----------|-----------|
| `POST` | `/projects/{project_id}/tasks` | Добавить задачу в проект | Header: `auth_token`, Path: `project_id`, Body: `{"name": str}` |
| `PATCH` | `/tasks/{task_id}` | Изменить статус задачи | Header: `auth_token`, Path: `task_id`, Body: `{"is_completed": bool}` |

---


## 🗄️ Структура проекта

```
├── main.py        # Эндпоинты API и инициализация приложения
├── models.py      # SQLAlchemy модели (User, Project, Task)
├── schemas.py     # Pydantic схемы для валидации данных
├── database.py    # Логика работы с БД и аутентификацией
└── requirements.txt # Зависимости проекта
```

---

## 🛠️ Технологии

- **FastAPI** — современный фреймворк для создания API
- **SQLAlchemy (async)** — асинхронная работа с базой данных
- **SQLite (aiosqlite)** — легковесная БД для разработки
- **Pydantic** — валидация и сериализация данных
- **Werkzeug** — хеширование паролей

---

