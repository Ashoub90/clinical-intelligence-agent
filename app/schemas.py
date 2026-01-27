from pydantic import ConfigDict, BaseModel
from datetime import datetime
from typing import List, Optional

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