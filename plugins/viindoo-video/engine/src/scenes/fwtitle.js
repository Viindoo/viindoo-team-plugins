// Scene: fwtitle - THE TEN SAN PHAM / NEN TANG (chuan forwarder).
// Clip mau dung hai lan: (1) ngay sau canh noi dau - icon module + ten san pham + phu de
// tieng Viet; (2) truoc khi vao quy trinh - nhan nganh + laptop dat tren be teal.
//
// data = {
//   icon?,            // icon module (anh, engine nhung thanh data URI)
//   name,             // vi du 'VIINDOO FREIGHT MANAGEMENT'
//   sub?,             // phu de tieng Viet, vi du 'Quan ly Van tai giao nhan'
//   audience?,        // nhan nganh in hoa dat tren cung, vi du 'FREIGHT FORWARDER'
//   shot?, shotSize?  // co anh -> dung laptop dat tren be teal thay cho the ten
// }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwtitle'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const tl = gsap.timeline({paused: true});

    if (data.shot) {
      // bien the "nen tang": nhan nganh + laptop tren be teal bo tron
      const nat = data.shotSize || {w: 1920, h: 1080};
      const lap = FW.laptop({x: 470, y: 300, w: 980});
      const h = Math.round(lap.screen.w * nat.h / nat.w);
      const scr = {...lap.screen, h: Math.min(h, lap.screen.h)};
      stage.innerHTML = FW.page(brand, `
        <div class="fw-base" style="position:absolute; left:50%; transform:translateX(-50%);
          bottom:-190px; width:1500px; height:420px; border-radius:50% 50% 0 0;
          background:${C.primary};"></div>
        ${data.audience ? `<div class="fw-aud" style="position:absolute; top:180px; left:0; right:0;
          text-align:center; font-family:${F.heading}; font-weight:700; font-size:40px;
          letter-spacing:3px; text-transform:uppercase; color:${C.primary};">${data.audience}</div>` : ''}
        ${lap.html}
        ${FW.screen(data.shot, scr, {radius: 4})}`);
      if (data.audience) tl.from('.fw-aud', {opacity: 0, y: -16, duration: 0.7}, 0);
      tl.from('.fw-base', {y: 150, duration: 1.0, ease: 'power3.out'}, 0.1);
      tl.from('.fw-shot', {opacity: 0, y: 40, duration: 0.9, ease: 'power3.out'}, 0.4);
      return tl;
    }

    const ic = data.icon
      ? `<img class="fw-ic" src="${data.icon}" style="width:150px;height:150px;object-fit:contain;
          border-radius:28px;">`
      : `<div class="fw-ic" style="width:150px;height:150px;border-radius:28px;
          background:${C.primary};"></div>`;
    stage.innerHTML = FW.page(brand, `
      ${FW.logoCorner(brand, 38)}
      <div style="position:absolute; inset:0; display:flex; flex-direction:column;
        align-items:center; justify-content:center;">
        ${ic}
        <div class="fw-name" style="font-family:${F.heading}; font-weight:700; font-size:54px;
          letter-spacing:1.5px; text-transform:uppercase; color:${C.primary}; margin-top:40px;
          text-align:center;">${data.name || ''}</div>
        ${data.sub ? `<div class="fw-sub2" style="font-size:32px; color:${C.text_muted};
          margin-top:12px;">${data.sub}</div>` : ''}
      </div>`);
    tl.from('.fw-ic', {opacity: 0, scale: 0.7, duration: 0.8, ease: 'back.out(1.8)'}, 0);
    tl.from('.fw-name', {opacity: 0, y: 22, duration: 0.7, ease: 'power3.out'}, 0.4);
    if (data.sub) tl.from('.fw-sub2', {opacity: 0, duration: 0.6}, 0.7);
    return tl;
  };
})();
