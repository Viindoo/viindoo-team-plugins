// Scene: fwcta - MAN KET theo chuan forwarder: logo goc + dia chi web + nut mau teal.
// Clip mau ket bang logo Viindoo lon, duoi la https://viindoo.com/ va nut "TRAI NGHIEM NGAY".
// Loi keu goi phai dan toi BAN HANG (dat demo / trai nghiem / lien he), khong dan sang blog.
//
// data = { url?, button?, sub? }   button:false -> AN nut (vd Lien 05/11: man ket chi mot cau,
// nut tu in hoa nen cau co chu "Viindoo" phai nam o sub, khong nam o nut)
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwcta'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    stage.innerHTML = FW.page(brand, `
      <div style="position:absolute; inset:0; display:flex; flex-direction:column;
        align-items:center; justify-content:center;">
        <div class="fw-lg">${FW.logo(brand, 132)}</div>
        ${data.sub ? `<div class="fw-s" style="font-size:34px; color:${C.text_heading};
          margin-top:26px; font-weight:500;">${data.sub}</div>` : ''}
        <div class="fw-u" style="font-size:28px; color:${C.primary}; margin-top:18px;">
          ${data.url || 'https://viindoo.com/'}</div>
        ${data.button === false ? '' : `<div class="fw-b" style="margin-top:46px; background:${C.primary}; color:${C.white};
          font-family:${F.heading}; font-weight:700; font-size:32px; letter-spacing:1.5px;
          text-transform:uppercase; padding:22px 58px; border-radius:10px;
          box-shadow:0 16px 40px rgba(0,187,206,.34);">${data.button || 'Trải nghiệm ngay'}</div>`}
      </div>`, {grid: false});

    const tl = gsap.timeline({paused: true});
    tl.from('.fw-lg', {opacity: 0, y: -24, scale: 0.92, duration: 0.8, ease: 'back.out(1.7)'}, 0);
    if (data.sub) tl.from('.fw-s', {opacity: 0, y: 14, duration: 0.6}, 0.45);
    tl.from('.fw-u', {opacity: 0, duration: 0.5}, 0.65);
    if (data.button !== false) tl.from('.fw-b', {opacity: 0, y: 20, duration: 0.6, ease: 'power3.out'}, 0.85);
    return tl;
  };
})();
