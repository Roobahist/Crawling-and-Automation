"""Offline tests for Meta API request construction and pagination."""

import unittest
from datetime import date

from crawling_automation.social.instagram import GraphAPIError, GraphSettings, InstagramClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, pages):
        self.pages = iter(pages)
        self.calls = []

    def get(self, url, params, timeout):
        self.calls.append((url, params, timeout))
        return FakeResponse(next(self.pages))


class GraphAPITests(unittest.TestCase):
    def setUp(self):
        self.settings = GraphSettings("example-fake-token", "v99.0", 5)

    def test_settings_require_explicit_version_and_token(self):
        with self.assertRaises(ValueError):
            GraphSettings("", "v99.0")
        with self.assertRaises(ValueError):
            GraphSettings("token", "latest")

    def test_pagination_and_optional_fields(self):
        session = FakeSession([
            {"data": [{"id": "a", "caption": "test"}],
             "paging": {"next": "unused", "cursors": {"after": "cursor-2"}}},
            {"data": [{"id": "b", "media_type": "IMAGE"}]},
        ])
        client = InstagramClient(session, self.settings)
        result = client.collect_posts("ig-1")
        self.assertEqual([r["id"] for r in result], ["a", "b"])
        self.assertEqual(session.calls[1][1]["after"], "cursor-2")
        self.assertEqual(session.calls[0][1]["access_token"], "example-fake-token")
        self.assertEqual(session.calls[0][2], 5)

    def test_account_discovery(self):
        client = InstagramClient(FakeSession([
            {"data": [{"id": "page-1"}]},
            {"instagram_business_account": {"id": "ig-123"}},
        ]), self.settings)
        self.assertEqual(client.resolve_business_account(), "ig-123")

    def test_graph_errors_do_not_include_access_token(self):
        client = InstagramClient(FakeSession([{"error": {"message": "private", "code": 190}}]), self.settings)
        with self.assertRaises(GraphAPIError) as caught:
            client.collect_posts("ig-1")
        self.assertNotIn("example-fake-token", str(caught.exception))
        self.assertIn("190", str(caught.exception))

    def test_account_insights_with_utc_dates(self):
        session = FakeSession([{"data": [
            {"name": "reach", "title": "Reach",
             "values": [{"value": 8, "end_time": "2026-10-02T00:00:00+0000"}]},
        ]}])
        client = InstagramClient(session, self.settings)
        rows = client.collect_account_insights("ig-1", ["reach"], date(2026, 10, 1), date(2026, 10, 2))
        self.assertEqual(rows[0]["value"], 8)
        self.assertEqual(session.calls[0][1]["period"], "day")
        self.assertLess(session.calls[0][1]["since"], session.calls[0][1]["until"])
        with self.assertRaises(ValueError):
            client.collect_account_insights("ig-1", ["reach"], date(2026, 10, 2), date(2026, 10, 1))

    def test_media_insights_must_be_requested_explicitly(self):
        session = FakeSession([{"data": [{"name": "reach", "values": [{"value": 7}]}]}])
        client = InstagramClient(session, self.settings)
        self.assertEqual(client.collect_media_insights("post-1", []), {})
        self.assertEqual(client.collect_media_insights("post-1", ["reach"])["reach"], 7)
        self.assertEqual(len(session.calls), 1)


if __name__ == "__main__":
    unittest.main()
