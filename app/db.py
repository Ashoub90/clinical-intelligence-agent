from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 1. The Connection String
# Use the direct IP address instead of the word 'localhost'
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@127.0.0.1:5433/medical_rag"
# 2. The Engine
# We removed create_url because the engine handles the string directly
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. The Session Factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Dependency to get a DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()