from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://wave:payroll123@localhost/payroll"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    pool_pre_ping=True,
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        print("Database is connected")
        yield session
