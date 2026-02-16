#!/usr/bin/env python3
"""
Web Search via DuckDuckGo API — Zero dependencies (stdlib only).

Uses DuckDuckGo's free Instant Answer API + HTML search.
No API key required. No pip install needed.

Usage:
    python web_search.py --query "best React frameworks 2025"
    python web_search.py --query "AI SaaS trends" --json
    python web_search.py --query "competitor analysis" --max 10
    python web_search.py --query "food delivery app" --output research.md
"""

import argparse
import json
import sys
import re
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser


# ─── DuckDuckGo Instant Answer API ──────────────────────────────

INSTANT_API = "https://api.duckduckgo.com/"

def instant_search(query):
    """
    Query DuckDuckGo Instant Answer API.
    Returns structured data: abstract, answer, related topics.
    Free, no API key, no rate limit issues for normal usage.
    """
    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "no_html": "1",
        "skip_disambig": "1",
        "no_redirect": "1"
    })

    url = f"{INSTANT_API}?{params}"

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "VibeGravityKit/2.7 (Research Agent)"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return parse_instant_response(data)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return {"error": str(e), "results": []}


def parse_instant_response(data):
    """Parse DuckDuckGo API response into clean structure."""
    result = {
        "type": data.get("Type", ""),
        "answer": data.get("Answer", ""),
        "abstract": data.get("AbstractText", ""),
        "abstract_source": data.get("AbstractSource", ""),
        "abstract_url": data.get("AbstractURL", ""),
        "definition": data.get("Definition", ""),
        "related_topics": [],
        "results": []
    }

    # Parse related topics
    for topic in data.get("RelatedTopics", []):
        if "Text" in topic:
            result["related_topics"].append({
                "text": topic["Text"],
                "url": topic.get("FirstURL", "")
            })
        # Handle sub-topics (grouped categories)
        elif "Topics" in topic:
            for sub in topic["Topics"]:
                if "Text" in sub:
                    result["related_topics"].append({
                        "text": sub["Text"],
                        "url": sub.get("FirstURL", ""),
                        "category": topic.get("Name", "")
                    })

    # Parse direct results
    for r in data.get("Results", []):
        result["results"].append({
            "title": r.get("Text", ""),
            "url": r.get("FirstURL", "")
        })

    return result


# ─── DuckDuckGo HTML Search (full web results) ─────────────────

HTML_SEARCH = "https://html.duckduckgo.com/html/"

class DDGHTMLParser(HTMLParser):
    """Parse DuckDuckGo HTML search results page."""

    def __init__(self):
        super().__init__()
        self.results = []
        self._current = None
        self._in_title = False
        self._in_snippet = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")

        # Result link
        if tag == "a" and "result__a" in cls:
            href = attrs_dict.get("href", "")
            # DuckDuckGo wraps URLs in redirect, extract actual URL
            actual_url = self._extract_url(href)
            self._current = {
                "title": "",
                "url": actual_url,
                "snippet": ""
            }
            self._in_title = True

        # Snippet
        if tag == "a" and "result__snippet" in cls:
            self._in_snippet = True

    def handle_endtag(self, tag):
        if tag == "a" and self._in_title:
            self._in_title = False
        if tag == "a" and self._in_snippet:
            self._in_snippet = False
            if self._current:
                self.results.append(self._current)
                self._current = None

    def handle_data(self, data):
        if self._in_title and self._current:
            self._current["title"] += data.strip()
        if self._in_snippet and self._current:
            self._current["snippet"] += data.strip()

    def _extract_url(self, href):
        """Extract actual URL from DuckDuckGo redirect wrapper."""
        if "uddg=" in href:
            match = re.search(r"uddg=([^&]+)", href)
            if match:
                return urllib.parse.unquote(match.group(1))
        return href


def html_search(query, max_results=10):
    """
    Search DuckDuckGo via HTML endpoint for full web results.
    No API key needed. Uses only stdlib.
    """
    data = urllib.parse.urlencode({"q": query}).encode("utf-8")

    try:
        req = urllib.request.Request(HTML_SEARCH, data=data, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")

        parser = DDGHTMLParser()
        parser.feed(html)
        return parser.results[:max_results]

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return [{"error": str(e)}]


# ─── Combined Search ────────────────────────────────────────────

def search(query, max_results=10):
    """
    Combined search: Instant Answer API + HTML web results.
    Returns both structured knowledge and web results.
    """
    # Get instant answer (fast, structured)
    instant = instant_search(query)

    # Get web results (broader coverage)
    web_results = html_search(query, max_results)

    return {
        "query": query,
        "instant_answer": instant.get("answer", ""),
        "abstract": instant.get("abstract", ""),
        "abstract_source": instant.get("abstract_source", ""),
        "abstract_url": instant.get("abstract_url", ""),
        "definition": instant.get("definition", ""),
        "related_topics": instant.get("related_topics", []),
        "web_results": web_results
    }


# ─── Output Formatters ─────────────────────────────────────────

def print_results(data, compact=False):
    """Print search results. Use compact=True for token-efficient output."""
    if compact:
        # Token-efficient: 1 line per result, no decoration
        if data.get("abstract"):
            print(f"[SUMMARY] {data['abstract'][:200]}")
        for i, r in enumerate(data.get("web_results", []), 1):
            if "error" not in r:
                print(f"{i}. {r['title']} | {r['url']}")
        return

    print("\n" + "=" * 80)
    print(f"🔍 SEARCH: {data['query']}")
    print("=" * 80)

    # Instant answer
    if data.get("instant_answer"):
        print(f"\n💡 Answer: {data['instant_answer']}")

    # Abstract
    if data.get("abstract"):
        print(f"\n📖 Summary ({data.get('abstract_source', '')})")
        print(f"   {data['abstract']}")
        if data.get("abstract_url"):
            print(f"   🔗 {data['abstract_url']}")

    # Definition
    if data.get("definition"):
        print(f"\n📚 Definition: {data['definition']}")

    # Related topics
    if data.get("related_topics"):
        print(f"\n🔗 Related Topics ({len(data['related_topics'])})")
        for i, topic in enumerate(data["related_topics"][:8], 1):
            text = topic["text"][:100] + "..." if len(topic["text"]) > 100 else topic["text"]
            print(f"   {i}. {text}")
            if topic.get("url"):
                print(f"      → {topic['url']}")

    # Web results
    if data.get("web_results"):
        print(f"\n🌐 Web Results ({len(data['web_results'])})")
        print("-" * 80)
        for i, r in enumerate(data["web_results"], 1):
            if "error" in r:
                print(f"   ⚠️ Error: {r['error']}")
                continue
            print(f"   {i}. {r['title']}")
            if r.get("snippet"):
                print(f"      {r['snippet'][:120]}")
            print(f"      🔗 {r['url']}")
            print()

    print("=" * 80 + "\n")


def save_markdown(data, output_path):
    """Save search results as Markdown file."""
    lines = [
        f"# Research: {data['query']}\n"
    ]

    if data["instant_answer"]:
        lines.append(f"**Answer:** {data['instant_answer']}\n")

    if data["abstract"]:
        lines.append(f"## Summary\n")
        lines.append(f"> {data['abstract']}\n")
        lines.append(f"> — [{data['abstract_source']}]({data['abstract_url']})\n")

    if data["web_results"]:
        lines.append(f"## Web Results\n")
        lines.append("| # | Title | URL |")
        lines.append("|---|-------|-----|")
        for i, r in enumerate(data["web_results"], 1):
            if "error" not in r:
                title = r["title"].replace("|", "\\|")
                lines.append(f"| {i} | {title} | [{r['url'][:50]}...]({r['url']}) |")
        lines.append("")

    if data["related_topics"]:
        lines.append(f"## Related Topics\n")
        for topic in data["related_topics"][:10]:
            text = topic["text"].replace("|", "\\|")
            if topic.get("url"):
                lines.append(f"- [{text[:80]}]({topic['url']})")
            else:
                lines.append(f"- {text[:80]}")
        lines.append("")

    content = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved to {output_path}")


# ─── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Web Search via DuckDuckGo — Zero Dependencies"
    )
    parser.add_argument(
        "--query", "-q", type=str, required=True,
        help="Search query"
    )
    parser.add_argument(
        "--max", "-m", type=int, default=10,
        help="Max web results (default: 10)"
    )
    parser.add_argument(
        "--json", "-j", action="store_true",
        help="Output raw JSON"
    )
    parser.add_argument(
        "--compact", "-c", action="store_true",
        help="Token-efficient output: 1 line per result, no decoration (for AI agents)"
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Save results to Markdown file"
    )
    parser.add_argument(
        "--instant-only", action="store_true",
        help="Only use Instant Answer API (faster, no web scraping)"
    )

    args = parser.parse_args()

    if args.instant_only:
        data = instant_search(args.query)
        data["query"] = args.query
        data["web_results"] = []
    else:
        data = search(args.query, args.max)

    if args.json:
        if args.compact:
            # Compact JSON: only essential fields
            compact_data = {
                "q": data.get("query", ""),
                "abstract": data.get("abstract", "")[:200],
                "results": [{"t": r["title"], "u": r["url"]} for r in data.get("web_results", []) if "error" not in r]
            }
            print(json.dumps(compact_data, ensure_ascii=False))
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.output:
        save_markdown(data, args.output)
    else:
        print_results(data, compact=args.compact)


if __name__ == "__main__":
    main()
