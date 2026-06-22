def build_features(match, team_stats):

    # =========================
    # V1-FREEZE: 安全读取match字段
    # =========================
    home = match.get("home", "")
    away = match.get("away", "")

    # =========================
    # V1-FREEZE: 基础强度特征
    # =========================
    home_strength = team_stats.get(home, 1.0)
    away_strength = team_stats.get(away, 1.0)

    # =========================
    # V1-FREEZE: 输出结构化特征
    # =========================
    return {
        "home_strength": home_strength,
        "away_strength": away_strength,
        "strength_diff": home_strength - away_strength,
    }
