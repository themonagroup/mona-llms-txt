"""Group pages by their first URL path segment."""

from collections import OrderedDict
from typing import Dict, Iterable, List
from urllib.parse import unquote, urlparse


def section_for_url(url: str) -> str:
    segments = [unquote(part) for part in urlparse(url).path.split("/") if part]
    return segments[0] if segments else "Trang chính"


def group_pages(pages: Iterable[dict]) -> Dict[str, List[dict]]:
    grouped: Dict[str, List[dict]] = OrderedDict()
    for page in pages:
        section = str(page.get("section") or section_for_url(str(page.get("url", ""))))
        copy = dict(page)
        copy["section"] = section
        grouped.setdefault(section, []).append(copy)
    return grouped

