from fastapi import APIRouter, Depends, Request, HTTPException
from src.models.query_models import QueryRequest, QueryResponse
from src.services.knowledge_service import KnowledgeService

router = APIRouter()

def get_service(request: Request) -> KnowledgeService:
    return request.app.state.knowledge_service

@router.post("/ask", response_model=QueryResponse)
def ask_question(request_body: QueryRequest, service: KnowledgeService = Depends(get_service)):
    try:
        answer = service.answer_question(request_body.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
