"""Public API for :mod:`mona_llms_txt`."""

from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

from .extract import extract_page
from .fetch import fetch_text
from .grouper import section_for_url
from .render import build_llms_txt
from .sitemap import read_sitemap

__all__ = ["build_llms_txt", "generate"]
__version__ = "0.1.0"


def _default_site_name(source: str, urls: list[str]) -> str:
    candidate = urls[0] if urls else source
    host = urlparse(candidate).hostname
    if host:
        return host.removeprefix("www.")
    return Path(source).stem.replace("-", " ").title() or "Website"


def generate(
    sitemap_source: str,
    *,
    full: bool = False,
    max_pages: int = 200,
    loader: Callable[[str], str] = fetch_text,
) -> str:
    """Fetch, extract, group, and render pages listed in a sitemap.

    ``loader`` is injectable so callers and tests can provide cached content.
    """
    if max_pages < 0:
        raise ValueError("max_pages must be non-negative")
    urls = read_sitemap(str(sitemap_source), loader=loader)[:max_pages]
    pages = []
    for url in urls:
        data = extract_page(loader(url))
        data.update(url=url, section=section_for_url(url))
        pages.append(data)

    site_title = _default_site_name(str(sitemap_source), urls)
    site_desc = f"Nội dung quan trọng từ {site_title}."
    # Ưu tiên metadata trang chủ làm thông tin website nếu sitemap có trang chủ.
    for page in pages:
        if urlparse(page["url"]).path in {"", "/"}:
            site_title = page["title"]
            site_desc = page["desc"]
            break
    return build_llms_txt(site_title, site_desc, pages, full=full)

