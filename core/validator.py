# core/validator.py

from core.constants import Result


def validate_match(m: dict):
    if not isinstance(m, dict):
        raise ValueError("match must be dict")

    required = ["home", "away", "result", "odds"]

    for f in required:
        if f not in m:
            raise ValueError(f"missing field: {f}")

    home = m["home"]
    away = m["away"]

    if not home or not away:
        raise ValueError("home/away invalid")

    # =========================
    # normalize result
    # =========================
    result = str(m["result"]).strip().upper()

    if result not in {r.value for r in Result}:
        raise ValueError("result must be H/D/A")

    # =========================
    # odds validation
    # =========================
    odds = m["odds"]

    if not isinstance(odds, dict):
        raise ValueError("odds must be dict")

    for k in ["H", "D", "A"]:
        if k not in odds:
            raise ValueError(f"missing odds key: {k}")

        if not isinstance(odds[k], (int, float)):
            raise ValueError(f"invalid odds type: {k}")

        if odds[k] <= 0:
            raise ValueError(f"invalid odds value: {k}")

    return True
