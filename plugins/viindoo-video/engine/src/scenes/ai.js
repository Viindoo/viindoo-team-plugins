// Scene: ai  -  hoi so lieu bang giong noi (dinh huong Viindoo AI), nhan "Hinh minh hoa".
// Hop dong: buildScene(stage, data, brand, gsap) -> gsap.timeline (paused).
// data = { kicker?, question, answerRows:[{k,v}], note? }
(function () {
  window.SCENES = window.SCENES || {};

  window.SCENES['ai'] = function (stage, data, brand, gsap) {
    const C = brand.colors;
    const F = brand.fonts;

    // Logo CHUAN = file SVG goc. Chi go lai bang font khi khong doc duoc file.
    const logo = (h) => (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span>`;
    const rows = data.answerRows || [];
    const bars = 13;
    const waves = Array.from({length: bars}, (_, i) =>
      `<div class="wave" style="width:9px; border-radius:6px;
        height:${20 + Math.round(60 * Math.abs(Math.sin(i * 1.1)))}px;
        background:linear-gradient(180deg, ${C.primary}, ${C.secondary});"></div>`).join('');

    const rowsHtml = rows.map(r => `
      <div class="arow" style="display:flex; justify-content:space-between; align-items:center;
        gap:24px; padding:20px 28px; background:${C.white}; border-radius:14px;
        border:1px solid #E4E7EA;">
        <div style="font-size:26px; color:${C.text_body};">${r.k}</div>
        <div style="font-family:${F.heading}; font-weight:700; font-size:28px; color:${C.text_heading};
          white-space:nowrap;">${r.v}</div>
      </div>`).join('');

    stage.innerHTML = `
      <div class="root" style="position:absolute; inset:0; background:${C.white};
        font-family:${F.body}; padding:96px 96px; color:${C.text_body}; overflow:hidden;">
        <div class="accent" style="position:absolute; top:0; left:0; height:10px; width:100%;
          background:linear-gradient(90deg, ${C.primary}, ${C.secondary});"></div>
        <div class="wm" style="font-family:${F.heading}; font-weight:700; font-size:30px;
          letter-spacing:.3px; margin-bottom:30px;">${logo(36)}<span
            style="color:${C.text_muted}; font-weight:600; vertical-align:middle;"> AI</span>
        </div>
        <div class="tag" style="position:absolute; top:84px; right:96px;
          background:${C.grey_light_bg}; color:${C.text_muted}; font-family:${F.heading};
          font-weight:600; font-size:20px; padding:9px 20px; border-radius:999px;">Hình minh họa</div>

        <div class="kicker" style="font-family:${F.heading}; font-weight:600; font-size:26px;
          letter-spacing:2px; text-transform:uppercase; color:${C.primary}; margin-bottom:26px;">
          ${data.kicker || 'Hỏi bằng giọng nói'}</div>

        <div class="askrow" style="display:flex; align-items:center; gap:30px; max-width:1600px;">
          <div class="mic" style="flex:none; width:104px; height:104px; border-radius:50%;
            background:linear-gradient(135deg, ${C.primary}, ${C.secondary});
            display:flex; align-items:center; justify-content:center;
            box-shadow:0 12px 30px rgba(0,187,206,.35);">
            <div style="width:30px; height:46px; border-radius:16px; background:${C.white};"></div>
          </div>
          <div class="waves" style="flex:none; display:flex; align-items:center; gap:7px; height:90px;">
            ${waves}
          </div>
        </div>

        <div class="q" style="font-family:${F.heading}; font-weight:700; font-size:46px;
          color:${C.text_heading}; margin-top:40px; max-width:1600px; line-height:1.25;">
          &ldquo;${data.question || ''}&rdquo;</div>

        <div class="answer" style="margin-top:40px; display:flex; flex-direction:column; gap:16px;
          max-width:1100px;">
          ${rowsHtml}
        </div>
        ${data.note ? `<div class="note" style="font-size:24px; color:${C.text_muted};
          margin-top:30px;">${data.note}</div>` : ''}
      </div>`;

    const tl = gsap.timeline({paused: true});
    tl.from('.accent', {scaleX: 0, transformOrigin: 'left center', duration: 0.7, ease: 'power2.out'}, 0);
    tl.from('.wm', {opacity: 0, y: -16, duration: 0.5, ease: 'power2.out'}, 0.1);
    tl.from('.tag', {opacity: 0, scale: 0.85, duration: 0.5, ease: 'power2.out'}, 0.2);
    tl.from('.kicker', {opacity: 0, x: -24, duration: 0.5, ease: 'power3.out'}, 0.25);
    tl.from('.mic', {opacity: 0, scale: 0.6, duration: 0.6, ease: 'back.out(2)'}, 0.4);
    tl.from('.wave', {scaleY: 0, transformOrigin: 'center', duration: 0.5,
      stagger: {each: 0.04, from: 'start', yoyo: true, repeat: 1}, ease: 'sine.inOut'}, 0.6);
    tl.from('.q', {opacity: 0, y: 24, duration: 0.6, ease: 'power3.out'}, 0.9);
    tl.from('.arow', {opacity: 0, y: 24, duration: 0.5, stagger: 0.14, ease: 'power3.out'}, 1.2);
    tl.to('.mic', {scale: 1.06, duration: 0.7, repeat: 2, yoyo: true, ease: 'sine.inOut'}, 0.9);
    if (data.note) tl.from('.note', {opacity: 0, duration: 0.5, ease: 'power2.out'}, 1.8);
    tl.to({}, {duration: 0.4});
    return tl;
  };
})();
