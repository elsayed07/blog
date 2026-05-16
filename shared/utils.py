from __future__ import annotations

import math
import re
import unicodedata

import bleach
import markdown as md


ALLOWED_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i",
    "li", "ol", "pre", "strong", "ul", "h1", "h2", "h3", "h4", "h5",
    "h6", "p", "img", "table", "thead", "tbody", "tr", "th", "td",
    "br", "hr", "span", "div", "figure", "figcaption",
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title", "width", "height"],
    "*": ["class"],
}


def render_markdown(text: str) -> str:
    extensions = ["fenced_code", "tables", "toc", "nl2br", "attr_list", "codehilite"]
    raw_html = md.markdown(text, extensions=extensions)
    return bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)


def estimate_reading_time(text: str, wpm: int = 200) -> int:
    word_count = len(re.findall(r"\w+", text))
    return max(1, math.ceil(word_count / wpm))


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)
