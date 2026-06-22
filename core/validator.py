def validate_match(m: dict):

    # =========================
    # V1-FREEZE: 类型检查
    # =========================
    if not isinstance(m, dict):
        raise ValueError("match 必须是 dict")

    必要字段 = ["home", "away", "result", "odds"]

    for f in 必要字段:
        if f not in m:
            raise ValueError(f"缺少字段: {f}")

    # =========================
    # V1-FREEZE: result 标准化
    # =========================
    result = str(m["result"]).strip().upper()

    if result not in ["H", "D", "A"]:
        raise ValueError("result 必须是 H/D/A")

    # =========================
    # V1-FREEZE: odds 类型检查
    # =========================
    if not isinstance(m["odds"], dict):
        raise ValueError("odds 必须是 dict")

    for k in ["H", "D", "A"]:
        if k not in m["odds"]:
            raise ValueError(f"缺少赔率字段: {k}")

    return True
