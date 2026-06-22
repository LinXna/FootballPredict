class EloModel:

    def __init__(self, k=32):

        # =========================
        # V1-FREEZE: learning rate
        # =========================
        self.k = k
        self.ratings = {}

    def get_rating(self, team):

        # =========================
        # V1-FREEZE: default rating
        # =========================
        return self.ratings.get(team, 1500)

    def expected(self, ra, rb):

        # =========================
        # V1-FREEZE: logistic expectation
        # =========================
        diff = (rb - ra) / 400
        return 1 / (1 + 10**diff)

    def update(self, home, away, result):

        # =========================
        # V1-FREEZE: ratings lookup
        # =========================
        ra = self.get_rating(home)
        rb = self.get_rating(away)

        ea = self.expected(ra, rb)
        eb = 1 - ea

        # =========================
        # V1-FREEZE: outcome encoding
        # =========================
        if result == "H":
            sa, sb = 1, 0
        elif result == "A":
            sa, sb = 0, 1
        else:
            sa, sb = 0.5, 0.5

        self.ratings[home] = ra + self.k * (sa - ea)
        self.ratings[away] = rb + self.k * (sb - eb)

    def predict(self, home, away):

        # =========================
        # V1-FREEZE: probability estimation
        # =========================
        ra = self.get_rating(home)
        rb = self.get_rating(away)

        ph = self.expected(ra, rb)
        pa = 1 - ph

        draw = max(0.05, 1 - abs(ph - pa))

        raw = {"H": ph, "A": pa, "D": draw}

        # =========================
        # V1-FREEZE: normalization
        # =========================
        total = sum(raw.values())

        return {k: v / total for k, v in raw.items()}
