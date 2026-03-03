import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

WANWU_BASE_URL = os.getenv("WANWU_BASE_URL","")
WANWU_API_KEY = os.getenv("WANWU_API_KEY", "")

class RagChatReq(BaseModel):
    uuid: str
    query: str
    stream: bool = False


@router.post("/wanwu/rag-chat")
def wanwu_rag_chat(req: RagChatReq):
    if not WANWU_API_KEY:
        raise HTTPException(status_code=500, detail="缺少 WANWU_API_KEY")

    url = f"{WANWU_BASE_URL}/rag/chat"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {WANWU_API_KEY}",
    }

    payload = {
        "uuid": req.uuid,
        "query": req.query,
        "stream": req.stream,
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"请求 wanwu 失败: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="wanwu 返回的不是合法 JSON")

    return {
        "code": data.get("code"),
        "message": data.get("message"),
        "msg_id": data.get("msg_id"),
        "output": data.get("data", {}).get("output", ""),
        "searchList": data.get("data", {}).get("searchList", []),
        "history": data.get("history", []),
        "finish": data.get("finish"),
    }