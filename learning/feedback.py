from learning.result_buffer import ResultBuffer


class FeedbackLoop:

    def __init__(self, updater):

        self.updater = updater
        self.buffer = ResultBuffer()

    def record(self, prediction, result, context=None):

        sample = {"prediction": prediction, "result": result, "context": context or {}}

        self.buffer.add(sample)

        if self.buffer.ready():

            samples = self.buffer.samples()

            self.updater.batch_update(samples)

            self.buffer.clear()

            return len(samples)

        return 0
