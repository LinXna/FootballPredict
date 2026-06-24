from live.manager import LiveManager

# ⚠️ 这里应该是你全局单例
from app.main import live_manager


# =========================
# WebSocket 业务适配层
# =========================
def handle_ws_event(match_id: str, data: dict):
    """
    WS → Runtime 转换层
    """

    runtime = live_manager.runtimes.get(match_id)

    if runtime is None:
        return {"error": f"match not found: {match_id}"}

    # =========================
    # 构造 event（轻量版）
    # =========================
    event = data  # V1.7先直接透传（后续可强化 schema）

    # =========================
    # 执行 runtime
    # =========================
    result = runtime.step(event)

    # =========================
    # 确保 JSON安全
    # =========================
    return {
        "match_id": match_id,
        "state": {
            "home_score": runtime.state.home_score,
            "away_score": runtime.state.away_score,
            "minute": runtime.state.minute,
        },
        "prob": result["prob"] if isinstance(result, dict) else result,
    }
