// Scene: fwcycle - VONG DOI CUA MOT CHIEC MAY, ve thanh VONG TRON.
//
// Vi sao co canh nay (Lien 24/10/2026): so do dong chay ve thanh duong thang "qua don dieu
// va nhieu khoang trang", va quan trong hon - duong thang ke sai cau chuyen. Mot chiec may
// cho thue KHONG di mot lan roi het: no mua ve, vao doi, cho thue, giao, thu hoi, bao tri,
// roi QUAY LAI cho thue, vong nay sang vong khac cho den khi thanh ly. Ve thanh vong tron
// thi nguoi xem thay ngay suc manh cua su lien ket tren mot giai phap tong the: moi vong
// deu di qua kho, ke toan, tai san va bao tri ma khong phai chep tay chO nao.
//
// data = {
//   kicker?, headline?, sub?,
//   steps: [{label, note?}],     // xep deu quanh vong tron, theo chieu kim dong ho
//   center?: {title, note?},     // chu giua vong
//   bg?: duong dan anh nen,      // anh that, de rat nhat
//   loopLabel?: 'Vòng sau'       // nhan tren mui ten khep vong
// }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwcycle'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const steps = data.steps || [];
    const n = Math.max(steps.length, 1);
    // Vong DET va RONG: nhan dat ngoai vong o dinh va day, neu vong cao qua thi
    // nhan tren de len tieu de va nhan duoi de len dong ket.
    const cx = 960, cy = 646;
    const rx = 712, ry = 212;            // vong det cho vua khung ngang
    const R = 50;                        // ban kinh nut so

    const pos = i => {
      const a = -Math.PI / 2 + (2 * Math.PI * i) / n;   // bat dau tu dinh vong
      return {x: cx + rx * Math.cos(a), y: cy + ry * Math.sin(a), a};
    };

    // Vong ellipse ve bang SVG de mui ten chay dung tren duong cong
    const seg = steps.map((_, i) => {
      const p0 = pos(i), p1 = pos((i + 1) % n);
      const b0 = 2 * Math.PI / n * 0.22;
      const a0 = p0.a + b0, a1 = p1.a - b0;            // chua cho nut so hai dau
      const q = {x: cx + rx * Math.cos(a0), y: cy + ry * Math.sin(a0)};
      const e = {x: cx + rx * Math.cos(a1), y: cy + ry * Math.sin(a1)};
      const mau = (i === n - 1) ? C.secondary : C.primary;   // doan khep vong mau tim
      return `<path class="fw-arc fw-arc-${i}" d="M ${q.x} ${q.y} A ${rx} ${ry} 0 0 1 ${e.x} ${e.y}"
        fill="none" stroke="${mau}" stroke-width="3" stroke-linecap="round" opacity="0"
        marker-end="url(#fwArrow${i === n - 1 ? 'S' : 'P'})"/>`;
    }).join('');

    // Nhan dat RA NGOAI vong theo huong ban kinh - khong bao gio de len tieu de hay len nhau
    const NW = 226, GAP = 78;
    const nut = steps.map((s, i) => {
      const p = pos(i);
      const lx0 = cx + (rx + GAP) * Math.cos(p.a);
      const ly0 = cy + (ry + GAP) * Math.sin(p.a);
      const c = Math.cos(p.a);
      const align = c > 0.3 ? 'left' : (c < -0.3 ? 'right' : 'center');
      const left = align === 'left' ? lx0 : (align === 'right' ? lx0 - NW : lx0 - NW / 2);
      const top = ly0 - (Math.sin(p.a) < -0.3 ? 74 : (Math.abs(Math.sin(p.a)) < 0.3 ? 30 : 0));
      return `
        <div class="fw-nut fw-nut-${i}" style="position:absolute; left:${p.x - R}px;
          top:${p.y - R}px; width:${R * 2}px; height:${R * 2}px; border-radius:50%;
          background:${C.primary}; color:${C.white}; font-family:${F.heading};
          font-weight:700; font-size:28px; display:flex; align-items:center;
          justify-content:center; opacity:0; box-shadow:0 10px 26px rgba(0,187,206,.28);">
          ${i + 1}</div>
        <div class="fw-nhan fw-nhan-${i}" style="position:absolute; left:${left}px;
          top:${top}px; width:${NW}px; text-align:${align}; opacity:0;">
          <div style="font-family:${F.heading}; font-weight:700; font-size:20px;
            letter-spacing:.4px; text-transform:uppercase; color:${C.text_heading};
            line-height:1.2;">${s.label}</div>
          ${s.note ? `<div style="font-size:16px; color:${C.text_muted}; margin-top:4px;
            line-height:1.3;">${s.note}</div>` : ''}
        </div>`;
    }).join('');

    const giua = data.center ? `
      <div class="fw-giua" style="position:absolute; left:${cx - 230}px; top:${cy - 76}px;
        width:460px; text-align:center; opacity:0;">
        <div style="font-family:${F.heading}; font-weight:700; font-size:40px;
          color:${C.primary}; line-height:1.15;">${data.center.title}</div>
        ${data.center.note ? `<div style="font-size:20px; color:${C.text_muted};
          margin-top:12px; line-height:1.35;">${data.center.note}</div>` : ''}
      </div>` : '';

    const bg = data.bg ? `
      <div class="fw-bg" style="position:absolute; inset:0; opacity:0;">
        <img src="${data.bg}" style="position:absolute; inset:0; width:100%; height:100%;
          object-fit:cover; filter:saturate(.5);">
        <div style="position:absolute; inset:0; background:
          linear-gradient(180deg, rgba(255,255,255,.92) 0%, rgba(255,255,255,.975) 40%,
          rgba(255,255,255,.975) 74%, rgba(255,255,255,.90) 100%);"></div>
      </div>` : '';

    stage.innerHTML = FW.page(brand, `
      ${bg}
      ${FW.logoCorner(brand, 38)}
      ${data.kicker ? `<div class="fw-kick" style="position:absolute; top:120px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:700; font-size:22px;
        letter-spacing:3px; text-transform:uppercase; color:${C.primary};">${data.kicker}</div>` : ''}
      ${data.headline ? `<div class="fw-head" style="position:absolute; top:164px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:700; font-size:50px;
        color:${C.text_heading};">${data.headline}</div>` : ''}
      <svg style="position:absolute; inset:0; width:1920px; height:1080px;">
        <defs>
          <marker id="fwArrowP" markerWidth="9" markerHeight="9" refX="7" refY="4.5"
            orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="${C.primary}"/></marker>
          <marker id="fwArrowS" markerWidth="9" markerHeight="9" refX="7" refY="4.5"
            orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="${C.secondary}"/></marker>
        </defs>${seg}
      </svg>
      ${nut}${giua}
      ${data.sub ? `<div class="fw-sub" style="position:absolute; bottom:30px; left:0; right:0;
        text-align:center; font-size:24px; color:${C.text_muted};">${data.sub}</div>` : ''}`);

    const tl = gsap.timeline({paused: true});
    if (data.bg) tl.to('.fw-bg', {opacity: 1, duration: 1.1, ease: 'power2.out'}, 0);
    if (data.kicker) tl.from('.fw-kick', {opacity: 0, y: -14, duration: 0.6}, 0.1);
    if (data.headline) tl.from('.fw-head', {opacity: 0, y: -16, duration: 0.7}, 0.25);
    // Vong chay dan tung doan, nut hien theo - nguoi xem di MOT VONG cung chiec may
    const b = (data.cueTimes && data.cueTimes.length === steps.length) ? data.cueTimes : null;
    steps.forEach((_, i) => {
      const t = b ? b[i] : 0.8 + i * 0.5;
      tl.to(`.fw-nut-${i}`, {opacity: 1, duration: 0.28}, t);
      tl.from(`.fw-nut-${i}`, {scale: 0.4, duration: 0.42, ease: 'back.out(2.2)'}, t);
      tl.to(`.fw-nhan-${i}`, {opacity: 1, duration: 0.32}, t + 0.06);
      tl.to(`.fw-arc-${i}`, {opacity: 0.5, duration: 0.3}, t + 0.18);
    });
    if (data.center) tl.to('.fw-giua', {opacity: 1, duration: 0.8}, '>-0.2');
    if (data.sub) tl.from('.fw-sub', {opacity: 0, duration: 0.6}, '>-0.3');
    return tl;
  };
})();
