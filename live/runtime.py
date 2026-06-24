from live.state import MatchState
from live.queue import EventQueue
from live.processor import EventProcessor
from live.predictor import LivePredictor
from live.events import MatchEvent


class MatchRuntime:
    """
    V1.7 Final：单场比赛运行容器
    """

    def __init__(self, match_id: str, predictor: LivePredictor):
        self.match_id = match_id

        # 唯一状态
        self.state: MatchState | None = None

        # 事件队列
        self.queue = EventQueue()

        # 事件处理器
        self.processor = EventProcessor()

        # 预测器（外部注入）
        self.predictor = predictor
        self._learning_done = False

    # =========================
    # 初始化比赛
    # =========================
    def start(self, home: str, away: str):
        self.state = MatchState(home, away)

    # =========================
    # 接收事件
    # =========================
    def push_event(self, event: MatchEvent):
        self.queue.push(event)

    # =========================
    # 处理事件流
    # =========================
    def _process_events(self):
        if self.state is None:
            raise ValueError("Match not started")

        while not self.queue.is_empty():
            event = self.queue.pop()
            if event is None:
                break

            self.state = self.processor.process(self.state, event)

    # =========================
    # 实时预测
    # =========================
    def predict(self):
        if self.state is None:
            raise ValueError("Match not started")

        return self.predictor.predict(self.state)

    # =========================
    # 单步执行（API/WS统一入口）
    # =========================
    def step(self, event):
        """
        V1.9 Runtime Step
        """

        # =========================
        # 1️⃣ 写入事件
        # =========================
        self.push_event(event)

        # =========================
        # 2️⃣ 更新状态
        # =========================
        self._process_events()

        # =========================
        # 3️⃣ 预测（核心）
        # =========================
        prob = self.predict()

        # =========================
        # 4️⃣ V1.9关键：缓存预测结果（用于Self-Learning）
        # =========================
        self.last_prediction = {
            "H": prob["H"],
            "D": prob["D"],
            "A": prob["A"],
            "minute": self.state.minute,
            "home_score": self.state.home_score,
            "away_score": self.state.away_score,
        }

        # =========================
        # 5️⃣ Snapshot记录（增强版）
        # =========================
        if hasattr(self, "snapshot_store"):
            self.snapshot_store.record(
                self.match_id, self.state.minute, event, self.state, prob
            )

        # =========================
        # V1.9 Self-Learning Hook（比赛结束触发点）
        # =========================
        if hasattr(self.state, "finished") and self.state.finished:

            # ✔ 防重复触发
            if not getattr(self, "_learning_done", False):

                self._learning_done = True

                if hasattr(self, "manager"):
                    self.manager.on_match_finished(
                        self.match_id, self.state.result  # 0=H,1=D,2=A
                    )

        # =========================
        # 6️⃣ 输出（保持不变）
        # =========================
        return {
            "state": {
                "home_score": self.state.home_score,
                "away_score": self.state.away_score,
                "minute": self.state.minute,
            },
            "prob": prob,
        }

    # 增加 snapshot 注入
    def attach_snapshot_store(self, snapshot_store):
        self.snapshot_store = snapshot_store
