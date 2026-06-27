from tools.preflight import preflight
from tools.repair_engine import RepairEngine
from tools.self_heal import SelfHeal

from learning.engine import LearningEngine
from learning.reward_engine import RewardEngine
from learning.weight_updater import WeightUpdater


def bootstrap():

    print("\n====================")
    print("   V3.5 ENGINE")
    print("====================\n")

    # 1️⃣ 修复引擎（必须最先）
    repair = RepairEngine()

    # 2️⃣ 启动检查 + 自动修复
    ok = preflight(repair)

    # 3️⃣ 自愈系统
    heal = SelfHeal()

    # 4️⃣ learning 引擎接入（正式）
    learning = LearningEngine(
        weight_updater=WeightUpdater(), reward_engine=RewardEngine()
    )

    print("\n[LEARNING ENGINE READY]")

    if not ok:
        print("[WARN] system repaired during bootstrap")

    print("[BOOT SUCCESS]\n")

    return {"repair": repair, "heal": heal, "learning": learning}


def main():

    context = bootstrap()

    print("[SYSTEM RUNNING]")


if __name__ == "__main__":
    main()
