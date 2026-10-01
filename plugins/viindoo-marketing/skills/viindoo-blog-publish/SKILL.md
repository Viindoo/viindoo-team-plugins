---
name: viindoo-blog-publish
description: Đăng bài blog song ngữ (tiếng Anh gốc + tiếng Việt) lên website viindoo.com (Odoo 17) ở dạng nháp, từ bản nháp tiếng Việt và ảnh tác giả gửi. Tối ưu nội dung nhưng giữ giọng tác giả, kiểm chứng mọi tính năng Viindoo qua mã nguồn, viết bản EN, chạy Auto Translate rồi ghi đè bản VI đã biên tập, SEO hai ngôn ngữ, ảnh theo từng ngôn ngữ, ảnh bìa, khối bài viết liên quan. Dùng skill này bất cứ khi nào người dùng muốn đăng / đưa / up bài lên blog hoặc website Viindoo, làm tiếp một bài trong chuỗi bài (ví dụ chuỗi "Từ dữ liệu đến Kaizen"), dịch bài blog sang song ngữ, hoặc gắn ảnh / SEO / bài liên quan cho một bài blog trên viindoo.com, kể cả khi người dùng chỉ dán nội dung và nói "đăng bài này".
---

# Đăng blog song ngữ lên viindoo.com

Tác giả gửi bản nháp tiếng Việt (có thể kèm ảnh trong `~/Downloads`). Kết quả là một bài **nháp** song ngữ trên viindoo.com, sạch tới mức tác giả chỉ cần đọc lại rồi bấm Publish. Trao đổi bằng tiếng Việt.

Sự thật về hệ thống (id website, blog, attachment ảnh có sẵn, phạm vi tính năng đã rà, bẫy riêng của site) nằm ở `references/site-facts.md`. Đọc file đó trước; nếu có mâu thuẫn thì dữ liệu sống trên viindoo.com là chuẩn, và cập nhật lại file.

## Cổng bắt buộc: rà mã nguồn trước khi viết (không được bỏ)

Chưa rà mã nguồn thì chưa được viết câu nào về tính năng. Blog là tài liệu bán hàng công khai; hứa sai tính năng sẽ thành vấn đề khi khách mua, nên tuyệt đối không được bịa.

1. **Lập bảng kê claim:** liệt kê mọi câu trong bản nháp (và mọi câu agent định viết thêm) khẳng định hoặc ngụ ý Viindoo làm được điều gì, kể cả câu chung chung như "hệ thống giúp theo dõi…", câu trong FAQ và chú thích ảnh.
2. **Rà từng claim trên Viindoo 17:** giao cho agent `viindoo-presales:viindoo-source-explorer` nếu đã cài plugin viindoo-presales (hoặc tự dùng OSM `describe_module` / `check_module_exists` / `model_inspect` và grep `${VIINDOO_SRC:-~/viindoo}/17.0`, bỏ qua repo `customer-*`). Kết quả từng dòng: **Có sẵn / Cần cấu hình / Chỉ có dữ liệu thô, chưa có báo cáo / Không có**, kèm tên module (tên hiển thị) và file:line làm bằng chứng.
3. **Viết theo kết quả:**
   - "Có sẵn": viết bình thường, nêu tên app.
   - "Cần cấu hình" hoặc "chỉ có dữ liệu": viết đúng mức, ví dụ "dữ liệu có sẵn để phân tích" hoặc "cần dựng báo cáo tổng hợp".
   - "Không có": bỏ câu đó hoặc chuyển thành việc doanh nghiệp tự làm. Tuyệt đối không ngụ ý phần mềm làm.
4. **Báo cáo** những câu đã sửa hoặc bỏ vì không đúng với mã nguồn, để tác giả biết bản đăng khác bản nháp ở đâu và vì sao.
5. **Chuẩn tới từng chi tiết, cho mọi bài ("tất cả các bài phải chuẩn").** Đúng tên module thôi là chưa đủ: phải đúng cả *phạm vi* của tính năng. Ví dụ đã gặp ở bài 5:
   - Điểm kiểm soát chất lượng chỉ chọn được sản phẩm, nhóm sản phẩm và loại hoạt động, **không** chọn được công đoạn.
   - "Không đi tiếp nếu không đạt" chỉ chặn phiếu kho; ở sản xuất chỉ chặn khi *chưa* kiểm tra.
   - QR chỉ chạy qua máy quét, không có xử lý riêng.

   Câu nào cũng phải khớp mã nguồn tới mức đó, nếu không thì viết hẹp lại cho đúng. Sau khi dựng spec, rà lại **toàn bộ** văn bản cuối một lượt nữa (kể cả danh sách, FAQ, chú thích ảnh, khối giới thiệu bài sau) trước khi báo xong. Không để tác giả phải hỏi "đã rà chưa".

## Kết quả phải đạt (hợp đồng)

1. **Nội dung:** giữ giọng và ý của tác giả. Chỉ tối ưu cấu trúc, SEO, độ mạch lạc và độ chính xác, không viết lại theo văn phong máy. Mọi câu về tính năng phải đi qua cổng rà mã nguồn ở trên. Trong văn xuôi dùng tên hiển thị của app (ví dụ "Manufacturing Progress Management"), không dùng tên kỹ thuật. Số liệu minh họa phải ghi "(ví dụ minh họa)".
1b. **Ảnh minh họa phần mềm phải là ảnh chụp màn hình thật.** Infographic do AI vẽ (Codex, ChatGPT) chỉ dùng làm minh họa khái niệm. Nếu trong ảnh có "màn hình Viindoo" do AI vẽ (dashboard, bảng, form giả), không dùng như ảnh sản phẩm: như vậy là hứa tính năng bằng hình. Nguồn ảnh thật:
   - attachment có sẵn trên viindoo.com (xem `references/site-facts.md`);
   - ảnh trong `static/description/` của module ở `${VIINDOO_SRC:-~/viindoo}/17.0`;
   - ảnh tài liệu `viindoo.com/documentation/17.0/_images/`.

   Ảnh ghép gợi ý bố cục (contact sheet) chỉ là gợi ý, không đăng.
   Ảnh chụp trong `static/description` thường có khổ 3200x2000 và thừa một vùng trống lớn phía dưới (danh sách ngắn, form ít trường, khung mô tả để trống). Trước khi upload, cắt bỏ phần trống ở đáy: giữ tới hàng cuối cùng còn nội dung, cộng thêm khoảng 60 px lề, cắt luôn khung "Description" nếu để trống. Sau đó thu về rộng 1400 px.
1c. **Bố cục phải gọn, chuyên nghiệp như các bài hay nhất trên web** (ví dụ "Đánh giá Mức độ Trưởng thành Số" 2529, "Flat Organization" 2480). Không dồn cả bài vào một khối văn bản; kiểu này bị chê là "các đoạn nối vào nhau, không rõ ràng". `build_post.py` tự tách mỗi `h2` thành một section riêng và thêm đường phân cách `s_hr` giữa các section. Agent chọn block theo nội dung:
   - Nhóm 2-6 ý song song (loại hoạt động, câu hỏi kiểm tra, các mức, dữ liệu dùng lại) dùng `cards`: thẻ `s_three_columns` có viền xanh.
   - Chuỗi bước hay vòng lặp (A → B → C) dùng `steps`: `s_process_steps` có icon Font Awesome và đường nối.
   - Câu thông điệp chính dùng `quote`: `s_blockquote` kiểu classic.
   - Lưu ý hoặc cảnh báo dùng `alert` (info, warning hoặc success). Phần "Bài tiếp theo" cũng đặt trong alert info.
   - FAQ dùng `faq`: `s_faq_collapse`, bấm để mở.

   Bài 2566 là mẫu đầu tiên dựng theo bố cục này, xem `references/redesign-example.py`. Bài cũ còn dạng một khối thì dựng lại bằng cách biến đổi spec tương tự: chữ giữ nguyên, sau đó gắn lại bản VI.
2. **Hai ngôn ngữ:** bản EN là ngôn ngữ gốc của website, agent tự viết bằng tiếng Anh tự nhiên. Bản VI là bản của tác giả đã biên tập, **không phải** bản Google dịch. Hai bản giữ cấu trúc từng đoạn tương ứng 1:1 để ghép bản dịch theo từng đoạn.
3. **Tính năng Auto Translate** (module `viin_website_auto_translation_blog`) vẫn được chạy vì cần dùng đúng tính năng của website. Chạy xong thì ghi đè bản VI từng đoạn.
4. **SEO cho cả hai ngôn ngữ, đạt chuẩn SEO Advisor của web** (`viin_website_seo_advisor_blog`, xem điểm ở `seo_percentage` và chi tiết ở `analyze_detail`; bài 2563 đạt 85% EN / 79% VI). Auto Translate không dịch các trường này nên phải tự ghi bản VI. Những gì cần có:
   - `focus_keyphrase` (có dịch), dài 20-40 ký tự, không trùng từ khóa của bài khác.
   - Meta title 50-60 ký tự, từ khóa nằm trong khoảng 25 ký tự đầu.
   - Meta description 50-155 ký tự, từ khóa nằm trong 120 ký tự đầu.
   - Slug chứa từ khóa (bản VI so sánh sau khi bỏ dấu).
   - Đoạn văn đầu tiên (sapo) chứa từ khóa trong 120 ký tự đầu.
   - Mật độ từ khóa 0,3-0,5%: số lần cụm từ khóa xuất hiện chia cho tổng số từ.
   - Có heading 2 và alt ảnh chứa từ khóa (một vài cái là đủ, không nhồi).
   - Mọi ảnh có alt, kể cả ảnh trong khối CTA.
   - Số ảnh ít nhất 0,3% tổng số từ. Bản VI dài hơn nên dễ thiếu ảnh.
   - Ít nhất 1 liên kết ngoài (ví dụ Wikipedia theo từng ngôn ngữ) và các liên kết nội bộ.
   - Ngoài ra: `website_meta_og_img` (ảnh chia sẻ mạng xã hội, dùng ảnh bìa), tag có sẵn (`blog.tag`), keywords.

   Chèn từ khóa bằng cách viết lại câu cho tự nhiên, không lặp máy móc.
4b. **Rà trùng trước khi chốt SEO.** Hai bài cùng nhắm một từ khóa *và* cùng một ý định tìm kiếm sẽ tranh nhau thứ hạng (keyword cannibalization). Vì vậy, trước khi chốt từ khóa, tiêu đề và meta:
   - **Tra từ khóa trên web:** tìm `blog.post` (cả bài đã publish lẫn bài nháp) có `focus_keyphrase` hoặc `name` chứa từ khóa định dùng hay các từ lõi của nó (MCP `odoo` `search_records`, lệnh chỉ đọc).
     - Trùng từ khóa mà cùng ý định: đổi sang góc hẹp hơn, đúng câu hỏi riêng của bài.
     - Trùng chữ nhưng khác ý định: được phép, nhưng phải link qua lại giữa hai bài.
   - **Không lấy từ khóa trần quá rộng** ("Kaizen", "ERP", "data entry", "số hóa") làm từ khóa chính. Các từ này đã có bài gốc hoặc bài khác trong chuỗi chiếm (xem bảng dưới).
   - **Tiêu đề, meta title, meta description, slug** không được gần giống bài nào khác trong chuỗi. Mở đầu mỗi tiêu đề bằng ý riêng của bài.
   - **Không lặp nguyên câu, nguyên đoạn giữa các bài** (nội dung trùng lặp): câu hỏi đáp (FAQ), đoạn kết về Viindoo, khung giới thiệu bài sau. Ý giống nhau thì viết lại theo góc của bài đó.
   - **Bài gốc về Kaizen trên site là 809 "What is Kaizen?"** (`/blog/business-management-3/what-is-kaizen-809`). Chưa ra lệnh đổi link Wikipedia ở bài đã public; bài mới cân nhắc link nội bộ về bài này.
   - **Báo cáo:** các bài có từ khóa gần nhất, và vì sao bài mới không tranh chấp với chúng.

   Từ khóa đã dùng trong chuỗi "Từ dữ liệu đến Kaizen" (EN / VI):

   | Bài | Post | Từ khóa |
   |---|---|---|
   | 1 | 2563 | Kaizen and digitalization |
   | 2 | 2564 | the flow of work |
   | 3 | 2565 | ERP and Kaizen |
   | 4 | 2566 | data entry |
   | 5 | 2567 | management value / giá trị quản trị |
   | 6 | 2568 | Minimum Management Backbone / xương sống quản trị tối thiểu |
   | 7 | 2569 | level of data detail / độ chi tiết dữ liệu |
   | 8 | 2570 | ERP flexibility for SMEs / tính linh hoạt của SME |
   | 9 | 2571 | standardize before you automate / chuẩn hóa trước khi tự động hóa |
   | 10 | 2572 | AI in Kaizen and ERP / AI trong Kaizen và ERP |

   Bài cũ của site: 809 "what is kaizen", 2089 "Kaizen in Manufacturing", các bài lean 1321, 1406, 1512.
5. **Ảnh:** mỗi ảnh có alt và chú thích ở cả hai ngôn ngữ. Nếu có ảnh riêng cho EN/VI thì gắn theo ngôn ngữ (qua `src`, nhờ module `viin_website_multilingual_multimedia`). Ảnh bìa nên là ảnh **không có chữ**, vì tiêu đề sẽ đè lên trên; infographic nhiều chữ để ở thân bài. Ảnh nào chưa có thì bỏ qua và ghi vào báo cáo, không tự bịa.
6. **Số liệu trong bài phải khớp số liệu trong infographic.** Đọc từng ảnh; lệch thì hỏi tác giả nên sửa bài hay làm lại ảnh.
7. **Cuối bài:** khối "Bài viết liên quan" gồm 3-5 bài đã publish, chọn đúng chủ đề (tìm theo từ khóa trên `blog.post`, lấy `website_url` và tên VI). Sau đó là khối CTA sẵn có của site ("CTA Blogs - Transform your business").
8. **Không bao giờ publish.** Giữ `is_published = False`; tác giả tự bấm Publish.
9. **Kiểm tra trước khi báo xong:** không còn đoạn nào là bản Google dịch; trang EN không lọt chữ tiếng Việt; không có dấu gạch dài (U+2012 đến U+2015); mọi ảnh tải được; mở trang thật (`/en/...` và `/vi/...`) và chụp màn hình phần đầu bài.

## Công cụ

- **Ghi dữ liệu:** gọi JSON-RPC (`/web/dataset/call_kw`) từ phiên trình duyệt chrome-devtools mà người dùng đã đăng nhập. Không dùng MCP `odoo` để ghi nội dung lớn: mỗi lần ghi phải preview, validate rồi execute với nguyên payload, còn các hàm dịch thì bị chặn theo policy. MCP `odoo` vẫn tiện cho các lệnh **đọc** (`search_records`, `read_record`).
- Nếu trình duyệt mở ra trang login, nhờ người dùng đăng nhập **trong cửa sổ Chrome do agent điều khiển**. Cửa sổ này dùng profile riêng, không chung đăng nhập với Chrome thường của người dùng. Agent không nhập mật khẩu.
- **Nạp file từ máy lên trình duyệt:** chèn `<input type=file>` vào trang, dùng `upload_file`, rồi đọc bằng FileReader. `upload_file` chỉ nhận đường dẫn trong thư mục home (ví dụ `~/Downloads`), không nhận thư mục scratchpad `/private/tmp`. Cách này dùng cho cả ảnh lẫn file JSON bảng đối chiếu, để khỏi phải dán hàng chục KB vào lệnh.
- **Đoạn mã dùng lại:** `references/rpc-snippets.md` gồm hàm gọi RPC, tạo bài, upload ảnh, chạy Auto Translate, ghi đè VI, đặt ảnh bìa, kiểm tra.
- **Dựng nội dung:** `python3 ${CLAUDE_SKILL_DIR}/scripts/build_post.py <spec.json> [thư mục ra]` nhận một file spec JSON (các khối đoạn văn, bảng, danh sách, ảnh, bài liên quan, mỗi khối có cả EN lẫn VI). Kết quả gồm HTML bản EN, bảng đối chiếu EN→VI (kể cả `src` ảnh theo ngôn ngữ), meta SEO và file giá trị để tạo bài. Xem đầu file script để biết định dạng spec.

## Trình tự gợi ý

Đây là trình tự đã chạy được ở bài 2563; đổi thứ tự thoải mái miễn đạt hợp đồng ở trên.

1. Đọc bản nháp và các ảnh. Kiểm chứng tính năng Viindoo. Soát số liệu giữa bài và ảnh.
2. Viết spec (EN + VI song song) rồi chạy `build_post.py`. Kiểm tra số chữ, không có dấu gạch dài, độ dài meta.
3. Upload ảnh, lấy URL dạng `/web/image/<id>-<checksum8>/<tên file>`, điền vào spec rồi build lại. Tìm bài liên quan.
4. Tạo bài EN (context `lang=en_US`, `is_published=False`, tác giả là partner của người đăng, hỏi nếu chưa biết).
5. Chạy Auto Translate (khoảng 35 giây).
6. Ghi đè VI: nội dung theo từng đoạn, sau đó các trường name, subtitle và SEO.
7. Đặt ảnh bìa.
8. Kiểm tra, chụp màn hình, báo cáo.

## Sửa bài đã tạo

- **Luôn sửa bản gốc tiếng Anh trước**, sau đó chạy lại Auto Translate của website để đồng bộ, rồi mới ghi đè bản VI đã biên tập từng đoạn. Không sửa riêng bản VI. Như vậy hai bản luôn cùng một cấu trúc.
- **Không sửa lại bài đã publish** (bố cục, ảnh, chữ), trừ khi người dùng yêu cầu đích danh bài đó. Nâng cấp bố cục chỉ áp dụng cho bài nháp và bài mới.
- Sau Auto Translate, chữ nằm trong link (tiêu đề bài liên quan, link giữa câu) bị tách thành đoạn dịch riêng và nhận bản Google, có khi dịch sai. Luôn gắn lại tiêu đề VI của các bài liên quan và đọc lại khối "Bài viết liên quan".

## Bẫy đã gặp

- **`update_field_translations` trên trường html (Odoo 17)** tra khóa theo **đoạn đang có ở ngôn ngữ đích**, tức là bản Google sau khi Auto Translate, không tra theo đoạn gốc EN. Ghép bằng cách: so văn bản thuần của `source` với bảng đối chiếu, rồi dùng `value || source` làm khóa. Đoạn nào ô dịch còn trống mới rơi về tra theo gốc. Sau khi ghi, đọc lại để chắc số đoạn còn là bản Google bằng 0.
- Nếu đoạn gốc được bọc trọn trong `<strong>`/`<em>` mà bản VI không có, thì bọc lại cho bản VI.
- **Sửa nội dung EN sau khi đã dịch:** ghi EN xong phải gắn lại bản VI cho các đoạn vừa sửa, nếu không bản VI sẽ còn chữ cũ hoặc câu dịch máy.
- **Thay ảnh ở bản EN sau khi đã dịch:** nếu ô dịch `src` của ảnh ở bản VI còn trống, bản VI đang hiện theo ảnh EN, nên thay ảnh EN là bản VI đổi theo. Trước khi ghi EN, lưu lại bản VI hiện tại của `src`, alt và chú thích. Ghi EN xong thì gắn lại chúng cho bản VI. Chú thích nằm trọn trong `<em>` nên đoạn dịch gồm cả thẻ `<em>`: tra theo văn bản thuần của `source`, không tra theo innerHTML, và giữ `<em>` trong bản VI.
- **Đoạn văn có link `<a>`** (kể cả khi link ở đầu câu) thường bị website tách thành nhiều mảnh dịch: phần trước link, chữ trên link, `href`, phần sau link. Khi đó bảng đối chiếu nguyên câu không khớp, dẫn tới bản VI bị lặp chữ hoặc giữ chữ tiếng Anh. Sau khi ghi, liệt kê các mảnh `unmatched` rồi gắn bản VI cho từng mảnh; `href` Wikipedia đổi sang trang `vi.wikipedia.org` nếu có. Đọc lại đoạn VI để chắc không lặp chữ.
- **Trình duyệt tự chuyển sang bản VI** vì cookie ngôn ngữ. Muốn xem bản EN thì mở đường dẫn có tiền tố `/en/`.
- **Auto Translate có thể trả 502** (dịch vụ dịch phía máy chủ, gặp ở bài 6 với khoảng 250 đoạn, thử lại vẫn lỗi).
  - Khi đó ghi thẳng bản VI (ô dịch trống thì khóa là `source`), báo người dùng.
  - **Không** chạy lại Auto Translate sau khi đã ghi VI, vì có thể đè văn của tác giả bằng bản máy dịch.
- **Tiêu đề bài liên quan** hay không ăn trong lượt ghi đè hàng loạt. Luôn gắn riêng một lượt nữa rồi đọc lại.
- **Ảnh tài liệu Viindoo có bản VI riêng:** `https://viindoo.com/documentation/17.0/vi/_images/<tên>.vi.jpg` (bản EN ở `/documentation/17.0/_images/<tên>.en.jpg`).
  - Danh sách trang lấy từ `searchindex.js`.
  - Ảnh trong trang nằm ở thuộc tính `data-src` (tải lười).
- **Gemini** (để chuốt văn tiếng Việt) có thể hết quota miễn phí trong ngày, đổi model qua biến `GEMINI_VI_MODEL` (ví dụ `gemini-3.5-flash-lite`) nếu model mặc định lỗi. Nếu Gemini hỏng thì agent tự biên tập, nhưng phải giữ văn của tác giả.
- **Agent không tự tạo được ảnh.** Muốn có bản EN của infographic tiếng Việt thì cần Codex (tài khoản ChatGPT của người dùng) hoặc người dùng tự tạo. Hỏi trước; nếu người dùng nói bỏ qua thì bỏ qua.

## Báo cáo cuối

Viết bằng tiếng Việt, ngắn gọn: link bài EN và VI (bản nháp), đã làm gì (những chỗ tối ưu nội dung, tính năng đã kiểm chứng, ảnh, SEO, bài liên quan), những gì còn thiếu hoặc cần người dùng quyết (ảnh chưa có, số liệu lệch, câu cần xác nhận). Kết bằng một trạng thái: DONE, DONE_WITH_CONCERNS, BLOCKED hoặc NEEDS_CONTEXT.
