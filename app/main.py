from fastapi import FastAPI
from app.api import router as api_router
from app.websocket import router as ws_router
import logging

# -----------------------
# Logger（替代 print）
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# -----------------------
# Debug WebSocket Routes
# -----------------------
logger.info(f"WS ROUTES COUNT: {len(ws_router.routes)}")

for r in ws_router.routes:
    logger.info(f"WS ROUTE: {r}")

# -----------------------
# Router Registration
# -----------------------
app.include_router(api_router)
app.include_router(ws_router)
