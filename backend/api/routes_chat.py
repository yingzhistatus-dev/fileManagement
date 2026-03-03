from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.wanwu_service import create_agent_conversation, agent_chat
from utils.response import success

router = APIRouter()


class CreateConversationRequest(BaseModel):
    title: str


class ChatRequest(BaseModel):
    conversation_id: str
    query: str
    stream: bool = False


@router.post("/chat/conversation")
def create_conversation(data: CreateConversationRequest):
    try:
        result = create_agent_conversation(title=data.title)
        return success(
            data=result,
            message="创建对话成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建对话失败: {str(e)}")


@router.post("/chat/message")
def chat_message(data: ChatRequest):
    try:
        result = agent_chat(
            conversation_id=data.conversation_id,
            query=data.query,
            stream=data.stream
        )
        return success(
            data=result,
            message="对话成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")