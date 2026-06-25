from collections import deque, defaultdict


class FormFeature:

    def __init__(self, window=5):
        self.window = window
        self.history = defaultdict(lambda: deque(maxlen=window))

    def update(self, match):

        if not isinstance(match, dict):
            return

        home = match.get("home")
        away = match.get("away")
        result = str(match.get("result", "")).strip().upper()

        if not home or not away or result not in {"H", "D", "A"}:
            return

        if result == "H":
            self.history[home].append(1.0)
            self.history[away].append(0.0)

        elif result == "A":
            self.history[home].append(0.0)
            self.history[away].append(1.0)

        else:
            self.history[home].append(0.5)
            self.history[away].append(0.5)

    def get_form(self, team):

        h = self.history.get(team)

        if not h or len(h) == 0:
            return 0.5

        val = sum(h) / len(h)

        return max(0.0, min(1.0, float(val)))
