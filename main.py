from fastapi import FastAPI, Depends, HTTPException
from schemas import UserCreate
from database import init_db, create_user, get_user_by_name


app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
def main():
    return "Hello world"

@app.post("/create_user")
async def create(data: UserCreate):
    existing = await get_user_by_name(data.name)
    if existing:
        return {"success": False, "message": f"Пользователь '{data.name}' уже существует"}
        
    result = await create_user(data.name)
    return {"success": True, "username": result}