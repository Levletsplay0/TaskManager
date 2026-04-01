from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import (UserRegister, UserLogin, UserProfile, 
                     Project, Task, GetProject, SetTask)
from database import (init_db, get_db, create_user, get_user_by_name, 
                      password_check, update_auth_token, get_user_by_token, 
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

    
@app.post("/user")
async def get_user(data: UserProfile, db: AsyncSession = Depends(get_db)):
    result, status_code, message = await get_user_by_token(data.token, db)
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    
    return {"success": True, "message": message, "data": result}


@app.post("/create_project")
async def create_project(data: Project, db: AsyncSession = Depends(get_db)):
    result, status_code, message = await create_user_project(data.token, data.name, db)
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": message}
        )
    
    return {"success": True, "message": message, "data": result}
    


@app.post("/add_task")
async def create_task(data: Task, db: AsyncSession = Depends(get_db)):
    task = await add_task_to_project(data.token, data.name, data.project_id, db)
    if task:
        return {"success": True, "data": task}
        
    else:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Токен устарел или невалидный"}
        )

@app.post("/get_project")
async def get_project(data: GetProject, db: AsyncSession = Depends(get_db)):
    project = await get_user_project(data.token, data.project_id, db)
    if project:
        return {"success": True, "data": project}
        
    else:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Токен устарел или невалидный"}
        )


@app.post("/set_task")
async def set_complete_task(data: SetTask, db: AsyncSession = Depends(get_db)):
    task = await set_task_is_complete(data.token, data.task_id, data.is_completed, db)
    if task:
        return {"success": True, "data": task}
        
    else:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Токен устарел или невалидный"}
        )
    

@app.post("/get_projects")
async def get_projects(data: UserProfile, db: AsyncSession = Depends(get_db)):
    project = await get_user_projects(data.token, db)
    if project:
        return {"success": True, "data": project}
        
    else:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Токен устарел или невалидный"}
        )