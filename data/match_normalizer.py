def normalize_match(match):
    return {
        # =========================
        # V1-FREEZE: 基础字段标准化
        # =========================
        "home": match.get("home", ""),
        "away": match.get("away", ""),
        # =========================
        # V1-FREEZE: result 标准化（关键）
        # =========================
        "result": str(match["result"]).strip().upper(),
        # =========================
        # V1-FREEZE: odds 安全兜底
        # =========================
        "odds": match.get("odds", {"H": 2.0, "D": 3.0, "A": 3.0}),
    }
