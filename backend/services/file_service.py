import os
import uuid

from utils.config import UPLOAD_DIR, OUTPUT_DIR


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def init_storage():
    ensure_dir(UPLOAD_DIR)
    ensure_dir(OUTPUT_DIR)


def save_upload_file(upload_file):
    init_storage()

    file_id = str(uuid.uuid4())
    original_name = upload_file.filename
    save_name = f"{file_id}_{original_name}"
    save_path = os.path.join(UPLOAD_DIR, save_name)

    return file_id, save_name, save_path


def find_file_by_id(file_id: str):
    init_storage()

    for filename in os.listdir(UPLOAD_DIR):
        if filename.startswith(file_id + "_"):
            return os.path.join(UPLOAD_DIR, filename)
    return None


def read_text_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="gbk", errors="ignore") as f:
            return f.read()