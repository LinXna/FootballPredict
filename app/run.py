from core.pipeline import Pipeline
from data.real_matches import load_real_matches


def main():

    # =========================
    # V1-FREEZE: 数据加载
    # =========================
    matches = load_real_matches()

    # =========================
    # V1-FREEZE: pipeline初始化
    # =========================
    pipe = Pipeline()
    pipe.train(matches)

    mode = "benchmark"  # backtest / benchmark / betting

    # =========================
    # BACKTEST MODE
    # =========================
    if mode == "backtest":

        from evaluation.backtest import Backtester

        bt = Backtester(pipe)
        result, _ = bt.run(matches)

        print("===== 回测结果 =====")
        print(result)

    # =========================
    # BENCHMARK MODE
    # =========================
    elif mode == "benchmark":

        from evaluation.benchmark import ModelBenchmark

        bm = ModelBenchmark(pipe)

        print("===== 模型对比 =====")
        print(bm.run(matches))

    # =========================
    # BETTING MODE
    # =========================
    elif mode == "betting":

        from evaluation.betting import BettingEngine
        from evaluation.value_engine import ValueBetEngine

        print("[RUN] Betting mode started")

        try:
            be = BettingEngine(bankroll=1000)
            ve = ValueBetEngine()
        except Exception as e:
            print(f"[ERROR] Engine init failed: {e}")
            return

        print("===== 投注结果 =====")

        for m in matches:

            try:
                odds = m.get("odds", None)

                pred = pipe.predict(m["home"], m["away"], odds=odds)

                ev = None
                try:
                    ev = ve.find_value_bets(pred, odds)
                except Exception:
                    ev = None

                # =========================
                # V1-FREEZE: EV仅分析
                # =========================
                if ev:
                    print(ev)

            except Exception as e:
                print(f"[WARN] match failed: {m.get('home')} vs {m.get('away')} -> {e}")
                continue

        try:
            print("ROI:", be.run(matches, pipe))
        except Exception as e:
            print(f"[ERROR] ROI calculation failed: {e}")


if __name__ == "__main__":
    main()
