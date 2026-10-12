"""Small command-line interface for supported, read-only data collectors."""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import date
from pathlib import Path
from typing import Callable, Mapping, Sequence

import requests

from crawling_automation.automotive.bama import collect_bama_prices, write_prices
from crawling_automation.social.instagram import GraphSettings, InstagramClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crawl-auto", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    bama = sub.add_parser("bama", help="Collect historic-format Bama car price listings")
    bama.add_argument("--url", default="https://bama.ir/price")
    bama.add_argument("--output", type=Path, required=True)
    bama.add_argument("--timeout", type=float, default=20)
    bama.add_argument("--brand-map", type=Path, help="Optional JSON mapping of Persian to English brands")

    for command in ("instagram-posts", "instagram-insights"):
        ig = sub.add_parser(command, help="Collect Instagram account data")
        ig.add_argument("--account-id", help="Automatically discover a linked business account if omitted")
        ig.add_argument("--output", type=Path, required=True)
        if command == "instagram-posts":
            ig.add_argument("--max-pages", type=int, default=10)
        else:
            ig.add_argument("--metrics", required=True, help="Comma-separated metrics accepted by your API version")
            ig.add_argument("--since", type=date.fromisoformat, required=True)
            ig.add_argument("--until", type=date.fromisoformat, required=True)
            ig.add_argument("--period", default="day")
    return parser


def _write_dicts(path: Path, headers: list[str], records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def run(
    argv: Sequence[str] | None = None,
    *,
    session_factory: Callable = requests.Session,
    environment: Mapping[str, str] | None = None,
) -> int:
    """Parse configuration, assemble dependencies, and execute one collector."""
    args = build_parser().parse_args(argv)
    env = os.environ if environment is None else environment
    with session_factory() as session:
        if args.command == "bama":
            if args.timeout <= 0:
                raise ValueError("HTTP timeout must be positive")
            brands = json.loads(args.brand_map.read_text(encoding="utf-8")) if args.brand_map else None
            records = collect_bama_prices(session, args.url, args.timeout, brands=brands)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("w", encoding="utf-8", newline="") as stream:
                write_prices(records, stream)
            return 0

        settings = GraphSettings.from_environment(env)
        client = InstagramClient(session, settings)
        account_id = args.account_id or client.resolve_business_account()
        if args.command == "instagram-posts":
            records = client.collect_posts(account_id, max_pages=args.max_pages)
            headers = ["id", "caption", "like_count", "comments_count", "media_type", "media_url"]
        else:
            metrics = [name.strip() for name in args.metrics.split(",") if name.strip()]
            records = client.collect_account_insights(
                account_id, metrics, args.since, args.until, args.period,
            )
            headers = ["metric", "title", "value", "end_time"]
        _write_dicts(args.output, headers, records)
    return 0


def main() -> None:
    raise SystemExit(run())
