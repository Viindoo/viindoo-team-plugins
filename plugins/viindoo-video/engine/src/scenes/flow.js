// Scene: flow  -  so do dong chay N o noi bang mui ten, brand Viindoo.
// Hop dong: buildScene(stage, data, brand, gsap) -> gsap.timeline (paused).
// data = { kicker?, tag?, headline, steps:[{label, note?}], caption? }
(function () {
  window.SCENES = window.SCENES || {};

  window.SCENES['flow'] = function (stage, data, brand, gsap) {
    const C = brand.colors;
    const F = brand.fonts;

    // Logo CHUAN = file SVG goc. Chi go lai bang font khi khong doc duoc file.
    const logo = (h) => (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span>`;
    const steps = data.steps || [];

    const tagHtml = data.tag ? `
      <div class="tag" style="position:absolute; top:84px; right:96px;
        background:${C.secondary}; color:${C.white}; font-family:${F.heading};
        font-weight:600; font-size:22px; padding:10px 22px; border-radius:999px;">
        ${data.tag}</div>` : '';

    const kickerHtml = data.kicker ? `
      <div class="kicker" style="font-family:${F.heading}; font-weight:600;
        font-size:26px; letter-spacing:2px; text-transform:uppercase;
        color:${C.primary}; margin-bottom:20px;">${data.kicker}</div>` : '';

    const boxes = steps.map((s, i) => `
      ${i > 0 ? `<div class="arrow" style="flex:none; color:${C.secondary}; font-size:52px;
        font-weight:700; align-self:center; margin:0 6px;">&rsaquo;</div>` : ''}
      <div class="box" style="flex:1; min-width:0; background:${C.grey_light_bg};
        border-radius:22px; padding:38px 30px; border-top:7px solid ${C.primary};
        display:flex; flex-direction:column; gap:14px; min-height:230px;">
        <div style="font-family:${F.heading}; font-weight:700; font-size:34px;
          color:${C.text_heading}; line-height:1.18;">${s.label}</div>
        ${s.note ? `<div style="font-size:24px; color:${C.text_muted}; line-height:1.35;">${s.note}</div>` : ''}
      </div>`).join('');

    stage.innerHTML = `
      <div class="root" style="position:absolute; inset:0; background:${C.white};
        font-family:${F.body}; padding:96px 96px; color:${C.text_body}; overflow:hidden;">
        <div class="bgglow" style="position:absolute; width:1000px; height:1000px; border-radius:50%;
          top:-260px; right:-200px; filter:blur(12px); pointer-events:none;
          background:radial-gradient(circle, rgba(0,187,206,.12), rgba(127,66,130,.05) 55%, transparent 72%);"></div>
        <div class="accent" style="position:absolute; top:0; left:0; height:10px; width:100%;
          background:linear-gradient(90deg, ${C.primary}, ${C.secondary});"></div>
        <div class="wm" style="font-family:${F.heading}; font-weight:700; font-size:30px;
          letter-spacing:.3px; margin-bottom:34px;">${logo(36)}</div>
        ${tagHtml}
        ${kickerHtml}
        <div class="headline" style="font-family:${F.heading}; font-weight:700;
          font-size:72px; line-height:1.1; color:${C.text_heading}; max-width:1600px;">
          ${data.headline || ''}</div>
        <div class="row" style="display:flex; align-items:stretch; gap:8px; margin-top:64px;">
          ${boxes}
        </div>
        ${data.caption ? `<div class="caption" style="font-size:30px; color:${C.text_muted};
          margin-top:48px; max-width:1600px; line-height:1.4;">${data.caption}</div>` : ''}
      </div>`;

    const tl = gsap.timeline({paused: true});
    tl.fromTo('.bgglow', {xPercent: -8, yPercent: -6, scale: 0.85}, {xPercent: 10, yPercent: 12, scale: 1.3, duration: 13, ease: 'none'}, 0);
    tl.from('.accent', {scaleX: 0, transformOrigin: 'left center', duration: 0.7, ease: 'power2.out'}, 0);
    tl.from('.wm', {opacity: 0, y: -16, duration: 0.5, ease: 'power2.out'}, 0.1);
    if (data.tag) tl.from('.tag', {opacity: 0, scale: 0.8, duration: 0.5, ease: 'back.out(2)'}, 0.3);
    if (data.kicker) tl.from('.kicker', {opacity: 0, x: -24, duration: 0.5, ease: 'power3.out'}, 0.25);
    tl.from('.headline', {opacity: 0, y: 36, duration: 0.7, ease: 'power3.out'}, 0.4);
    tl.from('.box', {opacity: 0, y: 40, duration: 0.6, stagger: 0.2, ease: 'power3.out'}, 0.85);
    tl.from('.arrow', {opacity: 0, duration: 0.4, stagger: 0.2, ease: 'power2.out'}, 1.05);
    if (data.caption) tl.from('.caption', {opacity: 0, y: 20, duration: 0.6, ease: 'power3.out'}, 1.6);
    tl.to({}, {duration: 0.4});
    return tl;
  };
})();
