import os
import json
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

WANWU_API_KEY = os.getenv("WANWU_API_KEY", "").strip()
WANWU_BASE_URL = os.getenv("WANWU_BASE_URL", "").strip()
WANWU_EMBEDDING_MODEL_ID = os.getenv("WANWU_EMBEDDING_MODEL_ID", "").strip()

DEFAULT_KNOWLEDGE_NAME = "Filemanagement Demo Knowledge"
DEFAULT_KNOWLEDGE_DESC = "Filemanagement Demo 自动创建知识库"


def mask_key(key: str) -> str:
    if not key:
        return "(empty)"
    if len(key) <= 8:
        return key[:2] + "***"
    return key[:4] + "***" + key[-4:]


def test_create_knowledge():
    if not WANWU_API_KEY:
        print("❌ 未读取到 WANWU_API_KEY，请检查 backend/.env")
        return

    if not WANWU_BASE_URL:
        print("❌ 未读取到 WANWU_BASE_URL，请检查 backend/.env")
        return

    if not WANWU_EMBEDDING_MODEL_ID:
        print("❌ 未读取到 WANWU_EMBEDDING_MODEL_ID，请检查 backend/.env")
        return

    url = f"{WANWU_BASE_URL}/knowledge"
    headers = {
        "Authorization": f"Bearer {WANWU_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": "产品说明书知识库",
        "description": "存储各产品的详细说明书内容",
        "embeddingModelInfo": {
            "modelId": "2027388627373264896"
        },
        "knowledgeGraph": {
            "switch": False,
            "llmModelId": "",
            "schemaUrl": ""
        },
        "category": 0
    }


    print("====== 万悟创建知识库测试开始 ======")
    print("请求地址:", url)
    print("API Key:", mask_key(WANWU_API_KEY))
    print("Embedding Model ID:", WANWU_EMBEDDING_MODEL_ID)
    print("请求体:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print("HTTP状态码:", response.status_code)
        print("响应原文:")
        print(response.text)
        print()

        try:
            data = response.json()
        except Exception:
            print("❌ 响应不是合法 JSON")
            return

        code = data.get("code")
        msg = data.get("msg")

        if response.status_code == 200 and code == 0:
            print("✅ 创建知识库成功")
            result = data.get("data") or {}
            print("返回数据:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("knowledgeId:", result.get("knowledgeId", ""))
        else:
            print("❌ 创建知识库失败")
            print("业务状态码 code:", code)
            print("业务消息 msg:", msg)

    except requests.exceptions.RequestException as e:
        print("❌ 请求异常:")
        print(str(e))


if __name__ == "__main__":
    test_create_knowledge()