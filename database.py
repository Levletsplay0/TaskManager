from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import Users, Base, Projects, Tasks
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from sqlalchemy.orm import selectinload



async_engine = create_async_engine("sqlite+aiosqlite:///users.db")

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_user(username, password, email, db: AsyncSession):
    hashed_password = generate_password_hash(password)
    user = Users(username=username, password=hashed_password, email=email)
    db.add(user)
    await db.commit()
    return user

async def get_user_by_name(username, db: AsyncSession):
    result = await db.execute(select(Users).where(Users.username == username))
    return result.scalar_one_or_none()
    
async def password_check(username, password, db: AsyncSession):
    result = await db.execute(select(Users).where(Users.username == username))
    user = result.scalar_one_or_none()
    is_valid = check_password_hash(user.password, password)
    if is_valid:
        return user
    else:
        return None
    
async def update_auth_token(user: Users, db: AsyncSession):
    token = secrets.token_hex(32)
    user.token = token
    await db.commit()
    return token

async def get_user_by_token(token, db: AsyncSession):
    result = await db.execute(select(Users).where(Users.token == token))
    user = result.scalar_one_or_none()
    if user:
        return user
    else:
        return None


async def create_user_project(token, name, db: AsyncSession):
    user = await get_user_by_token(token=token, db=db)
    if not user:
        return None
    user_id = user.id
    project = Projects(name=name, owner_id=user_id)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    
    return project


async def add_task_to_project(token, name, project_id, db: AsyncSession):
    user = await get_user_by_token(token=token, db=db)
    if not user:
        return None
    
    result = await db.execute(
        select(Projects).where(
            Projects.project_id == project_id,
            Projects.owner_id == user.id
        )
    )

    project = result.scalar_one_or_none()

    if not project:
        return None
    
    task = Tasks(name=name, project_id=project_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task



async def get_user_project(token, project_id, db: AsyncSession):
    user = await get_user_by_token(token=token, db=db)
    if not user:
        return None
    
    result = await db.execute(
        select(Projects)
        .options(selectinload(Projects.tasks)) 
        .where(
            Projects.project_id == project_id,
            Projects.owner_id == user.id
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        return None
    

    return {
        "project_id": project.project_id,
        "project_name": project.name,
        "created_at": project.created_at,
        "tasks_count": len(project.tasks),
        "tasks": [
            {
                "task_id": task.task_id,
                "name": task.name,
                "created_at": task.created_at,
                "is_completed": task.is_completed
            }
            for task in project.tasks
        ]
    }


async def set_task_is_complete(token, task_id, is_completed, db: AsyncSession):
    user = await get_user_by_token(token=token, db=db)
    if not user:
        return None
    
    result = await db.execute(
        select(Tasks)
        .join(Projects)
        .where(
            Tasks.task_id == task_id,
            Projects.owner_id == user.id
        )
    )
    task = result.scalar_one_or_none()
    if task:
        task.is_completed = is_completed
        await db.commit()
        return task
    else:
        return None
