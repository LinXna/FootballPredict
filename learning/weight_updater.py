class WeightUpdater:

    def __init__(self):

        self.learning_rate = 0.02

    def batch_update(self, matches):

        if not matches:
            return

        for match in matches:

            prediction = match["prediction"]
            result = match["result"]

            self._update_single(prediction, result)

    def _update_single(self, prediction, result):

        # TODO:
        # 后续这里接真正梯度更新
        pass
