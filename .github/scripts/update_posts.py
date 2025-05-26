#!/usr/bin/env python3
import json, re, requests

FEED_URL = "https://data.accentapi.com/feed/73691.json?no_cache=20250527001540"
README_PATH = "README.md"
START = "<!-- BLOG_POSTS_START -->"
END   = "<!-- BLOG_POSTS_END -->"

def fetch_posts():
    resp = requests.get(FEED_URL)
    resp.raise_for_status()
    data = resp.json()
    # adjust these keys to match your feed’s structure
    items = data.get("items", [])
    return items[:5]

def format_markdown(posts):
    lines = ["\n"]
    for post in posts:
        title = post.get("title")
        url   = post.get("url") or post.get("link")
        lines.append(f"- [{title}]({url})")
    lines.append("\n")
    return "\n".join(lines)

def update_readme(md):
    with open(README_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    pattern = re.compile(
        rf"({re.escape(START)})(.*)({re.escape(END)})",
        flags=re.DOTALL
    )
    new_section = START + format_markdown(fetch_posts()) + END
    new_text = pattern.sub(new_section, text)
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_text)

if __name__ == "__main__":
    update_readme(README_PATH)
