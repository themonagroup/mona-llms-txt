"""Offline demo: ``python examples/demo.py`` from the repository root."""

from pathlib import Path
import sys

# Cho phép chạy demo trực tiếp từ checkout mà chưa cần ``pip install -e .``.
root = Path(__file__).parents[1]
sys.path.insert(0, str(root))

from mona_llms_txt import build_llms_txt
from mona_llms_txt.extract import extract_page
from mona_llms_txt.grouper import section_for_url


samples = [
    ("https://example.test/", "home.html"),
    ("https://example.test/dich-vu/seo", "service.html"),
    ("https://example.test/blog/llms-txt", "article.html"),
]
pages = []
for url, filename in samples:
    page = extract_page((root / "fixtures" / filename).read_text(encoding="utf-8"))
    page.update(url=url, section=section_for_url(url))
    pages.append(page)

print(build_llms_txt("MONA Demo", "Website minh hoạ GEO.", pages))
