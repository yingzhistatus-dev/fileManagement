import os
import json
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

WANWU_API_KEY = os.getenv("WANWU_API_KEY", "").strip()
WANWU_BASE_URL = os.getenv("WANWU_BASE_URL", "").strip()


def mask_key(key: str) -> str:
    if not key:
        return "(empty)"
    if len(key) <= 8:
        return key[:2] + "***"
    return key[:4] + "***" + key[-4:]


def test_select_knowledge(name=""):
    if not WANWU_API_KEY:
        print("❌ 未读取到 WANWU_API_KEY，请检查 backend/.env")
        return

    if not WANWU_BASE_URL:
        print("❌ 未读取到 WANWU_BASE_URL，请检查 backend/.env")
        return

    url = f"{WANWU_BASE_URL}/knowledge/select"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WANWU_API_KEY}"
    }

    payload = {}
    if name:
        payload["name"] = name

    print("====== 查询知识库列表测试开始 ======")
    print("请求地址:", url)
    print("API Key:", mask_key(WANWU_API_KEY))
    print("请求体:", json.dumps(payload, ensure_ascii=False))
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
            print("✅ 接口调用成功")
            knowledge_list = (data.get("data") or {}).get("knowledgeList") or []
            print(f"知识库数量: {len(knowledge_list)}")

            if knowledge_list:
                print("\n知识库列表：")
                for i, item in enumerate(knowledge_list, 1):
                    print(f"\n--- 第 {i} 条 ---")
                    print("knowledgeId:", item.get("knowledgeId", ""))
                    print("name:", item.get("name", ""))
                    print("description:", item.get("description", ""))
                    print("docCount:", item.get("docCount", ""))
                    print("category:", item.get("category", ""))
                    print("createAt:", item.get("createAt", ""))
                    print("updatedAt:", item.get("updatedAt", ""))
                    print("embeddingModelInfo:", item.get("embeddingModelInfo", {}))
            else:
                print("当前没有查到知识库。")
        else:
            print("❌ 接口调用失败")
            print("业务状态码 code:", code)
            print("业务消息 msg:", msg)

    except requests.exceptions.RequestException as e:
        print("❌ 请求异常:")
        print(str(e))


if __name__ == "__main__":
    # 你可以把这里改成具体名称，比如 "产品说明书"
    test_select_knowledge("")