from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.doubao_service import generate_summary_with_doubao
from utils.response import success

router = APIRouter()


class SummaryRequest(BaseModel):
    content: str


@router.post("/summary")
def generate_summary(data: SummaryRequest):
    try:
        summary = generate_summary_with_doubao(data.content)

        return success(
            data={
                "summary": summary
            },
            message="摘要生成成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"摘要生成失败: {str(e)}")