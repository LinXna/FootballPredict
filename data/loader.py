# data/loader.py
import csv
from typing import List, Dict


class DataLoader:
    """
    V3.5 收敛数据入口
    只负责一件事：把 CSV → 标准 match list
    """

    def __init__(self, path="data/real_matches.csv"):
        self.path = path

    def load(self) -> List[Dict]:
        matches = []

        with open(self.path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                match = {
                    "home": row["home"],
                    "away": row["away"],
                    "result": self._normalize_result(row),
                    "odds": {
                        "H": float(row.get("odds_h", 2.0)),
                        "D": float(row.get("odds_d", 3.0)),
                        "A": float(row.get("odds_a", 3.0)),
                    },
                }
                matches.append(match)

        return matches

    def _normalize_result(self, row):
        hg = int(float(row["home_goals"]))
        ag = int(float(row["away_goals"]))

        if hg > ag:
            return "H"
        elif hg < ag:
            return "A"
        else:
            return "D"
