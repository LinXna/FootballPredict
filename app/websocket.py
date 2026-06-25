from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import uuid

from live.ws_adapter import handle_ws_event

router = APIRouter()

# -------------------------
# session store (safe key)
# -------------------------
sessions: dict[str, WebSocket] = {}
ws_to_match: dict[WebSocket, str] = {}


# =========================
# WebSocket entry
# =========================
@router.websocket("/ws/live")
async def live(ws: WebSocket):
    await ws.accept()

    session_id = str(uuid.uuid4())
    match_id = None

    try:
        # -------------------------
        # init message
        # -------------------------
        try:
            init = await ws.receive_json()
        except Exception:
            await ws.send_json({"error": "invalid json init"})
            await ws.close()
            return

        if init.get("type") != "connect":
            await ws.send_json({"error": "first message must be connect"})
            await ws.close()
            return

        match_id = init.get("match_id")

        if not match_id:
            await ws.send_json({"error": "missing match_id"})
            await ws.close()
            return

        # bind session
        sessions[session_id] = ws
        ws_to_match[ws] = match_id

        await ws.send_json(
            {"status": "connected", "session_id": session_id, "match_id": match_id}
        )

        # -------------------------
        # main loop
        # -------------------------
        while True:

            try:
                data = await ws.receive_json()
            except Exception:
                await ws.send_json({"error": "invalid json"})
                continue

            # -------------------------
            # heartbeat
            # -------------------------
            if data.get("type") == "ping":
                await ws.send_json({"type": "pong"})
                continue

            # -------------------------
            # business event
            # -------------------------
            try:
                result = handle_ws_event(match_id, data)

                if result is None:
                    raise ValueError("handler returned None")

                await ws.send_json(result)

            except Exception as e:
                # error is reported but connection kept alive
                await ws.send_json({"error": str(e), "recoverable": True})

    except WebSocketDisconnect:
        pass

    except Exception as e:
        try:
            await ws.send_json({"error": f"fatal: {str(e)}"})
        except Exception:
            pass

    finally:
        sessions.pop(session_id, None)
        ws_to_match.pop(ws, None)

        try:
            await ws.close()
        except Exception:
            pass
