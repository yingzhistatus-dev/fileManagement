from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_upload import router as upload_router
from api.routes_parse import router as parse_router
from api.routes_summary import router as summary_router
from api.routes_docs import router as docs_router
from api.routes_graph import router as graph_router
from api.routes_report import router as report_router
from api.routes_chat import router as chat_router

app = FastAPI(title="Filemanagement Demo Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(parse_router, prefix="/api")
app.include_router(summary_router, prefix="/api")
app.include_router(docs_router, prefix="/api")
app.include_router(graph_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Filemanagement Demo Backend is running"}