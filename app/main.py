from fastapi import FastAPI
from app.api import router as api_router
from app.websocket import router as ws_router
import logging

# -----------------------
# Logger (safe for production)
# -----------------------
logger = logging.getLogger("football_predict")

# 不再使用 basicConfig（避免污染 uvicorn）
logger.setLevel(logging.INFO)


# -----------------------
# FastAPI app
# -----------------------
app = FastAPI()


# -----------------------
# Startup hook（补齐架构缺失）
# -----------------------
@app.on_event("startup")
def startup_event():
    logger.info("[STARTUP] FootballPredict API starting...")

    # 不再打印 route 详情（避免污染日志）
    logger.info(f"[STARTUP] API routes loaded: {len(api_router.routes)}")
    logger.info(f"[STARTUP] WS routes loaded: {len(ws_router.routes)}")


# -----------------------
# Router registration
# -----------------------
app.include_router(api_router)

# websocket 作为独立模块注册
app.include_router(ws_router)


# -----------------------
# Optional: health check endpoint
# -----------------------
@app.get("/health")
def health():
    return {"status": "ok"}
