// Scene: fwsteps - SO DO DONG CHAY NGHIEP VU hien dan tung buoc (chuan forwarder).
// Day la canh dinh khung cho ca clip: no bay ra toan bo chuoi buoc cua nganh, roi cac canh
// fwscreen sau do di lai tung buoc mot voi thanh buoc tren dau.
//
// data = {
//   kicker?, headline?,
//   steps: [{label, note?, icon?}],   // icon = duong dan anh (engine nhung thanh data URI)
//   bg?: duong dan anh nen,           // anh that lam nen, de rat nhat + phu trang o giua
//   reveal?: true                     // hien dan tung buoc (mac dinh true)
// }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwsteps'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const steps = data.steps || [];
    const n = steps.length || 1;
    const gap = 26;
    const cellW = Math.min(230, Math.floor((1920 - 180 - gap * (n - 1)) / n));
    const totalW = cellW * n + gap * (n - 1);
    const x0 = Math.round((1920 - totalW) / 2);
    const y = data.headline ? 430 : 380;

    // Lien 24/10/2026: "phan nay qua don dieu va nhieu khoang trang". Cho phep dat mot anh
    // THAT lam nen, de rat nhat va phu mot lop trang o giua de chu van doc ro.
    const bg = data.bg ? `
      <div class="fw-bg" style="position:absolute; inset:0; opacity:0;">
        <img src="${data.bg}" style="position:absolute; inset:0; width:100%; height:100%;
          object-fit:cover; filter:saturate(.55);">
        <div style="position:absolute; inset:0; background:
          linear-gradient(180deg, rgba(255,255,255,.90) 0%, rgba(255,255,255,.97) 38%,
          rgba(255,255,255,.97) 72%, rgba(255,255,255,.88) 100%);"></div>
      </div>` : '';

    const items = steps.map((s, i) => {
      const x = x0 + i * (cellW + gap);
      const ic = s.icon
        ? `<img src="${s.icon}" style="width:84px;height:84px;object-fit:contain;">`
        : `<div style="width:84px;height:84px;border-radius:20px;background:${C.primary};
             color:#fff;font-family:${F.heading};font-weight:700;font-size:38px;
             display:flex;align-items:center;justify-content:center;">${i + 1}</div>`;
      const arrow = i < n - 1 ? `
        <div class="fw-arw" style="position:absolute; left:${x + cellW}px; top:${y + 36}px;
          width:${gap}px; height:12px; display:flex; align-items:center; opacity:0;">
          <div style="flex:1; height:2px; background:${C.primary}; opacity:.5;"></div>
          <div style="width:0;height:0;border-top:6px solid transparent;
            border-bottom:6px solid transparent;border-left:8px solid ${C.primary};"></div>
        </div>` : '';
      return `
        <div class="fw-stp" style="position:absolute; left:${x}px; top:${y}px; width:${cellW}px;
          text-align:center;">
          <div style="display:flex; justify-content:center;">${ic}</div>
          <div style="font-family:${F.heading}; font-weight:700; font-size:19px; letter-spacing:.5px;
            text-transform:uppercase; color:${C.text_heading}; margin-top:18px; line-height:1.25;">
            ${s.label}</div>
          ${s.note ? `<div style="font-size:17px; color:${C.text_muted}; margin-top:9px;
            line-height:1.35;">${s.note}</div>` : ''}
        </div>${arrow}`;
    }).join('');

    stage.innerHTML = FW.page(brand, `
      ${bg}
      ${FW.logoCorner(brand, 38)}
      ${data.kicker ? `<div class="fw-kick" style="position:absolute; top:210px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:600; font-size:26px;
        letter-spacing:2.4px; text-transform:uppercase; color:${C.primary};">${data.kicker}</div>` : ''}
      ${data.headline ? `<div class="fw-head" style="position:absolute; top:262px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:700; font-size:58px;
        color:${C.text_heading};">${data.headline}</div>` : ''}
      ${items}`);

    const tl = gsap.timeline({paused: true});
    if (data.bg) tl.to('.fw-bg', {opacity: 1, duration: 1.1, ease: 'power2.out'}, 0);
    if (data.kicker) tl.from('.fw-kick', {opacity: 0, y: -14, duration: 0.6}, 0);
    if (data.headline) tl.from('.fw-head', {opacity: 0, y: 18, duration: 0.7}, 0.15);
    // Hien dan tung buoc. `cueTimes` = GIAY THU MAY giong doc goi ten tung buoc (build_seq
    // tinh tu vi tri am tiet trong doan loi). Co cueTimes thi moi buoc cho dung luc giong
    // goi ten no - luat Lien 19/10: "dong chay dang nhanh hon giong doc".
    const cue = data.cueTimes;
    const step = data.reveal === false ? 0 : 0.42;
    if (cue && cue.length === steps.length) {
      const els = stage.querySelectorAll('.fw-stp');
      const arw = stage.querySelectorAll('.fw-arw');
      els.forEach((el, i) => {
        tl.from(el, {opacity: 0, y: 26, scale: 0.94, duration: 0.5,
          ease: 'back.out(1.6)'}, Math.max(0.3, cue[i]));
        if (arw[i]) tl.to(arw[i], {opacity: 1, duration: 0.3},
          Math.max(0.3, cue[i]) + 0.35);
      });
    } else {
      tl.from('.fw-stp', {opacity: 0, y: 26, scale: 0.94, duration: 0.55,
        ease: 'back.out(1.6)', stagger: step}, 0.5);
      tl.to('.fw-arw', {opacity: 1, duration: 0.3, stagger: step}, 0.5 + step * 0.75);
    }
    return tl;
  };
})();
