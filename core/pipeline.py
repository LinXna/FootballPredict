from models.elo_model import EloModel
from models.poisson_model import PoissonModel
from features.builder import FeatureBuilder
from ensemble.fusion import LearnedFusion
from data.odds_calibrator import odds_to_prob
from ensemble.market_fusion import MarketFusion


class Pipeline:
    def __init__(self):

        # 市场融合模型（最终层）
        self.market_fusion = MarketFusion(alpha=0.7)

        # 基础模型
        self.elo = EloModel()
        self.poisson = PoissonModel()

        # 特征（V2启用，当前仅训练）
        self.features = FeatureBuilder()

        # 融合模型
        self.fusion = LearnedFusion()

    def train(self, matches):

        for m in matches:

            self.elo.update(m["home"], m["away"], m["result"])
            self.features.train_update(m)

        self.poisson.train(matches)

    # =========================
    # 🎯 最终预测（推荐使用）
    # =========================
    def predict(self, home, away, odds=None):

        # 【V1-FREEZE】统一融合入口（唯一模型路径）
        base = self.predict_fusion(home, away)

        # 【V1-FREEZE】旧路径已废弃（不可恢复）
        # elo_pred = self.elo.predict(home, away)
        # poi_pred = self.poisson.predict_1x2(home, away)
        # model_raw = self.fusion.fuse(elo_pred, poi_pred)

        # 市场融合层
        if odds is not None:
            market_prob = odds_to_prob(odds)
            return self.market_fusion.fuse(base, market_prob)

        return base

    # =========================
    # 🔬 纯Elo
    # =========================
    def predict_raw(self, home, away):
        """core/pipeline.py | V1-FREEZE | Elo单模型输出（不可作为融合使用）"""
        return self.elo.predict(home, away)

    # =========================
    # 🔬 Poisson
    # =========================
    def predict_poisson(self, home, away):
        """core/pipeline.py | V1-FREEZE | Poisson单模型输出（不可直接用于决策）"""
        return self.poisson.predict_1x2(home, away)

    # =========================
    # 🔬 Fusion（标准入口）
    # =========================
    def predict_fusion(self, home, away):
        """
        core/pipeline.py | V1-FREEZE
        标准模型融合入口（Elo + Poisson）
        全系统唯一 Fusion 标准接口
        """

        elo = self.elo.predict(home, away)
        poi = self.poisson.predict_1x2(home, away)

        return self.fusion.fuse(elo, poi)
