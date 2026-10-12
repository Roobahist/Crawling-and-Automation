"""Guard against accidental recommit of the notebook's known cookie format."""

import json
import unittest
from pathlib import Path


class ArchivedNotebookSecurityTests(unittest.TestCase):
    def test_notebook_is_parseable_and_historical_authentication_is_redacted(self):
        notebook = Path(__file__).resolve().parents[1] / "legacy" / "notebooks" / "main.ipynb"
        raw = notebook.read_text(encoding="utf-8")
        self.assertNotIn("gAAAAAB", raw, "Archived authentication cookie was reintroduced")
        document = json.loads(raw)
        self.assertEqual(len(document["cells"]), 90)
        self.assertEqual(sum(len(cell.get("outputs", [])) for cell in document["cells"]), 37)


if __name__ == "__main__":
    unittest.main()
