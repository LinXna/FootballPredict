from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json

from live.ws_adapter import handle_ws_event

router = APIRouter()

# session: ws -> match_id
sessions = {}


# =========================
# WebSocket 主入口
# =========================
@router.websocket("/ws/live")
async def live(ws: WebSocket):
    await ws.accept()

    match_id = None

    try:
        # =========================
        # 1️⃣ 初始化连接（必须第一条消息）
        # =========================
        init = await ws.receive_json()

        if init.get("type") != "connect":
            await ws.send_json({"error": "first message must be connect"})
            await ws.close()
            return

        match_id = init["match_id"]
        sessions[ws] = match_id

        await ws.send_json({"status": "connected", "match_id": match_id})

        # =========================
        # 2️⃣ 主循环
        # =========================
        while True:
            data = await ws.receive_json()

            # =========================
            # 2.1 心跳
            # =========================
            if data.get("type") == "ping":
                await ws.send_json({"type": "pong"})
                continue

            # =========================
            # 2.2 业务事件
            # =========================
            try:
                result = handle_ws_event(match_id, data)

                await ws.send_json(result)

            except Exception as e:
                # ❗保证连接不断
                await ws.send_json({"error": str(e), "recoverable": True})

    except WebSocketDisconnect:
        pass

    except Exception as e:
        try:
            await ws.send_json({"error": f"fatal: {str(e)}"})
        except:
            pass

    finally:
        sessions.pop(ws, None)
        try:
            await ws.close()
        except:
            pass
