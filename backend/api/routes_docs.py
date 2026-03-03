from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

from services.wanwu_service import (
    get_doc_list,
    status_to_text,
    delete_docs_from_knowledge,
    get_doc_segments,
    get_doc_config,
    update_doc_config
)

from utils.response import success

router = APIRouter()


class DeleteDocsRequest(BaseModel):
    docIdList: list[str]


@router.get("/docs/list")
def docs_list():
    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()
    if not knowledge_id:
        raise HTTPException(status_code=500, detail="未配置 WANWU_KNOWLEDGE_ID")

    try:
        data = get_doc_list(
            knowledge_id=knowledge_id,
            doc_name="",
            page_no=1,
            page_size=100
        )

        doc_list = data.get("list") or []
        result = []

        for item in doc_list:
            file_name = item.get("docName", "")
            file_type = item.get("docType", "")
            if file_type and not str(file_type).startswith("."):
                file_type = f".{file_type}"

            result.append({
                "docId": item.get("docId", ""),
                "fileName": file_name,
                "fileType": file_type or "-",
                "parseMode": "wanwu",
                "segmentMode": item.get("segmentMethod", "通用分段"),
                "uploadTime": item.get("uploadTime", ""),
                "status": item.get("status", -1),
                "statusText": status_to_text(item.get("status", -1)),
                "errorMsg": item.get("errorMsg", "")
            })

        return success(
            data={
                "knowledge_id": knowledge_id,
                "list": result
            },
            message="获取当前知识库文档列表成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档列表失败: {str(e)}")


@router.delete("/docs")
def delete_docs(data: DeleteDocsRequest):
    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()
    if not knowledge_id:
        raise HTTPException(status_code=500, detail="未配置 WANWU_KNOWLEDGE_ID")

    try:
        delete_docs_from_knowledge(
            knowledge_id=knowledge_id,
            doc_id_list=data.docIdList
        )

        return success(
            data={},
            message="删除文档成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文档失败: {str(e)}")

@router.get("/docs/detail")
def doc_detail(docId: str, keyword: str = "", pageNo: int = 1, pageSize: int = 8):
    try:
        data = get_doc_segments(
            doc_id=docId,
            keyword=keyword,
            page_no=pageNo,
            page_size=pageSize
        )
        return success(
            data=data,
            message="获取文档详情成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档详情失败: {str(e)}")

class UpdateDocConfigRequest(BaseModel):
    docIdList: list[str]
    config: dict


@router.get("/docs/config")
def doc_config(docId: str):
    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()
    if not knowledge_id:
        raise HTTPException(status_code=500, detail="未配置 WANWU_KNOWLEDGE_ID")

    try:
        data = get_doc_config(
            knowledge_id=knowledge_id,
            doc_id=docId
        )
        return success(
            data=data,
            message="获取文档配置成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档配置失败: {str(e)}")


@router.post("/docs/update-config")
def docs_update_config(data: UpdateDocConfigRequest):
    knowledge_id = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()
    if not knowledge_id:
        raise HTTPException(status_code=500, detail="未配置 WANWU_KNOWLEDGE_ID")

    try:
        update_doc_config(
            knowledge_id=knowledge_id,
            doc_id_list=data.docIdList,
            config=data.config
        )
        return success(
            data={},
            message="更新文档配置成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新文档配置失败: {str(e)}")