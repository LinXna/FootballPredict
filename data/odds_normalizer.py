def normalize_odds(raw_odds):

    if not isinstance(raw_odds, dict):
        return {"H": 2.5, "D": 3.2, "A": 2.8}

    def safe_float(x):
        try:
            v = float(x)
        except Exception:
            return None
        return v

    def clamp(v):
        if v is None:
            return None
        return max(1.01, min(v, 20.0))  # 收紧上界

    result = {}

    for k in ["H", "D", "A"]:
        v = clamp(safe_float(raw_odds.get(k)))

        if v is None:
            # 不再用 1e9（避免 bias）
            v = 3.0

        result[k] = v

    return result
