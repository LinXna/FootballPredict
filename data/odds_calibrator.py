def odds_to_prob(odds):
    if not odds:
        return {"H": 0.33, "D": 0.33, "A": 0.34}

    inv = {}
    for k in ["H", "D", "A"]:
        v = float(odds.get(k, 3.0))
        v = max(1.01, v)
        inv[k] = 1.0 / v

    s = sum(inv.values())
    return {k: v / s for k, v in inv.items()}
