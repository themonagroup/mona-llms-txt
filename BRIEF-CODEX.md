# BRIEF — build repo `mona-llms-txt` (Python)

Bạn là kỹ sư. Dựng thư viện + CLI Python **chạy thật, có test pass** trong ĐÚNG thư mục hiện tại (`--cd`). KHÔNG hỏi lại. Xong in tóm tắt + kết quả `pytest`.

## Mục tiêu
`mona-llms-txt` = công cụ **sinh file `llms.txt` / `llms-full.txt`** cho website theo chuẩn llmstxt.org, để các AI (ChatGPT/Gemini/Claude/Perplexity) hiểu cấu trúc site + trích đúng trang quan trọng. Đây là công cụ GEO mở tách ra từ bộ MONA GEO OS — phải hữu ích thật.

## Chuẩn llms.txt (bám đúng)
File markdown gồm: `# <Tên site>` → dòng `> <mô tả blockquote>` → vài đoạn ghi chú tuỳ chọn → các mục `## <Section>` chứa list `- [Tiêu đề](URL): mô tả ngắn`. `llms-full.txt` = bản đầy đủ nhồi thêm nội dung/nhiều trang hơn.

## Kiến trúc (stdlib thuần cho core; fetch tách riêng)
```
mona_llms_txt/
  __init__.py        # export build_llms_txt(), generate()
  sitemap.py         # đọc sitemap.xml (kể cả sitemap index lồng nhau) -> list URL
  extract.py         # từ HTML -> title, meta description, h1 (parse bằng html.parser stdlib, KHÔNG bs4)
  grouper.py         # gom URL theo path segment đầu -> section (vd /blog/, /dich-vu/)
  render.py          # dựng chuỗi llms.txt + llms-full.txt đúng format
  fetch.py           # tải URL (urllib/requests) — CÔ LẬP, test KHÔNG gọi mạng (dùng fixture)
  cli.py             # `python -m mona_llms_txt <sitemap_url|file> [--full] [-o llms.txt]`
tests/               # pytest >=24 test: parse sitemap (fixture xml), extract (fixture html),
                     # grouper, render (so khớp chuỗi output mong đợi). KHÔNG network trong test.
fixtures/            # sitemap mẫu, vài html mẫu (tự soạn)
pyproject.toml       # python>=3.9; deps runtime tối thiểu (requests optional, ưu tiên urllib stdlib)
.gitignore
examples/demo.py     # dựng llms.txt từ fixture, in ra
```

## API
- `build_llms_txt(site_title, site_desc, pages: list[dict], *, full=False) -> str` (pages = [{url,title,desc,section}]) — hàm PURE, test được không cần mạng.
- `generate(sitemap_source, *, full=False, max_pages=200) -> str` — pipeline end-to-end (fetch + extract + group + render).

## Test khoá cứng
- Parse sitemap index lồng (1 index trỏ 2 sitemap con) → gộp URL đúng.
- Extract title/meta/h1 từ HTML fixture, kể cả thiếu meta (fallback h1/title).
- Grouper: URL `/blog/a`, `/blog/b`, `/dich-vu/x` → 2 section "blog", "dich-vu".
- Render: output bắt đầu `# Title`, có dòng `> desc`, mỗi section `## `, mỗi trang `- [..](..): ..`.
- `full=True` khác `full=False` (nhồi thêm).

## Ràng buộc
- ⛔️ KHÔNG lộ endpoint/key nội bộ, KHÔNG gọi mạng trong test, KHÔNG dữ liệu khách thật.
- Comment tiếng Việt chỗ khó. README + LICENSE để Claude viết sau (bạn để placeholder 1 dòng).
- `pytest -q` PASS hết (>=24 test). In kết quả cuối.
