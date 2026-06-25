# core/constants.py

from enum import Enum

# =========================
# Match Fields
# =========================


class Field(str, Enum):
    HOME = "home"
    AWAY = "away"
    RESULT = "result"
    ODDS = "odds"


# =========================
# Result Labels
# =========================


class Result(str, Enum):
    HOME_WIN = "H"
    DRAW = "D"
    AWAY_WIN = "A"
