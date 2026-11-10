// KHONG DUNG CHO CLIP MOI (Lien 09/11/2026): hinh ve nguoi + vong tron cong cu "xau qua, trinh bay
// khac di, bo het ca o cac clip sau". Canh noi dau nay = NGUOI THAT toan khung + nhan chu (mau:
// templates/clips/dung_noi_dau.py + noi_dau_chu.html cua skill viindoo-video-cum-nghiep-vu). Giu file nay chi de dung lai clip cu.
//
// Scene: fwpain - MO BAI BANG NOI DAU, ke bang HINH VE NGUOI (chuan forwarder).
// Clip mau mo bang canh nguoi that su dang khon kho (giay to chat dong, dien thoai reo),
// roi cho cac CONG CU ROI RAC (Excel, email, Zalo, Messenger, dien thoai, fax) bua vay
// noi bang nhung duong roi. Chu rat it - hinh mang cam xuc, khong phai chu.
//
// data = {
//   label?,                       // nhan lon kieu "BAO GIA ROI RAC"
//   image?,                       // anh minh hoa nguoi (engine nhung thanh data URI)
//   orbit?: [{text?, icon?}],     // cong cu roi rac bua quanh; <= 6 cai
//   sub?
// }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwpain'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const cx = 960, cy = 600, rx = 560, ry = 300;
    const orbit = (data.orbit || []).slice(0, 6);

    const bubbles = orbit.map((o, i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / Math.max(orbit.length, 1);
      const x = Math.round(cx + rx * Math.cos(a)) - 56;
      const y = Math.round(cy + ry * Math.sin(a)) - 56;
      const inner = o.icon
        ? `<img src="${o.icon}" style="width:56px;height:56px;object-fit:contain;">`
        : `<span style="font-family:${F.heading};font-weight:700;font-size:21px;
             color:${C.white};text-align:center;line-height:1.1;">${o.text || ''}</span>`;
      return `<div class="fw-orb" style="position:absolute; left:${x}px; top:${y}px;
        width:112px; height:112px; border-radius:50%; background:${C.primary};
        display:flex; align-items:center; justify-content:center; opacity:0;
        box-shadow:0 12px 30px rgba(0,187,206,.30);">${inner}</div>`;
    }).join('');

    const img = data.image
      ? `<img class="fw-illu" src="${data.image}" style="position:absolute; left:${cx - 430}px;
          top:${cy - 240}px; width:860px; height:480px; object-fit:contain;">`
      : `<div class="fw-illu" style="position:absolute; left:${cx - 430}px; top:${cy - 240}px;
          width:860px; height:480px; border-radius:20px; background:${C.grey_light_bg};
          display:flex; align-items:center; justify-content:center; color:${C.text_muted};
          font-size:24px;">[ thiếu ảnh minh hoạ người ]</div>`;

    stage.innerHTML = FW.page(brand, `
      ${FW.logoCorner(brand, 38)}
      ${data.label ? `<div class="fw-lbl" style="position:absolute; top:150px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:700; font-size:52px;
        letter-spacing:1px; text-transform:uppercase; color:${C.primary};">${data.label}</div>` : ''}
      ${img}${bubbles}
      ${data.sub ? `<div class="fw-sub" style="position:absolute; bottom:90px; left:0; right:0;
        text-align:center; font-size:28px; color:${C.text_muted};">${data.sub}</div>` : ''}`);

    const tl = gsap.timeline({paused: true});
    tl.from('.fw-illu', {opacity: 0, scale: 0.96, duration: 0.9, ease: 'power3.out'}, 0);
    if (data.label) tl.from('.fw-lbl', {opacity: 0, y: -18, duration: 0.7}, 0.3);
    // cong cu roi rac bua vay dan - cang ve sau cang ngop
    tl.to('.fw-orb', {opacity: 1, duration: 0.45, stagger: 0.22, ease: 'back.out(2)'}, 1.0);
    tl.from('.fw-orb', {scale: 0.4, duration: 0.5, stagger: 0.22, ease: 'back.out(2)'}, 1.0);
    if (data.sub) tl.from('.fw-sub', {opacity: 0, duration: 0.6}, 1.9);
    return tl;
  };
})();
