"""Parse URL sets and recursively resolve sitemap indexes."""

from pathlib import Path
from typing import Callable, List, Optional
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

from .fetch import fetch_text


def _local_join(parent: str, child: str) -> str:
    parsed = urlparse(child)
    if parsed.scheme or Path(child).is_absolute():
        return child
    if urlparse(parent).scheme in {"http", "https", "file"}:
        return urljoin(parent, child)
    return str(Path(parent).parent / child)


def parse_sitemap(xml_text: str) -> tuple[str, List[str]]:
    """Return ``(kind, locations)`` where kind is ``urlset`` or ``index``."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid sitemap XML: {exc}") from exc
    tag = root.tag.rsplit("}", 1)[-1]
    if tag not in {"urlset", "sitemapindex"}:
        raise ValueError(f"Unsupported sitemap root: {tag}")
    item_tag = "url" if tag == "urlset" else "sitemap"
    locations: List[str] = []
    for item in root:
        if item.tag.rsplit("}", 1)[-1] != item_tag:
            continue
        for child in item:
            if child.tag.rsplit("}", 1)[-1] == "loc" and child.text:
                value = child.text.strip()
                if value:
                    locations.append(value)
                break
    return ("index" if tag == "sitemapindex" else "urlset", locations)


def read_sitemap(
    source: str,
    *,
    loader: Callable[[str], str] = fetch_text,
    max_depth: int = 10,
    _seen: Optional[set[str]] = None,
) -> List[str]:
    """Read a sitemap source and recursively flatten nested indexes.

    Duplicate URLs retain their first-seen order. Cyclic indexes are ignored.
    """
    if max_depth < 0:
        raise ValueError("Sitemap nesting is too deep")
    seen = _seen if _seen is not None else set()
    if source in seen:
        return []
    seen.add(source)
    kind, locations = parse_sitemap(loader(source))
    if kind == "urlset":
        return list(dict.fromkeys(locations))
    urls: List[str] = []
    for location in locations:
        child_source = _local_join(source, location)
        urls.extend(
            read_sitemap(
                child_source, loader=loader, max_depth=max_depth - 1, _seen=seen
            )
        )
    return list(dict.fromkeys(urls))

