class ReplayBuffer:
    """
    Stores past matches for reinforcement learning
    """

    def __init__(self, max_size=500):

        self.buffer = []
        self.max_size = max_size

    def add(self, sample):

        self.buffer.append(sample)

        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def sample(self, batch_size=32):

        return self.buffer[-batch_size:]
