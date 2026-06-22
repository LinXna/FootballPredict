import csv
from data.match_normalizer import normalize_match
from data.odds_normalizer import normalize_odds


def load_real_matches(path="data/real_matches.csv"):
    matches = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            # =========================
            # V1-FREEZE: 安全解析比分
            # =========================
            try:
                hg = int(float(row["home_goals"]))
                ag = int(float(row["away_goals"]))
            except:
                continue

            # =========================
            # V1-FREEZE: 结果推导
            # =========================
            if hg > ag:
                result = "H"
            elif hg < ag:
                result = "A"
            else:
                result = "D"

            # =========================
            # V1-FREEZE: match标准化
            # =========================
            match = normalize_match(
                {
                    "home": row.get("home", "").strip(),
                    "away": row.get("away", "").strip(),
                    "result": result,
                }
            )

            # =========================
            # V1-FREEZE: odds安全接入
            # =========================
            raw_odds = {
                "H": row.get("odds_h", 2.0),
                "D": row.get("odds_d", 3.0),
                "A": row.get("odds_a", 3.0),
            }

            odds = normalize_odds(raw_odds)

            match["odds"] = odds

            matches.append(match)

    return matches
