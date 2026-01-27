from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import engine
from app.models import Base
from sqlalchemy import text

# 1. The Lifespan "Manager"
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up: Checking Database Tables...")
    async with engine.begin() as conn:
        # 1. Enable the pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        # 2. Create the tables
        await conn.run_sync(Base.metadata.create_all)
        
    print("✅ Extension enabled and Tables are ready.")
    yield
    print("🛑 Shutting down...")
    await engine.dispose()

# 2. Initialize the App
app = FastAPI(
    title="Clinical Intelligence Agent",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Clinical Intelligence Agent API is Live"}