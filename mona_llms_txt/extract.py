"""Extract useful page metadata using only :mod:`html.parser`."""

from html.parser import HTMLParser
from typing import Dict, List, Optional
import re


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: List[str] = []
        self.h1_parts: List[str] = []
        self.body_parts: List[str] = []
        self.description: Optional[str] = None
        self._in_title = False
        self._in_h1 = False
        self._ignored = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        values = {key.lower(): value for key, value in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag in {"script", "style", "noscript", "svg"}:
            self._ignored += 1
        elif tag == "meta":
            key = (values.get("name") or values.get("property") or "").lower()
            if key in {"description", "og:description"} and not self.description:
                self.description = _clean(values.get("content") or "") or None

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag in {"script", "style", "noscript", "svg"} and self._ignored:
            self._ignored -= 1

    def handle_data(self, data: str) -> None:
        if self._ignored:
            return
        if self._in_title:
            self.title_parts.append(data)
        if self._in_h1:
            self.h1_parts.append(data)
        # Phần thân phục vụ llms-full; loại title để tránh lặp.
        if not self._in_title:
            value = _clean(data)
            if value:
                self.body_parts.append(value)


def extract_page(html_text: str, *, content_limit: int = 2000) -> Dict[str, str]:
    """Extract title, H1, description, and readable text from HTML."""
    parser = PageParser()
    parser.feed(html_text)
    title = _clean(" ".join(parser.title_parts))
    h1 = _clean(" ".join(parser.h1_parts))
    display_title = title or h1 or "Untitled"
    description = parser.description or h1 or title
    content = _clean(" ".join(parser.body_parts))
    if content_limit >= 0 and len(content) > content_limit:
        content = content[: max(0, content_limit - 1)].rstrip() + "…"
    return {"title": display_title, "desc": description, "h1": h1, "content": content}

