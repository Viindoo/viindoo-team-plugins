// fwcards.js - the chu VUONG 1:1: dung cho cau hoi mo dau va man keu goi cuoi clip ngan.
//
// Vi sao co canh rieng chu khong letterbox tu 16:9: duong sinh ban vuong cu cua
// sequence.mjs chi la `scale=1080:-2,pad=1080:1080` - chu bi nho lai con 56% va hai dai
// trang chiem gan mot nua khung. Clip ngan xem tren dien thoai nen chu phai to.
//
// Khung vuong thap hon khung doc 9:16 gan mot nua (1080 so voi 1920), nen moi manh deu
// nho hon ban doc mot bac: logo 42, tieu de 62, phu 34. Giu nguyen nhip hieu ung cua
// `fwcardv` de bo clip ngan nghe-nhin lien mach voi bo short doc da duyet.
//
// data:
//   kicker?   nhan nho in hoa phia tren
//   headline  cau hoi hoac cau chot, chu rat to
//   sub?      mot dong phu
//   button?   chu trong nut (co nut thi thanh man keu goi, chu can giua)
//   url?      dia chi web duoi nut
//   _dur?     thoi luong canh (giay) - build_seq gui sang de co nhip hieu ung cho vua
(function () {
  window.SCENES = window.SCENES || {};

  window.SCENES['fwcards'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts;
    const FW = window.FW;
    const mid = !!data.button;                   // man ket thi can giua

    const kicker = data.kicker ? `<div class="fwc-kick" style="font-family:${F.heading};
      font-weight:700; font-size:24px; letter-spacing:2.6px; text-transform:uppercase;
      color:${C.primary}; margin-bottom:24px;">${data.kicker}</div>` : '';

    const sub = data.sub ? `<div class="fwc-sub" style="font-size:34px; line-height:1.4;
      color:${C.text_body}; margin-top:28px; font-weight:500;">${data.sub}</div>` : '';

    const button = data.button ? `<div class="fwc-btn" style="display:inline-block;
      margin-top:46px; background:${C.primary}; color:${C.white}; font-family:${F.heading};
      font-weight:700; font-size:34px; padding:22px 44px; border-radius:999px;
      box-shadow:0 14px 36px rgba(0,187,206,.34);">${data.button}</div>` : '';

    const url = data.url ? `<div class="fwc-url" style="margin-top:26px; font-size:27px;
      color:${C.text_muted};">${data.url}</div>` : '';

    stage.innerHTML = FW.page(brand, `
      <div style="position:absolute; left:64px; right:64px; top:50%;
        transform:translateY(-50%); text-align:${mid ? 'center' : 'left'};">
        <div class="fwc-logo" style="margin-bottom:${mid ? 48 : 60}px;">
          ${FW.logo(brand, mid ? 70 : 42)}</div>
        ${kicker}
        <div class="fwc-head" style="font-family:${F.heading}; font-weight:700;
          font-size:${mid ? 56 : 62}px; line-height:1.17; color:${C.text_heading};">
          ${data.headline}</div>
        ${sub}${button}${url}
      </div>`);

    // Nhip hieu ung phai VUA trong thoi luong canh - cau chot cua clip ngan co khi chi
    // 1,6 giay, de nguyen nhip day du thi nut keu goi bi cat ngang. Lay nguyen cach co
    // deu cua `fwcardv`.
    const FULL = 1.95;
    const dur = data._dur || FULL;
    const k = Math.min(1, Math.max(0.42, (dur - 0.3) / FULL));
    const at = (t) => +(t * k).toFixed(3);
    const d = (t) => +(t * Math.max(k, 0.6)).toFixed(3);

    const tl = gsap.timeline({paused: true});
    tl.from('.fwc-logo', {opacity: 0, y: 18, duration: d(0.6), ease: 'power3.out'}, 0);
    if (data.kicker) FW.inUp(tl, '.fwc-kick', at(0.2), {y: 18, d: d(0.6)});
    FW.inUp(tl, '.fwc-head', at(0.35), {y: 30, d: d(0.9)});
    if (data.sub) FW.inUp(tl, '.fwc-sub', at(0.75), {y: 22, d: d(0.8)});
    if (data.button) tl.from('.fwc-btn', {opacity: 0, scale: 0.9, duration: d(0.6),
      ease: 'back.out(1.7)'}, at(1.0));
    if (data.url) FW.inUp(tl, '.fwc-url', at(1.3), {y: 16, d: d(0.6)});
    return tl;
  };
})();
