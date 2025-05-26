#!/usr/bin/env python3
import json
import re
import requests
import sys

# ── CONFIG ─────────────────────────────────────────────────────────────────────
FEED_URL    = "https://data.accentapi.com/feed/73691.json?no_cache=20250527022219"
README_PATH = "README.md"
START_MARK  = "<!-- BLOG_POSTS_START -->"
END_MARK    = "<!-- BLOG_POSTS_END -->"
MAX_POSTS   = 5
# ────────────────────────────────────────────────────────────────────────────────

def fetch_posts():
    resp = requests.get(FEED_URL)
    resp.raise_for_status()
    data = resp.json()

    # 1) Top-level "items"
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"][:MAX_POSTS]

    # 2) Inside "feed" → "items"
    if isinstance(data, dict) and "feed" in data and isinstance(data["feed"], dict):
        items = data["feed"].get("items")
        if isinstance(items, list):
            return items[:MAX_POSTS]

    # 3) Inside "data" → "items"
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
        items = data["data"].get("items")
        if isinstance(items, list):
            return items[:MAX_POSTS]

    # 4) Fallback: first list found at top level
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, list):
                print(f"DEBUG: using top-level list at key '{key}' with {len(val)} entries", file=sys.stderr)
                return val[:MAX_POSTS]

    # nothing matched
    print("WARNING: no list of posts found in JSON feed", file=sys.stderr)
    return []

def format_markdown(posts):
    md = []
    for post in posts:
        title = post.get("title") or post.get("name") or "Untitled"
        url   = post.get("url") or post.get("link") or post.get("permalink")
        if not url:
            continue
        md.append(f"- [{title}]({url})")
    return "\n".join(md)

def update_readme():
    posts = fetch_posts()
    if not posts:
        # no changes — prevent accidental clearing of your README section
        return

    new_block = f"{START_MARK}\n{format_markdown(posts)}\n{END_MARK}"
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    updated = re.sub(
        rf"{re.escape(START_MARK)}.*?{re.escape(END_MARK)}",
        new_block,
        content,
        flags=re.DOTALL
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"✔️ README updated with {len(posts)} posts")

if __name__ == "__main__":
    update_readme()
