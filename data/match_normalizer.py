def normalize_match(match):
    return {
        "home": match.get("home", "").strip(),
        "away": match.get("away", "").strip(),
        "result": str(match.get("result", "")).strip().upper(),
        "odds": match.get("odds", None),
    }
