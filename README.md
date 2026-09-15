# mona-llms-txt

**Sinh file `llms.txt` cho website để AI hiểu đúng cấu trúc site và trích đúng trang.**
*Generate an `llms.txt` (and `llms-full.txt`) for any website, following the llmstxt.org convention.*

Đây là công cụ GEO mở tách ra từ bộ [MONA GEO OS](https://mona.media/mona-geo-os/). `llms.txt` với AI giống như `robots.txt` với Google: một file gọn ở gốc site, liệt kê các trang quan trọng kèm mô tả, để ChatGPT, Gemini, Claude, Perplexity đọc cấu trúc site nhanh và trích dẫn đúng chỗ thay vì đoán mò.

## Vì sao có bộ này

Website doanh nghiệp Việt phần lớn chưa có `llms.txt`. Model đọc site qua HTML lộn xộn, dễ bỏ sót trang tiền hoặc trích nhầm trang phụ. Một file `llms.txt` viết đàng hoàng giúp AI biết "trang dịch vụ nằm đây, bảng giá nằm kia, blog nằm chỗ này" — tăng khả năng được nhắc tên đúng ngữ cảnh. Tool này đọc sitemap của anh chị, rút title + mô tả từng trang, gom theo nhóm, rồi dựng ra file chuẩn.

## Chạy thử

```bash
git clone https://github.com/themonagroup/mona-llms-txt
cd mona-llms-txt
python examples/demo.py                     # demo offline từ fixture

# Sinh llms.txt thật từ sitemap của site anh chị:
python -m mona-llms-txt https://your-site.com/sitemap.xml -o llms.txt
python -m mona-llms-txt https://your-site.com/sitemap.xml --full -o llms-full.txt
```

Flag: `--full` nhồi thêm nội dung trang (bản đầy đủ), `--max-pages N` giới hạn số trang, `-o` chỉ nơi lưu (không có thì in ra màn hình).

## Dùng như thư viện

```python
from mona_llms_txt import generate, build_llms_txt

# end-to-end từ sitemap
txt = generate("https://your-site.com/sitemap.xml", full=False)

# hoặc tự dựng từ danh sách trang (hàm thuần, test được không cần mạng)
txt = build_llms_txt("Tên site", "Mô tả site", pages=[
    {"url": "https://s.com/dich-vu/seo", "title": "Dịch vụ SEO", "desc": "...", "section": "dich-vu"},
])
```

## Nó xử lý được

- Đọc `sitemap.xml`, kể cả **sitemap index lồng nhau** (một index trỏ nhiều sitemap con).
- Rút `title`, meta description, `h1` từ HTML bằng thư viện chuẩn Python (không cần bs4).
- Gom URL theo nhánh path đầu (`/blog/`, `/dich-vu/`…) thành từng section.
- Dựng đúng format llms.txt: `# Tiêu đề` → `> mô tả` → các mục `## Section` → `- [Trang](URL): mô tả`.

```bash
pip install -e . && pytest -q     # 41 test, chạy offline, không gọi mạng trong test
```

Python >=3.9, ưu tiên thư viện chuẩn.

## Dữ liệu

Fixture test là HTML/sitemap **tự soạn**, không có dữ liệu site khách thật. Phần fetch mạng được tách riêng và inject được, nên test chạy hoàn toàn offline.

## Tuyên ngôn thị trường cùng tiến

MONA là một công ty phần mềm, chuyển đổi số, chuyển đổi AI, nhưng trên hết, MONA là một công ty dịch vụ B2B, là người hưởng lợi trực tiếp từ việc: **những doanh nghiệp Việt càng thành công, MONA càng có lợi**. Thị trường đi xuống, đi chậm, công nghệ yếu mới chính là điểm giết chết các cơ hội làm ăn trong tương lai của MONA. Nên, hơn ai hết, MONA mong muốn, và MONA thật sự can thiệp vào việc giúp đỡ anh chị thành công. Và chuyển đổi AI là chìa khóa cho sự thành công đó của chúng ta.

## Từ đâu ra

Một mảnh của [MONA GEO OS](https://mona.media/mona-geo-os/) — bộ công cụ để website được ChatGPT, Gemini, Claude nhắc tên. Muốn kiểm site đã cho AI vào đọc chưa thì xem [mona-ai-crawler-check](https://github.com/themonagroup/mona-ai-crawler-check). Toàn bộ kho mở của MONA ở [MONA Open](https://mona.media/mona-open/); chuyên mục test model ở [MONA AI Lab](https://mona.media/ai-lab/); tác giả [Khánh Hùng — Founder The MONA](https://mona.media/profile/vy-nguyen-khanh-hung/).

Giấy phép: [MIT](LICENSE).
