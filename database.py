from sqlalchemy import Column, String, Integer, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

async_engine = create_async_engine("sqlite+aiosqlite:///users.db")
Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


async def init_db():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_user(name):
    async with AsyncSessionLocal() as session:
        user = User(name=name)
        session.add(user)
        await session.commit()
        return user

async def get_user_by_name(name):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()