from typing import Dict
import threading
import time

from live.runtime import MatchRuntime
from live.predictor import LivePredictor
from core.pipeline import Pipeline
from live.events import MatchEvent
from live.snapshot import SnapshotStore


class LiveManager:
    """
    Clean V2 LiveManager (NO learning side effects)
    """

    def __init__(self, core_pipeline: Pipeline):

        # =========================
        # Core
        # =========================
        self.core_pipeline = core_pipeline

        # =========================
        # State
        # =========================
        self.runtimes: Dict[str, MatchRuntime] = {}
        self.last_active: Dict[str, float] = {}

        # =========================
        # Lock
        # =========================
        self._lock = threading.RLock()

        # =========================
        # Snapshot
        # =========================
        self.snapshot_store = SnapshotStore()

        # =========================
        # Predictor
        # =========================
        self.predictor = LivePredictor(core_pipeline)

        # =========================
        # TTL
        # =========================
        self.match_ttl = 60 * 30

        # =========================
        # GC control
        # =========================
        self._stop_gc = False
        self._start_gc_thread()

    # =====================================================
    # CREATE MATCH
    # =====================================================
    def create_match(self, match_id: str, home: str, away: str):

        with self._lock:

            if match_id in self.runtimes:
                raise ValueError("Match exists")

            runtime = MatchRuntime(match_id=match_id, predictor=self.predictor)

            runtime.attach_snapshot_store(self.snapshot_store)
            runtime.start(home, away)

            self.runtimes[match_id] = runtime
            self.last_active[match_id] = time.time()

        return {"status": "created", "match_id": match_id}

    # =====================================================
    # GET RUNTIME
    # =====================================================
    def get_runtime(self, match_id: str) -> MatchRuntime:

        with self._lock:
            if match_id not in self.runtimes:
                raise ValueError(f"Match not found: {match_id}")
            return self.runtimes[match_id]

    # =====================================================
    # HANDLE EVENT
    # =====================================================
    def handle_event(self, match_id: str, event: MatchEvent):

        runtime = self.get_runtime(match_id)

        self.last_active[match_id] = time.time()

        return runtime.step(event)

    # =====================================================
    # STATE
    # =====================================================
    def get_state(self, match_id: str):

        runtime = self.get_runtime(match_id)

        return {
            "match_id": match_id,
            "state": {
                "home_score": runtime.state.home_score,
                "away_score": runtime.state.away_score,
                "minute": runtime.state.minute,
            },
            "prob": runtime.predict(),
        }

    # =====================================================
    # REMOVE MATCH
    # =====================================================
    def remove_match(self, match_id: str):

        with self._lock:
            self.runtimes.pop(match_id, None)
            self.last_active.pop(match_id, None)

        return {"status": "removed", "match_id": match_id}

    # =====================================================
    # CLEANUP
    # =====================================================
    def cleanup(self):

        now = time.time()
        to_remove = []

        with self._lock:

            for match_id, last_time in self.last_active.items():
                if now - last_time > self.match_ttl:
                    to_remove.append(match_id)

            for match_id in to_remove:
                self.runtimes.pop(match_id, None)
                self.last_active.pop(match_id, None)

    # =====================================================
    # GC LOOP
    # =====================================================
    def _gc_loop(self):

        while not self._stop_gc:
            time.sleep(60)
            self.cleanup()

    def _start_gc_thread(self):

        t = threading.Thread(target=self._gc_loop, daemon=True)
        t.start()

    # =====================================================
    # SHUTDOWN SAFE
    # =====================================================
    def shutdown(self):
        self._stop_gc = True
