// fwwrapv.js - NEN DOC 9:16 de long mot doan clip 16:9 vao giua.
//
// Dung khi cat short tu mot clip tong da dung san: thay vi letterbox (hai dai trang tren duoi,
// chu nho, nhin nhu bi cat vung ve), canh nay dung mot trang DOC dung nghia - logo tren cung,
// tieu de chuong chu to, o trong de ghep khung hinh goc vao, loi keu goi duoi cung.
//
// Canh chi ve NEN. Doan video that duoc ghep vao o trong bang FFmpeg o buoc sau, dung toa do
// khai o `BOX` duoi day (giu nguyen hai ben cho khop).
//
// data:
//   title   tieu de chuong, xuong dong bang \n
//   cta?    dong keu goi duoi cung (mac dinh "Đặt lịch demo - viindoo.com")
(function () {
  window.SCENES = window.SCENES || {};

  // O ghep video. Toa do PHAI khop voi lenh overlay cua FFmpeg - doc bang ham `oGhep()`
  // duoi day thay vi go tay hai noi.
  // Khung DOC 1080x1920 con nhieu cho nen co tieu de chuong; khung VUONG 1080x1080 thi chi
  // vua logo + video + loi keu goi, bo tieu de di cho khoi chen.
  const W_BOX = 1000;
  function oGhep(H) {
    const h = Math.round(W_BOX * 9 / 16);
    return {x: 40, y: Math.round((H - h) / 2 + (H > 1400 ? 40 : 0)), w: W_BOX, h: h};
  }
  window.FW_O_GHEP = oGhep;   // de script dung lenh FFmpeg doc lai

  window.SCENES['fwwrapv'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts;
    const FW = window.FW;
    const H = stage.offsetHeight || 1920;
    const vuong = H < 1400;
    const BOX = oGhep(H);
    const cta = data.cta || 'Đặt lịch demo - viindoo.com';
    const title = vuong ? '' : (data.title || '').split('\n')
      .map(t => `<div>${t}</div>`).join('');

    stage.innerHTML = FW.page(brand, `
      <div style="position:absolute; top:${vuong ? 60 : 88}px; left:56px;">
        ${FW.logo(brand, vuong ? 44 : 54)}</div>

      <div style="position:absolute; left:56px; right:56px; top:224px;
        font-family:${F.heading}; font-weight:700; font-size:66px; line-height:1.18;
        color:${C.text_heading};">${title}</div>

      <!-- o ghep video: ve san khung bo goc + do bong cho khop voi anh se dat vao -->
      <div style="position:absolute; left:${BOX.x}px; top:${BOX.y}px;
        width:${BOX.w}px; height:${BOX.h}px; border-radius:14px; background:${C.white};
        box-shadow:0 26px 70px rgba(19,60,70,.22); border:1px solid rgba(19,60,70,.08);"></div>

      <div style="position:absolute; left:56px; right:56px; bottom:${vuong ? 58 : 140}px;
        text-align:center; font-family:${F.heading}; font-weight:700;
        font-size:${vuong ? 38 : 44}px; color:${C.primary};">${cta}</div>`);

    // nen tinh - khong can nhip
    return gsap.timeline({paused: true});
  };
})();
