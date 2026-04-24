"""
LLM Narrator — generates analyst-style commentary from structured insights.

Uses the Google Gemini API with strict guardrails:
- Only references data provided in the insights
- No hallucination of events, dates, or policy actions
- Supports tone control (neutral, bullish, bearish, cautious)
"""

from __future__ import annotations
import hashlib
import json
import logging
import os
import httpx

from ..models.schemas import ChartInsight, Narrative

logger = logging.getLogger(__name__)

# ─── Google Gemini Configuration ──────────────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}"
    f":generateContent?key={GEMINI_API_KEY}"
)

def _get_gemini_endpoint() -> str:
    """Build endpoint URL using current env vars (allows runtime changes)."""
    api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
    model = os.getenv("GEMINI_MODEL", GEMINI_MODEL)
    return (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
        f":generateContent?key={api_key}"
    )

# Shared async HTTP client
_http_client = httpx.AsyncClient(timeout=120.0)

# In-memory narrative cache
_narrative_cache: dict[str, Narrative] = {}


async def close_http_client() -> None:
    """Close the shared HTTP client. Called on application shutdown."""
    if not _http_client.is_closed:
        await _http_client.aclose()


# ─── Prompt Templates ─────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior financial analyst at a global research firm.
Your task is to generate clear, professional commentary from STRUCTURED DATA ONLY.

STRICT RULES:
1. ONLY reference data, statistics, trends, and anomalies provided in the JSON below.
2. NEVER mention specific events, policy decisions, geopolitical actions, or causes NOT in the data.
3. Use hedging language for interpretive statements: "appears to", "suggests", "indicates".
4. All numbers must come directly from the data provided.
5. Do NOT invent dates or time periods not present in the data.

WRITING STYLE:
- Write like a Bloomberg or Reuters market brief — concise, authoritative, narrative-driven.
- Lead with the most important insight, not raw numbers.
- Embed key figures naturally within sentences. NEVER list raw statistics.
- Describe direction and magnitude in plain language: "climbed sharply", "remained broadly stable", "pulled back modestly".
- Round aggressively: say "roughly 54%" not "53.96%", "nearly doubled" not "increased 181.41%".
- Use comparative language: "outpaced peers", "lagged the group average", "diverged markedly".
- For anomalies, explain significance to an analyst: "an outlier that warrants further investigation" rather than citing z-scores.
- Key takeaways should be actionable observations an analyst can brief to a portfolio manager, not restated statistics.

OUTPUT FORMAT — respond with valid JSON only:
{
  "summary": "2-3 sentence headline-style finding. Lead with the narrative, embed one or two rounded figures.",
  "detailed": "A 4-6 sentence analyst paragraph telling the data story. Emphasize direction, pace, and relative performance. Cite only the most meaningful numbers, rounded and in context.",
  "key_takeaways": ["Actionable observation 1", "Actionable observation 2", "Actionable observation 3"],
  "tone": "the tone you used"
}"""


def _build_user_prompt(insight: ChartInsight, tone: str = "neutral", focus_series: str = "") -> str:
    """Build the user prompt with structured insight data."""

    # Only send stats per series (not raw data points — far too verbose)
    series_summaries = [
        {"name": s.name, "stats": s.stats.model_dump()}
        for s in insight.series
    ]

    data_block = {
        "chart_title": insight.metadata.title,
        "chart_subtitle": insight.metadata.subtitle,
        "chart_type": insight.metadata.chart_type,
        "series": series_summaries,
        # Cap to avoid inflating prompt size / token count
        "trends": [t.model_dump() for t in insight.trends[:8]],
        "anomalies": [a.model_dump() for a in insight.anomalies[:5]],
        "correlations": [c.model_dump() for c in insight.correlations[:4]],
        "confidence": insight.overall_confidence,
    }

    # Compact JSON (no indent/spaces) — ~25-35% fewer prompt tokens vs indent=2
    data_json = json.dumps(data_block, separators=(",", ":"))

    focus_line = f"FOCUS ON SERIES: {focus_series}\n" if focus_series else ""
    return (
        f"Analyze this financial chart data and generate commentary.\n\n"
        f"TONE: {tone}\n"
        f"{focus_line}"
        f"CHART DATA:\n```json\n{data_json}\n```\n\n"
        "Generate the analyst commentary as JSON following the system instructions."
    )


# ─── API Call ─────────────────────────────────────────────────────────────────

async def generate_narrative(
    insight: ChartInsight,
    tone: str = "neutral",
    focus_series: str = "",
) -> Narrative:
    """
    Call Google Gemini to generate narrative from structured insights.
    Returns cached result instantly if the same insight+tone was seen before.
    """
    user_prompt = _build_user_prompt(insight, tone, focus_series)

    # Cache lookup
    cache_key = hashlib.md5(user_prompt.encode()).hexdigest()
    if cache_key in _narrative_cache:
        logger.info("Narrative cache hit")
        return _narrative_cache[cache_key]

    full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

    payload = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 1500,
            "temperature": 0.7,
        },
    }

    try:
        endpoint = _get_gemini_endpoint()
        response = await _http_client.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        result = response.json()
        candidates = result.get("candidates", [])
        if not candidates:
            logger.warning("Gemini returned no candidates, using fallback")
            return _fallback_narrative(insight, tone)

        content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")

        if not content.strip():
            logger.warning("Gemini returned empty content, using fallback")
            return _fallback_narrative(insight, tone)

        # Parse JSON response — handle potential markdown code blocks
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        if not content.startswith("{"):
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                content = content[json_start:json_end]

        narrative_data = json.loads(content)

        narrative = Narrative(
            summary=narrative_data.get("summary", ""),
            detailed=narrative_data.get("detailed", ""),
            key_takeaways=narrative_data.get("key_takeaways", []),
            tone=narrative_data.get("tone", tone),
        )
        _narrative_cache[cache_key] = narrative
        return narrative

    except httpx.HTTPStatusError as e:
        logger.error(f"Gemini API error: {e.response.status_code} - {e.response.text}")
        return _fallback_narrative(insight, tone)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        return _fallback_narrative(insight, tone)
    except Exception as e:
        logger.error(f"Gemini call failed: {e}")
        return _fallback_narrative(insight, tone)


def generate_narrative_sync(
    insight: ChartInsight,
    tone: str = "neutral",
    focus_series: str = "",
) -> Narrative:
    """Synchronous version for testing."""
    import asyncio
    return asyncio.run(generate_narrative(insight, tone, focus_series))


async def stream_narrative(
    insight: ChartInsight,
    tone: str = "neutral",
    focus_series: str = "",
):
    """
    Async generator that yields narrative text from Gemini.
    Since Gemini REST API does not support true streaming easily,
    we generate the full response and yield it in chunks.
    """
    try:
        narrative = await generate_narrative(insight, tone, focus_series)
        # Yield the full JSON as a single chunk
        result = json.dumps({
            "summary": narrative.summary,
            "detailed": narrative.detailed,
            "key_takeaways": narrative.key_takeaways,
            "tone": narrative.tone,
        })
        yield result
    except Exception as e:
        logger.error(f"stream_narrative failed: {e}")
        yield "[Streaming error — narrative unavailable]"


# ─── Fallback Narrative (no LLM needed) ──────────────────────────────────────

def _fallback_narrative(insight: ChartInsight, tone: str = "neutral") -> Narrative:
    """Generate a basic narrative without LLM when API fails."""
    title = insight.metadata.title or "this chart"

    # Build summary from stats
    parts = []
    for s in insight.series:
        if s.stats.data_point_count > 0:
            direction = "increased" if s.stats.overall_change_pct > 0 else "decreased"
            parts.append(
                f"{s.name} {direction} by {abs(s.stats.overall_change_pct):.1f}% "
                f"from {s.stats.first_value:.1f} to {s.stats.latest_value:.1f}"
            )

    summary = f"Analysis of {title}. " + ". ".join(parts[:2]) + "." if parts else f"Analysis of {title}."

    # Build takeaways from trends
    takeaways = []
    for t in insight.trends[:5]:
        takeaways.append(
            f"{t.series_name}: {t.direction.value} trend from {t.start_label} to {t.end_label} "
            f"({t.magnitude_pct:+.1f}%)"
        )

    # Add anomaly takeaways
    for a in insight.anomalies[:3]:
        takeaways.append(f"Anomaly: {a.description}")

    return Narrative(
        summary=summary,
        detailed=summary + " " + " ".join(takeaways),
        key_takeaways=takeaways[:5],
        tone=tone,
    )


# ─── Multi-Chart Comparison ──────────────────────────────────────────────────

async def generate_comparison_narrative(
    insights: list[ChartInsight],
    tone: str = "neutral",
) -> Narrative:
    """Generate a comparative narrative across multiple charts."""

    charts_summary = []
    for ins in insights:
        chart_info = {
            "title": ins.metadata.title,
            "series_count": len(ins.series),
            "series": [
                {"name": s.name, "change_pct": s.stats.overall_change_pct, "latest": s.stats.latest_value}
                for s in ins.series
            ],
            "trend_count": len(ins.trends),
            "anomaly_count": len(ins.anomalies),
        }
        charts_summary.append(chart_info)

    user_prompt = f"""Compare these financial charts and identify cross-cutting themes.

TONE: {tone}

CHARTS:
```json
{json.dumps(charts_summary, separators=(',', ':'))}
```

Generate a comparative analyst commentary as JSON following the system instructions."""

    full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

    payload = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 1500,
            "temperature": 0.7,
        },
    }

    try:
        endpoint = _get_gemini_endpoint()
        response = await _http_client.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        result = response.json()
        candidates = result.get("candidates", [])
        if not candidates:
            raise ValueError("No candidates returned")
        content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
        if not content.startswith("{"):
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                content = content[json_start:json_end]
        data = json.loads(content)
        return Narrative(
            summary=data.get("summary", ""),
            detailed=data.get("detailed", ""),
            key_takeaways=data.get("key_takeaways", []),
            tone=data.get("tone", tone),
        )
    except Exception as e:
        logger.error(f"Comparison Gemini call failed: {e}")
        return Narrative(
            summary="Comparison analysis unavailable.",
            detailed="Unable to generate comparison at this time.",
            key_takeaways=[],
            tone=tone,
        )

