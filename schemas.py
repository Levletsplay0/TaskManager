from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    token: str

class Project(BaseModel):
    token: str
    name: str

class Task(BaseModel):
    token: str
    name: str
    project_id: int

class GetProject(BaseModel):
    token: str
    project_id: int

class SetTask(BaseModel):
    token: str
    task_id: int
    is_completed: bool

