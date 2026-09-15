"""Command-line entry point."""

import argparse
from pathlib import Path
from typing import Optional, Sequence

from . import generate


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mona-llms-txt", description="Generate llms.txt from a sitemap"
    )
    parser.add_argument("sitemap_source", help="sitemap URL or local XML file")
    parser.add_argument("--full", action="store_true", help="include extracted page content")
    parser.add_argument("--max-pages", type=int, default=200, help="maximum pages to fetch")
    parser.add_argument("-o", "--output", help="output path (stdout when omitted)")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = make_parser().parse_args(argv)
    try:
        result = generate(args.sitemap_source, full=args.full, max_pages=args.max_pages)
        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
        else:
            print(result, end="")
    except (OSError, ValueError) as exc:
        make_parser().error(str(exc))
    return 0

