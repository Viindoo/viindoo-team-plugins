// fwscreenv.js - ban DOC 9:16 cua canh xuong song `fwscreen`.
//
// Vi sao co canh rieng: `fwscreen` go cung chieu ngang 1920 trong phan tinh bo cuc, va
// duong sinh ban doc cu cua sequence.mjs chi la letterbox tu 16:9 (scale=1080:-2,pad) nen
// chu Odoo bi nho - kich ban clip HRM muc 7 da ghi "chu nho kho doc".
//
// Canh nay dung cho khung 1080x1920: xep DOC - cau hoi quan tri o tren, man phan mem
// PHONG THANG VAO VUNG CO CON SO (chiem tron chieu ngang khung) o giua, so keo ra chu to
// o duoi. Nho phong vao vung focus nen chu Odoo to hon han ban letterbox.
//
// data:
//   shot        duong dan anh (engine tu nhung thanh data URI)
//   shotSize?   he toa do cua anh, mac dinh {w:1920,h:1080}; anh chup CSS 1280x720 thi khai 1280x720
//   focus       {x,y,w,h} vung can khoanh, TOA DO TRONG he shotSize (lay tu shots.json)
//   question?   cau hoi quan tri dat tren dau
//   number?     con so keo ra
//   meaning?    mot cau con so do nghia la gi
//   caption?    dong chan, thuong la loi keu goi
//   padRatio?   do rong them quanh vung focus khi phong (mac dinh 0.55)
(function () {
  window.SCENES = window.SCENES || {};

  // Lam toi + khoanh, nhung GIOI HAN trong khung anh.
  // FW.focus dung box-shadow lan 9999px nen o khuon doc no phu toi ca cau hoi va con so
  // nam ngoai anh - ca trang bi xam. O day boc trong mot lop overflow:hidden dung bang
  // khung anh, nen chi rieng anh bi lam toi.
  function vfocus(brand, box, org, focus, scale, zoom) {
    const C = brand.colors;
    const pad = 10;
    // Kep vung khoanh vao trong vung phong: toa do focus do tren CA buc anh, nen khi canh
    // cat sat vao mot goc thi vong khoanh se cham ra ngoai khung va bi xen - trong nhu loi.
    const f = {x: Math.max(focus.x, zoom.x), y: Math.max(focus.y, zoom.y)};
    f.w = Math.min(focus.x + focus.w, zoom.x + zoom.w) - f.x;
    f.h = Math.min(focus.y + focus.h, zoom.y + zoom.h) - f.y;
    if (f.w <= 0 || f.h <= 0) return '';            // khoanh nam ngoai vung cat
    const fx = org.x + f.x * scale - box.x, fy = org.y + f.y * scale - box.y;
    const fw = f.w * scale, fh = f.h * scale;
    return `<div class="fwv-mask" style="position:absolute; left:${box.x}px; top:${box.y}px;
      width:${box.w}px; height:${box.h}px; border-radius:14px; overflow:hidden; z-index:54;
      pointer-events:none;">
      <div class="fw-hole" style="position:absolute; left:${fx - pad}px; top:${fy - pad}px;
        width:${fw + pad * 2}px; height:${fh + pad * 2}px; border-radius:8px;
        box-shadow:0 0 0 9999px rgba(12,32,38,.62); opacity:0;"></div>
      <div class="fw-ring" style="position:absolute; left:${fx - pad}px; top:${fy - pad}px;
        width:${fw + pad * 2}px; height:${fh + pad * 2}px; border-radius:8px;
        border:3px solid ${C.primary}; box-shadow:0 0 0 5px rgba(0,187,206,.26);
        opacity:0;"></div></div>`;
  }

  window.SCENES['fwscreenv'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts;
    const FW = window.FW;
    const nat = data.shotSize || {w: 1920, h: 1080};

    // ---- VUNG PHONG tinh TRUOC, KHUNG ANH suy ra sau --------------------------
    // Lam nguoc lai (khung co dinh truoc) thi vung khoanh dang dung bi ep vao khung nam
    // ngang, phai phong rat rong moi du ti le, ket qua la chu Odoo nho lai. Tinh vung
    // phong truoc roi cho khung bam theo dang cua no thi anh luon duoc phong het co.
    // `data.zoom` de de tay khi tu dong chon chua dat (vi du phieu luong rat nhieu cot).
    const f = data.focus || {x: 0, y: 0, w: nat.w, h: nat.h};
    const padR = data.padRatio != null ? data.padRatio : 0.45;
    const boxW = 1000, H_MIN = 280, H_MAX = 1010;

    let zoom;
    if (data.zoom) {
      zoom = Object.assign({}, data.zoom);
    } else {
      let zw = Math.min(nat.w, f.w * (1 + padR));
      let zh = Math.min(nat.h, f.h * (1 + padR * 2.2));
      zoom = {w: zw, h: zh, x: f.x + f.w / 2 - zw / 2, y: f.y + f.h / 2 - zh / 2};
    }
    // khung bam theo dang vung phong, ke trong khoang cho phep
    let boxH = Math.round(boxW / (zoom.w / zoom.h));
    if (boxH < H_MIN || boxH > H_MAX) {
      boxH = Math.max(H_MIN, Math.min(H_MAX, boxH));
      // ke lai vung phong cho dung dang khung, nhung khong vuot ra ngoai anh
      const want = boxW / boxH;
      if (zoom.w / zoom.h > want) {
        const nz = Math.min(nat.h, zoom.w / want);
        zoom.y -= (nz - zoom.h) / 2; zoom.h = nz; zoom.w = nz * want;
      } else {
        const nz = Math.min(nat.w, zoom.h * want);
        zoom.x -= (nz - zoom.w) / 2; zoom.w = nz; zoom.h = nz / want;
      }
      boxH = Math.round(boxW / (zoom.w / zoom.h));
    }
    zoom.x = Math.max(0, Math.min(zoom.x, nat.w - zoom.w));
    zoom.y = Math.max(0, Math.min(zoom.y, nat.h - zoom.h));
    const box = {x: 40, w: boxW, h: boxH, y: Math.round(430 + (1010 - boxH) / 2)};

    const scale = box.w / zoom.w;                 // ti le anh sau khi phong
    const org = {x: box.x - zoom.x * scale, y: box.y - zoom.y * scale};

    // ---- cac manh ----------------------------------------------------------------
    const question = data.question ? `<div class="fwv-q" style="position:absolute;
      left:56px; right:56px; top:188px; font-family:${F.heading}; font-weight:700;
      font-size:62px; line-height:1.18; color:${C.text_heading};">${data.question}</div>` : '';

    const callout = (data.number || data.meaning) ? `<div class="fwv-callout"
      style="position:absolute; left:56px; right:56px; top:${box.y + box.h + 70}px;
      opacity:0; z-index:58;">
      ${data.number ? `<div style="font-family:${F.heading}; font-weight:700;
        font-size:${data.number.length > 17 ? 88 : data.number.length > 12 ? 108 : 132}px;
        line-height:1.04; color:${C.primary}; letter-spacing:-1px;">${data.number}</div>` : ''}
      ${data.meaning ? `<div style="font-size:42px; color:${C.text_heading}; margin-top:22px;
        line-height:1.32; font-weight:500;">${data.meaning}</div>` : ''}</div>` : '';

    const caption = data.caption ? `<div class="fwv-cap" style="position:absolute;
      left:56px; right:56px; bottom:84px; text-align:center; font-size:36px;
      font-weight:600; color:${C.primary}; opacity:0;">${data.caption}</div>` : '';

    stage.innerHTML = FW.page(brand, `
      <div class="fwv-logo" style="position:absolute; top:62px; left:56px;">
        ${FW.logo(brand, 46)}</div>
      ${question}
      ${FW.screen(data.shot, box, {zoom: zoom, nat: nat, radius: 14})}
      ${vfocus(brand, box, org, f, scale, zoom)}
      ${callout}
      ${caption}
    `);

    // ---- nhip: anh vao -> lam toi + khoanh -> keo so ra -> chan -----------------
    const tl = gsap.timeline({paused: true});
    tl.from('.fwv-logo', {opacity: 0, duration: 0.5, ease: 'power2.out'}, 0);
    if (data.question) FW.inUp(tl, '.fwv-q', 0.15, {y: 30, d: 0.8});
    tl.from('.fw-shot', {opacity: 0, y: 46, duration: 0.9, ease: 'power3.out'}, 0.35);
    tl.to('.fw-hole', {opacity: 1, duration: 0.55, ease: 'power2.inOut'}, 1.5);
    tl.to('.fw-ring', {opacity: 1, duration: 0.45, ease: 'power2.out'}, 1.6);
    if (data.number || data.meaning)
      tl.to('.fwv-callout', {opacity: 1, y: 0, duration: 0.7, ease: 'power3.out'}, 2.1)
        .from('.fwv-callout', {y: 34, duration: 0.7, ease: 'power3.out'}, 2.1);
    if (data.caption) tl.to('.fwv-cap', {opacity: 1, duration: 0.6}, 2.7);
    return tl;
  };
})();
