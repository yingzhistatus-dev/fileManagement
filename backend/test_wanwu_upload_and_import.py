import os
import json
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

WANWU_API_KEY = os.getenv("WANWU_API_KEY", "").strip()
WANWU_BASE_URL = os.getenv("WANWU_BASE_URL", "").strip()
WANWU_KNOWLEDGE_ID = os.getenv("WANWU_KNOWLEDGE_ID", "").strip()

TEST_FILE_PATH = os.path.join(BASE_DIR, "uploads", "关于建立客户沟通与答疑统一口径的建议.docx")


def upload_file():
    url = f"{WANWU_BASE_URL}/file/upload/direct"
    headers = {
        "Authorization": f"Bearer {WANWU_API_KEY}"
    }

    with open(TEST_FILE_PATH, "rb") as f:
        files = {
            "files": (os.path.basename(TEST_FILE_PATH), f)
        }
        response = requests.post(url, headers=headers, files=files, timeout=120)

    print("===== 上传文件响应 =====")
    print("HTTP状态码:", response.status_code)
    print(response.text)

    data = response.json()
    if response.status_code != 200 or data.get("code") != 0:
        raise ValueError(f"上传失败: {response.text}")

    data_obj = data.get("data") or {}
    file_list = data_obj.get("files") or []
    if not file_list:
        raise ValueError("上传成功，但未返回 files 列表")

    return file_list[0]


def import_doc(upload_info):
    url = f"{WANWU_BASE_URL}/knowledge/doc/import"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WANWU_API_KEY}"
    }

    file_name = upload_info.get("fileName", "")
    file_size = upload_info.get("fileSize", 0)

    payload = {
        "knowledgeId": WANWU_KNOWLEDGE_ID,
        "docImportType": 0,
        "docInfoList": [
            {
                "docId": upload_info.get("fileId"),
                "docName": file_name,
                "docUrl": upload_info.get("filePath"),
                "docType": os.path.splitext(file_name)[1],
                "docSize": int(file_size)
            }
        ],
        "docSegment": {
            "segmentMethod": "0",
            "segmentType": "0"
        },
        "docAnalyzer": ["text"],
        "docPreprocess": ["replaceSymbols", "deleteLinks"]
    }

    print("\n===== 导入请求体 =====")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    response = requests.post(url, headers=headers, json=payload, timeout=120)

    print("\n===== 导入文档响应 =====")
    print("HTTP状态码:", response.status_code)
    print(response.text)

    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception:
        pass


if __name__ == "__main__":
    if not WANWU_API_KEY:
        print("❌ 未读取到 WANWU_API_KEY")
        raise SystemExit

    if not WANWU_BASE_URL:
        print("❌ 未读取到 WANWU_BASE_URL")
        raise SystemExit

    if not WANWU_KNOWLEDGE_ID:
        print("❌ 未读取到 WANWU_KNOWLEDGE_ID")
        raise SystemExit

    if not os.path.exists(TEST_FILE_PATH):
        print(f"❌ 测试文件不存在: {TEST_FILE_PATH}")
        raise SystemExit

    upload_info = upload_file()
    print("\n===== 上传得到的文件信息 =====")
    print(json.dumps(upload_info, ensure_ascii=False, indent=2))

    import_doc(upload_info)