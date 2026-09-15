"""Render documents in the llms.txt Markdown shape."""

from typing import Iterable
import re

from .grouper import group_pages


def _one_line(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _link_text(value: object) -> str:
    return _one_line(value).replace("[", "\\[").replace("]", "\\]")


def build_llms_txt(
    site_title: str, site_desc: str, pages: Iterable[dict], *, full: bool = False
) -> str:
    """Pure renderer for an llms.txt or expanded llms-full.txt document."""
    lines = [f"# {_one_line(site_title) or 'Website'}", "", f"> {_one_line(site_desc)}"]
    for section, items in group_pages(pages).items():
        lines.extend(["", f"## {_one_line(section)}", ""])
        for page in items:
            title = _link_text(page.get("title") or page.get("h1") or page.get("url"))
            url = _one_line(page.get("url"))
            desc = _one_line(page.get("desc") or page.get("h1") or title)
            lines.append(f"- [{title}]({url}): {desc}")
            content = _one_line(page.get("content"))
            if full and content and content != desc:
                lines.append(f"  - Nội dung: {content}")
    return "\n".join(lines).rstrip() + "\n"

