from fastapi import APIRouter, File, UploadFile, HTTPException

from services.file_service import save_upload_file
from utils.response import success

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    try:
        file_id, save_name, save_path = save_upload_file(file)

        content = await file.read()
        with open(save_path, "wb") as f:
            f.write(content)

        return success(
            data={
                "file_id": file_id,
                "file_name": file.filename,
                "save_name": save_name,
                "file_path": save_path
            },
            message="文件上传成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")