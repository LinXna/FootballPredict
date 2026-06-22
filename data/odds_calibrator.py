def odds_to_prob(odds):
    """
    data/odds_calibrator.py | V1-FREEZE
    odds = {"H": 2.1, "D": 3.2, "A": 3.5}
    """

    # =========================
    # V1-FREEZE: 安全转换 + 限幅
    # =========================
    raw = {}

    for k, v in odds.items():

        # 防止非法输入
        try:
            v = float(v)
        except:
            v = 1e9

        # V1-FREEZE: 合理赔率区间约束
        v = max(v, 1.01)
        v = min(v, 100.0)

        raw[k] = 1 / v

    total = sum(raw.values())

    # =========================
    # V1-FREEZE: 防止异常输入
    # =========================
    if total <= 0:
        return {"H": 0.33, "D": 0.34, "A": 0.33}

    # =========================
    # V1-FREEZE: 去水归一化
    # =========================
    return {k: v / total for k, v in raw.items()}
