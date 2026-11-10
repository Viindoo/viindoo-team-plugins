// Scene: statement  -  cau khang dinh lon + phu + danh sach y, brand Viindoo.
// Hop dong: buildScene(stage, data, brand, gsap) -> gsap.timeline (paused).
// data = { kicker?, tag?, headline, sub?, points?:[string], accent?:'primary'|'secondary' }
(function () {
  window.SCENES = window.SCENES || {};

  window.SCENES['statement'] = function (stage, data, brand, gsap) {
    const C = brand.colors;
    const F = brand.fonts;

    // Logo CHUAN = file SVG goc. Chi go lai bang font khi khong doc duoc file.
    const logo = (h) => (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span>`;
    const accent = data.accent === 'secondary' ? C.secondary : C.primary;
    const points = data.points || [];

    const tagHtml = data.tag ? `
      <div class="tag" style="position:absolute; top:84px; right:96px;
        background:${C.secondary}; color:${C.white}; font-family:${F.heading};
        font-weight:600; font-size:22px; padding:10px 22px; border-radius:999px;">
        ${data.tag}</div>` : '';

    const kickerHtml = data.kicker ? `
      <div class="kicker" style="font-family:${F.heading}; font-weight:600;
        font-size:26px; letter-spacing:2px; text-transform:uppercase;
        color:${accent}; margin-bottom:22px;">${data.kicker}</div>` : '';

    const subHtml = data.sub ? `
      <div class="sub" style="font-size:34px; color:${C.text_muted};
        margin-top:26px; max-width:1500px; line-height:1.4;">${data.sub}</div>` : '';

    const pointsHtml = points.length ? `
      <div class="points" style="margin-top:54px; display:flex; flex-direction:column; gap:26px;">
        ${points.map((p, i) => `
          <div class="pt" style="display:flex; align-items:flex-start; gap:22px; max-width:1500px;">
            <div style="flex:none; width:40px; height:40px; border-radius:12px;
              background:linear-gradient(135deg, ${C.primary}, ${C.secondary});
              display:flex; align-items:center; justify-content:center;
              color:${C.white}; font-family:${F.heading}; font-weight:700; font-size:24px;">${i + 1}</div>
            <div style="font-size:32px; color:${C.text_body}; line-height:1.35;">${p}</div>
          </div>`).join('')}
      </div>` : '';

    stage.innerHTML = `
      <div class="root" style="position:absolute; inset:0; background:${C.white};
        font-family:${F.body}; padding:96px 96px; color:${C.text_body}; overflow:hidden;">
        <div class="bgglow" style="position:absolute; width:1000px; height:1000px; border-radius:50%;
          top:-240px; right:-200px; filter:blur(12px); pointer-events:none;
          background:radial-gradient(circle, rgba(0,187,206,.12), rgba(127,66,130,.05) 55%, transparent 72%);"></div>
        <div class="bgglow2" style="position:absolute; width:760px; height:760px; border-radius:50%;
          bottom:-260px; left:-160px; filter:blur(14px); pointer-events:none;
          background:radial-gradient(circle, rgba(127,66,130,.08), transparent 68%);"></div>
        <div class="accent" style="position:absolute; top:0; left:0; height:10px; width:100%;
          background:linear-gradient(90deg, ${C.primary}, ${C.secondary});"></div>
        <div class="wm" style="font-family:${F.heading}; font-weight:700; font-size:30px;
          letter-spacing:.3px; margin-bottom:40px;">${logo(36)}</div>
        ${tagHtml}
        ${kickerHtml}
        <div class="headline" style="font-family:${F.heading}; font-weight:700;
          font-size:88px; line-height:1.1; color:${C.text_heading}; max-width:1600px;">
          ${data.headline || ''}</div>
        ${subHtml}
        ${pointsHtml}
      </div>`;

    const tl = gsap.timeline({paused: true});
    // nen chuyen dong LIEN TUC suot canh (khong de dung im)
    tl.fromTo('.bgglow', {xPercent: -8, yPercent: -6, scale: 0.85}, {xPercent: 10, yPercent: 12, scale: 1.3, duration: 13, ease: 'none'}, 0);
    tl.fromTo('.bgglow2', {xPercent: 8, yPercent: 10, scale: 1.15}, {xPercent: -10, yPercent: -8, scale: 0.8, duration: 13, ease: 'none'}, 0);
    tl.from('.accent', {scaleX: 0, transformOrigin: 'left center', duration: 0.7, ease: 'power2.out'}, 0);
    tl.from('.wm', {opacity: 0, y: -16, duration: 0.5, ease: 'power2.out'}, 0.1);
    if (data.tag) tl.from('.tag', {opacity: 0, scale: 0.8, duration: 0.5, ease: 'back.out(2)'}, 0.3);
    if (data.kicker) tl.from('.kicker', {opacity: 0, x: -24, duration: 0.5, ease: 'power3.out'}, 0.25);
    tl.from('.headline', {opacity: 0, y: 40, duration: 0.8, ease: 'power3.out'}, 0.4);
    if (data.sub) tl.from('.sub', {opacity: 0, y: 24, duration: 0.6, ease: 'power3.out'}, 0.85);
    if (points.length) tl.from('.pt', {opacity: 0, y: 34, x: -12, duration: 0.6, stagger: 0.7, ease: 'power3.out'}, 1.1);
    // troi nhe keo dai de con song
    tl.to('.headline', {y: '+=7', duration: 6, ease: 'sine.inOut', yoyo: true, repeat: 1}, 3);
    return tl;
  };
})();
