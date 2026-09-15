"""Network and file I/O, kept separate from the parsing core."""

from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen


USER_AGENT = "mona-llms-txt/0.1 (+https://llmstxt.org/)"


def fetch_text(source: str, *, timeout: float = 15.0) -> str:
    """Read UTF-8-ish text from a local path, file URL, or HTTP(S) URL."""
    parsed = urlparse(str(source))
    if parsed.scheme in {"http", "https"}:
        request = Request(str(source), headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=timeout) as response:  # nosec B310
            data = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
        return data.decode(charset, errors="replace")
    if parsed.scheme == "file":
        return Path(unquote(parsed.path)).read_text(encoding="utf-8")
    if parsed.scheme:
        raise ValueError(f"Unsupported source scheme: {parsed.scheme}")
    return Path(source).read_text(encoding="utf-8")

