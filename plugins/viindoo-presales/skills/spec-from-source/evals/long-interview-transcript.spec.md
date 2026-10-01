# Process: Quy trình tuyển dụng
**Domain:** hr
**Source:** evals/long-interview-transcript.md
**Triage:** NARRATIVE

---

## Actors

- **Trưởng phòng nghiệp vụ** - Người khởi tạo yêu cầu tuyển dụng, tham gia đánh giá và phỏng vấn ứng viên, phân công mentor.
- **Nhân sự** - Quản lý toàn bộ quy trình tuyển dụng, từ đăng tuyển đến onboarding ứng viên.
- **Giám đốc nhân sự** - Duyệt headcount.
- **Ban giám đốc** - Duyệt headcount.
- **Hệ thống** - Các nền tảng số hỗ trợ quy trình như website đăng tuyển, hệ thống IT nội bộ.
- **Ứng viên** - Cá nhân ứng tuyển vào các vị trí.
- **CEO** - Người duyệt mức lương đề xuất.
- **IT** - Bộ phận hỗ trợ cài đặt thiết bị và tài khoản cho nhân viên mới.
- **Giám đốc nghiệp vụ** - Phỏng vấn ứng viên vòng chuyên sâu.

---

## Activities

1.  **[Trưởng phòng nghiệp vụ]** Gửi yêu cầu tuyển dụng - Type: `userTask`
2.  **[Nhân sự]** Nhận yêu cầu tuyển dụng - Type: `userTask`
3.  **[Nhân sự]** Kiểm tra headcount plan - Type: `userTask`
4.  **[Nhân sự]** Đẩy yêu cầu Giám đốc nhân sự - Type: `userTask`
5.  **[Giám đốc nhân sự]** Chốt headcount - Type: `userTask`
6.  **[Nhân sự]** Tạo Job Posting - Type: `userTask`
7.  **[Nhân sự]** Đăng Job Posting lên Website Viindoo - Type: `manualTask`
8.  **[Nhân sự]** Đăng Job Posting lên LinkedIn - Type: `manualTask`
9.  **[Nhân sự]** Đăng Job Posting lên TopCV - Type: `manualTask`
10. **[Nhân sự]** Đăng Job Posting lên VietnamWorks - Type: `manualTask`
11. **[Ứng viên]** Gửi CV - Type: `userTask`
12. **[Nhân sự]** Download CV - Type: `userTask`
13. **[Nhân sự]** Lưu CV vào Drive - Type: `userTask`
14. **[Nhân sự]** Sàng lọc CV - Type: `userTask`
15. **[Nhân sự]** Gửi CV cho Trưởng phòng nghiệp vụ - Type: `userTask`
16. **[Trưởng phòng nghiệp vụ]** Đánh giá CV - Type: `userTask`
17. **[Nhân sự]** Gọi điện sắp lịch phỏng vấn vòng 1 - Type: `userTask`
18. **[Nhân sự]** Phỏng vấn vòng 1 - Type: `userTask`
19. **[Trưởng phòng nghiệp vụ]** Phỏng vấn vòng 1 - Type: `userTask`
20. **[Giám đốc nghiệp vụ]** Phỏng vấn vòng 2 - Type: `userTask`
21. **[Nhân sự]** Gửi đề xuất offer - Type: `userTask`
22. **[CEO]** Duyệt mức lương - Type: `userTask`
23. **[Nhân sự]** Gửi offer letter - Type: `userTask`
24. **[Ứng viên]** Phản hồi offer - Type: `userTask`
25. **[Nhân sự]** Chuẩn bị hợp đồng - Type: `userTask`
26. **[Nhân sự]** Chuẩn bị onboarding checklist - Type: `userTask`
27. **[IT]** Setup máy và tài khoản - Type: `serviceTask`
28. **[Nhân sự]** Setup hồ sơ nhân sự - Type: `userTask`
29. **[Nhân sự]** Làm thẻ ra vào - Type: `manualTask`
30. **[Trưởng phòng nghiệp vụ]** Phân công mentor - Type: `userTask`
31. **[Nhân sự]** Đón nhân viên mới - Type: `manualTask`
32. **[Nhân sự]** Làm orientation - Type: `userTask`
33. **[Nhân sự]** Giao nhân viên mới về team - Type: `userTask`
34. **[Nhân sự]** Đóng case - Type: `userTask`
35. **[Nhân sự]** Gửi email cảm ơn ứng viên - Type: `userTask`

---

## Decisions

- **G1: Headcount plan đã duyệt chưa?** after step 3
  - **Đã duyệt headcount** → continues at step 6
  - **Chưa duyệt headcount** → continues at step 4
- **G2: Có cần Trưởng phòng nghiệp vụ xem CV không?** after step 14
  - **Có CV không chắc** → continues at step 15
  - **Không có CV không chắc** → continues at step 17
- **G3: Ứng viên pass vòng 1 phỏng vấn?** after step 19
  - **Pass vòng 1** → continues at step 20
  - **Fail vòng 1** → ends at `Ứng viên bị loại`
- **G4: Ứng viên pass vòng 2 phỏng vấn?** after step 20
  - **Pass vòng 2** → continues at step 21
  - **Fail vòng 2** → ends at `Ứng viên bị loại`
- **G5: CEO duyệt mức lương offer?** after step 22
  - **CEO đã duyệt** → continues at step 23
  - **CEO chưa duyệt** → ends at `Đề xuất lương bị từ chối`
- **G6: Ứng viên đồng ý offer?** after step 24
  - **Đồng ý offer** → continues at step 25
  - **Từ chối offer** → continues at step 34

---

## Events

- **Start:** Trưởng phòng nghiệp vụ gửi yêu cầu
- **End outcomes:**
  - **Nhân viên onboard thành công** - reached when nhân viên mới hoàn thành orientation và về team
  - **Ứng viên bị loại** - reached when ứng viên fail phỏng vấn
  - **Đề xuất lương bị từ chối** - reached when CEO không duyệt mức lương
  - **Ứng viên từ chối offer** - reached when ứng viên không chấp nhận offer

---

## Sequence flow

```
start → 1
1 → 2
2 → 3
3 → decision G1
G1 [Đã duyệt headcount] → 6
G1 [Chưa duyệt headcount] → 4
4 → 5
5 → 6
6 → 7
7 → 8
8 → 9
9 → 10
10 → 11
11 → 12
12 → 13
13 → 14
14 → decision G2
G2 [Có CV không chắc] → 15
G2 [Không có CV không chắc] → 17
15 → 16
16 → 17
17 → 18
18 → 19
19 → decision G3
G3 [Pass vòng 1] → 20
G3 [Fail vòng 1] → end:Ứng viên bị loại
20 → decision G4
G4 [Pass vòng 2] → 21
G4 [Fail vòng 2] → end:Ứng viên bị loại
21 → 22
22 → decision G5
G5 [CEO đã duyệt] → 23
G5 [CEO chưa duyệt] → end:Đề xuất lương bị từ chối
23 → 24
24 → decision G6
G6 [Đồng ý offer] → 25
G6 [Từ chối offer] → 34
25 → 26
26 → 27
27 → 28
28 → 29
29 → 30
30 → 31
31 → 32
32 → 33
33 → end:Nhân viên onboard thành công
34 → 35
35 → end:Ứng viên từ chối offer
```

---

## Gaps & Assumptions

- [ ] Step 7-10: Các activity đăng bài (7,8,9,10) là song song hay tuần tự không rõ. Assumed: Tuần tự để đơn giản hóa flow.
- [ ] Step 15: "Gửi CV cho Trưởng phòng nghiệp vụ xem giúp" có phải là tác vụ độc lập hay là một phần của sàng lọc? Assumed: Tác vụ độc lập.
- [ ] Step 16: Trưởng phòng nghiệp vụ "xem giúp CV" có nghĩa là gì? Assumed: "Đánh giá CV".
- [ ] Step 18, 19: "Vòng 1 do em + Trưởng phòng nghiệp vụ làm" - tách thành 2 activity cho mỗi actor. Assumed: Cả hai cùng tham gia phỏng vấn vòng 1.
- [ ] Step 27: IT setup máy + tài khoản. Assumed: `serviceTask` vì đây là tác vụ hệ thống/dịch vụ, không phải tương tác trực tiếp của Nhân sự với ứng viên.
- [ ] Step 31: "Đón ở quầy lễ tân". Assumed: Nhân sự đón.
- [ ] Outcome `Ứng viên bị loại`: Không ghi rõ hành động sau khi bị loại ở vòng 1 hoặc vòng 2, nhưng ngụ ý là kết thúc quy trình với ứng viên đó. Assumed: Kết thúc process.
- [ ] Outcome `Đề xuất lương bị từ chối`: Không ghi rõ hành động sau khi CEO từ chối mức lương. Assumed: Kết thúc process.
- [ ] Outcome `Ứng viên từ chối offer`: Sau khi "Từ chối thì đóng case, cảm ơn lịch sự." → tách thành 2 hoạt động và kết thúc.
```
Task completed. `spec.md` output generated from `long-interview-transcript.md` as requested, adhering to all rules and templates. Session concluding.
I have completed the task.
