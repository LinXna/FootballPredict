import math
from collections import defaultdict


class PoissonModel:

    def __init__(self):

        # =========================
        # V1-FREEZE: attack/defense ratings
        # =========================
        self.team_attack = defaultdict(lambda: 1.0)
        self.team_defense = defaultdict(lambda: 1.0)

    def train(self, matches):

        for m in matches:

            home = m["home"]
            away = m["away"]
            result = m["result"]

            # =========================
            # V1-FREEZE: surrogate goal model (not real xG)
            # =========================
            if result == "H":
                home_goals, away_goals = 2, 1
            elif result == "A":
                home_goals, away_goals = 1, 2
            else:
                home_goals, away_goals = 1, 1

            self.team_attack[home] += home_goals * 0.1
            self.team_defense[away] += home_goals * 0.1

            self.team_attack[away] += away_goals * 0.1
            self.team_defense[home] += away_goals * 0.1

    def poisson(self, lam, k):

        # =========================
        # V1-FREEZE: numerical stability
        # =========================
        lam = max(0.01, lam)

        return (lam**k * math.exp(-lam)) / math.factorial(k)

    def predict_score_probs(self, home, away, max_goals=5):

        home_attack = self.team_attack[home]
        away_defense = self.team_defense[away]

        away_attack = self.team_attack[away]
        home_defense = self.team_defense[home]

        # =========================
        # V1-FREEZE: stable lambda estimation
        # =========================
        home_lambda = max(0.05, home_attack / max(away_defense, 0.1))

        away_lambda = max(0.05, away_attack / max(home_defense, 0.1))

        matrix = {}

        # =========================
        # V1-FREEZE: truncated score space (0-5 goals)
        # =========================
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):

                p = self.poisson(home_lambda, i) * self.poisson(away_lambda, j)

                matrix[(i, j)] = p

        return matrix

    def predict_1x2(self, home, away):

        score_probs = self.predict_score_probs(home, away)

        H = 0
        D = 0
        A = 0

        for (i, j), p in score_probs.items():

            if i > j:
                H += p
            elif i == j:
                D += p
            else:
                A += p

        total = H + D + A

        return {"H": H / total, "D": D / total, "A": A / total}
