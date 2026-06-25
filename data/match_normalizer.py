def normalize_match(match):
    if not isinstance(match, dict):
        return None

    home = (match.get("home") or "").strip()
    away = (match.get("away") or "").strip()

    if not home or not away:
        return None

    result = match.get("result")

    if result is None:
        return None

    result = str(result).strip().upper()

    if result not in {"H", "D", "A"}:
        return None

    odds = match.get("odds")

    return {
        "home": home,
        "away": away,
        "result": result,
        "odds": odds if isinstance(odds, dict) else {"H": 2.5, "D": 3.2, "A": 2.8},
    }
