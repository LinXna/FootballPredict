from typing import TypedDict


class Odds(TypedDict):
    H: float
    D: float
    A: float


class Match(TypedDict):
    home: str
    away: str
    result: str
    odds: Odds | None
