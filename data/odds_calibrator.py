def odds_to_prob(odds):
    """
    Convert bookmaker odds to normalized probability
    """

    if not isinstance(odds, dict):
        return {"H": 0.33, "D": 0.34, "A": 0.33}

    required = ["H", "D", "A"]

    raw = {}

    for k in required:

        v = odds.get(k, 100.0)

        try:
            v = float(v)
        except Exception:
            v = 100.0

        # clamp odds
        v = max(1.01, min(v, 100.0))

        raw[k] = 1.0 / v

    total = sum(raw.values())

    if total <= 0:
        return {"H": 0.33, "D": 0.34, "A": 0.33}

    return {k: raw[k] / total for k in required}
