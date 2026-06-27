def validate_match(m: dict):
    if "home" not in m or "away" not in m:
        raise ValueError("invalid match")

    m["home"] = str(m["home"]).strip()
    m["away"] = str(m["away"]).strip()
    m["result"] = str(m.get("result", "")).upper()

    return m
