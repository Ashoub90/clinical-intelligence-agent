from pydantic import ConfigDict, BaseModel
from datetime import datetime
from typing import Optional

# This is the "Base" rules for a document
class MedicalDocumentBase(BaseModel):
    filename: str
    content: str

# This is what the API sends BACK to the user
# It includes the ID and the timestamp from the DB
class MedicalDocumentRead(MedicalDocumentBase):
    id: int
    created_at: datetime
    
    # This part is crucial! It tells Pydantic to play nice with SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

# This is for when we want to search (The Query)
class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 5

# =========================
# Coverage Rules
# =========================
class CoverageRuleRead(BaseModel):
    plan: str
    treatment_type: str
    covered: bool
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# =========================
# Users
# =========================
class UserRead(BaseModel):
    id: int
    name: str
    plan: str
    age: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# Agent Query
# =========================
class AgentQueryRequest(BaseModel):
    user_id: int
    question: str


class AgentQueryResponse(BaseModel):
    action: str        # answer | clarify | escalate
    answer: str
    confidence: float
    evidence: Optional[str]    