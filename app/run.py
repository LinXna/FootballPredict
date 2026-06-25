import os

from core.pipeline import Pipeline
from data.loader import load_real_matches


def main():
    matches = load_real_matches()

    if not matches:
        raise ValueError("[FATAL] No match data loaded")

    pipe = Pipeline()
    pipe.train(matches)

    mode = os.getenv("MODE", "benchmark")

    # -----------------------------
    # BACKTEST MODE
    # -----------------------------
    if mode == "backtest":

        from evaluation.backtest import Backtester

        bt = Backtester(pipe)

        try:
            result, _ = bt.run(matches)
        except Exception as e:
            raise RuntimeError(f"[BACKTEST ERROR] {e}")

        print("===== 回测结果 =====")
        print(result)

    # -----------------------------
    # BENCHMARK MODE
    # -----------------------------
    elif mode == "benchmark":

        from evaluation.benchmark import ModelBenchmark

        bm = ModelBenchmark(pipe)

        try:
            result = bm.run(matches)
        except Exception as e:
            raise RuntimeError(f"[BENCHMARK ERROR] {e}")

        print("===== 模型对比 =====")
        print(result)

    # -----------------------------
    # BETTING MODE
    # -----------------------------
    elif mode == "betting":

        from evaluation.betting import BettingEngine
        from evaluation.value_engine import ValueBetEngine

        print("[RUN] Betting mode started")

        try:
            be = BettingEngine(bankroll=1000)
            ve = ValueBetEngine()
        except Exception as e:
            raise RuntimeError(f"[INIT FAILED] {e}")

        print("===== 投注结果 =====")

        for m in matches:

            try:
                # -------------------------
                # input validation
                # -------------------------
                home = m.get("home")
                away = m.get("away")

                if not home or not away:
                    raise ValueError(f"Invalid match data: {m}")

                odds = m.get("odds", None)

                # -------------------------
                # prediction
                # -------------------------
                pred = pipe.predict(home, away, odds=odds)

                if pred is None:
                    raise ValueError(f"Prediction returned None: {home} vs {away}")

                # -------------------------
                # value betting
                # -------------------------
                try:
                    ev = ve.find_value_bets(pred, odds)
                except Exception as e:
                    raise RuntimeError(f"[EV ENGINE ERROR] {e}")

                if ev:
                    print(ev)

            except Exception as e:
                # fail fast: do not silently continue
                raise RuntimeError(
                    f"[MATCH FAILURE] {m.get('home')} vs {m.get('away')} | {e}"
                )

        # -------------------------
        # ROI summary
        # -------------------------
        try:
            roi = be.run(matches, pipe)

            if roi is None:
                raise ValueError("ROI returned None")

            print("===== ROI =====")
            print(roi)

        except Exception as e:
            raise RuntimeError(f"[ROI ERROR] {e}")

    else:
        raise ValueError(f"[FATAL] Unknown mode: {mode}")


if __name__ == "__main__":
    main()
