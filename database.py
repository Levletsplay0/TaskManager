from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import User, Base

async_engine = create_async_engine("sqlite+aiosqlite:///users.db")

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)



async def init_db():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_user(username, password, email):
    async with AsyncSessionLocal() as session:
        user = User(username=username, password=password, email=email)
        session.add(user)
        await session.commit()
        return user

async def get_user_by_name(username):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()