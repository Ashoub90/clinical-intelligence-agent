from pydantic import BaseModel




class AgentQueryRequest(BaseModel):
    user_id: int
    question: str


class AgentQueryResponse(BaseModel):
    answer: str
 