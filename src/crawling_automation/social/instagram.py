"""Configurable, read-only Meta Graph API client.

Available metrics and permissions vary by API version and account type.
Callers choose insight metrics rather than relying on the 2020 sample list.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from typing import Mapping


class GraphAPIError(RuntimeError):
    """An API response could not be used by the caller."""


@dataclass(frozen=True)
class GraphSettings:
    access_token: str
    api_version: str
    timeout_seconds: float = 20

    def __post_init__(self) -> None:
        if not self.access_token.strip():
            raise ValueError("META_ACCESS_TOKEN is required")
        if not re.fullmatch(r"v\d+\.\d+", self.api_version):
            raise ValueError("META_GRAPH_API_VERSION must look like vXX.X")
        if not 0 < self.timeout_seconds <= 300:
            raise ValueError("HTTP timeout must be between 0 and 300 seconds")

    @classmethod
    def from_environment(cls, environment: Mapping[str, str]) -> GraphSettings:
        """Load secrets only at the application boundary."""
        return cls(
            access_token=environment.get("META_ACCESS_TOKEN", ""),
            api_version=environment.get("META_GRAPH_API_VERSION", ""),
            timeout_seconds=float(environment.get("HTTP_TIMEOUT_SECONDS", "20")),
        )


class InstagramClient:
    """Thin Graph API adapter. The injected session allows offline tests."""

    def __init__(self, session, settings: GraphSettings) -> None:
        self._session = session
        self._settings = settings
        self._base_url = f"https://graph.facebook.com/{settings.api_version}/"

    def _get(self, endpoint: str, parameters: Mapping[str, object] | None = None) -> dict:
        if not endpoint or endpoint.startswith(("/", "http")) or ".." in endpoint:
            raise ValueError("Expected a relative Graph API endpoint")
        params = dict(parameters or {})
        params["access_token"] = self._settings.access_token
        response = self._session.get(
            self._base_url + endpoint,
            params=params,
            timeout=self._settings.timeout_seconds,
        )
        response.raise_for_status()
        try:
            payload = response.json()
        except ValueError as exc:
            raise GraphAPIError("Graph API returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise GraphAPIError("Graph API returned an unexpected response")
        if "error" in payload:
            error = payload["error"]
            code = error.get("code", "unknown") if isinstance(error, dict) else "unknown"
            raise GraphAPIError(f"Graph API rejected the request (code {code})")
        return payload

    def _pages(self, endpoint: str, parameters: dict, max_pages: int):
        if max_pages <= 0:
            raise ValueError("max_pages must be positive")
        cursor = None
        seen = set()
        for _ in range(max_pages):
            page_params = dict(parameters)
            if cursor is not None:
                page_params["after"] = cursor
            payload = self._get(endpoint, page_params)
            records = payload.get("data")
            if not isinstance(records, list):
                raise GraphAPIError("Graph API page is missing its data list")
            yield records
            paging = payload.get("paging") or {}
            next_cursor = (paging.get("cursors") or {}).get("after")
            if not paging.get("next") or not next_cursor:
                break
            if next_cursor in seen:
                raise GraphAPIError("Graph API pagination cursor was repeated")
            seen.add(next_cursor)
            cursor = next_cursor

    def resolve_business_account(self, max_pages: int = 10) -> str:
        """Find the first Instagram business account linked to an accessible page."""
        for pages in self._pages("me/accounts", {"fields": "id", "limit": 100}, max_pages):
            for page in pages:
                page_id = str(page["id"])
                info = self._get(page_id, {"fields": "instagram_business_account"})
                account = info.get("instagram_business_account") or {}
                if account.get("id"):
                    return str(account["id"])
        raise GraphAPIError("No linked Instagram business account is accessible")

    def collect_posts(self, account_id: str, max_pages: int = 10) -> list[dict]:
        """Fetch post metadata; missing optional fields remain absent."""
        fields = "id,caption,like_count,comments_count,media_type,media_url"
        output = []
        for posts in self._pages(f"{account_id}/media", {"fields": fields}, max_pages):
            for post in posts:
                if "id" not in post:
                    raise GraphAPIError("Graph API media record has no id")
                output.append(dict(post))
        return output

    def collect_media_insights(self, media_id: str, metrics: list[str]) -> dict:
        """Read caller-selected metrics for a single media item."""
        if not metrics:
            return {}
        payload = self._get(f"{media_id}/insights", {"metric": ",".join(metrics)})
        output = {}
        for metric in payload.get("data", []):
            values = metric.get("values") or []
            output[metric["name"]] = values[0].get("value") if values else None
        return output

    def collect_account_insights(
        self, account_id: str, metrics: list[str], since: date, until: date,
        period: str = "day",
    ) -> list[dict]:
        """Fetch time-bounded insight observations for caller-selected metrics."""
        if not metrics or since >= until:
            raise ValueError("Supply metrics and an end date later than the start date")
        start = int(datetime.combine(since, time.min, tzinfo=timezone.utc).timestamp())
        end = int(datetime.combine(until, time.min, tzinfo=timezone.utc).timestamp())
        payload = self._get(f"{account_id}/insights", {
            "metric": ",".join(metrics), "period": period, "since": start, "until": end,
        })
        observations = []
        for metric in payload.get("data", []):
            for point in metric.get("values", []):
                observations.append({
                    "metric": metric.get("name", ""),
                    "title": metric.get("title", ""),
                    "value": point.get("value"),
                    "end_time": point.get("end_time", ""),
                })
        return observations
