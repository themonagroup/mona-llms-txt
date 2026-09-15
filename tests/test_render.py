from mona_llms_txt import build_llms_txt


PAGES = [
    {"url": "https://x.test/blog/a", "title": "Bài A", "desc": "Mô tả A", "section": "blog", "content": "Nội dung dài A"},
    {"url": "https://x.test/dich-vu/x", "title": "Dịch vụ X", "desc": "Mô tả X", "section": "dich-vu"},
]


def test_starts_with_title():
    assert build_llms_txt("Title", "desc", PAGES).startswith("# Title\n")


def test_has_blockquote_description():
    assert "\n> desc\n" in build_llms_txt("Title", "desc", PAGES)


def test_has_each_section():
    result = build_llms_txt("Title", "desc", PAGES)
    assert "## blog" in result and "## dich-vu" in result


def test_page_line_exact_shape():
    assert "- [Bài A](https://x.test/blog/a): Mô tả A" in build_llms_txt("Title", "desc", PAGES)


def test_full_differs_and_adds_content():
    short = build_llms_txt("Title", "desc", PAGES)
    full = build_llms_txt("Title", "desc", PAGES, full=True)
    assert full != short
    assert "  - Nội dung: Nội dung dài A" in full


def test_short_omits_content():
    assert "Nội dung dài A" not in build_llms_txt("Title", "desc", PAGES)


def test_output_ends_with_single_newline():
    assert build_llms_txt("Title", "desc", []).endswith("\n")
    assert not build_llms_txt("Title", "desc", []).endswith("\n\n")


def test_multiline_values_are_flattened():
    result = build_llms_txt("A\nB", "C\nD", [])
    assert result == "# A B\n\n> C D\n"


def test_brackets_in_title_are_escaped():
    page = [{"url": "https://x", "title": "A [guide]", "desc": "D"}]
    assert "[A \\[guide\\]](https://x)" in build_llms_txt("T", "D", page)

