import requests
import json

url = "http://119.188.221.193:8081/service/api/openapi/v1/knowledge/select"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer ww-c0c50cb5ee324b5f8a78d4dd8ff4f1cd"
}

payload = {
    "name": "产品说明书知识库",
    "description": "存储各产品的详细说明书内容",
    "embeddingModelInfo": {
        "modelId": "3"
    },
    "category": 0
}

response = requests.post(url, headers=headers, json=payload, timeout=30)

print("HTTP状态码:", response.status_code)
print("响应内容:")
try:
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
except Exception:
    print(response.text)
