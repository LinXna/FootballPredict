from typing import Dict
import threading
import time

from live.runtime import MatchRuntime
from live.predictor import LivePredictor
from core.pipeline import Pipeline
from live.events import MatchEvent
from live.snapshot import SnapshotStore
from evolution.self_learning.feedback_loop import FeedbackLoop
from evolution.self_learning.weight_updater import WeightUpdater


class LiveManager:
    """
    V1.7 Multi-Match Manager
    """

    def __init__(self, core_pipeline: Pipeline):

        # =========================
        # 1️⃣ Core dependency
        # =========================
        self.core_pipeline = core_pipeline

        # =========================
        # 2️⃣ State containers（必须最先）
        # =========================
        self.runtimes = {}
        self.last_active = {}

        # =========================
        # 3️⃣ Locks（并发安全）
        # =========================
        self._lock = threading.Lock()

        # =========================
        # 4️⃣ Snapshot system
        # =========================
        self.snapshot_store = SnapshotStore()

        # =========================
        # 5️⃣ Predictor（建议：可选弱绑定）
        # =========================
        self.predictor = LivePredictor(core_pipeline)

        # =========================
        # 6️⃣ V1.9 Self-Learning
        # =========================
        self.weight_updater = WeightUpdater()
        self.self_learning_loop = FeedbackLoop(self.weight_updater)
        self.self_learning_loop.record(
            prediction=pred,
            result=actual_result,
            context={"match_id": match_id, "minute": runtime.state.minute},
        )

        # =========================
        # 7️⃣ TTL config
        # =========================
        self.match_ttl = 60 * 30  # 30min

        # =========================
        # 8️⃣ GC thread（必须最后启动）
        # =========================
        self._start_gc_thread()

    # =========================
    # 创建比赛
    # =========================
    def create_match(self, match_id: str, home: str, away: str):

        with self._lock:
            if match_id in self.runtimes:
                raise ValueError("Match exists")
            runtime = MatchRuntime(match_id=match_id, predictor=self.predictor)

            # ✔ 注入 snapshot_store（关键点）
            runtime.attach_snapshot_store(self.snapshot_store)

            runtime.start(home, away)

            self.last_active[match_id] = time.time()
            self.runtimes[match_id] = runtime

        return {"status": "created", "match_id": match_id}

    # =========================
    # 获取 runtime
    # =========================
    def get_runtime(self, match_id: str) -> MatchRuntime:
        if match_id not in self.runtimes:
            raise ValueError(f"Match not found: {match_id}")

        return self.runtimes[match_id]

    # =========================
    # 分发事件
    # =========================
    def handle_event(self, match_id: str, event: MatchEvent):
        with self._lock:
            runtime = self.runtimes[match_id]

        # runtime step 不加锁（避免阻塞）
        return runtime.step(event)

    # =========================
    # 获取状态
    # =========================
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

    # =========================
    # 删除比赛
    # =========================
    def remove_match(self, match_id: str):
        if match_id in self.runtimes:
            del self.runtimes[match_id]

        return {"status": "removed", "match_id": match_id}

    def cleanup(self):
        import time

        now = time.time()
        to_remove = []

        for match_id, last_time in self.last_active.items():
            if now - last_time > self.match_ttl:
                to_remove.append(match_id)

        for match_id in to_remove:
            print(f"[GC] removing match: {match_id}")

            self.runtimes.pop(match_id, None)
            self.last_active.pop(match_id, None)

    def _gc_loop(self):
        while True:
            time.sleep(60)
            self.cleanup()

    def _start_gc_thread(self):
        import threading

        t = threading.Thread(target=self._gc_loop, daemon=True)
        t.start()

    def on_match_finished(self, match_id: str, actual_result: int):
        """
        V1.9 Batch Learning Entry Point
        """

        runtime = self.runtimes.get(match_id)

        if runtime is None:
            return

        # =========================
        # 1️⃣ 获取预测
        # =========================
        pred = getattr(runtime, "last_prediction", None)

        if pred is None:
            print(f"[V1.9] No prediction cached for {match_id}")
            return

        # =========================
        # 2️⃣ 写入学习缓冲区
        # =========================
        batch_size = self.self_learning_loop.record(
            prediction=pred,
            result=actual_result,
            context={"match_id": match_id, "minute": runtime.state.minute},
        )

        print(f"[V1.9 LEARNING] match={match_id} buffered, batch_size={batch_size}")

        # =========================
        # 3️⃣ 可选释放 runtime
        # =========================
        # self.runtimes.pop(match_id, None)
