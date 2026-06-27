import importlib
import os


class RepairEngine:

    def __init__(self):
        self.created = []

    def fix_missing_import(self, module_name: str):

        try:
            importlib.import_module(module_name)
            return True

        except Exception:

            print(f"[REPAIR] missing -> {module_name}")

            self._create_stub(module_name)
            return False

    def _create_stub(self, module_name: str):

        path = module_name.replace(".", "/") + ".py"

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(path):

            with open(path, "w", encoding="utf-8") as f:

                f.write(f"""
# AUTO-GENERATED STUB

class AutoStub:
    def __init__(self):
        pass

def stub():
    return "stub:{module_name}"
""")

            self.created.append(module_name)

            print(f"[REPAIR] created -> {module_name}")
