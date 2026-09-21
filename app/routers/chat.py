from fastapi import APIRouter, Depends
from app.security.auth import get_current_user
from pydantic import BaseModel

from app.ai.graph import chat_graph


router = APIRouter(
    prefix="/chat",
    tags=["AI Chatbot"],
    dependencies=[Depends(get_current_user)]
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Ask the AI chatbot",
    description="Ask a question about the student database."
)
def chat(request: ChatRequest):
    result = chat_graph.invoke({
        "question": request.question
    })

    return {
        "answer": result["answer"]
    }