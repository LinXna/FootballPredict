from collections import defaultdict


class H2HFeature:

    def __init__(self):
        self.record = defaultdict(lambda: {"H": 0, "D": 0, "A": 0, "total": 0})

    def update(self, match):

        if not isinstance(match, dict):
            return

        home = match.get("home")
        away = match.get("away")
        result = str(match.get("result", "")).strip().upper()

        if not home or not away or result not in {"H", "D", "A"}:
            return

        key = (home, away)

        if result == "H":
            self.record[key]["H"] += 1
        elif result == "A":
            self.record[key]["A"] += 1
        else:
            self.record[key]["D"] += 1

        self.record[key]["total"] += 1

    def get_h2h(self, home, away):

        key = (home, away)
        r = self.record.get(key)

        if not r or r["total"] == 0:
            return {"H": 0.34, "D": 0.33, "A": 0.33}

        total = float(r["total"])

        h = r["H"] / total
        d = r["D"] / total
        a = r["A"] / total

        # smoothing safety
        s = h + d + a
        if s <= 0:
            return {"H": 0.34, "D": 0.33, "A": 0.33}

        return {
            "H": h / s,
            "D": d / s,
            "A": a / s,
        }
