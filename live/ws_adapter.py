from live.events import MatchEvent


def parse_event(data: dict) -> MatchEvent:
    return MatchEvent(
        minute=data.get("minute", 0),
        type=data.get("type", "unknown"),
        team=data.get("team"),
        player=data.get("player"),
    )


def handle_ws_event(live_engine, match_id: str, data: dict):
    event = parse_event(data)
    return live_engine.push_event(match_id, event)
