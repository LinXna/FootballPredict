from collections import deque, defaultdict


class FormFeature:

    def __init__(self, window=5):

        # =========================
        # V1-FREEZE: rolling window form tracking
        # =========================
        self.window = window
        self.history = defaultdict(lambda: deque(maxlen=window))

    def update(self, match):

        # =========================
        # V1-FREEZE: safe field access
        # =========================
        home = match.get("home")
        away = match.get("away")
        result = str(match.get("result", "")).strip().upper()

        if not home or not away or not result:
            return

        # =========================
        # V1-FREEZE: form encoding
        # =========================
        if result == "H":
            self.history[home].append(1)
            self.history[away].append(0)

        elif result == "A":
            self.history[home].append(0)
            self.history[away].append(1)

        else:
            self.history[home].append(0.5)
            self.history[away].append(0.5)

    def get_form(self, team):

        # =========================
        # V1-FREEZE: cold start handling
        # =========================
        h = self.history.get(team)

        if not h:
            return 0.5

        return sum(h) / len(h)
