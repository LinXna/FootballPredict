"""
live/pipeline.py

LIVE SYSTEM V1.5

总控管道（Orchestrator）

职责：
    - 接收事件流
    - 更新状态
    - 输出实时概率
"""

from live.state import MatchState
from live.queue import EventQueue
from live.processor import EventProcessor
from live.predictor import LivePredictor
from live.events import MatchEvent
from live.state_store import StateStore


class LivePipeline:
    """
    LIVE系统总入口
    """

    def __init__(self, core_pipeline):
        # V1静态模型
        self.predictor = LivePredictor(core_pipeline)

        # 事件处理
        self.queue = EventQueue()
        self.processor = EventProcessor()

        # 当前比赛状态
        self.store = StateStore()

    # =========================
    # 初始化比赛
    # =========================
    def start_match(self, home: str, away: str):
        self.state = MatchState(home, away)

    # =========================
    # 接收事件
    # =========================
    def push_event(self, event: MatchEvent):
        self.queue.push(event)

    # =========================
    # 处理队列
    # =========================
    def process(self):
        """
        清空队列 → 更新 state
        """

        if self.state is None:
            raise ValueError("Match not started")

        while not self.queue.is_empty():
            event = self.queue.pop()
            self.state = self.processor.process(self.state, event)

    # =========================
    # 实时预测
    # =========================
    def predict(self):
        """
        输出当前比赛概率
        """

        if self.state is None:
            raise ValueError("Match not started")

        return self.predictor.predict(self.state)

    # =========================
    # 一步执行（API模式）step 改为多 match
    # =========================
    def step(self, match_id, event):
        self.queue.push(match_id, event)

        state = self.store.get(match_id)

        while not self.queue.is_empty(match_id):
            e = self.queue.pop(match_id)
            state = self.processor.process(state, e)

        self.store.states[match_id] = state

        return self.predictor.predict(state)

    # 新增 match 管理
    def start_match(self, match_id, home, away):
        self.store.create(match_id, home, away)
