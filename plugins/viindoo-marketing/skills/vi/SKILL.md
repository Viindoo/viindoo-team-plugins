---
name: vi
description: Sinh nội dung tiếng Việt qua Gemini 2.5 Flash. Dùng khi user gõ /vi <prompt> hoặc cần văn phong tiếng Việt tự nhiên (blog, commit message, README, mô tả PR, email, caption, slogan). KHÔNG dùng cho dịch thuật hay code.
---

# /vi - Sinh nội dung tiếng Việt qua Gemini

Khi skill này được gọi, args là prompt mô tả nội dung cần sinh (bằng tiếng Việt).

## Quy trình

1. Nếu args rỗng: hỏi user nội dung muốn sinh, dừng.
2. Nếu args có ý nói "lưu vào file X" hoặc "ghi ra file X": tách path ra, phần còn lại là prompt nội dung.
3. Chạy Bash: `GEMINI_CLI_TRUST_WORKSPACE=true gemini -m "${GEMINI_VI_MODEL:-gemini-2.5-flash}" -o text -p "<prompt>"`
   - Truyền nguyên prompt tiếng Việt từ args. KHÔNG dịch sang tiếng Anh.
   - Nếu prompt có dấu nháy kép, escape bằng `\"` hoặc dùng heredoc qua stdin.
4. Lấy stdout làm output.
   - Nếu user yêu cầu lưu file: dùng Write tool ghi output vào path, báo path.
   - Nếu không: in output trực tiếp cho user xem.
5. KHÔNG paraphrase, KHÔNG thêm bình luận, KHÔNG dịch lại. Trình bày output Gemini sạch.

## Xử lý lỗi

- Nếu Bash trả non-zero (vd Gemini chưa login, hết quota): báo user lỗi cụ thể và nhắc kiểm tra biến môi trường `GEMINI_API_KEY` (lấy key tại https://aistudio.google.com/apikey) hoặc đổi model qua `GEMINI_VI_MODEL`.
- Nếu output Gemini quá ngắn so với yêu cầu (vd user hỏi 500 chữ mà ra 50 chữ): gọi lại 1 lần với prompt làm rõ độ dài.

## Ví dụ

User: `/vi viết commit message tiếng Việt mô tả việc thêm tính năng login Google`

→ Chạy:
```
GEMINI_CLI_TRUST_WORKSPACE=true gemini -m "${GEMINI_VI_MODEL:-gemini-2.5-flash}" -o text -p "Viết commit message ngắn gọn (1 dòng tiêu đề + 2-3 dòng mô tả) bằng tiếng Việt cho commit thêm tính năng đăng nhập Google. Theo convention: tiêu đề bắt đầu bằng động từ ở thì hiện tại."
```

→ In output trực tiếp.
