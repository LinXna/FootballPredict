from collections import defaultdict


class H2HFeature:

    def __init__(self):

        # =========================
        # V1-FREEZE: head-to-head统计
        # =========================
        self.record = defaultdict(lambda: {"H": 0, "D": 0, "A": 0, "total": 0})

    def update(self, match):

        # =========================
        # V1-FREEZE: 安全读取
        # =========================
        home = match.get("home")
        away = match.get("away")
        result = str(match.get("result", "")).strip().upper()

        if not home or not away or not result:
            return

        # =========================
        # V1-FREEZE: directional key
        # =========================
        key = (home, away)

        if result == "H":
            self.record[key]["H"] += 1

        elif result == "A":
            self.record[key]["A"] += 1

        else:
            self.record[key]["D"] += 1

        self.record[key]["total"] += 1

    def get_h2h(self, home, away):

        # =========================
        # V1-FREEZE: query key
        # =========================
        key = (home, away)
        r = self.record[key]

        if r["total"] == 0:
            # V1-FREEZE: weak prior (avoid full symmetry)
            return {"H": 0.34, "D": 0.33, "A": 0.33}

        return {
            "H": r["H"] / r["total"],
            "D": r["D"] / r["total"],
            "A": r["A"] / r["total"],
        }
