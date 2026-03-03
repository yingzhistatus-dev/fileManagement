import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

load_dotenv(os.path.join(BASE_DIR, ".env"))

ARK_API_KEY = os.getenv("ARK_API_KEY", "").strip()
ARK_BASE_URL = os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3").strip()
ARK_MODEL = os.getenv("ARK_MODEL", "").strip()

WANWU_API_KEY = os.getenv("WANWU_API_KEY", "").strip()
WANWU_BASE_URL = os.getenv("WANWU_BASE_URL", "").strip()
WANWU_EMBEDDING_MODEL_ID = os.getenv("WANWU_EMBEDDING_MODEL_ID", "").strip()
WANWU_USER_TOKEN = os.getenv("WANWU_USER_TOKEN", "").strip()
WANWU_X_ORG_ID = os.getenv("WANWU_X_ORG_ID", "").strip()
WANWU_X_USER_ID = os.getenv("WANWU_X_USER_ID", "").strip()
WANWU_X_CLIENT_ID = os.getenv("WANWU_X_CLIENT_ID", "").strip()
WANWU_AGENT_UUID = os.getenv("WANWU_AGENT_UUID", "").strip()

DEFAULT_KNOWLEDGE_NAME = os.getenv("DEFAULT_KNOWLEDGE_NAME", "Filemanagement Demo Knowledge").strip()
DEFAULT_KNOWLEDGE_DESC = os.getenv("DEFAULT_KNOWLEDGE_DESC", "Filemanagement Demo 自动创建知识库").strip()