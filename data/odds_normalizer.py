def normalize_odds(raw_odds):

    # =========================
    # V1-FREEZE: 安全转换函数
    # =========================
    def safe_float(x):
        try:
            return float(x)
        except:
            return 1e9

    def clamp(v):
        v = max(v, 1.01)
        v = min(v, 100.0)
        return v

    return {
        # =========================
        # V1-FREEZE: 赔率标准化 + 防御
        # =========================
        "H": clamp(safe_float(raw_odds.get("H", 2.0))),
        "D": clamp(safe_float(raw_odds.get("D", 3.0))),
        "A": clamp(safe_float(raw_odds.get("A", 3.0))),
    }
