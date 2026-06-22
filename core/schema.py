from typing import TypedDict


class Match(TypedDict):
    home: str
    away: str

    # V1-FREEZE: must be one of ["H", "D", "A"] (upper-case only)
    result: str

    # V1-FREEZE: must contain keys {"H","D","A"} with float odds
    odds: dict  # {"H": float, "D": float, "A": float}
