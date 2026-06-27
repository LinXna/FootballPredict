import os
import ast
from collections import defaultdict


class ImportGraph:

    def __init__(self, root="."):

        self.root = root
        self.graph = defaultdict(set)

        # ❗ 强制白名单（关键修复）
        self.allow_dirs = {
            "core",
            "models",
            "ensemble",
            "features",
            "live",
            "learning",
            "evolution",
            "app",
            "data",
        }

        self.block_dirs = {
            ".venv",
            "venv",
            "__pycache__",
            "site-packages",
            ".git",
            "reports",
            "node_modules",
        }

    def scan(self):

        for path, dirs, files in os.walk(self.root):

            # ❗ 剪枝：跳过黑名单目录
            dirs[:] = [d for d in dirs if d not in self.block_dirs]

            for f in files:
                if not f.endswith(".py"):
                    continue

                full = os.path.join(path, f)

                # ❗ 只允许业务目录
                if not self._is_allowed(full):
                    continue

                self._parse(full)

    def _is_allowed(self, path: str) -> bool:

        path_norm = path.replace("\\", "/")

        return any(
            f"/{d}/" in path_norm or path_norm.endswith(f"/{d}")
            for d in self.allow_dirs
        )

    def _parse(self, file_path):

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read(), filename=file_path)

            module = file_path.replace("\\", ".").replace("/", ".").replace(".py", "")

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):
                    for n in node.names:
                        self.graph[module].add(n.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.graph[module].add(node.module)

        except Exception as e:
            print("[PARSE ERROR]", file_path, e)

    def detect_cycles(self):

        visited = set()
        stack = set()
        cycles = []

        def dfs(node):

            if node in stack:
                cycles.append(node)
                return

            if node in visited:
                return

            visited.add(node)
            stack.add(node)

            for nei in self.graph.get(node, []):
                dfs(nei)

            stack.remove(node)

        for node in list(self.graph.keys()):
            dfs(node)

        return cycles

    def export(self, path="reports/import_graph.json"):

        import json

        with open(path, "w", encoding="utf-8") as f:
            json.dump({k: list(v) for k, v in self.graph.items()}, f, indent=2)

        print("[GRAPH] exported ->", path)
