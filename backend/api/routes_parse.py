import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.file_service import find_file_by_id, read_text_file
from services.wanwu_service import parse_file_with_wanwu
from utils.response import success

router = APIRouter()


from typing import Optional, Dict, Any

class ParseRequest(BaseModel):
    file_id: str
    config: Optional[Dict[str, Any]] = None


@router.post("/parse")
def parse_file(data: ParseRequest):
    file_path = find_file_by_id(data.file_id)

    if not file_path:
        raise HTTPException(status_code=404, detail="未找到对应文件，请先上传")

    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()

    try:
        # txt 文件继续走本地读取，方便你保留原有演示
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext == ".txt":
            text = read_text_file(file_path)
            return success(
                data={
                    "text": text,
                    "file_name": os.path.basename(file_path),
                    "mode": "local_text"
                },
                message="解析成功"
            )

        # 其他文档走真实万悟
        result = parse_file_with_wanwu(
            file_path=file_path,
            knowledge_id=knowledge_id,
            config=data.config or {}
        )
        result["mode"] = "wanwu"

        return success(
            data=result,
            message="万悟解析流程执行完成"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")