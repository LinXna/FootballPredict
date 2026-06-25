from learning.result_buffer import ResultBuffer


class FeedbackLoop:
    """
    V2.0 AI Adaptive Feedback System

    Upgrade Goals:
    ✔ 防重复学习（duplicate guard）
    ✔ 稳定 batch trigger
    ✔ context-aware learning
    ✔ 兼容 LiveManager
    ✔ 避免噪声训练
    """

    def __init__(self, updater, max_buffer_size=50):

        # =========================
        # Core dependency
        # =========================
        self.updater = updater

        # =========================
        # Buffer
        # =========================
        self.buffer = ResultBuffer()
        self.max_buffer_size = max_buffer_size

        # =========================
        # Anti-duplication cache
        # =========================
        self._seen = set()

    # =========================================================
    # Public API
    # =========================================================

    def record(self, prediction, result, context=None):

        context = context or {}

        match_id = context.get("match_id")

        # =========================
        # 1️⃣ 防重复学习（关键）
        # =========================
        if match_id in self._seen:
            return 0

        self._seen.add(match_id)

        # =========================
        # 2️⃣ 构造样本
        # =========================
        sample = {"prediction": prediction, "result": result, "context": context}

        self.buffer.add(sample)

        # =========================
        # 3️⃣ Batch trigger
        # =========================
        if self.buffer.ready() or self._force_flush():

            samples = self.buffer.samples()

            self.updater.batch_update(samples)

            self.buffer.clear()

            return len(samples)

        return 0

    # =========================================================
    # Internal logic
    # =========================================================

    def _force_flush(self):

        return len(self.buffer.samples()) >= self.max_buffer_size

    # =========================================================
    # Reset mechanism (for live restart safety)
    # =========================================================

    def reset(self):

        self.buffer.clear()
        self._seen.clear()

    def __repr__(self):

        return (
            f"FeedbackLoop("
            f"buffer_size={len(self.buffer.samples())}, "
            f"seen={len(self._seen)})"
        )
