import math
from collections import defaultdict


class PoissonModel:
    """
    V3.5 Stable Poisson Model
    - 支持 train + predict_1x2
    - 用于 pipeline.train / ensemble
    """

    def __init__(self, league_avg_goals=1.35):
        self.league_avg_goals = league_avg_goals

        # 简化版攻击/防守强度
        self.team_attack = defaultdict(lambda: 1.0)
        self.team_defense = defaultdict(lambda: 1.0)

    # =====================================================
    # TRAIN (关键补丁)
    # =====================================================
    def train(self, matches):
        """
        V3.5 最小训练逻辑：
        根据进球更新 attack / defense
        """

        for m in matches:
            home = m["home"]
            away = m["away"]

            hg = self._get_goals(m, "home")
            ag = self._get_goals(m, "away")

            # update attack/defense (lightweight learning)
            self.team_attack[home] += hg * 0.01
            self.team_defense[home] += ag * 0.01

            self.team_attack[away] += ag * 0.01
            self.team_defense[away] += hg * 0.01

    # =====================================================
    # GOAL SAFE GETTER
    # =====================================================
    def _get_goals(self, m, side: str):
        if "home_goals" in m:
            return float(m[f"{side}_goals"])
        return 1.0  # fallback for normalized data

    # =====================================================
    # POISSON CORE
    # =====================================================
    def poisson(self, lam, k):
        lam = max(lam, 1e-6)
        return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))

    def _lambda(self, attack, defense):
        return self.league_avg_goals * (attack / max(defense, 1e-6))

    # =====================================================
    # SCORE MATRIX
    # =====================================================
    def predict_score_probs(self, home, away, max_goals=5):
        home_lambda = self._lambda(
            self.team_attack[home],
            self.team_defense[away],
        )
        away_lambda = self._lambda(
            self.team_attack[away],
            self.team_defense[home],
        )

        matrix = {}
        total = 0.0

        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                p = self.poisson(home_lambda, i) * self.poisson(away_lambda, j)
                matrix[(i, j)] = p
                total += p

        # normalize
        for k in matrix:
            matrix[k] /= total

        return matrix

    # =====================================================
    # 1X2 OUTPUT
    # =====================================================
    def predict_1x2(self, home, away):
        score_probs = self.predict_score_probs(home, away)

        H = D = A = 0.0

        for (i, j), p in score_probs.items():
            if i > j:
                H += p
            elif i == j:
                D += p
            else:
                A += p

        total = H + D + A

        return {
            "H": H / total,
            "D": D / total,
            "A": A / total,
        }
