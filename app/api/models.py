
from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []
    summary: Optional[str] = ""

class ChatResponse(BaseModel):
    response: str
    detail: Optional[str] = None

class ExecuteRequest(BaseModel):
    code: str

class ExecuteResponse(BaseModel):
    success: bool
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""
    error: Optional[str] = None

class SummarizeRequest(BaseModel):
    history: List[dict]

class SummarizeResponse(BaseModel):
    summary: str
