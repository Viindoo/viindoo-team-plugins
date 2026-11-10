// Scene: fwtwo - HAI (hoac N) MUC DICH / TRU COT, dat TRUOC phan dong chay nghiep vu.
//
// Luat Lien 19/10/2026: phai di cai TONG THE xong moi lay vi du cu the de CHUNG MINH muc dich.
// Canh nay la phan "tong the": no neu ro ap dung phan mem de LAM GI, roi cac canh `fwscreen`
// phia sau moi lan luot chung minh tung muc dich bang so that tren man hinh.
//
// data = {
//   kicker?, headline?,
//   pillars: [{tag, title, note?, icon?,
//              icons?: [{icon,label}],                    // mot dai icon
//              groups?: [{label?, muted?, icons:[...]}]}], // HOAC nhieu nhom co nhan
//   sub?
// }
// Luat Lien 19/10: canh tong ket khac biet phai XEP ICON THEO HAI TIEU CHI Quan / Xay
// -> dung `groups`, moi nhom mot nhan.
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fwtwo'] = function (stage, data, brand, gsap) {
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const ps = data.pillars || [];
    const n = Math.max(ps.length, 1);
    const gap = 60;
    const cardW = Math.min(680, Math.floor((1920 - 240 - gap * (n - 1)) / n));
    const totalW = cardW * n + gap * (n - 1);
    const x0 = Math.round((1920 - totalW) / 2);
    const y = 352, cardH = 560;

    const cards = ps.map((p, i) => {
      const x = x0 + i * (cardW + gap);
      const accent = i % 2 === 0 ? C.primary : C.secondary;
      const ic = p.icon
        ? `<img src="${p.icon}" style="width:76px;height:76px;object-fit:contain;">`
        : `<div style="width:76px;height:76px;border-radius:18px;background:${accent};"></div>`;
      return `
        <div class="fw-pil" style="position:absolute; left:${x}px; top:${y}px;
          width:${cardW}px; height:${cardH}px; background:${C.white};
          border:2px solid rgba(19,60,70,.10); border-left:8px solid ${accent};
          border-radius:18px; box-shadow:0 22px 56px rgba(19,60,70,.13); padding:34px 36px;">
          ${ic}
          <div style="display:inline-block; margin-top:26px; background:${accent}; color:${C.white};
            font-family:${F.heading}; font-weight:700; font-size:20px; letter-spacing:1.6px;
            text-transform:uppercase; padding:7px 18px; border-radius:999px;">${p.tag || ''}</div>
          <div style="font-family:${F.heading}; font-weight:700; font-size:34px; line-height:1.2;
            color:${C.text_heading}; margin-top:16px;">${p.title || ''}</div>
          ${p.note ? `<div style="font-size:22px; color:${C.text_muted}; margin-top:12px;
            line-height:1.4;">${p.note}</div>` : ''}
          ${(p.groups || (p.icons ? [{icons: p.icons}] : [])).map(g => `
            <div style="margin-top:20px;">
              ${g.label ? `<div style="font-family:${F.heading}; font-weight:700; font-size:16px;
                letter-spacing:1.6px; text-transform:uppercase; color:${accent};
                margin-bottom:9px;">${g.label}</div>` : ''}
              <div class="fw-ics" style="display:flex; flex-wrap:wrap; gap:12px 14px;">
                ${(g.icons || []).map(ic => `
                  <div style="width:74px; text-align:center;">
                    <img src="${ic.icon}" style="width:46px;height:46px;object-fit:contain;
                      border-radius:11px; box-shadow:0 5px 14px rgba(19,60,70,.16);
                      ${g.muted ? 'filter:grayscale(1); opacity:.55;' : ''}">
                    <div style="font-size:13px; line-height:1.15; margin-top:6px; height:30px;
                      overflow:hidden; color:${C.text_muted};">${ic.label || ''}</div>
                  </div>`).join('')}
              </div>
            </div>`).join('')}
        </div>`;
    }).join('');

    stage.innerHTML = FW.page(brand, `
      ${FW.logoCorner(brand, 38)}
      ${data.kicker ? `<div class="fw-k" style="position:absolute; top:200px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:600; font-size:26px;
        letter-spacing:2.4px; text-transform:uppercase; color:${C.primary};">${data.kicker}</div>` : ''}
      ${data.headline ? `<div class="fw-h" style="position:absolute; top:252px; left:0; right:0;
        text-align:center; font-family:${F.heading}; font-weight:700; font-size:56px;
        color:${C.text_heading};">${data.headline}</div>` : ''}
      ${cards}
      ${data.sub ? `<div class="fw-s" style="position:absolute; bottom:92px; left:0; right:0;
        text-align:center; font-size:27px; color:${C.text_muted};">${data.sub}</div>` : ''}`);

    // The khung cao co dinh nen ban tieng Anh (nhan dai hon, vi du "Business trips" xuong
    // hai dong) bi TRAN CHU RA NGOAI khung trang. Do lai chieu cao that cua tung the roi
    // keo CA HAI the len bang nhau - de ngon ngu nao cung vua, khong phai cat bot chu.
    {
      // Do bang day cua CON CUOI CUNG chu khong dung scrollHeight: khung de overflow
      // visible thi scrollHeight khong chac ke phan tran ra.
      const pil = [...stage.querySelectorAll('.fw-pil')];
      const can = pil.map(el => {
        const con = [...el.children];
        if (!con.length) return cardH;
        const day = Math.max(...con.map(c => c.getBoundingClientRect().bottom));
        const dem = parseFloat(getComputedStyle(el).paddingBottom) || 0;
        return day - el.getBoundingClientRect().top + dem;
      });
      const cao = Math.ceil(Math.max(cardH, ...can));
      if (cao > cardH) pil.forEach(el => { el.style.height = cao + 'px'; });
    }

    const tl = gsap.timeline({paused: true});
    if (data.kicker) tl.from('.fw-k', {opacity: 0, y: -14, duration: 0.6}, 0);
    if (data.headline) tl.from('.fw-h', {opacity: 0, y: 18, duration: 0.7}, 0.15);
    // `cueTimes` = luc giong doc goi ten tung tru cot ("thu nhat", "thu hai") - the cho
    // dung luc do moi hien ra, khong chay truoc tieng (luat Lien 19/10).
    const cue = data.cueTimes;
    if (cue && cue.length === ps.length) {
      stage.querySelectorAll('.fw-pil').forEach((el, i) => {
        tl.from(el, {opacity: 0, y: 40, duration: 0.7, ease: 'power3.out'},
          Math.max(0.55, cue[i]));
      });
    } else {
      tl.from('.fw-pil', {opacity: 0, y: 40, duration: 0.8, ease: 'power3.out',
        stagger: 0.75}, 0.55);
    }
    tl.from('.fw-ics img', {opacity: 0, scale: 0.5, duration: 0.45,
      ease: 'back.out(2)', stagger: 0.05}, 2.0);
    if (data.sub) tl.from('.fw-s', {opacity: 0, duration: 0.6}, 2.9);
    return tl;
  };
})();
