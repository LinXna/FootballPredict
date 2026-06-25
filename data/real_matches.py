import csv
import logging

from data.match_normalizer import normalize_match
from data.odds_normalizer import normalize_odds

logger = logging.getLogger(__name__)


def load_real_matches(path="data/real_matches.csv"):
    matches = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader):

            try:
                hg = row.get("home_goals")
                ag = row.get("away_goals")

                if hg is None or ag is None:
                    logger.warning(f"missing goals at row {idx}")
                    continue

                hg = int(float(hg))
                ag = int(float(ag))

            except Exception as e:
                logger.warning(f"invalid score row {idx}: {e}")
                continue

            # result inference
            if hg > ag:
                result = "H"
            elif hg < ag:
                result = "A"
            else:
                result = "D"

            try:
                match = normalize_match(
                    {
                        "home": (row.get("home") or "").strip(),
                        "away": (row.get("away") or "").strip(),
                        "result": result,
                    }
                )

                if not match:
                    continue

            except Exception as e:
                logger.warning(f"normalize_match failed row {idx}: {e}")
                continue

            raw_odds = {
                "H": row.get("odds_h"),
                "D": row.get("odds_d"),
                "A": row.get("odds_a"),
            }

            try:
                odds = normalize_odds(raw_odds)
            except Exception:
                odds = {"H": 2.5, "D": 3.2, "A": 2.8}

            match["odds"] = odds

            matches.append(match)

    return matches
