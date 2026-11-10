// fwscreens.js - ban VUONG 1:1 cua canh xuong song `fwscreen`.
//
// Vi sao co canh rieng: `fwscreen` go cung chieu ngang 1920 trong phan tinh bo cuc, con
// duong sinh ban vuong cu cua sequence.mjs chi la letterbox tu 16:9
// (scale=1080:-2,pad=1080:1080) - anh that chi cao 608px giua hai dai trang 236px, chu
// Odoo nho khong doc noi tren dien thoai. Day la cung mot ly do da phai lam `fwscreenv`
// cho khung doc.
//
// Khuon vuong: cau hoi quan tri o tren, man phan mem PHONG THANG VAO VUNG CO CON SO
// (chiem tron chieu ngang khung) o giua, so keo ra chu to o duoi - giong `fwscreenv`
// nhung moi tang thap hon vi khung chi cao 1080 thay vi 1920.
//
// data:
//   shot        duong dan anh (engine tu nhung thanh data URI)
//   shotSize?   he toa do cua anh, mac dinh {w:1920,h:1080}; anh chup CSS 1280x720 thi khai 1280x720
//   focus       {x,y,w,h} vung can khoanh, TOA DO TRONG he shotSize (lay tu shots.json)
//   zoom?       de tay vung cat khi tu dong chon chua dat
//   question?   cau hoi quan tri dat tren dau
//   number?     con so keo ra
//   meaning?    mot cau con so do nghia la gi
//   caption?    dong chan
//   padRatio?   do rong them quanh vung focus khi phong (mac dinh 0.45)
(function () {
  window.SCENES = window.SCENES || {};

  // Lam toi + khoanh, GIOI HAN trong khung anh. FW.focus dung box-shadow lan 9999px nen
  // o khuon vuong no phu toi ca cau hoi va con so nam ngoai anh - ca trang bi xam. Boc
  // trong mot lop overflow:hidden dung bang khung anh thi chi rieng anh bi lam toi.
  function sfocus(brand, box, org, focus, scale, zoom) {
    const C = brand.colors;
    const pad = 10;
    // Kep vung khoanh vao trong vung phong: toa do focus do tren CA buc anh, nen khi canh
    // cat sat mot goc thi vong khoanh cham ra ngoai khung va bi xen - trong nhu loi.
    const f = {x: Math.max(focus.x, zoom.x), y: Math.max(focus.y, zoom.y)};
    f.w = Math.min(focus.x + focus.w, zoom.x + zoom.w) - f.x;
    f.h = Math.min(focus.y + focus.h, zoom.y + zoom.h) - f.y;
    if (f.w <= 0 || f.h <= 0) return '';            // khoanh nam ngoai vung cat
    const fx = org.x + f.x * scale - box.x, fy = org.y + f.y * scale - box.y;
    const fw = f.w * scale, fh = f.h * scale;
    return `<div class="fws-mask" style="position:absolute; left:${box.x}px; top:${box.y}px;
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

  window.SCENES['fwscreens'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts;
    const FW = window.FW;
    const nat = data.shotSize || {w: 1920, h: 1080};

    // ---- VUNG PHONG tinh TRUOC, KHUNG ANH suy ra sau --------------------------
    // Lam nguoc lai (khung co dinh truoc) thi vung khoanh dang nam ngang bi ep vao khung
    // vuong, phai phong rat rong moi du ti le, ket qua la chu Odoo nho lai. Tinh vung
    // phong truoc roi cho khung bam theo dang cua no thi anh luon duoc phong het co.
    const f = data.focus || {x: 0, y: 0, w: nat.w, h: nat.h};
    const padR = data.padRatio != null ? data.padRatio : 0.45;
    // Khung vuong chi cao 1080 nen o anh thap hon ban doc (1010 -> 580). Da thu 440 va
    // PHAI noi len: man nao nhieu dong (bon dong phu thu, sau ho so bo phan) co dang gan
    // vuong, ep vao 440 thi canh phai keo rong vung cat ra het 1280 CSS - chu Odoo tut
    // xuong 11px, dung loi "man hinh qua be" Lien da che. Doi lai, cau hoi va dong nghia
    // phai NGAN: cau hoi toi da hai dong, dong nghia mot dong.
    const boxW = 1000, H_MIN = 200, H_MAX = 580, SLOT_Y = 196;

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
    const box = {x: 40, w: boxW, h: boxH, y: Math.round(SLOT_Y + (H_MAX - boxH) / 2)};

    const scale = box.w / zoom.w;                 // ti le anh sau khi phong
    const org = {x: box.x - zoom.x * scale, y: box.y - zoom.y * scale};

    // ---- cac manh ----------------------------------------------------------------
    const question = data.question ? `<div class="fws-q" style="position:absolute;
      left:44px; right:44px; top:88px; font-family:${F.heading}; font-weight:700;
      font-size:42px; line-height:1.16; color:${C.text_heading};">${data.question}</div>` : '';

    const callout = (data.number || data.meaning) ? `<div class="fws-callout"
      style="position:absolute; left:44px; right:44px; top:${box.y + box.h + 34}px;
      opacity:0; z-index:58;">
      ${data.number ? `<div style="font-family:${F.heading}; font-weight:700;
        font-size:${data.number.length > 17 ? 56 : data.number.length > 12 ? 68 : 86}px;
        line-height:1.05; color:${C.primary}; letter-spacing:-1px;">${data.number}</div>` : ''}
      ${data.meaning ? `<div style="font-size:30px; color:${C.text_heading}; margin-top:14px;
        line-height:1.3; font-weight:500;">${data.meaning}</div>` : ''}</div>` : '';

    const caption = data.caption ? `<div class="fws-cap" style="position:absolute;
      left:44px; right:44px; bottom:34px; text-align:center; font-size:26px;
      font-weight:600; color:${C.primary}; opacity:0;">${data.caption}</div>` : '';

    stage.innerHTML = FW.page(brand, `
      <div class="fws-logo" style="position:absolute; top:36px; left:44px;">
        ${FW.logo(brand, 36)}</div>
      ${question}
      ${FW.screen(data.shot, box, {zoom: zoom, nat: nat, radius: 14})}
      ${sfocus(brand, box, org, f, scale, zoom)}
      ${callout}
      ${caption}
    `);

    // ---- nhip: anh vao -> lam toi + khoanh -> keo so ra -> chan -----------------
    // Canh ngan nhat cua clip ngan khoang 3,2 giay nen moc cuoi (2,7s) van vao kip; canh
    // nao ngan hon nua thi `_dur` cua build_seq co lai, giong `fwcards`.
    const FULL = 2.7;
    const dur = data._dur || FULL;
    const k = Math.min(1, Math.max(0.5, (dur - 0.4) / FULL));
    const at = (t) => +(t * k).toFixed(3);

    const tl = gsap.timeline({paused: true});
    tl.from('.fws-logo', {opacity: 0, duration: 0.5, ease: 'power2.out'}, 0);
    if (data.question) FW.inUp(tl, '.fws-q', at(0.15), {y: 26, d: 0.8});
    tl.from('.fw-shot', {opacity: 0, y: 40, duration: 0.9, ease: 'power3.out'}, at(0.35));
    tl.to('.fw-hole', {opacity: 1, duration: 0.55, ease: 'power2.inOut'}, at(1.5));
    tl.to('.fw-ring', {opacity: 1, duration: 0.45, ease: 'power2.out'}, at(1.6));
    if (data.number || data.meaning)
      tl.to('.fws-callout', {opacity: 1, y: 0, duration: 0.7, ease: 'power3.out'}, at(2.1))
        .from('.fws-callout', {y: 30, duration: 0.7, ease: 'power3.out'}, at(2.1));
    if (data.caption) tl.to('.fws-cap', {opacity: 1, duration: 0.6}, at(2.7));
    return tl;
  };
})();
