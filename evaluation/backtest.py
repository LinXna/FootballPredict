class BacktestEngine:
    def __init__(self, pipeline, evaluator):
        self.pipeline = pipeline
        self.evaluator = evaluator

    def run(self, matches):
        for m in matches:
            pred = self.pipeline.predict(m["home"], m["away"])
            self.evaluator.evaluate_match(pred, m["result"])

        return self.evaluator.summary()
