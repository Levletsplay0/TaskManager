from fastapi import FastAPI
from schemas import UserCreate
from database import init_db, create_user, get_user_by_name


app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def main():
    return "Hello world"

@app.post("/create_user")
async def create(data: UserCreate):
    existing = await get_user_by_name(data.username)
    if existing:
        return {"success": False, "message": f"Пользователь '{data.username}' уже существует"}
        
    result = await create_user(data.username, data.password, data.email)
    return {"success": True, "id": result.id, "username": result.username}