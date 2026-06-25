from features.form import FormFeature
from features.h2h import H2HFeature


class FeatureBuilder:

    def __init__(self):
        self.form = FormFeature(window=5)
        self.h2h = H2HFeature()

    def train_update(self, match):

        if not isinstance(match, dict):
            return

        self.form.update(match)
        self.h2h.update(match)

    def build(self, home, away):

        if not home or not away:
            return None

        home_form = self.form.get_form(home)
        away_form = self.form.get_form(away)

        h2h = self.h2h.get_h2h(home, away)

        if not isinstance(h2h, dict):
            h2h = {"H": 0.34, "D": 0.33, "A": 0.33}

        return {
            "home_form": float(home_form),
            "away_form": float(away_form),
            "h2h_H": float(h2h.get("H", 0.34)),
            "h2h_D": float(h2h.get("D", 0.33)),
            "h2h_A": float(h2h.get("A", 0.33)),
        }
