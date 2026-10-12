"""Check CLI wiring using an injected offline HTTP session."""

import csv
import tempfile
import unittest
from pathlib import Path

from crawling_automation.cli import run


class FakeResponse:
    text = """<div class="sefr-price-list"><section>
    <div class="price-list-brand-name"><a>قیمت خودرو پژو</a></div>
    <ul><li><span>206</span><small>1399</small>
    <small class="sefr-price">12,345,000 تومان</small></li></ul>
    </section></div>"""

    def raise_for_status(self):
        return None


class FakeSession:
    calls = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def get(self, url, timeout):
        self.calls.append((url, timeout))
        return FakeResponse()


class CLITests(unittest.TestCase):
    def test_bama_command_writes_parsed_rows_without_credential_or_network(self):
        with tempfile.TemporaryDirectory() as location:
            path = Path(location) / "nested" / "prices.csv"
            exit_code = run(
                ["bama", "--url", "https://example.invalid/prices",
                 "--output", str(path), "--timeout", "4"],
                session_factory=FakeSession,
                environment={},
            )
            self.assertEqual(exit_code, 0)
            with path.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.reader(stream, delimiter="$"))
            self.assertEqual(rows[1][7], "12,345,000 تومان")
            self.assertEqual(FakeSession.calls[-1], ("https://example.invalid/prices", 4))

    def test_instagram_requires_configuration_before_network_request(self):
        with tempfile.TemporaryDirectory() as location:
            with self.assertRaises(ValueError):
                run(["instagram-posts", "--account-id", "sample",
                     "--output", str(Path(location) / "posts.csv")],
                    session_factory=FakeSession, environment={})


if __name__ == "__main__":
    unittest.main()
