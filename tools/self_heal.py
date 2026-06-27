import importlib


class SelfHeal:

    def safe_import(self, module_name, fallback=None):

        try:
            return importlib.import_module(module_name)

        except Exception:

            print(f"[SELF-HEAL] fallback -> {module_name}")

            if fallback:
                return fallback()

            return None
