from live.state import MatchState
from live.queue import EventQueue
from live.processor import EventProcessor
from live.predictor import LivePredictor
from live.events import MatchEvent


class MatchRuntime:
    """
    V1.7 最小执行单元（Single Match Engine）
    """

    def __init__(self, core_pipeline):
        # 静态模型（共享）
        self.predictor = LivePredictor(core_pipeline)

        # 动态状态（每场独立）
        self.state: MatchState | None = None
        self.queue = EventQueue()
        self.processor = EventProcessor()

    # =========================
    # 初始化比赛
    # =========================
    def start(self, home: str, away: str):
        self.state = MatchState(home, away)

    # =========================
    # 接收事件
    # =========================
    def push(self, event: MatchEvent):
        self.queue.push(event)

    # =========================
    # 执行更新 + 预测
    # =========================
    def step(self, event: MatchEvent):
        """
        外部唯一入口：
        event → state update → prediction
        """

        if self.state is None:
            raise ValueError("Match not started")

        # 1. 入队
        self.push(event)

        # 2. 处理队列（保证顺序）
        while not self.queue.is_empty():
            e = self.queue.pop()
            if e:
                self.state = self.processor.process(self.state, e)

        # 3. 输出预测
        return self.predictor.predict(self.state)
