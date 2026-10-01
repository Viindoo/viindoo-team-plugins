# Process: Quy trình xử lý yêu cầu báo giá nhanh

**Domain:** sales
**Source:** evals/short-quote-request.md
**Triage:** NARRATIVE

---

## Actors

- **Khách hàng** - Người yêu cầu báo giá.
- **Nhân viên kinh doanh** - Người xử lý yêu cầu báo giá và tương tác với khách hàng.

---

## Activities

1. **[Khách hàng]** Gửi email yêu cầu báo giá - Type: `manualTask`
2. **[Nhân viên kinh doanh]** Nhận email yêu cầu báo giá - Type: `userTask`
3. **[Nhân viên kinh doanh]** Kiểm tra thông tin yêu cầu - Type: `userTask`
4. **[Nhân viên kinh doanh]** Tạo báo giá trên Viindoo CRM - Type: `userTask`
5. **[Nhân viên kinh doanh]** Phát hành báo giá qua email - Type: `userTask`
6. **[Nhân viên kinh doanh]** Gọi điện khách bổ sung thông tin - Type: `manualTask`
7. **[Nhân viên kinh doanh]** Theo dõi báo giá - Type: `manualTask`

---

## Decisions

- **Thông tin yêu cầu đã đủ?** after step 3
  - **Đủ thông tin** → continues at step 4
  - **Thiếu thông tin** → continues at step 6
- **Khách hàng phản hồi đồng ý?** after step 7
  - **Đồng ý** → ends at `Chuyển sang ký hợp đồng`
  - **Từ chối hoặc im lặng quá 7 ngày** → ends at `Đóng cơ hội`

---

## Events

- **Start:** Khách gửi yêu cầu báo giá
- **End outcomes:**
  - **Chuyển sang ký hợp đồng** - reached when Khách hàng phản hồi đồng ý
  - **Đóng cơ hội** - reached when Khách hàng từ chối hoặc im lặng quá 7 ngày

---

## Sequence flow

```
start → 1
1 → 2
2 → 3
3 → decision G1
G1 [Đủ thông tin] → 4
G1 [Thiếu thông tin] → 6
6 → 3
4 → 5
5 → 7
7 → decision G2
G2 [Đồng ý] → end:Chuyển sang ký hợp đồng
G2 [Từ chối hoặc im lặng quá 7 ngày] → end:Đóng cơ hội
```

---

## Gaps & Assumptions

- [ ] `Decision G1`: Loop back from step 6 (Gọi điện khách bổ sung thông tin) to step 3 (Kiểm tra thông tin yêu cầu) is an assumption based on typical process flow for incomplete information.
- [ ] `Decision G2`: The "theo dõi 3 ngày" and "im lặng quá 7 ngày" are time-based aspects that are implicitly handled by the decision condition.
