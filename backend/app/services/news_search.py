"""
News Search — fetches relevant news headlines for chart breakpoints.

Uses Google News RSS feed (no API key required, publicly accessible)
to find real-world events that may explain trend changes.
Falls back to Bing News search if RSS fails.
"""

from __future__ import annotations
import re
import logging
from dataclasses import dataclass
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import httpx

logger = logging.getLogger(__name__)

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


@dataclass
class NewsResult:
    title: str
    snippet: str
    url: str
    date_hint: str  # approximate date from snippet


async def search_news(query: str, max_results: int = 5) -> list[NewsResult]:
    """
    Search Google News RSS for headlines matching a query.
    Returns a list of NewsResult with title, snippet, url.
    """
    results = []
    try:
        url = GOOGLE_NEWS_RSS.format(query=quote_plus(query))
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(
                url,
                headers={"User-Agent": USER_AGENT},
            )
            resp.raise_for_status()
            xml_text = resp.text

            # Parse RSS XML
            root = ET.fromstring(xml_text)
            channel = root.find("channel")
            if channel is None:
                return results

            items = channel.findall("item")
            for item in items[:max_results]:
                title_el = item.find("title")
                link_el = item.find("link")
                pub_date_el = item.find("pubDate")
                desc_el = item.find("description")

                title_text = (title_el.text or "").strip() if title_el is not None else ""
                link_text = (link_el.text or "").strip() if link_el is not None else ""
                pub_date = (pub_date_el.text or "").strip() if pub_date_el is not None else ""
                snippet_text = ""
                if desc_el is not None and desc_el.text:
                    snippet_text = _strip_html(desc_el.text)[:300]

                if title_text:
                    results.append(NewsResult(
                        title=title_text,
                        snippet=snippet_text,
                        url=link_text,
                        date_hint=pub_date,
                    ))

    except Exception as e:
        logger.warning(f"Google News RSS failed for '{query}': {e}")
        # Fallback: try Bing News search
        results = await _fallback_bing_news(query, max_results)

    return results


async def _fallback_bing_news(query: str, max_results: int = 5) -> list[NewsResult]:
    """Fallback news search using Bing News HTML scraping."""
    results = []
    try:
        search_url = f"https://www.bing.com/news/search?q={quote_plus(query)}&format=rss"
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(
                search_url,
                headers={"User-Agent": USER_AGENT},
            )
            resp.raise_for_status()
            xml_text = resp.text

            root = ET.fromstring(xml_text)
            channel = root.find("channel")
            if channel is None:
                return results

            items = channel.findall("item")
            for item in items[:max_results]:
                title_el = item.find("title")
                link_el = item.find("link")
                pub_date_el = item.find("pubDate")
                desc_el = item.find("description")

                title_text = (title_el.text or "").strip() if title_el is not None else ""
                link_text = (link_el.text or "").strip() if link_el is not None else ""
                pub_date = (pub_date_el.text or "").strip() if pub_date_el is not None else ""
                snippet_text = ""
                if desc_el is not None and desc_el.text:
                    snippet_text = _strip_html(desc_el.text)[:300]

                if title_text:
                    results.append(NewsResult(
                        title=title_text,
                        snippet=snippet_text,
                        url=link_text,
                        date_hint=pub_date,
                    ))
    except Exception as e:
        logger.warning(f"Bing News RSS fallback also failed for '{query}': {e}")

    return results


def build_search_queries(
    chart_title: str,
    trends: list[dict],
    anomalies: list[dict],
) -> list[str]:
    """
    Build targeted search queries from chart metadata and breakpoints.
    """
    queries = []
    topic = re.sub(r'^\d+\.\s*', '', chart_title)
    topic = re.sub(r'\s*-\s*\d+\s*', ' ', topic)
    topic = topic.strip()

    if not topic:
        return queries

    for t in trends:
        if abs(t.get("magnitude_pct", 0)) > 5:
            direction = t.get("direction", "")
            start = t.get("start_label", "")
            end = t.get("end_label", "")
            period = ""
            if start and end:
                period = f"{start} {end}"
            elif start:
                period = start

            if direction in ("rising", "spike"):
                queries.append(f"{topic} increase {period} reason why")
            elif direction in ("falling", "dip"):
                queries.append(f"{topic} decline {period} reason why")

    for a in anomalies[:2]:
        label = a.get("x_label", "")
        queries.append(f"{topic} {label} unusual change")

    queries.append(f"{topic} major events trends analysis")

    seen = set()
    unique = []
    for q in queries:
        key = q.lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(q)

    return unique[:5]


def _strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&#x27;', "'").replace('&quot;', '"').replace('&#39;', "'")
    return text
