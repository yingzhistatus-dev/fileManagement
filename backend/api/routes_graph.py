from fastapi import APIRouter, HTTPException
import os

from services.wanwu_service import get_knowledge_graph
from utils.response import success

router = APIRouter()


@router.get("/graph")
def graph_data():
    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()
    if not knowledge_id:
        raise HTTPException(status_code=500, detail="未配置 WANWU_KNOWLEDGE_ID")

    try:
        data = get_knowledge_graph(knowledge_id)
        return success(
            data={
                "knowledgeId": knowledge_id,
                **data
            },
            message="获取知识图谱成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识图谱失败: {str(e)}")