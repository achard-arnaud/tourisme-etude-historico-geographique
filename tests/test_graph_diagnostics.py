import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from graph_link_audit import graph_diagnostics


class GraphDiagnosticsTests(unittest.TestCase):
    def test_reports_orphan_claims_without_mutating_graph(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            claims = project / "01_arcs" / "A01" / "claims"
            graph = project / "04_graph"
            claims.mkdir(parents=True)
            graph.mkdir()
            (claims / "claims.json").write_text(
                json.dumps([{"id": "C1", "arc": "A01"}, {"id": "C2", "arc": "A01"}]), encoding="utf-8"
            )
            (graph / "edges.jsonl").write_text(
                json.dumps({"from": "C1", "relation": "CAUSES", "to": "C1"}) + "\n", encoding="utf-8"
            )
            report = graph_diagnostics(project)
            self.assertEqual(["C2"], report["orphan_claims"])
            self.assertEqual(1, report["arcs"][0]["linked_claims"])


if __name__ == "__main__":
    unittest.main()
