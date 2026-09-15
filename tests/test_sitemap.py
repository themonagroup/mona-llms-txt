from pathlib import Path

import pytest

from mona_llms_txt.sitemap import parse_sitemap, read_sitemap


FIXTURES = Path(__file__).parents[1] / "fixtures"


def test_parse_namespaced_urlset():
    kind, urls = parse_sitemap((FIXTURES / "child-pages.xml").read_text())
    assert kind == "urlset"
    assert urls == ["https://example.test/", "https://example.test/dich-vu/seo"]


def test_parse_index():
    kind, urls = parse_sitemap((FIXTURES / "sitemap-index.xml").read_text())
    assert kind == "index"
    assert urls == ["child-pages.xml", "child-blog.xml"]


def test_nested_index_two_children():
    urls = read_sitemap(str(FIXTURES / "sitemap-index.xml"))
    assert urls == [
        "https://example.test/",
        "https://example.test/dich-vu/seo",
        "https://example.test/blog/llms-txt",
        "https://example.test/blog/geo",
    ]


def test_nested_loader_resolves_http_relative_paths():
    docs = {
        "https://x.test/sitemap.xml": "<sitemapindex><sitemap><loc>a.xml</loc></sitemap></sitemapindex>",
        "https://x.test/a.xml": "<urlset><url><loc>https://x.test/a</loc></url></urlset>",
    }
    assert read_sitemap("https://x.test/sitemap.xml", loader=docs.__getitem__) == ["https://x.test/a"]


def test_duplicates_removed_preserving_order():
    xml = "<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/a</loc></url></urlset>"
    assert read_sitemap("memory", loader=lambda _: xml) == ["https://x/a"]


def test_cyclic_index_is_safe():
    xml = "<sitemapindex><sitemap><loc>same.xml</loc></sitemap></sitemapindex>"
    assert read_sitemap("same.xml", loader=lambda _: xml) == []


@pytest.mark.parametrize("xml", ["<broken", "<rss></rss>"])
def test_invalid_sitemap(xml):
    with pytest.raises(ValueError):
        parse_sitemap(xml)


def test_depth_limit():
    xml = "<sitemapindex><sitemap><loc>next.xml</loc></sitemap></sitemapindex>"
    with pytest.raises(ValueError, match="too deep"):
        read_sitemap("start.xml", loader=lambda _: xml, max_depth=0)

