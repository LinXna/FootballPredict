import subprocess
from datetime import datetime


def freeze_requirements(output="requirements.lock"):
    """
    锁定当前Python环境依赖
    """
    result = subprocess.check_output(["pip", "freeze"]).decode()

    with open(output, "w", encoding="utf-8") as f:
        f.write(f"# Frozen on {datetime.utcnow()}\n")
        f.write(result)

    print("[LOCK] requirements locked →", output)
