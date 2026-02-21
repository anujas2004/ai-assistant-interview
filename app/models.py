from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    user_id: str
    question: str
    mode: Optional[str] = "dsa"   # default mode


class ChatResponse(BaseModel):
    response: str