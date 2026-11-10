// Scene: demoframe2 - chu GON ben trai, man hinh demo TO ben phai (gan full chieu cao).
// Dung lam anh nen tinh; ffmpeg crop bo tour + phong to + zoom roi overlay vao o phai.
// data = { kicker?, tag?, headline, sub? }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['demoframe2'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, BG = '#1B2227';

    // Logo CHUAN = file SVG goc. Chi go lai bang font khi khong doc duoc file.
    const logo = (h) => (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span>`;
    const tag = data.tag ? `<div style="display:inline-block; background:${C.secondary};
      color:${C.white}; font-family:${F.heading}; font-weight:600; font-size:24px;
      padding:8px 20px; border-radius:999px; margin-bottom:20px;">${data.tag}</div><br>` : '';
    stage.innerHTML = `
      <div style="position:absolute; inset:0; background:${BG}; overflow:hidden; font-family:${F.body};">
        <div style="position:absolute; top:0; left:0; height:9px; width:50%; background:${C.primary};"></div>
        <div style="position:absolute; top:0; left:50%; height:9px; width:50%; background:${C.secondary};"></div>
        <div style="position:absolute; top:52px; left:80px; font-family:${F.heading};
          font-weight:700; font-size:40px;
          background:${C.white}; border-radius:12px; padding:9px 16px;">${logo(48)}</div>
        <div style="position:absolute; left:80px; top:300px; width:950px;">
          ${tag}
          ${data.kicker ? `<div style="font-family:${F.heading}; font-weight:600; font-size:28px;
            letter-spacing:2px; text-transform:uppercase; color:${C.primary}; margin-bottom:18px;">${data.kicker}</div>` : ''}
          <div style="font-family:${F.heading}; font-weight:700; font-size:60px; line-height:1.1;
            color:${C.white};">${data.headline || ''}</div>
          ${data.sub ? `<div style="font-size:25px; color:#9AA1A6; margin-top:20px; line-height:1.4;">${data.sub}</div>` : ''}
        </div>
        <div style="position:absolute; left:1104px; top:22px; width:788px; height:1036px;
          border:2px solid rgba(255,255,255,.14); border-radius:16px;
          box-shadow:0 24px 60px rgba(0,0,0,.5);"></div>
      </div>`;
    const tl = gsap.timeline({paused: true}); tl.to({}, {duration: 0.1}); return tl;
  };
})();
