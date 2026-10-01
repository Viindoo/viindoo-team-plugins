# Process: Quy trình bán hàng - mẫu smoke test

**Domain:** generic
**Source:** evals/sales-4step.spec.md
**Triage:** SPEC_CLEAN

---

## Actors

- **Khách hàng** - bên mua, gửi yêu cầu báo giá
- **Nhân viên kinh doanh** - bên bán, xử lý và phát hành báo giá

---

## Activities

1. **[Khách hàng]** Gửi yêu cầu báo giá - Type: `userTask`
2. **[Nhân viên kinh doanh]** Duyệt & phát hành báo giá - Type: `userTask`

---

## Decisions

(không có decision trong process này)

---

## Events

- **Start:** Khách có nhu cầu
- **End outcomes:**
  - **Báo giá đã gửi** - reached when nhân viên kinh doanh phát hành báo giá thành công

---

## Sequence flow

```
start → 1
1 → 2
2 → end:Báo giá đã gửi
```

---

## Gaps & Assumptions

(file mẫu - không có gap)
