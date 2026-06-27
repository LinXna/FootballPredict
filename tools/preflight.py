import importlib

REQUIRED_MODULES = [
    "core.pipeline",
    "models.elo_model",
    "models.poisson_model",
    "ensemble.fusion",
    "live.manager",
    "live.runtime",
    "live.events",
    "live.processor",
    "learning.engine",
]


def preflight(repair_engine=None):

    print("\n[V3.5 PREFLIGHT]\n")

    ok = True

    for m in REQUIRED_MODULES:

        try:
            importlib.import_module(m)
            print("[OK]", m)

        except Exception as e:

            print("[FAIL]", m, "->", e)

            ok = False

            # 自动修复触发
            if repair_engine:
                repair_engine.fix_missing_import(m)

    return ok
