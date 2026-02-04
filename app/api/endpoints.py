
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.models import ChatRequest, ChatResponse, ExecuteRequest, ExecuteResponse, SummarizeRequest, SummarizeResponse
from app.core.llm import LLMService
from app.core.sandbox import Sandbox
from app.services.analyzer import AnalysisService

router = APIRouter()
llm_service = LLMService()
sandbox = Sandbox()
analyzer = AnalysisService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = llm_service.chat(request.message, request.history)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    """
    Direct execution of code in sandbox (triggered by Run button).
    """
    result = sandbox.execute(request.code)
    return ExecuteResponse(
        success=result['success'],
        stdout=result['output'],
        stderr=result['error'],
        error=result['error']
    )

@router.post("/analyze")
async def analyze_error(code: str, error: str):
    """
    Analyze and fix endpoint (could be used by chat or separate UI action).
    """
    result = await analyzer.analyze_and_fix(code, error)
    return result

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    # Basic summarization - could use LLM for this too
    return SummarizeResponse(summary="Chat history summarized.")
