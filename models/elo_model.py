import math
from collections import defaultdict


class EloModel:
    """
    V3.5 Stable Elo Model
    - 支持 update / predict / rating storage
    - 用于 Pipeline.train + Pipeline.predict
    """

    def __init__(self, k: float = 32, clamp: float = 400):
        self.k = k
        self.clamp = clamp

        # ⭐ 必须存在：球队评分表
        self.ratings = defaultdict(lambda: 1500)

    # =====================================================
    # BASIC RATING
    # =====================================================
    def get_rating(self, team: str) -> float:
        return self.ratings[team]

    # =====================================================
    # EXPECTED SCORE
    # =====================================================
    def expected(self, ra: float, rb: float) -> float:
        diff = (rb - ra) / self.clamp
        return 1 / (1 + 10**diff)

    # =====================================================
    # UPDATE (TRAINING)
    # =====================================================
    def update(self, home: str, away: str, result: str):
        ra = self.get_rating(home)
        rb = self.get_rating(away)

        # result mapping
        if result == "H":
            sa, sb = 1.0, 0.0
        elif result == "A":
            sa, sb = 0.0, 1.0
        else:
            sa, sb = 0.5, 0.5

        ea = self.expected(ra, rb)
        eb = 1 - ea

        self.ratings[home] = ra + self.k * (sa - ea)
        self.ratings[away] = rb + self.k * (sb - eb)

    # =====================================================
    # PREDICT (1X2 PROBABILITY)
    # =====================================================
    def predict(self, home: str, away: str) -> dict:
        ra = self.get_rating(home)
        rb = self.get_rating(away)

        ph = self.expected(ra, rb)
        pa = 1 - ph

        # draw model (simple symmetric heuristic)
        draw = max(0.05, 1 - abs(ph - pa))

        raw = {"H": ph, "D": draw, "A": pa}

        # normalize
        total = sum(raw.values())
        return {k: v / total for k, v in raw.items()}
