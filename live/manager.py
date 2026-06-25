from typing import Dict
import threading
import time

from live.runtime import MatchRuntime
from live.predictor import LivePredictor
from core.pipeline import Pipeline
from live.events import MatchEvent
from live.snapshot import SnapshotStore

from evolution.self_learning.feedback import FeedbackLoop
from learning.weight_updater import WeightUpdater


class LiveManager:
    """
    V2.0 AI Adaptive Live Manager

    Upgrade:
    ✔ Online learning integration
    ✔ Safe learning trigger
    ✔ Runtime isolation
    ✔ TTL GC system
    ✔ Self-learning loop binding
    ✔ No duplicate training
    """

    def __init__(self, core_pipeline: Pipeline):

        # =========================
        # Core dependency
        # =========================
        self.core_pipeline = core_pipeline

        # =========================
        # Runtime state
        # =========================
        self.runtimes: Dict[str, MatchRuntime] = {}
        self.last_active: Dict[str, float] = {}

        # =========================
        # Concurrency lock
        # =========================
        self._lock = threading.Lock()

        # =========================
        # Snapshot system
        # =========================
        self.snapshot_store = SnapshotStore()

        # =========================
        # Predictor
        # =========================
        self.predictor = LivePredictor(core_pipeline)

        # =========================
        # V2.0 Adaptive Learning
        # =========================
        self.weight_updater = WeightUpdater()
        self.feedback_loop = FeedbackLoop(self.weight_updater)

        # =========================
        # TTL config
        # =========================
        self.match_ttl = 60 * 30  # 30 minutes

        # =========================
        # Start GC thread
        # =========================
        self._start_gc_thread()

    # =========================================================
    # Match lifecycle
    # =========================================================

    def create_match(self, match_id: str, home: str, away: str):

        with self._lock:

            if match_id in self.runtimes:
                raise ValueError("Match already exists")

            runtime = MatchRuntime(match_id=match_id, predictor=self.predictor)

            runtime.attach_snapshot_store(self.snapshot_store)
            runtime.start(home, away)

            self.runtimes[match_id] = runtime
            self.last_active[match_id] = time.time()

        return {"status": "created", "match_id": match_id}

    # =========================================================
    # Event handling
    # =========================================================

    def handle_event(self, match_id: str, event: MatchEvent):

        with self._lock:
            runtime = self.runtimes.get(match_id)

        if runtime is None:
            return None

        self.last_active[match_id] = time.time()

        return runtime.step(event)

    # =========================================================
    # State query
    # =========================================================

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

    def get_runtime(self, match_id: str):

        runtime = self.runtimes.get(match_id)

        if runtime is None:
            raise ValueError(f"Match not found: {match_id}")

        return runtime

    # =========================================================
    # Match finished → AI Learning Hook
    # =========================================================

    def on_match_finished(self, match_id: str, actual_result: int):

        runtime = self.runtimes.get(match_id)

        if runtime is None:
            return

        # =========================
        # 1️⃣ 获取缓存预测
        # =========================
        pred = runtime.last_prediction

        if pred is None:
            return

        # =========================
        # 2️⃣ 触发学习（核心）
        # =========================
        reward = self.feedback_loop.record(
            prediction=pred,
            result=actual_result,
            context={"match_id": match_id, "minute": runtime.state.minute},
        )

        # =========================
        # 3️⃣ 更新权重日志
        # =========================
        if reward > 0:
            print(f"[V2.0 LEARN] match={match_id} samples={reward}")

        # =========================
        # 4️⃣ 可选释放 runtime
        # =========================
        # self.runtimes.pop(match_id, None)

    # =========================================================
    # GC system
    # =========================================================

    def cleanup(self):

        now = time.time()
        to_remove = []

        for match_id, last in self.last_active.items():

            if now - last > self.match_ttl:
                to_remove.append(match_id)

        for match_id in to_remove:

            print(f"[GC] removing match {match_id}")

            self.runtimes.pop(match_id, None)
            self.last_active.pop(match_id, None)

    def _gc_loop(self):

        while True:

            time.sleep(60)
            self.cleanup()

    def _start_gc_thread(self):

        t = threading.Thread(target=self._gc_loop, daemon=True)
        t.start()
