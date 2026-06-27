from tools.import_graph import ImportGraph


def generate_report():
    g = ImportGraph()
    g.scan()

    cycles = g.detect_cycles()
    g.export()

    report = {"cycle_count": len(cycles), "cycles": cycles, "modules": len(g.graph)}

    print("[REPORT]", report)
    return report
