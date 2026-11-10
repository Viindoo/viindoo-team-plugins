// Scene: cta  -  man ket, loi moi dat demo, logo Viindoo lon. brand Viindoo.
// Hop dong: buildScene(stage, data, brand, gsap) -> gsap.timeline (paused).
// data = { headline, sub?, button?, closing? }
(function () {
  window.SCENES = window.SCENES || {};

  window.SCENES['cta'] = function (stage, data, brand, gsap) {
    const C = brand.colors;
    const F = brand.fonts;

    // Logo CHUAN = file SVG goc (net chu rieng). Chi go lai bang font khi khong doc duoc file.
    const logo = (h) => (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span>`;

    stage.innerHTML = `
      <div class="root" style="position:absolute; inset:0; background:${C.white};
        font-family:${F.body}; color:${C.text_body}; overflow:hidden;
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        text-align:center; padding:0 120px;">
        <div class="accent" style="position:absolute; top:0; left:0; height:10px; width:100%;
          background:linear-gradient(90deg, ${C.primary}, ${C.secondary});"></div>

        <div class="logo" style="font-family:${F.heading}; font-weight:700; font-size:72px;
          letter-spacing:.5px; margin-bottom:40px;">${logo(88)}</div>
        <div class="headline" style="font-family:${F.heading}; font-weight:700; font-size:72px;
          line-height:1.15; color:${C.text_heading}; max-width:1500px;">${data.headline || ''}</div>
        ${data.sub ? `<div class="sub" style="font-size:34px; color:${C.text_muted};
          margin-top:26px; max-width:1400px; line-height:1.4;">${data.sub}</div>` : ''}
        ${data.button ? `<div class="btn" style="margin-top:56px; display:inline-block;
          background:linear-gradient(135deg, ${C.primary}, ${C.secondary}); color:${C.white};
          font-family:${F.heading}; font-weight:700; font-size:34px; padding:26px 56px;
          border-radius:999px; box-shadow:0 14px 34px rgba(127,66,130,.32);">${data.button}</div>` : ''}
        ${data.closing ? `<div class="closing" style="font-size:26px; color:${C.text_muted};
          margin-top:44px;">${data.closing}</div>` : ''}
      </div>`;

    const tl = gsap.timeline({paused: true});
    tl.from('.accent', {scaleX: 0, transformOrigin: 'left center', duration: 0.7, ease: 'power2.out'}, 0);
    tl.from('.logo', {opacity: 0, y: -24, scale: 0.9, duration: 0.7, ease: 'back.out(1.8)'}, 0.15);
    tl.from('.headline', {opacity: 0, y: 34, duration: 0.8, ease: 'power3.out'}, 0.5);
    if (data.sub) tl.from('.sub', {opacity: 0, y: 22, duration: 0.6, ease: 'power3.out'}, 0.85);
    if (data.button) tl.from('.btn', {opacity: 0, scale: 0.8, duration: 0.6, ease: 'back.out(2)'}, 1.1);
    if (data.closing) tl.from('.closing', {opacity: 0, duration: 0.5, ease: 'power2.out'}, 1.4);
    tl.to('.btn', {scale: 1.04, duration: 0.8, repeat: 2, yoyo: true, ease: 'sine.inOut'}, 1.5);
    tl.to({}, {duration: 0.4});
    return tl;
  };
})();
