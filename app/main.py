from fastapi import FastAPI
from app.api import router as api_router
from app.websocket import router as ws_router

app = FastAPI()
print("WS ROUTES COUNT:", len(ws_router.routes))
for r in ws_router.routes:
    print(r)
app.include_router(api_router)
app.include_router(ws_router)
