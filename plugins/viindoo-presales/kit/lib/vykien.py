# -*- coding: utf-8 -*-
"""O y kien va phieu xac nhan - khach doc tai lieu tren trinh duyet, danh dau va ghi y kien ngay tren trang.

Trinh duyet giu noi dung tren may khach (localStorage); khach bam mot nut la in ra PDF phieu y kien
gom (1) y kien theo tung phan, (2) cac diem da xac nhan, (3) tong hop - roi gui lai cho Viindoo.

Nguyen tac noi dung cua moi diem xac nhan:
  Viindoo NEU CACH HIEU VA DE XUAT cua minh kem can cu, khach chi tich dong y hay ghi y kien.
  KHONG hoi lai tu dau nhung gi da doc duoc tu tai lieu khach gui.
  CHI dua vao day cau hoi ma cau tra loi LAM DOI giai phap, pham vi goi hay chi phi.
"""
from __future__ import annotations

import html
import os

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
esc = html.escape


def css() -> str:
    with open(os.path.join(KIT, "css", "y-kien.css"), encoding="utf-8") as f:
        return f.read()


def js(khoa: str, khach: str) -> str:
    """JS tu luu + dung phieu y kien. `khoa` la tien to localStorage rieng cho moi du an."""
    return (_JS.replace("{{KHOA}}", khoa).replace("{{KHACH}}", khach.replace('"', "'")))


# ----------------------------------------------------------------- cac khoi HTML
def mo_dau(de_lam_gi, co_xac_nhan: bool = True, bo_tai_lieu=(), dang_doc: str = "") -> str:
    """Ghi chu dau tai lieu: tai lieu nay de lam gi, o y kien de lam gi.

    `bo_tai_lieu` la list (so, ten) - chi liet ke khi dot nay gui tu hai tai lieu tro len,
    va khong dan chieu sang tai lieu chua gui.
    """
    o = ['<div class="mdau">', "<h3>Tài liệu này để làm gì</h3><ul>"]
    o += [f"<li>{d}</li>" for d in de_lam_gi]
    o.append("</ul>")
    if len(bo_tai_lieu) > 1:
        o.append('<div class="bo">')
        o += [f'<span class="{"day" if s == dang_doc else ""}">{esc(s)}. {esc(t)}</span>' for s, t in bo_tai_lieu]
        o.append("</div>")
    o.append("<h3>Ô ý kiến ở cuối mỗi phần để làm gì</h3><ul>")
    o += [
        "<li><b>Cách dùng:</b> mở tệp này bằng trình duyệt, đánh dấu và ghi ý kiến ngay trên trang. "
        "Trình duyệt giữ lại nội dung trên máy của Công ty, mở lại tệp vẫn còn.</li>",
        "<li>Chỗ nào Viindoo <b>hiểu chưa đúng</b>, Công ty sửa lại ở ô ý kiến cuối phần đó.</li>",
        "<li>Chỗ nào Công ty muốn <b>thêm, bớt hoặc điều chỉnh nhu cầu</b>, ghi vào cùng ô - "
        "Viindoo cập nhật phạm vi trong bản kế tiếp.</li>",
    ]
    if co_xac_nhan:
        o.append("<li>Phần cuối tài liệu có các điểm Viindoo đã nêu <b>cách hiểu và đề xuất</b> của mình; "
                 "Công ty chỉ cần đánh dấu vào dòng phù hợp.</li>")
    o.append("<li>Điền xong, bấm <b>In phiếu ý kiến ra PDF</b> ở cuối tài liệu rồi gửi tệp PDF đó cho Viindoo.</li>")
    o.append("</ul></div>")
    return "\n".join(o)


def y_kien(ma: str, nhan: str, khach: str, dong: int = 4) -> str:
    """O y kien dat o CUOI MOI PHAN tai lieu."""
    return (f'<div class="ykien" data-nhan="{esc(nhan)}">'
            f"<b>Ý kiến của {esc(khach)} về phần {esc(nhan)}</b>"
            '<p class="tt">Chỗ nào chưa đúng hoặc Công ty muốn điều chỉnh, ghi vào đây.</p>'
            f'<textarea rows="{dong}" data-xnkey="YK-{ma}" '
            'placeholder="Ví dụ: phần này đúng rồi; hoặc chỗ này chúng tôi làm khác, cụ thể là..."></textarea></div>')


def thanh_nut(nhac: str = "") -> str:
    """Thanh nut xuat phieu y kien - dat o cuoi phan xac nhan va o cuoi tai lieu."""
    nhac = nhac or ("Đánh dấu và ghi ý kiến trực tiếp trên trang. Trình duyệt giữ lại nội dung trên máy của Công ty. "
                    "Điền xong, Công ty bấm In phiếu ý kiến ra PDF rồi gửi tệp PDF đó cho Viindoo.")
    return ('<div class="xnbar">'
            '<button type="button" class="xnbtn xn-in">In phiếu ý kiến ra PDF</button>'
            '<button type="button" class="xnbtn phu xn-xoa">Xoá hết</button>'
            f'<span class="xntt xn-tt">{esc(nhac)}</span>'
            "</div>")


def khoi_xac_nhan(diem) -> str:
    """Muc 'Nhung diem can Cong ty xac nhan'.

    `diem` la list dict: {"ma","ten","hieu":[...],"tich":[...]}
      hieu = cach hieu va de xuat cua Viindoo kem can cu (gach dau dong, loi de hieu)
      tich = cac dong khach tich chon
    """
    o = [thanh_nut()]
    for x in diem:
        o.append(f'<div class="xn" id="{x["ma"]}">')
        o.append(f'<h4><span class="brc">{esc(x["ma"])}</span> {esc(x["ten"])}</h4>')
        o.append('<p class="xnl">Viindoo hiểu và đề xuất</p><ul>')
        o += [f"<li>{esc(d)}</li>" for d in x["hieu"]]
        o.append("</ul>")
        o.append('<p class="xnl">Đề nghị Công ty xác nhận - đánh dấu vào ô phù hợp</p><ul class="tick">')
        for n, t in enumerate(x["tich"], start=1):
            o.append(f'<li><label><input type="checkbox" data-xnkey="{x["ma"]}-{n}"> <span>{esc(t)}</span></label></li>')
        o.append("</ul>")
        o.append('<div class="cmt"><b>Ý kiến của Công ty</b>'
                 f'<textarea rows="5" data-xnkey="{x["ma"]}-y" '
                 'placeholder="Công ty ghi ý kiến, điều kiện hoặc thông tin bổ sung ở đây"></textarea></div>')
        o.append("</div>")
    return "\n".join(o)


def dong_xlsx(diem) -> list:
    """Dong cho sheet 'Điểm cần xác nhận' trong workbook BR: (ma, ten, hieu_gop, dong_tich)."""
    out = []
    for x in diem:
        hieu = "\n".join("- " + d for d in x["hieu"])
        for t in x["tich"]:
            out.append((x["ma"], x["ten"], hieu, t))
    return out


_JS = """
<script>
(function () {
  var KHOA = "{{KHOA}}-xn-", NL = String.fromCharCode(10), KHACH = "{{KHACH}}";
  function bao(t) { document.querySelectorAll(".xn-tt").forEach(function (e) { e.textContent = t; }); }
  function luu(o) {
    try { localStorage.setItem(KHOA + o.dataset.xnkey, o.type === "checkbox" ? (o.checked ? "1" : "") : o.value); } catch (e) {}
    bao("Đã lưu trên máy của Công ty lúc " + new Date().toLocaleTimeString("vi-VN"));
  }
  document.querySelectorAll("[data-xnkey]").forEach(function (o) {
    try {
      var v = localStorage.getItem(KHOA + o.dataset.xnkey);
      if (v) { if (o.type === "checkbox") o.checked = true; else o.value = v; }
    } catch (e) {}
    if (o.tagName === "TEXTAREA") {
      var g = document.createElement("div");
      g.className = "in-cmt";
      g.textContent = o.value;
      o.parentNode.insertBefore(g, o.nextSibling);
      o.xnGuong = g;
    }
    o.addEventListener(o.type === "checkbox" ? "change" : "input", function () {
      if (o.xnGuong) o.xnGuong.textContent = o.value;
      luu(o);
    });
  });

  function esc(t) {
    return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function doan(t) { return esc(t).split(NL).join("<br>"); }

  function dungPhieu() {
    var ten = (document.querySelector("h1") || {}).textContent || "Tài liệu";
    var h = [];
    h.push("<!doctype html><html lang=vi><head><meta charset=utf-8>");
    h.push("<title>Phiếu ý kiến - " + esc(KHACH) + "</title>");
    h.push("<style>");
    h.push("body{font-family:Arial,Helvetica,sans-serif;color:#21272B;max-width:900px;margin:28px auto;padding:0 20px;line-height:1.6}");
    h.push("h1{font-size:22px;margin:0 0 4px;color:#007f8c}h2{font-size:16px;margin:26px 0 8px;border-bottom:2px solid #00BBCE;padding-bottom:4px}");
    h.push(".dau{font-size:13px;color:#5B6770;margin:0 0 18px}");
    h.push(".k{border:1px solid #E3E6E8;border-left:4px solid #7F4282;border-radius:8px;padding:10px 14px;margin:10px 0;page-break-inside:avoid}");
    h.push(".k b{font-size:14px}.chon{margin:6px 0 0;padding-left:18px;font-size:14px}.chon li{margin:3px 0}");
    h.push(".yk{margin:8px 0 0;font-size:14px;background:#F7FDFD;border:1px dashed #9AA5AD;border-radius:6px;padding:8px 10px;white-space:pre-wrap}");
    h.push(".tr{color:#8A6800;font-size:13px}table{width:100%;border-collapse:collapse;font-size:13.5px}");
    h.push("td,th{border:1px solid #E3E6E8;padding:7px 9px;text-align:left;vertical-align:top}th{background:#F2F7F8}");
    h.push("</style></head><body>");
    h.push("<h1>Phiếu ý kiến của " + esc(KHACH) + "</h1>");
    h.push("<p class=dau>Tài liệu: " + esc(ten) + " · Ghi lúc " + esc(new Date().toLocaleString("vi-VN")) +
           " · Gửi lại phiếu này cho Viindoo</p>");

    var yk = [];
    document.querySelectorAll(".ykien").forEach(function (b) {
      var v = ((b.querySelector("textarea") || {}).value || "").trim();
      if (v) yk.push("<div class=k><b>" + esc(b.dataset.nhan) + "</b><div class=yk>" + doan(v) + "</div></div>");
    });
    h.push("<h2>1. Ý kiến theo từng phần tài liệu</h2>");
    h.push(yk.length ? yk.join("") : "<p class=tr>Công ty chưa ghi ý kiến ở phần nào.</p>");

    var xn = [], soChon = 0;
    document.querySelectorAll(".xn").forEach(function (b) {
      var chon = [];
      b.querySelectorAll("input[type=checkbox]").forEach(function (i) {
        if (i.checked) { chon.push(esc(i.closest("label").innerText.trim())); soChon++; }
      });
      var v = ((b.querySelector("textarea") || {}).value || "").trim();
      if (!chon.length && !v) return;
      var r = "<div class=k><b>" + esc(b.querySelector("h4").innerText.trim()) + "</b>";
      if (chon.length) r += "<ul class=chon><li>" + chon.join("</li><li>") + "</li></ul>";
      else r += "<p class=tr>Chưa đánh dấu lựa chọn nào.</p>";
      if (v) r += "<div class=yk>" + doan(v) + "</div>";
      xn.push(r + "</div>");
    });
    h.push("<h2>2. Các điểm Công ty đã xác nhận</h2>");
    h.push(xn.length ? xn.join("") : "<p class=tr>Công ty chưa đánh dấu điểm xác nhận nào.</p>");
    h.push("<h2>3. Tổng hợp</h2><table><tr><th>Nội dung</th><th>Số lượng</th></tr>");
    h.push("<tr><td>Phần tài liệu có ý kiến</td><td>" + yk.length + "</td></tr>");
    h.push("<tr><td>Điểm xác nhận đã trả lời</td><td>" + xn.length + "</td></tr>");
    h.push("<tr><td>Dòng lựa chọn đã đánh dấu</td><td>" + soChon + "</td></tr></table>");
    h.push("</body></html>");
    return h.join(NL);
  }

  document.querySelectorAll(".xn-in").forEach(function (n) {
    n.addEventListener("click", function () {
      var f = document.getElementById("xn-khung-in");
      if (f) f.remove();
      f = document.createElement("iframe");
      f.id = "xn-khung-in";
      f.style.cssText = "position:fixed;right:0;bottom:0;width:0;height:0;border:0";
      document.body.appendChild(f);
      var d = f.contentWindow.document;
      d.open(); d.write(dungPhieu()); d.close();
      f.contentWindow.focus();
      setTimeout(function () { f.contentWindow.print(); }, 250);
      bao("Hộp thoại in đã mở - Công ty chọn Lưu thành PDF.");
    });
  });

  document.querySelectorAll(".xn-xoa").forEach(function (n) {
    n.addEventListener("click", function () {
      if (!confirm("Xoá toàn bộ lựa chọn và ý kiến đã ghi trên máy này?")) return;
      document.querySelectorAll("[data-xnkey]").forEach(function (o) {
        if (o.type === "checkbox") o.checked = false; else o.value = "";
        if (o.xnGuong) o.xnGuong.textContent = "";
        try { localStorage.removeItem(KHOA + o.dataset.xnkey); } catch (e) {}
      });
      bao("Đã xoá hết.");
    });
  });
})();
</script>
"""
