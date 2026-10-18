#!/usr/bin/env python3
"""Fetch Japanese headlines server-side for GitHub Pages.

The workflow creates site/news.json before deployment, so the browser never
needs to call third-party news APIs directly (and is not blocked by CORS).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import email.utils
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

USER_AGENT = "ChatSpamNewsTicker/1.0 (+https://github.com/harunobushishido-boop/chat-spam)"
PUBLISHED_NEWS_URL = "https://harunobushishido-boop.github.io/chat-spam/news.json"
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
RSS_FEEDS = [
    ("Google News 総合", "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"),
    ("Google News 国内", "https://news.google.com/rss/headlines/section/topic/NATION?hl=ja&gl=JP&ceid=JP:ja"),
    ("Google News 世界", "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ja&gl=JP&ceid=JP:ja"),
    ("Google News 経済", "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=ja&gl=JP&ceid=JP:ja"),
    ("Google News 科学・技術", "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ja&gl=JP&ceid=JP:ja"),
]
MAX_HEADLINES = 45


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def isoformat(value: dt.datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def request_bytes(url: str, timeout: int = 10) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/xml, application/json, text/xml, */*",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def parse_datetime(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    text = str(value).strip()
    try:
        # GDELT date format: 20261018T083000Z
        if len(text) == 16 and text.endswith("Z") and "T" in text:
            parsed = dt.datetime.strptime(text, "%Y%m%dT%H%M%SZ")
            return parsed.replace(tzinfo=dt.timezone.utc)
        parsed = email.utils.parsedate_to_datetime(text)
        if parsed:
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)
    except (ValueError, TypeError, OverflowError):
        pass
    try:
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def normalize_url(value: str | None) -> str:
    url = str(value or "").strip()
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        return ""
    return url


def clean_article(title: str, url: str, source: str, date_value: str | None) -> dict[str, Any] | None:
    title = " ".join(str(title or "").split())
    url = normalize_url(url)
    if len(title) < 6 or not url:
        return None
    parsed_date = parse_datetime(date_value)
    parsed_url = urllib.parse.urlparse(url)
    domain = (parsed_url.hostname or source or "ニュース配信元").removeprefix("www.")
    return {
        "title": title[:300],
        "url": url,
        "source": str(source or domain)[:100],
        "domain": domain[:100],
        "publishedAt": isoformat(parsed_date),
    }


def parse_rss(feed_name: str, feed_url: str) -> list[dict[str, Any]]:
    data = request_bytes(feed_url, timeout=10)
    root = ET.fromstring(data)
    articles: list[dict[str, Any]] = []

    # Google News uses RSS 2.0. Namespace-independent matching is used for
    # source elements and other feeds with namespace declarations.
    for item in root.findall(".//item"):
        def text_of(tag: str) -> str:
            element = item.find(tag)
            return (element.text or "").strip() if element is not None else ""

        title = text_of("title")
        link = text_of("link")
        date_value = text_of("pubDate")
        source_element = item.find("source")
        source_name = (source_element.text or "").strip() if source_element is not None else feed_name
        article = clean_article(title, link, source_name or feed_name, date_value)
        if article:
            articles.append(article)

    return articles


def fetch_gdelt() -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({
        "query": "sourcelang:japanese",
        "mode": "ArtList",
        "format": "json",
        "sort": "DateDesc",
        "timespan": "24h",
        "maxrecords": "50",
    })
    payload = json.loads(request_bytes(f"{GDELT_URL}?{params}", timeout=12).decode("utf-8-sig"))
    results: list[dict[str, Any]] = []
    for item in payload.get("articles", []):
        article = clean_article(
            item.get("title", ""),
            item.get("url", ""),
            item.get("domain", "GDELT"),
            item.get("seendate"),
        )
        if article:
            results.append(article)
    return results


def deduplicate_sort(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for article in articles:
        key = article.get("url") or article.get("title", "").casefold()
        if key and key not in unique:
            unique[key] = article
    values = list(unique.values())
    values.sort(key=lambda item: item.get("publishedAt") or "", reverse=True)
    return values[:MAX_HEADLINES]


def fetch_previous_published() -> dict[str, Any] | None:
    url = PUBLISHED_NEWS_URL + "?cacheBust=" + str(int(time.time()))
    try:
        raw = request_bytes(url, timeout=8)
        data = json.loads(raw.decode("utf-8-sig"))
        if isinstance(data, dict) and isinstance(data.get("articles"), list):
            return data
    except Exception as error:  # Existing Pages file may not exist on first deploy.
        print(f"Could not restore previous published news: {error}", file=sys.stderr)
    return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="site/news.json")
    args = parser.parse_args()
    output_path = Path(args.output)
    checked_at = isoformat(utc_now())

    jobs: list[tuple[str, Any]] = [("GDELT", fetch_gdelt)]
    jobs.extend((feed_name, lambda name=feed_name, url=feed_url: parse_rss(name, url)) for feed_name, feed_url in RSS_FEEDS)

    all_articles: list[dict[str, Any]] = []
    successful_sources: list[str] = []
    errors: list[str] = []

    # Query all sources concurrently so a slow API does not make the ticker
    # wait for each service one by one.
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        future_names = {pool.submit(fetcher): name for name, fetcher in jobs}
        for future in concurrent.futures.as_completed(future_names):
            source_name = future_names[future]
            try:
                articles = future.result()
                if articles:
                    all_articles.extend(articles)
                    successful_sources.append(source_name)
                else:
                    errors.append(f"{source_name}: 記事なし")
            except Exception as error:
                errors.append(f"{source_name}: {type(error).__name__}: {error}")
                print(errors[-1], file=sys.stderr)

    articles = deduplicate_sort(all_articles)
    if articles:
        payload = {
            "schemaVersion": 1,
            "updatedAt": checked_at,
            "checkedAt": checked_at,
            "stale": False,
            "source": " / ".join(successful_sources),
            "articles": articles,
        }
        write_json(output_path, payload)
        print(f"OK: {len(articles)} headlines from {payload['source']}; wrote {output_path}")
        return 0

    # Total outage: retain the last published feed so the ticker does not go
    # blank. The previous successful updatedAt is intentionally preserved.
    previous = fetch_previous_published()
    if previous is None and output_path.exists():
        try:
            local_payload = json.loads(output_path.read_text(encoding="utf-8"))
            if isinstance(local_payload, dict) and isinstance(local_payload.get("articles"), list):
                previous = local_payload
        except Exception as error:
            print(f"Could not read local previous news: {error}", file=sys.stderr)

    if previous is None:
        previous = {
            "schemaVersion": 1,
            "updatedAt": None,
            "source": "none",
            "articles": [],
        }
    previous["checkedAt"] = checked_at
    previous["stale"] = True
    previous["lastError"] = "全てのニュース取得元で取得に失敗しました。前回データを保持しています。"
    write_json(output_path, previous)
    print(
        f"WARNING: all sources failed; preserved {len(previous.get('articles', []))} previous headlines. "
        f"Errors: {'; '.join(errors)}",
        file=sys.stderr,
    )
    # This is a valid build even during an upstream outage.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
