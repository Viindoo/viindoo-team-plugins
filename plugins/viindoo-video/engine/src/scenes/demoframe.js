// Scene: demoframe  -  nen 16:9 brand + cot chu ben trai, chua o trong ben phai cho clip vuong.
// Dung lam ANH NEN TINH (chup 1 khung) roi ffmpeg overlay clip demo vuong len o phai.
// data = { kicker?, tag?, headline, sub? }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['demoframe'] = function (stage, data, brand, gsap) {
    const C = brand.colors;
    const F = brand.fonts;

    // Logo CHUAN = file SVG goc. Chi go lai bang font khi khong doc duoc file.
    const logo = (h) => (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span>`;
    const BG = '#1B2227';
    const tag = data.tag ? `<div style="display:inline-block; background:${C.secondary};
      color:${C.white}; font-family:${F.heading}; font-weight:600; font-size:26px;
      padding:9px 22px; border-radius:999px; margin-bottom:22px;">${data.tag}</div><br>` : '';

    stage.innerHTML = `
      <div style="position:absolute; inset:0; background:${BG}; overflow:hidden; font-family:${F.body};">
        <div style="position:absolute; top:0; left:0; height:10px; width:50%; background:${C.primary};"></div>
        <div style="position:absolute; top:0; left:50%; height:10px; width:50%; background:${C.secondary};"></div>
        <div style="position:absolute; top:62px; left:90px; font-family:${F.heading};
          font-weight:700; font-size:46px; letter-spacing:.3px;
          background:${C.white}; border-radius:14px; padding:10px 18px;">${logo(56)}</div>

        <div style="position:absolute; left:90px; top:300px; width:770px;">
          ${tag}
          ${data.kicker ? `<div style="font-family:${F.heading}; font-weight:600; font-size:30px;
            letter-spacing:2px; text-transform:uppercase; color:${C.primary}; margin-bottom:22px;">${data.kicker}</div>` : ''}
          <div style="font-family:${F.heading}; font-weight:700; font-size:76px; line-height:1.1;
            color:${C.white};">${data.headline || ''}</div>
          ${data.sub ? `<div style="font-size:28px; color:#AEB4B8; margin-top:24px; line-height:1.4;">${data.sub}</div>` : ''}
        </div>

        <div style="position:absolute; left:946px; top:86px; width:908px; height:908px;
          border:2px solid rgba(255,255,255,.14); border-radius:18px;
          box-shadow:0 24px 60px rgba(0,0,0,.45);"></div>
      </div>`;
    const tl = gsap.timeline({paused: true});
    tl.to({}, {duration: 0.1});
    return tl;
  };
})();
