// fwcardv.js - the chu DOC 9:16: dung cho cau hoi mo dau va cho man keu goi cuoi short.
//
// Short khong du cho de dung ca bo canh mo bai cua clip tong (noi dau -> the ten -> hai muc
// dich -> dong chay). Mot short chi co ~35 giay, nen mo bang DUNG MOT cau hoi quan tri roi
// vao thang man hinh that - dung luat "so phai sau": mot canh, mot cau hoi, mot con so.
//
// data:
//   kicker?   nhan nho in hoa phia tren (vi du "QUAN TRI NHAN SU")
//   headline  cau hoi hoac cau chot, chu rat to
//   sub?      mot dong phu
//   button?   chu trong nut (co nut thi thanh man keu goi)
//   url?      dia chi web duoi nut
(function () {
  window.SCENES = window.SCENES || {};

  window.SCENES['fwcardv'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts;
    const FW = window.FW;

    const kicker = data.kicker ? `<div class="fwc-kick" style="font-family:${F.heading};
      font-weight:700; font-size:30px; letter-spacing:3px; text-transform:uppercase;
      color:${C.primary}; margin-bottom:34px;">${data.kicker}</div>` : '';

    const sub = data.sub ? `<div class="fwc-sub" style="font-size:44px; line-height:1.4;
      color:${C.text_body}; margin-top:40px; font-weight:500;">${data.sub}</div>` : '';

    const button = data.button ? `<div class="fwc-btn" style="display:inline-block;
      margin-top:64px; background:${C.primary}; color:${C.white}; font-family:${F.heading};
      font-weight:700; font-size:42px; padding:28px 56px; border-radius:999px;
      box-shadow:0 18px 46px rgba(0,187,206,.34);">${data.button}</div>` : '';

    const url = data.url ? `<div class="fwc-url" style="margin-top:38px; font-size:34px;
      color:${C.text_muted};">${data.url}</div>` : '';

    stage.innerHTML = FW.page(brand, `
      <div style="position:absolute; left:72px; right:72px; top:50%;
        transform:translateY(-50%); text-align:${data.button ? 'center' : 'left'};">
        <div class="fwc-logo" style="margin-bottom:${data.button ? 70 : 90}px;">
          ${FW.logo(brand, data.button ? 92 : 56)}</div>
        ${kicker}
        <div class="fwc-head" style="font-family:${F.heading}; font-weight:700;
          font-size:${data.button ? 72 : 82}px; line-height:1.16; color:${C.text_heading};">
          ${data.headline}</div>
        ${sub}${button}${url}
      </div>`);

    // Nhip hieu ung phai VUA trong thoi luong canh. Canh lay thoi luong tu file tieng, co
    // cau ngan chi 1,6 giay - ma bo hieu ung day du mat gan 2 giay, nen nut va dia chi web
    // bi cat ngang. `_dur` do build_seq_shorts.py gui sang; ngan thi co deu moi moc lai.
    const FULL = 1.95;
    const dur = data._dur || FULL;
    const k = Math.min(1, Math.max(0.42, (dur - 0.3) / FULL));
    const at = (t) => +(t * k).toFixed(3);
    const d = (t) => +(t * Math.max(k, 0.6)).toFixed(3);

    const tl = gsap.timeline({paused: true});
    tl.from('.fwc-logo', {opacity: 0, y: 20, duration: d(0.6), ease: 'power3.out'}, 0);
    if (data.kicker) FW.inUp(tl, '.fwc-kick', at(0.2), {y: 20, d: d(0.6)});
    FW.inUp(tl, '.fwc-head', at(0.35), {y: 34, d: d(0.9)});
    if (data.sub) FW.inUp(tl, '.fwc-sub', at(0.75), {y: 26, d: d(0.8)});
    if (data.button) tl.from('.fwc-btn', {opacity: 0, scale: 0.9, duration: d(0.6),
      ease: 'back.out(1.7)'}, at(1.0));
    if (data.url) FW.inUp(tl, '.fwc-url', at(1.3), {y: 18, d: d(0.6)});
    return tl;
  };
})();
