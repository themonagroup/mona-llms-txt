from mona_llms_txt.grouper import group_pages, section_for_url


def test_expected_path_groups():
    pages = [{"url": "/blog/a"}, {"url": "/blog/b"}, {"url": "/dich-vu/x"}]
    grouped = group_pages(pages)
    assert list(grouped) == ["blog", "dich-vu"]
    assert len(grouped["blog"]) == 2


def test_homepage_section():
    assert section_for_url("https://example.test/") == "Trang chính"


def test_query_does_not_affect_section():
    assert section_for_url("https://x.test/news?a=1") == "news"


def test_percent_encoded_section_is_decoded():
    assert section_for_url("https://x.test/kien%20thuc/a") == "kien thuc"


def test_explicit_section_wins():
    assert list(group_pages([{"url": "/blog/a", "section": "Tin tức"}])) == ["Tin tức"]


def test_group_does_not_mutate_input():
    page = {"url": "/blog/a"}
    group_pages([page])
    assert "section" not in page

