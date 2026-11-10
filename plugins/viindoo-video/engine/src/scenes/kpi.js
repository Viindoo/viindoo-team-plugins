// Scene: kpi  -  tieu de + the chi so dem len + bieu do cot moc dan, brand Viindoo.
// Chay trong trinh duyet (headless Chrome). Dang ky vao window.SCENES.
// Hop dong: buildScene(stage, data, brand, gsap) -> gsap.timeline (paused).
// data = { title, subtitle, metrics:[{label,value,prefix?,suffix?,decimals?}], bars:[{label,value}] }
(function () {
  window.SCENES = window.SCENES || {};

  function fmt(v, m) {
    const d = m.decimals || 0;
    const n = Number(v).toLocaleString('vi-VN', {
      minimumFractionDigits: d, maximumFractionDigits: d,
    });
    return (m.prefix || '') + n + (m.suffix || '');
  }

  window.SCENES['kpi'] = function (stage, data, brand, gsap) {
    const C = brand.colors;
    const F = brand.fonts;

    // Logo CHUAN = file SVG goc. Chi go lai bang font khi khong doc duoc file.
    const logo = (h) => (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span>`;
    const metrics = data.metrics || [];
    const bars = data.bars || [];
    const maxBar = Math.max(1, ...bars.map(b => b.value));

    stage.innerHTML = `
      <div class="root" style="
        position:absolute; inset:0; background:${C.white};
        font-family:${F.body}; padding:84px 96px; color:${C.text_body};">
        <div class="accent" style="
          position:absolute; top:0; left:0; height:10px; width:100%;
          background:linear-gradient(90deg, ${C.primary}, ${C.secondary});"></div>

        <div class="wm" style="font-family:${F.heading}; font-weight:700;
          font-size:30px; letter-spacing:.3px; margin-bottom:28px;">${logo(36)}</div>

        <div class="title" style="font-family:${F.heading}; font-weight:700;
          font-size:64px; line-height:1.12; color:${C.text_heading}; max-width:1400px;">
          ${data.title || ''}</div>
        <div class="subtitle" style="font-size:28px; color:${C.text_muted};
          margin-top:14px; max-width:1300px;">${data.subtitle || ''}</div>

        <div class="cards" style="display:flex; gap:28px; margin-top:56px;">
          ${metrics.map(() => `
            <div class="card" style="flex:1; background:${C.grey_light_bg};
              border-radius:20px; padding:34px 32px; border-bottom:6px solid ${C.primary};">
              <div class="card-val" style="font-family:${F.heading}; font-weight:700;
                font-size:58px; color:${C.primary}; line-height:1;">0</div>
              <div class="card-lbl" style="font-size:22px; color:${C.text_muted};
                margin-top:14px;">LBL</div>
            </div>`).join('')}
        </div>

        <div class="bars" style="margin-top:52px; display:flex; flex-direction:column; gap:20px; max-width:1500px;">
          ${bars.map(b => `
            <div style="display:flex; align-items:center; gap:22px;">
              <div style="width:280px; font-size:24px; color:${C.text_body};">${b.label}</div>
              <div style="flex:1; height:34px; background:${C.grey_light_bg}; border-radius:17px; overflow:hidden;">
                <div class="bar-fill" style="height:100%; width:${(b.value / maxBar) * 100}%;
                  background:linear-gradient(90deg, ${C.primary}, ${C.secondary}); border-radius:17px;"></div>
              </div>
              <div style="width:120px; text-align:right; font-weight:600; font-size:24px; color:${C.text_heading};">${b.value.toLocaleString('vi-VN')}</div>
            </div>`).join('')}
        </div>
      </div>`;

    // dien label the chi so
    const cardEls = [...stage.querySelectorAll('.card')];
    cardEls.forEach((el, i) => { el.querySelector('.card-lbl').textContent = metrics[i].label; });

    const tl = gsap.timeline({paused: true});
    tl.from('.accent', {scaleX: 0, transformOrigin: 'left center', duration: 0.8, ease: 'power2.out'}, 0);
    tl.from('.wm', {opacity: 0, y: -18, duration: 0.6, ease: 'power2.out'}, 0.1);
    tl.from('.title', {opacity: 0, y: 34, duration: 0.8, ease: 'power3.out'}, 0.25);
    tl.from('.subtitle', {opacity: 0, y: 22, duration: 0.6, ease: 'power3.out'}, 0.55);
    tl.from('.card', {opacity: 0, y: 44, duration: 0.6, stagger: 0.14, ease: 'power3.out'}, 0.85);

    metrics.forEach((m, i) => {
      const valEl = cardEls[i].querySelector('.card-val');
      const o = {v: 0};
      tl.to(o, {v: m.value, duration: 1.2, ease: 'power2.out',
        onUpdate: () => { valEl.textContent = fmt(o.v, m); }}, 0.95 + i * 0.14);
    });

    tl.from('.bar-fill', {scaleX: 0, transformOrigin: 'left center', duration: 1.0, stagger: 0.12, ease: 'power3.out'}, 1.7);
    tl.to({}, {duration: 1.0}); // giu khung cuoi
    return tl;
  };
})();
