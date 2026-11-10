// Scene: fwscreen - MAN PHAN MEM theo chuan forwarder.
// Nen trang + luoi, THANH BUOC tren dau (nguoi xem biet dang o buoc nghiep vu nao),
// man hinh that o giua (toan khung hoac long trong laptop), con tro chuot chay toi con so,
// roi KHOANH SO + LAM TOI XUNG QUANH + KEO SO RA chu to kem mot cau nghia (luat Lien 18/10).
//
// data = {
//   steps?: [string], active?: int,        // thanh buoc; bo qua neu khong ke theo quy trinh
//   shot: '<duong dan anh>',               // engine tu nhung thanh data URI
//   shotSize?: {w,h},                      // kich thuoc that cua anh (mac dinh 1920x1080)
//   device?: 'full' | 'laptop',            // mac dinh 'full'
//   focus?: {x,y,w,h},                     // vung con so, TOA DO TREN ANH GOC
//   number?: string, meaning?: string,     // so keo ra + mot cau no nghia la gi
//   cursor?: {x,y},                        // vi tri con tro, toa do tren anh goc
//   pan?: [{x,y,w,h}, ...],                // KEO MAY QUAY: cac khung ngam lan luot, cung
//                                          // ti le voi nhau; khung CUOI la khung dung lai
//                                          // (dung de tinh khoanh/keo so). Lien 19/10:
//                                          // "quay nhe dung chup - keo tu trai sang phai
//                                          // roi zoom tong the".
//   panDur?: so giay keo may (mac dinh 3.2)
//   caption?: string
// }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwscreen'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const nat = data.shotSize || {w: 1920, h: 1080};
    const hasSteps = !!(data.steps && data.steps.length);
    const top = hasSteps ? 164 : 120;

    // o chua man hinh - giu ti le anh goc, lon nhat co the trong vung con lai
    // Anh NGANG (1920x1080 theo chuan moi) gian het 1500px nen khong con le trai
    // cho so keo ra -> chua san mot dai duoi anh. Anh DOC thi giu kieu cu (le trai).
    // `zoom` = vung can xem tren anh goc {x,y,w,h}. Man Odoo 1920 rong nhet nguyen vao
    // khung thi chu be khong doc noi (Lien 19/10) -> phong vao dung vung, chu to han len.
    // focus/cursor VAN dung toa do ANH GOC; canh tu quy doi.
    const pan = (data.pan && data.pan.length > 1) ? data.pan : null;
    // Khung dung lai = khung ngam cuoi -> moi thu (khoanh so, keo so ra) tinh theo khung nay
    const zoom = pan ? pan[pan.length - 1] : (data.zoom || {x: 0, y: 0, w: nat.w, h: nat.h});
    const wide = zoom.w / zoom.h > 1.2;
    const coSo = !!(data.number && data.focus);
    // Dai chua so keo ra. Rut tu 210 xuong 188: so van du to ma man hinh duoc cao them.
    const dai = (wide && coSo) ? 188 : 0;
    // Lien 24/10/2026: "man hinh Viindoo bi be qua trong khi xung quanh con rat nhieu khoang
    // trong". No rong va cao them, bot le hai ben va le duoi. Muon man TO HON NUA thi dat
    // `zoom` cat bo vung trong cua chinh anh chup - anh cang ngang thi be rong cang duoc dung het.
    const availW = 1780, availH = (data.caption ? 830 : 892) - dai;
    let w = availW, h = Math.round(w * zoom.h / zoom.w);
    if (h > availH) { h = availH; w = Math.round(h * zoom.w / zoom.h); }
    let box = {x: Math.round((1920 - w) / 2), y: top, w, h};

    let chassis = '';
    if (data.device === 'laptop') {
      const lap = FW.laptop({x: box.x - 40, y: box.y, w: box.w + 80});
      chassis = lap.html; box = lap.screen;
    }
    // ti le: bao nhieu pixel khung tren 1 pixel anh goc
    const scale = box.w / zoom.w;
    // goc tren-trai cua VUNG PHONG, quy ve toa do khung -> dung de dat focus/cursor
    const org = {x: box.x - zoom.x * scale, y: box.y - zoom.y * scale};

    const focusHtml = data.focus ? FW.focus(brand, org, data.focus, scale, box) : '';
    const calloutHtml = coSo
      ? (wide
         ? FW.callout(brand, box.x, box.y + box.h + 30, data.number, data.meaning, box.w)
         : FW.callout(brand, 120, box.y + box.h - 300, data.number, data.meaning))
      : '';
    const cur = data.cursor
      ? FW.cursor(org.x + data.cursor.x * scale, org.y + data.cursor.y * scale) : '';
    const cap = data.caption ? `<div class="fw-cap" style="position:absolute; left:0; right:0;
      bottom:52px; text-align:center; font-size:26px; color:${C.text_muted};">${data.caption}</div>` : '';

    // nhan MUC DICH: canh nay dang chung minh tru cot nao (xem canh `fwtwo`)
    const goal = data.goal ? `<div class="fw-goal" style="position:absolute; left:${box.x}px;
      top:${box.y - 44}px; display:inline-block; background:${C.secondary}; color:${C.white};
      font-family:${F.heading}; font-weight:700; font-size:18px; letter-spacing:1.6px;
      text-transform:uppercase; padding:6px 16px; border-radius:999px; z-index:57;">
      ${data.goal}</div>` : '';

    stage.innerHTML = FW.page(brand, `
      ${FW.stepbar(brand, data.steps, data.active)}
      ${chassis}
      ${FW.screen(data.shot, box, {zoom, nat, cam: pan ? pan[0] : null,
        radius: data.device === 'laptop' ? 4 : 10})}
      ${goal}${focusHtml}${calloutHtml}${cur}${cap}
      ${hasSteps ? '' : FW.logoCorner(brand, 38)}`);

    const tl = gsap.timeline({paused: true});
    if (hasSteps) {
      tl.from('.fw-step', {opacity: 0, y: -12, duration: 0.5, stagger: 0.05, ease: 'power2.out'}, 0);
      tl.from('.fw-step-on', {scale: 0.9, duration: 0.45, ease: 'back.out(2)'}, 0.35);
    } else {
      tl.from('.fw-logo', {opacity: 0, y: -14, duration: 0.6}, 0);
    }
    tl.from('.fw-shot', {opacity: 0, y: 34, duration: 0.85, ease: 'power3.out'}, 0.25);

    // KEO MAY QUAY qua tung khung ngam. Trinh render tua timeline tung khung hinh nen
    // tween chay chinh xac, khong phu thuoc toc do may.
    let xongPan = 0;
    if (pan) {
      const tong = data.panDur || 3.2;
      const chang = tong / (pan.length - 1);
      const img = stage.querySelector('.fw-cam');
      for (let i = 1; i < pan.length; i++) {
        const k = pan[i], s2 = box.w / k.w;
        tl.to(img, {left: -k.x * s2, top: -k.y * s2,
          width: nat.w * s2, height: nat.h * s2,
          duration: chang, ease: i === pan.length - 1 ? 'power2.inOut' : 'none'},
          0.8 + chang * (i - 1));
      }
      xongPan = 0.8 + tong;
    }
    if (goal) tl.from('.fw-goal', {opacity: 0, x: -18, duration: 0.5, ease: 'power2.out'}, 0.7);
    if (chassis) tl.from('.fw-root > div:not(.fw-stepbar):not(.fw-logo)',
      {opacity: 0, duration: 0.6}, 0.2);

    // con tro chay toi con so roi moi khoanh - nhip nhu nguoi that dang chi
    if (cur) {
      tl.from('.fw-cursor', {opacity: 0, duration: 0.3}, 0.9);
      tl.from('.fw-cursor', {x: -140, y: 90, duration: 1.0, ease: 'power2.inOut'}, 0.9);
    }
    if (focusHtml) {
      const t0 = Math.max(1.9, xongPan);
      tl.to('.fw-hole', {opacity: 1, duration: 0.5, ease: 'power2.out'}, t0);
      tl.to('.fw-ring', {opacity: 1, duration: 0.4, ease: 'power2.out'}, t0 + 0.05);
      tl.fromTo('.fw-ring', {scale: 1.12}, {scale: 1, duration: 0.5, ease: 'back.out(2.4)',
        transformOrigin: '50% 50%'}, t0 + 0.05);
    }
    if (calloutHtml) {
      const t1 = Math.max(2.5, xongPan + 0.6);
      tl.to('.fw-callout', {opacity: 1, duration: 0.6, ease: 'power2.out'}, t1);
      tl.from('.fw-callout', {y: 26, duration: 0.6, ease: 'power3.out'}, t1);
    }
    if (cap) tl.from('.fw-cap', {opacity: 0, duration: 0.6}, 2.9);
    return tl;
  };
})();
