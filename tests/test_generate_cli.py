from pathlib import Path
import subprocess
import sys

import pytest

from mona_llms_txt import generate
from mona_llms_txt.cli import main


def fake_docs():
    return {
        "map.xml": "<urlset><url><loc>https://x.test/</loc></url><url><loc>https://x.test/blog/a</loc></url></urlset>",
        "https://x.test/": "<title>Site X</title><meta name='description' content='About X'><h1>Home</h1>",
        "https://x.test/blog/a": "<title>Article</title><h1>Article H1</h1><p>Details</p>",
    }


def test_generate_end_to_end_with_injected_loader():
    result = generate("map.xml", loader=fake_docs().__getitem__)
    assert result.startswith("# Site X\n\n> About X")
    assert "## blog" in result and "[Article]" in result


def test_generate_full_adds_body():
    result = generate("map.xml", full=True, loader=fake_docs().__getitem__)
    assert "Nội dung:" in result


def test_generate_honors_max_pages():
    result = generate("map.xml", max_pages=1, loader=fake_docs().__getitem__)
    assert "Article" not in result


def test_generate_rejects_negative_limit():
    with pytest.raises(ValueError):
        generate("map.xml", max_pages=-1, loader=fake_docs().__getitem__)


def test_cli_writes_output(tmp_path, monkeypatch):
    monkeypatch.setattr("mona_llms_txt.cli.generate", lambda *a, **k: "# Done\n")
    output = tmp_path / "llms.txt"
    assert main(["map.xml", "-o", str(output)]) == 0
    assert output.read_text() == "# Done\n"


def test_cli_prints_stdout(monkeypatch, capsys):
    monkeypatch.setattr("mona_llms_txt.cli.generate", lambda *a, **k: "# Done\n")
    assert main(["map.xml"]) == 0
    assert capsys.readouterr().out == "# Done\n"


def test_module_help_runs():
    proc = subprocess.run([sys.executable, "-m", "mona_llms_txt", "--help"], text=True, capture_output=True)
    assert proc.returncode == 0
    assert "sitemap URL or local XML file" in proc.stdout

