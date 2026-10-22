# -*- coding: utf-8 -*-
"""Vi du du lieu BR chay duoc - chep sang work/data.py cua du an roi viet lai noi dung.

Chay thu:
    python3 skills/viindoo-danh-muc-br/scripts/build_br.py \
        skills/viindoo-danh-muc-br/references/vi-du-data.py /tmp/thu-br.xlsx
"""
import os
import sys

KHACH = "Công ty cổ phần Bao bì Mẫu"
TO_CHUC = [KHACH]
GHI_CHU = ("Phương án dùng gói Viindoo Express 400 giờ (2 gói Nâng cao 200 giờ); "
           "phần phát triển thêm nằm ngoài gói, tính riêng.")

XAC_NHAN = [
    {"ma": "XN-01", "ten": "Cách tính giá thành",
     "hieu": [
         "Tài liệu Công ty gửi nêu giá thành gồm nguyên liệu, nhân công và khấu hao máy, "
         "nhưng chưa nêu cách phân bổ khấu hao máy.",
         "Viindoo đề xuất phân bổ khấu hao theo giờ máy chạy của từng lệnh sản xuất - "
         "cách này khớp với số liệu nhật ký máy Công ty đang ghi.",
     ],
     "tich": ["Đồng ý phân bổ theo giờ máy chạy",
              "Phân bổ theo sản lượng thành phẩm",
              "Cách khác - ghi ở ô ý kiến"]},
]

R = [
    {"id": "BR-MH-01",
     "ten": "Đề nghị mua hàng theo mức tồn tối thiểu",
     "ct": "Kho lập đề nghị mua khi vật tư xuống dưới mức tối thiểu.",
     "nv": "Mua hàng", "nhom": "Chuỗi cung ứng",
     "pbd": "Kho vận", "pbs": "Mua hàng",
     "pl": "Cấu hình",
     "gp": ("Phạm vi: gói Viindoo Express 400 giờ. Quy tắc đặt hàng lại sẵn có trong phân hệ kho "
            "(stock.warehouse.orderpoint) tự sinh đề nghị mua theo mức tối thiểu và tối đa; "
            "khai mức cho từng vật tư là xong, không viết code.")},

    {"id": "BR-MH-02",
     "ten": "Duyệt đề nghị mua theo ngưỡng giá trị",
     "ct": "Đề nghị mua trên một ngưỡng giá trị phải có giám đốc duyệt.",
     "dep": "BR-MH-01",
     "nv": "Mua hàng", "nhom": "Chuỗi cung ứng",
     "pbd": "Mua hàng", "pbs": "Ban giám đốc",
     "pl": "Cấu hình",
     "gp": ("Phạm vi: gói Viindoo Express 400 giờ. Phân hệ mua hàng có sẵn ngưỡng duyệt theo giá trị "
            "đơn; khai ngưỡng và người duyệt trong cấu hình.")},

    {"id": "BR-SX-01",
     "ten": "Giá thành theo lệnh sản xuất, có khấu hao máy",
     "ct": "Giá thành từng lệnh gồm nguyên liệu, nhân công và khấu hao máy theo giờ chạy.",
     "nv": "Sản xuất", "nhom": "Sản xuất & Chất lượng",
     "pbd": "Kế toán", "pbs": "Kế toán",
     "pl": "Phát triển",
     "gp": ("Phạm vi: ngoài gói Express - dịch vụ phát triển. Mở rộng trên phân hệ giá thành sản xuất "
            "sẵn có: phần nguyên liệu và nhân công đã có, viết thêm phần phân bổ khấu hao máy theo "
            "giờ chạy lấy từ nhật ký máy. Không dựng đối tượng giá thành song song."),
     "note": "Cách phân bổ khấu hao chờ Công ty xác nhận - xem XN-01.",
     # Gio da chot theo quy tac tinh gia hien hanh (hoi Lien) - plugin khong giu cong thuc gia
     "gio": {"tk": (3, "Expert"), "lt": (12, "Senior"), "qa": (5, "Junior"),
             "tl": (2, "Junior"), "ch": (2, "Senior"), "dt": (2, "Senior")}},

    {"id": "BR-KT-01",
     "ten": "Kết nối hóa đơn điện tử",
     "ct": "Phát hành hóa đơn điện tử ngay từ phần mềm.",
     "nv": "Kế toán", "nhom": "Tài chính & Kế toán",
     "pbd": "Kế toán", "pbs": "Kế toán",
     "pl": "Tích hợp",
     "gp": ("Phạm vi: gói Viindoo Express 400 giờ. Cầu nối hóa đơn điện tử đã có sẵn; "
            "khai tài khoản nhà cung cấp hóa đơn và mẫu số là dùng được.")},

    {"id": "BR-BC-01",
     "ten": "Báo cáo lãi lỗ theo từng đơn hàng",
     "ct": "Ban giám đốc xem lãi lỗ theo từng đơn hàng.",
     "nv": "Báo cáo quản trị", "nhom": "Quản trị & Tuân thủ",
     "pbd": "Ban giám đốc", "pbs": "Ban giám đốc",
     "pl": "Cần làm rõ",
     "gp": ("Cần làm rõ trước khi đưa vào phạm vi: chưa rõ lãi lỗ tính trên giá thành thực tế "
            "hay giá thành định mức, và có phân bổ chi phí bán hàng vào từng đơn không.")},
]
