// Scene: fwapps - CÁC ICON APP VIINDOO BAY VÀO TỤ LẠI quanh logo (bức tranh tổng thể).
//
// Liên 19/10/2026: phần kết nói "nằm trên một hệ thống" thì phải CHO THẤY hệ thống đó -
// màn hình gồm các icon app Viindoo chuyển động tập hợp lại. Đây là cảnh đó.
// Icon lấy từ static/description/icon.png của chính các module Viindoo (ảnh thật, không vẽ lại).
//
// data = {
//   kicker?, headline?, sub?,
//   apps: [{icon, label}],      // icon = đường dẫn ảnh (engine tự nhúng), thứ tự = thứ tự bay vào
//   highlight?                  // nhãn app cần làm nổi (ví dụ "Nhân sự")
// }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwapps'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const apps = (data.apps || []).slice(0, 14);
    const n = Math.max(apps.length, 1);
    const cx = 960, cy = 640, R = 400;          // tâm và bán kính vòng tụ
    const S = 96;                                // cỡ icon
    const Wc = 190;                              // bề ngang Ô CHỮ - rộng hơn icon để nhãn không đè nhau

    const items = apps.map((a, i) => {
      const ang = -Math.PI / 2 + (i * 2 * Math.PI) / n;
      const x = Math.round(cx + R * Math.cos(ang)) - Wc / 2;
      const y = Math.round(cy + R * 0.70 * Math.sin(ang)) - S / 2;
      const on = data.highlight && a.label === data.highlight;
      // điểm xuất phát: văng ra xa theo đúng hướng, rồi bay vào chỗ của mình
      const fx = Math.round(Math.cos(ang) * 760), fy = Math.round(Math.sin(ang) * 520);
      return `
        <div class="fw-app ${on ? 'fw-app-on' : ''}" data-fx="${fx}" data-fy="${fy}"
          style="position:absolute; left:${x}px; top:${y}px; width:${Wc}px; text-align:center;">
          <img src="${a.icon}" style="width:${S}px; height:${S}px; object-fit:contain; display:inline-block;
            border-radius:22px; ${on ? `box-shadow:0 0 0 5px ${C.primary}, 0 14px 34px rgba(0,187,206,.42);`
                                     : 'box-shadow:0 10px 26px rgba(19,60,70,.16);'}">
          <div style="font-family:${F.heading}; font-weight:${on ? 700 : 500}; font-size:16px;
            margin-top:9px; line-height:1.2; height:38px; overflow:hidden;
            color:${on ? C.primary : C.text_muted};">${a.label || ''}</div>
        </div>`;
    }).join('');

    stage.innerHTML = FW.page(brand, `
      ${FW.logoCorner(brand, 38)}
      ${data.kicker ? `<div class="fw-k" style="position:absolute; top:150px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:600; font-size:25px;
        letter-spacing:2.4px; text-transform:uppercase; color:${C.primary};">${data.kicker}</div>` : ''}
      ${data.headline ? `<div class="fw-h" style="position:absolute; top:198px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:700; font-size:54px;
        color:${C.text_heading};">${data.headline}</div>` : ''}
      <div class="fw-core" style="position:absolute; left:${cx - 230}px; top:${cy - 56}px;
        width:460px; text-align:center;">${FW.logo(brand, 86)}</div>
      ${items}
      ${data.sub ? `<div class="fw-s" style="position:absolute; bottom:70px; left:0; right:0;
        text-align:center; font-size:26px; color:${C.text_muted};">${data.sub}</div>` : ''}`);

    const tl = gsap.timeline({paused: true});
    if (data.kicker) tl.from('.fw-k', {opacity: 0, y: -14, duration: 0.5}, 0);
    if (data.headline) tl.from('.fw-h', {opacity: 0, y: 16, duration: 0.6}, 0.1);
    // các icon văng từ ngoài bay vào tụ quanh logo
    tl.from('.fw-app', {
      opacity: 0, scale: 0.4, duration: 0.95, ease: 'back.out(1.5)', stagger: 0.075,
      x: (i, el) => parseFloat(el.dataset.fx), y: (i, el) => parseFloat(el.dataset.fy),
    }, 0.35);
    tl.from('.fw-core', {opacity: 0, scale: 0.7, duration: 0.7, ease: 'back.out(2)'}, 1.5);
    if (data.highlight) tl.fromTo('.fw-app-on', {scale: 1},
      {scale: 1.14, duration: 0.5, yoyo: true, repeat: 1, ease: 'power2.inOut',
       transformOrigin: '50% 40%'}, 2.3);
    if (data.sub) tl.from('.fw-s', {opacity: 0, duration: 0.6}, 2.6);
    return tl;
  };
})();
