from features.form import FormFeature
from features.h2h import H2HFeature


class FeatureBuilder:

    def __init__(self):

        # =========================
        # V1-FREEZE: 子特征模块
        # =========================
        self.form = FormFeature(window=5)
        self.h2h = H2HFeature()

    def train_update(self, match):

        # =========================
        # V1-FREEZE: 防御更新
        # =========================
        if not match:
            return

        self.form.update(match)
        self.h2h.update(match)

    def build(self, home, away):

        # =========================
        # V1-FREEZE: form特征
        # =========================
        home_form = self.form.get_form(home) or 1.0
        away_form = self.form.get_form(away) or 1.0

        # =========================
        # V1-FREEZE: 对战特征
        # =========================
        h2h = self.h2h.get_h2h(home, away) or 0.5

        # =========================
        # V1-FREEZE: feature contract输出
        # =========================
        return {
            "home_form": home_form,
            "away_form": away_form,
            "h2h": h2h,
        }
