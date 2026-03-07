from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import Users, Base, Projects
from werkzeug.security import generate_password_hash, check_password_hash
import secrets



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
    if user:
        user_id = user.id
        project = Projects(name=name, owner_id=user_id)
        db.add(project)
        await db.commit()
        
        return project
    else:
        return None
