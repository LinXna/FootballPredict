def build_features(match, team_stats):

    if not isinstance(match, dict):
        return None

    home = (match.get("home") or "").strip()
    away = (match.get("away") or "").strip()

    if not home or not away:
        return None

    if not isinstance(team_stats, dict):
        team_stats = {}

    home_strength = float(team_stats.get(home, 1.0) or 1.0)
    away_strength = float(team_stats.get(away, 1.0) or 1.0)

    return {
        "home_strength": home_strength,
        "away_strength": away_strength,
        "strength_diff": home_strength - away_strength,
    }
