from live.manager import LiveManager
from live.events import MatchEvent, EventType

from app.main import live_manager


# =====================================================
# EVENT PARSER (CRITICAL FIX)
# =====================================================
def _parse_event(data: dict) -> MatchEvent:

    event_type = data.get("event_type", "unknown")

    try:
        event_type = EventType(event_type)
    except Exception:
        event_type = EventType.UNKNOWN

    return MatchEvent(
        minute=int(data.get("minute", 0)),
        event_type=event_type,
        team=data.get("team"),
        player=data.get("player"),
        payload=data.get("payload", {}),
    )


# =====================================================
# WS HANDLER
# =====================================================
def handle_ws_event(match_id: str, data: dict):

    # -------------------------
    # runtime via manager (FIXED)
    # -------------------------
    runtime = live_manager.get_runtime(match_id)

    if runtime is None:
        return {"error": f"match not found: {match_id}"}

    # -------------------------
    # SAFE EVENT CONVERSION
    # -------------------------
    try:
        event = _parse_event(data)
    except Exception as ex:
        return {"error": f"invalid event: {str(ex)}"}

    # -------------------------
    # EXECUTE
    # -------------------------
    result = runtime.step(event)

    # -------------------------
    # SAFE RESPONSE
    # -------------------------
    state = runtime.state

    return {
        "match_id": match_id,
        "state": {
            "home_score": state.home_score,
            "away_score": state.away_score,
            "minute": state.minute,
        },
        "prob": result.get("prob") if isinstance(result, dict) else result,
    }
5