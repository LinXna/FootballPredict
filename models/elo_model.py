class EloModel:
    def __init__(self):
        self.rating = {}

    def get(self, team):
        return self.rating.get(team, 1500)

    def expected(self, ra, rb):
        return 1 / (1 + 10 ** ((rb - ra) / 400))

    def predict(self, home, away):
        ra = self.get(home)
        rb = self.get(away)

        ph = self.expected(ra, rb)
        pa = 1 - ph

        draw = 0.25

        raw = {"H": ph * 0.7, "A": pa * 0.7, "D": draw}

        s = sum(raw.values())
        return {k: v / s for k, v in raw.items()}
