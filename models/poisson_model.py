import math


class PoissonModel:
    def __init__(self):
        self.base = 1.35

    def _p(self, lam, k):
        return (lam**k) * math.exp(-lam) / math.factorial(k)

    def predict_1x2(self, home, away):
        home_lambda = 1.4
        away_lambda = 1.1

        H = D = A = 0.0

        for i in range(0, 4):
            for j in range(0, 4):
                p = self._p(home_lambda, i) * self._p(away_lambda, j)

                if i > j:
                    H += p
                elif i == j:
                    D += p
                else:
                    A += p

        s = H + D + A
        return {"H": H / s, "D": D / s, "A": A / s}
