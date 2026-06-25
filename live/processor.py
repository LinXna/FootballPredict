import time
from collections import defaultdict, deque

from live.state import MatchState
from live.events import MatchEvent, EventType


class EventProcessor:

    def __init__(self):

        # match_id -> recent events
        self._seen = defaultdict(deque)

        # TTL for dedup (seconds equivalent proxy via size window)
        self._max_seen = 500

    # =====================================================
    # PROCESS SINGLE EVENT
    # =====================================================
    def process(self, state: MatchState, event: MatchEvent) -> MatchState:

        event_key = self._make_key(event)

        if self._is_duplicate(state, event_key):
            return state

        self._mark_seen(state, event_key)

        # -------------------------
        # append event
        # -------------------------
        state.events.append(event)

        # -------------------------
        # goal logic
        # -------------------------
        if event.event_type == EventType.GOAL:

            if event.team == state.home:
                state.home_score += 1
            elif event.team == state.away:
                state.away_score += 1

        # -------------------------
        # own goal logic
        # -------------------------
        elif event.event_type == EventType.OWN_GOAL:

            if event.team == state.home:
                state.away_score += 1
            elif event.team == state.away:
                state.home_score += 1

        # -------------------------
        # time update
        # -------------------------
        if event.minute > state.minute:
            state.minute = event.minute

        # -------------------------
        # state transition
        # -------------------------
        self._update_status(state)

        return state

    # =====================================================
    # BATCH PROCESS
    # =====================================================
    def process_all(self, state: MatchState, events: list[MatchEvent]) -> MatchState:

        # assume upstream may or may not sort → safe idempotent
        for event in sorted(events, key=lambda e: e.minute):
            state = self.process(state, event)

        return state

    # =====================================================
    # KEY GENERATION (stronger)
    # =====================================================
    def _make_key(self, event: MatchEvent):

        return (
            event.minute,
            event.event_type.value,
            event.team,
            event.player,
        )

    # =====================================================
    # DEDUP CONTROL (bounded memory)
    # =====================================================
    def _is_duplicate(self, state: MatchState, key):

        dq = self._seen[id(state)]

        return key in dq

    def _mark_seen(self, state: MatchState, key):

        dq = self._seen[id(state)]

        dq.append(key)

        if len(dq) > self._max_seen:
            dq.popleft()

    # =====================================================
    # STATE MACHINE (cleaned)
    # =====================================================
    def _update_status(self, state: MatchState):

        if state.status == "FT":
            return

        if state.minute >= 90:
            state.status = "FT"

        elif state.minute >= 45 and state.status == "1H":
            state.status = "2H"
