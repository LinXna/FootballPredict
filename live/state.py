"""
live/state.py

LIVE SYSTEM V1.5

比赛状态对象（MatchState）

职责：
    1. 保存比赛当前状态
    2. 不负责任何预测
    3. 不负责任何计算
"""

from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class MatchState:
    """
    保存一场比赛当前状态。
    """

    # 基本信息
    home: str
    away: str

    # 比赛状态
    minute: int = 0
    status: str = "NS"  # NS / 1H / HT / 2H / ET / FT

    # 当前比分
    home_score: int = 0
    away_score: int = 0

    # 已发生事件（由 processor.py 维护）
    events: List[Any] = field(default_factory=list)

    @property
    def score(self) -> str:
        """返回当前比分字符串，例如：1-0"""
        return f"{self.home_score}-{self.away_score}"

    def is_finished(self) -> bool:
        """比赛是否结束"""
        return self.status == "FT"

    def reset(self) -> None:
        """重置比赛状态（Replay 测试使用）"""
        self.minute = 0
        self.status = "NS"
        self.home_score = 0
        self.away_score = 0
        self.events.clear()

    def __str__(self) -> str:
        return (
            f"[{self.status}] "
            f"{self.home} "
            f"{self.home_score}-{self.away_score} "
            f"{self.away} "
            f"({self.minute}')"
        )

    def to_dict(self):
        return self.__dict__
