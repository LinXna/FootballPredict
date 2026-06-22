from live.state import MatchState


class StateStore:
    def __init__(self):
        self.states = {}

    def create(self, match_id, home, away):
        self.states[match_id] = MatchState(home, away)

    def get(self, match_id):
        return self.states.get(match_id)

    def exists(self, match_id):
        return match_id in self.states