from sqlalchemy import Column, Integer, Text, String, DateTime, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


# =========================
# 1. Medical Documents (RAG)
# =========================
class MedicalDocument(Base):
    __tablename__ = "medical_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    embedding = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# =========================
# 2. Coverage Rules (Policy DB - MVP)
# =========================
class CoverageRule(Base):
    __tablename__ = "coverage_rules"

    id = Column(Integer, primary_key=True, index=True)
    plan = Column(String, index=True)  # Silver, Gold, Bronze
    treatment_type = Column(String, index=True)  # medication, injection, surgery
    covered = Column(Boolean)
    notes = Column(Text)


# =========================
# 3. Users (Customers)
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    plan = Column(String, index=True)  # Silver, Gold, Bronze
    age = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# =========================
# 4. Query Logs (Audit & HITL)
# =========================
class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    query = Column(Text)
    answer = Column(Text)
    confidence = Column(Float)
    action = Column(String)  # answer | clarify | escalate
    retrieved_chunks = Column(Text)  # store text or IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
