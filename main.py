from fastapi import FastAPI, Depends, Header, Path, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import (UserRegister, UserLogin, TaskCreate, TaskStatusUpdate)
from database import (init_db, get_db, create_user, get_user_by_token, 
                      create_user_project, add_task_to_project, get_user_project, 
                      set_task_is_complete, get_user_projects, auth_user)
app = FastAPI()



@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def main():
    return {"success": True, "message": "This is a future project with task management for users."}

@app.post("/register")
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    result, status_code, message = await create_user(data.username, data.password, data.email, db)
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    return {"success": True, "message": message, "data": {"id": result.id, "username": result.username}}

@app.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result, status_code, message = await auth_user(data.username, data.password, db)
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    
    return {"success": True, "message": message, "data": {"access_token": result}}

    
@app.get("/users/me")
async def get_user(auth_token: str = Header(..., description="Токен аутентификации"), db: AsyncSession = Depends(get_db)):
    user, status_code, message = await get_user_by_token(auth_token, db)
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    
    return {
        "success": True,
        "message": message,
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@app.post("/projects")
async def create_project(auth_token: str = Header(..., description="Токен аутентификации"), name: str = Body(..., description="..."), db: AsyncSession = Depends(get_db)):
    result, status_code, message = await create_user_project(auth_token, name, db)
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    
    return {"success": True, "message": message, "data": result}
    


@app.post("/projects/{project_id}/tasks")
async def create_task(project_id: int = Path(..., description="ID проекта"), auth_token: str = Header(..., description="Токен аутентификации"), task_data: TaskCreate = Body(..., description="Данные задачи"), db: AsyncSession = Depends(get_db)):
    task, status_code, message = await add_task_to_project(auth_token, task_data.name, project_id, db)
    if status_code != 200:
        return JSONResponse(status_code=status_code, content={"success": False, "message": message})
        
    return {"success": True, "message": message, "data": task}


@app.get("/projects/{project_id}")
async def get_project(project_id: int = Path(..., description="ID проекта"), auth_token: str = Header(..., description="Токен аутентификации"), db: AsyncSession = Depends(get_db)):
    project, status_code, message = await get_user_project(auth_token, project_id, db)
    
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
        
    return {"success": True, "message": message, "data": project}



@app.patch("/tasks/{task_id}")
async def set_complete_task(task_id: int = Path(..., description="ID задачи"), auth_token: str = Header(..., description="Токен авторизации"), task_data: TaskStatusUpdate = Body(..., description="Данные для обновления"), db: AsyncSession = Depends(get_db)):
    task, status_code, message = await set_task_is_complete(auth_token, task_id, task_data.is_completed, db)
    
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    
    return {"success": True, "message": message, "data": task}


@app.get("/projects")
async def get_projects(auth_token: str = Header(..., description="Токен аутентификации"), db: AsyncSession = Depends(get_db)):
    projects, status_code, message = await get_user_projects(auth_token, db)
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    
    return {"success": True, "message": message, "data": projects}
