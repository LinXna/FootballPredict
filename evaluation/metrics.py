import math


def logloss(pred, actual):

    p = max(1e-9, min(pred.get(actual, 0.0), 1 - 1e-9))
    return -math.log(p)


def brier_score(pred, actual):

    score = 0.0

    for k in ["H", "D", "A"]:
        y = 1 if k == actual else 0
        p = pred.get(k, 0.0)
        score += (p - y) ** 2

    return score
