import math
from collections import defaultdict


class PoissonModel:

    def __init__(self, league_avg_goals=1.35):

        # attack/defense strength
        self.team_attack = defaultdict(lambda: 1.0)
        self.team_defense = defaultdict(lambda: 1.0)

        self.league_avg = league_avg_goals

    # =====================================================
    # TRAIN (heuristic but stabilized)
    # =====================================================
    def train(self, matches):

        for m in matches:

            home = m["home"]
            away = m["away"]
            result = m["result"]

            # NOTE: still heuristic proxy (not real xG)
            if result == "H":
                home_goals, away_goals = 2, 1
            elif result == "A":
                home_goals, away_goals = 1, 2
            else:
                home_goals, away_goals = 1, 1

            # update attack/defense
            self.team_attack[home] += home_goals * 0.1
            self.team_defense[away] += home_goals * 0.1

            self.team_attack[away] += away_goals * 0.1
            self.team_defense[home] += away_goals * 0.1

    # =====================================================
    # STABLE POISSON (log-space)
    # =====================================================
    def poisson(self, lam, k):

        lam = max(lam, 1e-6)

        # log Poisson for stability
        log_p = k * math.log(lam) - lam - math.lgamma(k + 1)

        return math.exp(log_p)

    # =====================================================
    # LAMBDA ESTIMATION (calibrated)
    # =====================================================
    def _lambda(self, attack, defense):

        return max(0.05, self.league_avg * (attack / max(defense, 1e-3)))

    # =====================================================
    # SCORE MATRIX
    # =====================================================
    def predict_score_probs(self, home, away, max_goals=5):

        home_lambda = self._lambda(self.team_attack[home], self.team_defense[away])

        away_lambda = self._lambda(self.team_attack[away], self.team_defense[home])

        matrix = {}

        total = 0.0

        for i in range(max_goals + 1):
            for j in range(max_goals + 1):

                p = self.poisson(home_lambda, i) * self.poisson(away_lambda, j)

                matrix[(i, j)] = p
                total += p

        # normalize (CRITICAL FIX)
        for k in matrix:
            matrix[k] /= total

        return matrix

    # =====================================================
    # 1X2 AGGREGATION
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

        return {"H": H / total, "D": D / total, "A": A / total}
