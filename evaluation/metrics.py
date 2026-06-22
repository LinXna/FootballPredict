import math


def logloss(pred, actual):

    # =========================
    # V1-FREEZE: 安全读取
    # =========================
    p = pred.get(actual, 1e-15)

    # =========================
    # V1-FREEZE: 概率裁剪
    # =========================
    p = min(max(p, 1e-15), 1 - 1e-15)

    return -math.log(p)


def brier_score(pred, actual):

    # =========================
    # V1-FREEZE: 结构防御
    # =========================
    if not all(k in pred for k in ["H", "D", "A"]):
        return 1.0

    score = 0.0

    for k in ["H", "D", "A"]:
        y = 1 if k == actual else 0
        score += (pred[k] - y) ** 2

    return score


def accuracy(pred, actual):

    # =========================
    # V1-FREEZE: 安全判断
    # =========================
    if not pred:
        return False

    return max(pred, key=pred.get) == actual
