class EloModel:

    def __init__(self, k: float = 32, clamp: float = 400):

        self.k = k
        self.clamp = clamp

        # ratings store
        self.ratings = {}

    # =====================================================
    # GET RATING
    # =====================================================
    def get_rating(self, team):

        return self.ratings.get(team, 1500)

    # =====================================================
    # EXPECTED SCORE
    # =====================================================
    def expected(self, ra, rb):

        diff = (rb - ra) / self.clamp
        return 1 / (1 + 10**diff)

    # =====================================================
    # TRAIN STEP (controlled update)
    # =====================================================
    def update(self, home, away, result):

        ra = self.get_rating(home)
        rb = self.get_rating(away)

        ea = self.expected(ra, rb)
        eb = 1 - ea

        # outcome encoding
        if result == "H":
            sa, sb = 1, 0
        elif result == "A":
            sa, sb = 0, 1
        else:
            sa, sb = 0.5, 0.5

        # =========================
        # bounded update (FIX)
        # =========================
        delta_a = self.k * (sa - ea)
        delta_b = self.k * (sb - eb)

        self.ratings[home] = self._clamp_rating(ra + delta_a)
        self.ratings[away] = self._clamp_rating(rb + delta_b)

    # =====================================================
    # PREDICT (deterministic)
    # =====================================================
    def predict(self, home, away):

        ra = self.get_rating(home)
        rb = self.get_rating(away)

        ph = self.expected(ra, rb)
        pa = 1 - ph

        # stable draw model (kept but constrained)
        draw = self._draw_probability(ph, pa)

        raw = {"H": ph, "A": pa, "D": draw}

        total = sum(raw.values())

        return {k: v / total for k, v in raw.items()}

    # =====================================================
    # DRAW MODEL (isolated)
    # =====================================================
    def _draw_probability(self, ph, pa):

        base = 1 - abs(ph - pa)

        # safe lower bound
        if base < 0.05:
            base = 0.05

        return base

    # =====================================================
    # RATING CLAMP (FIX DRIFT)
    # =====================================================
    def _clamp_rating(self, rating):

        # prevent extreme drift
        if rating > 3000:
            return 3000
        if rating < 1000:
            return 1000

        return rating
