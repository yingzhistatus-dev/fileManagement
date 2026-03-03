from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

from services.wanwu_service import (
    get_community_report_list,
    generate_community_report
)
from utils.response import success

router = APIRouter()


class GenerateReportRequest(BaseModel):
    pass


@router.get("/reports")
def report_list(pageNo: int = 1, pageSize: int = 8):
    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()
    if not knowledge_id:
        raise HTTPException(status_code=500, detail="未配置 WANWU_KNOWLEDGE_ID")

    try:
        data = get_community_report_list(
            knowledge_id=knowledge_id,
            page_no=pageNo,
            page_size=pageSize
        )
        return success(
            data={
                "knowledgeId": knowledge_id,
                **data
            },
            message="获取社区报告列表成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取社区报告列表失败: {str(e)}")


@router.post("/reports/generate")
def report_generate():
    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()
    if not knowledge_id:
        raise HTTPException(status_code=500, detail="未配置 WANWU_KNOWLEDGE_ID")

    try:
        generate_community_report(knowledge_id)
        return success(
            data={},
            message="已提交社区报告生成任务"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成社区报告失败: {str(e)}")