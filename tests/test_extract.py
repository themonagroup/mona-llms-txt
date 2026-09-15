from pathlib import Path

from mona_llms_txt.extract import extract_page


FIXTURES = Path(__file__).parents[1] / "fixtures"


def load(name):
    return (FIXTURES / name).read_text()


def test_extract_title():
    assert extract_page(load("home.html"))["title"] == "MONA Demo"


def test_extract_meta_description():
    assert extract_page(load("home.html"))["desc"] == "Website minh hoạ GEO."


def test_extract_h1():
    assert extract_page(load("article.html"))["h1"] == "llms.txt là gì?"


def test_og_description_fallback():
    assert extract_page(load("article.html"))["desc"] == "Cách tạo tệp cho AI."


def test_missing_meta_falls_back_to_h1():
    page = extract_page(load("service.html"))
    assert page["desc"] == "SEO bền vững"


def test_missing_title_falls_back_to_h1():
    assert extract_page("<h1>Hello</h1>")["title"] == "Hello"


def test_empty_page_has_safe_fallbacks():
    page = extract_page("")
    assert page == {"title": "Untitled", "desc": "", "h1": "", "content": ""}


def test_ignores_script_and_style_content():
    page = extract_page("<style>bad</style><h1>Good</h1><script>worse</script><p>Text</p>")
    assert "bad" not in page["content"] and "worse" not in page["content"]
    assert "Good" in page["content"] and "Text" in page["content"]


def test_whitespace_is_normalized():
    page = extract_page("<title> A\n B </title><h1> C   D </h1>")
    assert page["title"] == "A B" and page["h1"] == "C D"


def test_content_is_truncated():
    assert extract_page("<p>abcdef</p>", content_limit=4)["content"] == "abc…"

