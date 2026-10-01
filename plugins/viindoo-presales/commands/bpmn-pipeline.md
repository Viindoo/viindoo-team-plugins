---
description: Chạy pipeline BPMN có checkpoint từ raw doc → 4 deliverable file (.spec.md + .bpmn + .drawio + .html), kèm reviewer gate cuối
---

Chạy pipeline BPMN cho raw doc / file được nhắc trong `$ARGUMENTS` theo flow 4 stage, MỖI stage có checkpoint rõ.

## QUY TẮC CỨNG (không được phá)

1. **KHÔNG được Read file trung gian** (.bpmn / .drawio / .html / spec.md sau khi đã sinh). Chỉ truyền **file path** xuống skill kế tiếp. Lý do: tránh nuốt 20-80KB XML/HTML vào context.
2. **DỪNG sau STAGE 1 và STAGE 2.** Đợi người dùng confirm "ok" / "next" / "tiếp" trước khi qua stage sau. Không tự chạy thẳng.
3. **Validate FAIL → DỪNG, không tự retry.** In punch list, đợi quyết định.
4. **Output mỗi stage ≤ 10 dòng.** Chỉ summary từ stdout của script + path. Không paraphrase, không bình luận.
5. **Workspace mặc định:** `~/Downloads/bpmn-from-spec/<slug>/` - `<slug>` lấy từ tên raw doc hoặc người dùng chỉ định. Tạo folder nếu chưa có.

## STAGE 1 - spec-from-source

Mục tiêu: raw doc → `spec.md` (6 section Actors/Activities/Decisions/Events/Sequence flow/Gaps).

Thao tác:
- Skill `viindoo-presales:spec-from-source` với input là raw doc trong `$ARGUMENTS`.
- Output: `<workspace>/spec.md`.

Khi xong → in path + counts (~N actors, ~M activities) → DỪNG.
Message: "STAGE 1 xong → `<path>`. người dùng review spec.md, gõ 'next' để qua stage 2 hoặc 'edit ...' để sửa."

## STAGE 2 - spec-to-bpmn + bpmn-validate

CHỈ chạy khi người dùng đã confirm.

Thao tác:
- Skill `viindoo-presales:spec-to-bpmn` với input `spec.md`.
- Output: `<workspace>/<slug>.bpmn`.
- Ngay sau đó → Skill `viindoo-presales:bpmn-validate` với input vừa sinh.

Nhánh:
- **Validate PASS** → in 2 dòng "OK spec-to-bpmn: ..." + "OK validate: ...", DỪNG, đợi "next" để qua stage 3.
- **Validate FAIL** → in punch list errors từ stderr (không tóm tắt thêm), DỪNG. KHÔNG tự sửa.

## STAGE 3 - bpmn-to-drawio + bpmn-to-html (parallel)

CHỈ chạy khi người dùng đã confirm stage 2 PASS.

Thao tác (parallel trong 1 message):
- Skill `viindoo-presales:bpmn-to-drawio` → `<workspace>/<slug>.drawio` (palette Viindoo Nasilkmex).
- Skill `viindoo-presales:bpmn-to-html` → `<workspace>/<slug>.html` (self-contained).

Khi xong → in 2 paths + counts → tự chạy tiếp STAGE 4 (reviewer là gate Doer≠Reviewer, không cần confirm nữa).

## STAGE 4 - Reviewer gate

Triệu hồi agent `viindoo-presales:viindoo-deliverable-reviewer` với 4 file: `spec.md`, `<slug>.bpmn`, `<slug>.drawio`, `<slug>.html`. Truyền **path**, không truyền content.

Khi reviewer trả về → in punch list Blocker/Major/Minor đúng nguyên văn. KẾT THÚC.

## Khi gặp lỗi

- Gemini timeout / API fail → in stderr, DỪNG, hỏi người dùng retry hay đổi model.
- File path không tồn tại → DỪNG, hỏi người dùng đường dẫn đúng.
- Skill nào không có sẵn → DỪNG, in tên skill thiếu.

Tuyệt đối KHÔNG: tự sinh nội dung BPMN/spec bằng head (không dùng skill), tự retry validate, tự edit spec.md để pass validate.
