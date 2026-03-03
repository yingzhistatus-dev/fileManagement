import os
import time
import requests

from utils.config import (
    WANWU_API_KEY,
    WANWU_BASE_URL,
    WANWU_USER_TOKEN,
    WANWU_X_ORG_ID,
    WANWU_X_USER_ID,
    WANWU_X_CLIENT_ID,
    WANWU_AGENT_UUID
)

def _user_headers():
    if not WANWU_USER_TOKEN:
        raise ValueError("未配置 WANWU_USER_TOKEN")
    if not WANWU_X_ORG_ID:
        raise ValueError("未配置 WANWU_X_ORG_ID")
    if not WANWU_X_USER_ID:
        raise ValueError("未配置 WANWU_X_USER_ID")
    if not WANWU_X_CLIENT_ID:
        raise ValueError("未配置 WANWU_X_CLIENT_ID")

    return {
        "Authorization": f"Bearer {WANWU_USER_TOKEN}",
        "X-Org-Id": WANWU_X_ORG_ID,
        "X-User-Id": WANWU_X_USER_ID,
        "X-Client-Id": WANWU_X_CLIENT_ID,
        "Accept": "application/json, text/plain, */*"
    }

def _headers(json_type=True):
    headers = {
        "Authorization": f"Bearer {WANWU_API_KEY}"
    }
    if json_type:
        headers["Content-Type"] = "application/json"
    return headers


def _check_config():
    if not WANWU_API_KEY:
        raise ValueError("未配置 WANWU_API_KEY")
    if not WANWU_BASE_URL:
        raise ValueError("未配置 WANWU_BASE_URL")


def _check_response(resp):
    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"万悟接口返回非 JSON：{resp.text}")

    if resp.status_code != 200:
        raise ValueError(f"万悟接口请求失败：HTTP {resp.status_code} - {resp.text}")

    if data.get("code") != 0:
        raise ValueError(f"万悟接口业务失败：{data.get('msg', '未知错误')}")

    return data


def upload_file_to_wanwu(file_path):
    """
    上传文件到万悟文件服务
    """
    _check_config()

    url = f"{WANWU_BASE_URL}/file/upload/direct"

    if not os.path.exists(file_path):
        raise ValueError("本地文件不存在")

    # 本地文件名格式是：{file_id}_{原始文件名}
    saved_name = os.path.basename(file_path)

    # 上传到万悟时，恢复成原始文件名
    if "_" in saved_name:
        original_name = saved_name.split("_", 1)[1]
    else:
        original_name = saved_name

    with open(file_path, "rb") as f:
        files = {
            "files": (original_name, f)
        }
        resp = requests.post(
            url,
            files=files,
            headers={"Authorization": f"Bearer {WANWU_API_KEY}"},
            timeout=120
        )

    data = _check_response(resp)

    data_obj = data.get("data") or {}
    file_list = data_obj.get("files") or []
    if not file_list:
        raise ValueError("上传成功，但未返回 files 列表")

    return file_list[0]


def import_doc_to_knowledge(knowledge_id, upload_info, config=None):
    """
    导入文档到已有知识库
    """
    _check_config()

    url = f"{WANWU_BASE_URL}/knowledge/doc/import"

    config = config or {}

    file_name = upload_info.get("fileName", "")
    file_size = upload_info.get("fileSize", 0)
    file_ext = os.path.splitext(file_name)[1]   # 保留点号，如 .docx

    payload = {
        "knowledgeId": knowledge_id,
        "docImportType": config.get("docImportType", 0),
        "docInfoList": [
            {
                "docId": upload_info.get("fileId"),
                "docName": file_name,
                "docUrl": upload_info.get("filePath"),
                "docType": file_ext,
                "docSize": int(file_size)
            }
        ],
        "docSegment": config.get("docSegment", {
            "segmentMethod": "0",
            "segmentType": "0"
        }),
        "docAnalyzer": config.get("docAnalyzer", ["text"]),
        "docPreprocess": config.get("docPreprocess", ["replaceSymbols"])
    }

    parser_model_id = config.get("parserModelId", "")
    if parser_model_id:
        payload["parserModelId"] = parser_model_id

    doc_meta_data = config.get("docMetaData", [])
    if doc_meta_data:
        payload["docMetaData"] = doc_meta_data

    resp = requests.post(url, json=payload, headers=_headers(), timeout=120)
    data = _check_response(resp)
    return data.get("data", {})


def get_doc_list(knowledge_id, doc_name="", page_no=1, page_size=20):
    """
    获取知识库文档列表
    """
    _check_config()

    url = f"{WANWU_BASE_URL}/knowledge/doc/list"
    payload = {
        "knowledgeId": knowledge_id,
        "docName": doc_name,
        "pageNo": page_no,
        "pageSize": page_size
    }

    resp = requests.post(url, json=payload, headers=_headers(), timeout=60)
    data = _check_response(resp)
    return data.get("data", {})


def find_doc_in_list(knowledge_id, doc_name):
    """
    在知识库文档列表里按名称查找文档
    """
    data = get_doc_list(
        knowledge_id=knowledge_id,
        doc_name=doc_name,
        page_no=1,
        page_size=50
    )

    doc_list = data.get("list") or []
    for item in doc_list:
        if item.get("docName") == doc_name:
            return item
    return None


def status_to_text(status):
    mapping = {
        -1: "全部",
        0: "待处理",
        1: "处理完成",
        2: "正在审核中",
        3: "正在解析中",
        4: "审核未通过",
        5: "解析失败"
    }
    return mapping.get(status, "未知状态")


def poll_doc_status(knowledge_id, doc_name, max_retries=12, interval=5):
    """
    轮询文档状态
    """
    last_doc = None

    for _ in range(max_retries):
        doc = find_doc_in_list(knowledge_id, doc_name)
        if doc:
            last_doc = doc
            status = doc.get("status")

            if status == 1:
                return {
                    "finished": True,
                    "success": True,
                    "doc": doc
                }

            if status in [4, 5]:
                return {
                    "finished": True,
                    "success": False,
                    "doc": doc
                }

        time.sleep(interval)

    return {
        "finished": False,
        "success": False,
        "doc": last_doc
    }


def parse_file_with_wanwu(file_path, knowledge_id, config=None):
    """
    真实万悟解析流程：
    1. 上传文件
    2. 导入已有知识库
    3. 轮询文档状态
    """
    if not knowledge_id:
        raise ValueError("未提供 knowledge_id，请先配置已有知识库ID")

    upload_info = upload_file_to_wanwu(file_path)

    # 导入任务提交
    import_doc_to_knowledge(knowledge_id, upload_info, config=config or {})

    file_name = upload_info.get("fileName")
    poll_result = poll_doc_status(knowledge_id, file_name)

    doc = poll_result.get("doc") or {}
    status = doc.get("status", -1)

    success = poll_result.get("success", False)
    finished = poll_result.get("finished", False)

    if success:
        text = (
            f"文件已成功导入万悟知识库并完成解析。\n\n"
            f"知识库ID：{knowledge_id}\n"
            f"文档ID：{doc.get('docId', '')}\n"
            f"文件名：{file_name}\n"
            f"当前状态：{status_to_text(status)}"
        )
    elif finished:
        text = (
            f"文件已提交到万悟知识库，但解析失败。\n\n"
            f"知识库ID：{knowledge_id}\n"
            f"文档ID：{doc.get('docId', '')}\n"
            f"文件名：{file_name}\n"
            f"当前状态：{status_to_text(status)}\n"
            f"错误信息：{doc.get('errorMsg', '') or '无'}"
        )
    else:
        text = (
            f"文件已提交到万悟知识库，当前仍在处理中。\n\n"
            f"知识库ID：{knowledge_id}\n"
            f"文档ID：{doc.get('docId', '')}\n"
            f"文件名：{file_name}\n"
            f"当前状态：{status_to_text(status)}"
        )

    return {
        "knowledge_id": knowledge_id,
        "file_id": upload_info.get("fileId"),
        "file_name": file_name,
        "doc_id": doc.get("docId", ""),
        "status": status,
        "status_text": status_to_text(status),
        "error_msg": doc.get("errorMsg", ""),
        "finished": finished,
        "success": success,
        "text": text
    }

def delete_docs_from_knowledge(knowledge_id, doc_id_list):
    """
    从知识库删除一个或多个文档
    """
    _check_config()

    if not knowledge_id:
        raise ValueError("knowledge_id 不能为空")

    if not doc_id_list:
        raise ValueError("doc_id_list 不能为空")

    url = f"{WANWU_BASE_URL}/knowledge/doc"
    payload = {
        "knowledgeId": knowledge_id,
        "docIdList": doc_id_list
    }

    resp = requests.delete(url, json=payload, headers=_headers(), timeout=60)
    data = _check_response(resp)
    return data

def get_doc_segments(doc_id, keyword="", page_no=1, page_size=8):
    if not doc_id:
        raise ValueError("doc_id 不能为空")

    base = WANWU_BASE_URL.replace("/service/api/openapi/v1", "")
    url = f"{base}/user/api/v1/knowledge/doc/segment/list"

    params = {
        "keyword": keyword,
        "docId": doc_id,
        "pageNo": page_no,
        "pageSize": page_size
    }

    resp = requests.get(
        url,
        params=params,
        headers=_user_headers(),
        timeout=60
    )

    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"万悟详情接口返回非 JSON：{resp.text}")

    if resp.status_code != 200:
        raise ValueError(f"万悟详情接口请求失败：HTTP {resp.status_code} - {resp.text}")

    if data.get("code") != 0:
        raise ValueError(f"万悟详情接口业务失败：{data.get('msg', '未知错误')}")

    return data.get("data", {})

def get_doc_config(knowledge_id, doc_id):
    """
    获取文档配置
    """
    _check_config()

    if not knowledge_id:
        raise ValueError("knowledge_id 不能为空")
    if not doc_id:
        raise ValueError("doc_id 不能为空")

    url = f"{WANWU_BASE_URL}/knowledge/doc/config"
    params = {
        "knowledgeId": knowledge_id,
        "docId": doc_id
    }

    resp = requests.get(url, params=params, headers=_headers(), timeout=60)
    data = _check_response(resp)
    return data.get("data", {})


def update_doc_config(knowledge_id, doc_id_list, config):
    """
    更新文档配置并重新解析
    """
    _check_config()

    if not knowledge_id:
        raise ValueError("knowledge_id 不能为空")
    if not doc_id_list:
        raise ValueError("doc_id_list 不能为空")

    payload = {
        "knowledgeId": knowledge_id,
        "docIdList": doc_id_list,
        "docImportType": config.get("docImportType", 0),
        "docSegment": config.get("docSegment", {}),
        "docAnalyzer": config.get("docAnalyzer", ["text"]),
        "parserModelId": config.get("parserModelId", ""),
        "docPreprocess": config.get("docPreprocess", ["replaceSymbols"]),
        "docMetaData": config.get("docMetaData", [])
    }

    url = f"{WANWU_BASE_URL}/knowledge/doc/update/config"
    resp = requests.post(url, json=payload, headers=_headers(), timeout=120)
    data = _check_response(resp)
    return data

def get_knowledge_graph(knowledge_id):
    """
    获取知识图谱（万悟内部用户接口）
    """
    _check_config()

    if not knowledge_id:
        raise ValueError("knowledge_id 不能为空")

    base = WANWU_BASE_URL.replace("/service/api/openapi/v1", "")
    url = f"{base}/user/api/v1/knowledge/graph"

    params = {
        "knowledgeId": knowledge_id
    }

    resp = requests.get(
        url,
        params=params,
        headers=_user_headers(),
        timeout=60
    )

    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"万悟图谱接口返回非 JSON：{resp.text}")

    if resp.status_code != 200:
        raise ValueError(f"万悟图谱接口请求失败：HTTP {resp.status_code} - {resp.text}")

    if data.get("code") != 0:
        raise ValueError(f"万悟图谱接口业务失败：{data.get('msg', '未知错误')}")

    return data.get("data", {})

def get_community_report_list(knowledge_id, page_no=1, page_size=8):
    """
    获取社区报告列表（万悟内部用户接口）
    """
    _check_config()

    if not knowledge_id:
        raise ValueError("knowledge_id 不能为空")

    base = WANWU_BASE_URL.replace("/service/api/openapi/v1", "")
    url = f"{base}/user/api/v1/knowledge/report/list"

    params = {
        "knowledgeId": knowledge_id,
        "pageNo": page_no,
        "pageSize": page_size
    }

    resp = requests.get(
        url,
        params=params,
        headers=_user_headers(),
        timeout=60
    )

    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"万悟社区报告列表接口返回非 JSON：{resp.text}")

    if resp.status_code != 200:
        raise ValueError(f"万悟社区报告列表接口请求失败：HTTP {resp.status_code} - {resp.text}")

    if data.get("code") != 0:
        raise ValueError(f"万悟社区报告列表接口业务失败：{data.get('msg', '未知错误')}")

    return data.get("data", {})


def generate_community_report(knowledge_id):
    """
    生成/重新生成社区报告（万悟内部用户接口）
    """
    _check_config()

    if not knowledge_id:
        raise ValueError("knowledge_id 不能为空")

    base = WANWU_BASE_URL.replace("/service/api/openapi/v1", "")
    url = f"{base}/user/api/v1/knowledge/report/generate"

    payload = {
        "knowledgeId": knowledge_id
    }

    # 这里沿用用户态 header；如果后续 403，再补 Origin/Referer
    resp = requests.post(
        url,
        json=payload,
        headers={**_user_headers(), "Content-Type": "application/json"},
        timeout=60
    )

    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"万悟社区报告生成接口返回非 JSON：{resp.text}")

    if resp.status_code != 200:
        raise ValueError(f"万悟社区报告生成接口请求失败：HTTP {resp.status_code} - {resp.text}")

    if data.get("code") != 0:
        raise ValueError(f"万悟社区报告生成接口业务失败：{data.get('msg', '未知错误')}")

    return data

def create_agent_conversation(title, uuid=None):
    """
    创建智能体对话
    """
    _check_config()

    agent_uuid = uuid or WANWU_AGENT_UUID
    if not agent_uuid:
        raise ValueError("未配置 WANWU_AGENT_UUID")

    url = f"{WANWU_BASE_URL}/agent/conversation"
    payload = {
        "uuid": agent_uuid,
        "title": title
    }

    resp = requests.post(url, json=payload, headers=_headers(), timeout=60)
    data = _check_response(resp)
    return data.get("data", {})


def agent_chat(conversation_id, query, uuid=None, stream=False):
    """
    智能体对话
    """
    _check_config()

    agent_uuid = uuid or WANWU_AGENT_UUID
    if not agent_uuid:
        raise ValueError("未配置 WANWU_AGENT_UUID")
    if not conversation_id:
        raise ValueError("conversation_id 不能为空")
    if not query:
        raise ValueError("query 不能为空")

    url = f"{WANWU_BASE_URL}/agent/chat"
    payload = {
        "uuid": agent_uuid,
        "conversation_id": conversation_id,
        "query": query,
        "stream": stream
    }

    resp = requests.post(url, json=payload, headers=_headers(), timeout=120)
    data = _check_response(resp)
    return data