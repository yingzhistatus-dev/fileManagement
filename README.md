# fileManagement

一个面向文档管理与知识库处理的示例项目。  
本项目基于 **JavaScript 前端 + Python 后端** 搭建，集成了 **Wanwu 知识库相关接口** 与 **豆包大模型**，用于完成文档上传、解析入库、知识库文档管理、分段查看、内容总结、知识图谱展示、社区报告展示以及智能问答等功能。

---

## 1. 项目简介

`fileManagement` 是一个档案/文档智能管理演示项目，核心目标是：

- 将本地文件上传到系统
- 调用 Wanwu 接口完成文档解析并导入已有知识库
- 对知识库中的文档进行展示、删除、配置修改与重解析
- 查看文档分段详情
- 基于文档内容生成摘要
- 展示知识图谱与社区报告
- 提供基于知识库内容的智能问答能力

这个项目适合作为以下场景的原型或 Demo：

- 档案资料智能管理
- 企业知识库管理
- 文档解析与结构化处理
- 基于大模型的文档摘要与问答应用

---

## 2. 已实现功能

### 2.1 文件上传
支持用户从本地选择文件并上传到系统中。

### 2.2 文档解析并导入知识库
上传后的文件可调用 Wanwu 相关接口进行解析，并导入**已有知识库**中。  
目前项目不是新建知识库，而是直接使用一个已经存在的知识库。

### 2.3 知识库文档列表展示
以表格形式展示当前知识库中的文档列表，便于查看和管理。

### 2.4 批量删除文档
支持勾选多个知识库文档后进行批量删除。

### 2.5 查看文档分段详情
支持查看某个文档被解析后的分段内容，便于后续摘要生成与内容分析。

### 2.6 单文档摘要生成
可以基于选中文档的分段内容，调用大模型生成对应摘要。

### 2.7 文档配置获取与更新
支持获取指定文档的解析配置，并在修改后重新解析文档。

### 2.8 知识图谱页面
通过后端代理 Wanwu 用户侧接口，获取并展示知识图谱相关内容。

### 2.9 社区报告页面
通过后端代理 Wanwu 用户侧接口，获取并展示社区报告内容。

### 2.10 智能问答
项目中已接入问答能力，支持：

- API 方式问答
- 嵌入式 WebChat 方式问答

---

## 3. 技术栈

### 前端
- Vue
- JavaScript
- Axios
- Vue Router
- Element Plus（如项目中已使用）

### 后端
- Python 3.11
- Flask / FastAPI（按你的实际项目框架替换）
- Requests
- Python-dotenv

### 模型与平台
- **Wanwu**：用于知识库、文档解析、文档分段、图谱、社区报告等能力
- **豆包大模型**：用于摘要生成等文本理解与生成任务

---

## 4. 项目结构示例

```bash
fileManagement/
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── assets/
│   │   │   └── styles/
│   │   ├── components/
│   │   ├── router/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── requirements.txt
│   └── .env
└── README.md
```
## 5. 环境要求
### 前端环境
- Node.js 16 及以上
- npm 或 yarn
### 后端环境
- Python 3.11
- conda 或 venv 均可

## 6. 配置说明
### 配置说明
```
WANWU_BASE_URL=你的万悟接口地址
WANWU_API_KEY=你的万悟API_KEY
WANWU_KNOWLEDGE_BASE_ID=你的已有知识库ID

WANWU_USER_TOKEN=你的用户token
WANWU_ORG_ID=你的X-Org-Id
WANWU_USER_ID=你的X-User-Id
WANWU_CLIENT_ID=你的X-Client-Id

DOUBAO_API_KEY=你的豆包API_KEY
DOUBAO_MODEL=你的豆包模型名称
```
## 7. 安装与启动

### 7.1 启动后端

先进入后端目录：

```bash
cd backend
conda create -n filemanagement python=3.11 -y
conda activate filemanagement
pip install -r requirements.txt
```
启动命令
```
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 7.1 启动前端
进入前端目录：
```bash
cd frontend
npm install
```

启动命令
```
npm run dev
```

启动成功后，浏览器中打开前端本地地址，例如：
```
http://localhost:5173
```

