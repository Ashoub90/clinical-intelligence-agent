from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import engine
from app.models import Base
from sqlalchemy import text
from app.agent import ClinicalAgent
from app.schemas import AgentQueryRequest
from fastapi.middleware.cors import CORSMiddleware
from app.models import QueryLog
from app.db import AsyncSessionLocal
from sqlalchemy import select


agent = ClinicalAgent()

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask")
async def ask_agent(request: AgentQueryRequest):
    result = await agent.handle_query(
        user_id=request.user_id,
        question=request.question
    )
    return result

@app.get("/logs")
async def get_logs():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(QueryLog).order_by(QueryLog.created_at.desc()).limit(50)
        )
        logs = result.scalars().all()

        return [
            {
                "id": log.id,
                "user_id": log.user_id,
                "query": log.query,
                "answer": log.answer,
                "confidence": log.confidence,
                "action": log.action,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]




