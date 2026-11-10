// _fw.js - lop dung chung cho bo canh CHUAN FORWARDER (nap tu dong truoc moi canh).
//
// Chuan lay tu clip "V61. Viindoo Freight Management" (129s, 1920x1080) - Lien chot lam mau:
//   nen TRANG + luoi mo, nhan teal gan don sac, chu it, minh hoa nguoi ve phang mang cam xuc,
//   man phan mem that mang bang chung, va MOT THANH BUOC chay suot de nguoi xem luon biet
//   dang o dau trong dong chay nghiep vu.
//
// Moi canh fw* goi cac ham duoi day. Khong go chu "Viindoo" bang tay - dung FW.logo().
(function () {
  if (window.FW) return;

  const FW = {};

  // ---- nen trang + luoi mo (dau an thi giac cua clip chuan) -------------------
  FW.page = (brand, inner, opt = {}) => {
    const C = brand.colors, F = brand.fonts;
    const grid = opt.grid === false ? '' : `
      background-image:
        linear-gradient(rgba(0,187,206,.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,187,206,.055) 1px, transparent 1px);
      background-size: 48px 48px;`;
    return `<div class="fw-root" style="position:absolute; inset:0; background:${C.white};
      font-family:${F.body}; color:${C.text_body}; overflow:hidden;${grid}">${inner}</div>`;
  };

  // ---- logo goc (SVG trong <plugin>/brand/assets), KHONG go chu --------------------------------
  FW.logo = (brand, h) => {
    const C = brand.colors;
    return (brand.logo && brand.logo.svg)
      ? brand.logo.svg.replace('<svg ',
          `<svg style="height:${h}px;width:auto;display:inline-block;vertical-align:middle;" `)
      : `<span style="font-weight:700;font-size:${h}px">
           <span style="color:${C.primary}">Viin</span><span style="color:${C.secondary}">doo</span></span>`;
  };

  FW.logoCorner = (brand, h = 40) =>
    `<div class="fw-logo" style="position:absolute; top:46px; left:64px;">${FW.logo(brand, h)}</div>`;

  // ---- THANH BUOC: xuong song cua cach ke theo dong chay nghiep vu -------------
  // steps = ['Yeu cau khach hang','Bao gia',...]; active = chi so dang noi (tu 0)
  FW.stepbar = (brand, steps, active) => {
    if (!steps || !steps.length) return '';
    const C = brand.colors, F = brand.fonts;
    const cells = steps.map((s, i) => {
      const on = i === active;
      return `<div class="fw-step ${on ? 'fw-step-on' : ''}" style="flex:1; text-align:center;
        font-family:${F.heading}; font-weight:${on ? 700 : 500}; font-size:19px; letter-spacing:.6px;
        text-transform:uppercase; line-height:1.25; padding:0 10px;
        color:${on ? C.primary : '#9AA6AC'};">
        ${on ? `<div style="width:0;height:0;margin:0 auto 7px;
                 border-left:7px solid transparent;border-right:7px solid transparent;
                 border-top:8px solid ${C.primary};"></div>`
             : '<div style="height:15px"></div>'}
        ${s}</div>`;
    }).join('');
    return `<div class="fw-stepbar" style="position:absolute; top:52px; left:0; right:0;
      display:flex; align-items:flex-start; padding:0 70px;">${cells}</div>`;
  };

  // ---- con tro chuot (luat 18/10: man phan mem phai co con tro) ----------------
  FW.cursor = (x, y) => `
    <svg class="fw-cursor" width="34" height="34" viewBox="0 0 24 24"
      style="position:absolute; left:${x}px; top:${y}px; z-index:60;
      filter:drop-shadow(0 3px 6px rgba(0,0,0,.45));">
      <path d="M5 2 L5 20 L10 15.5 L13 22 L16 20.5 L13 14.5 L19.5 14.5 Z"
        fill="#fff" stroke="#21272B" stroke-width="1.4" stroke-linejoin="round"/></svg>`;

  // ---- khung anh man hinh: toan khung co do bong, hoac long trong laptop -------
  // Ve anh man hinh. Co opt.zoom + opt.nat -> PHONG vao dung vung can xem:
  // anh duoc phong to roi dich chuyen sao cho vung do lap kin o `box`.
  FW.screen = (shot, box, opt = {}) => {
    const r = opt.radius != null ? opt.radius : 10;
    const shell = `position:absolute; left:${box.x}px; top:${box.y}px;
      width:${box.w}px; height:${box.h}px; border-radius:${r}px; overflow:hidden;
      box-shadow:0 26px 70px rgba(19,60,70,.26); border:1px solid rgba(19,60,70,.10);
      background:#fff;`;
    if (opt.zoom && opt.nat) {
      // Anh nam trong o cat (overflow hidden). Dat anh theo KHUNG NGAM dau tien (opt.cam
      // neu co, khong thi chinh opt.zoom) de canh co the KEO MAY QUAY sang khung khac.
      const kf = opt.cam || opt.zoom;
      const s = box.w / kf.w;
      return `<div class="fw-shot" style="${shell}">
        <img class="fw-cam" src="${shot}" style="position:absolute;
          left:${-kf.x * s}px; top:${-kf.y * s}px;
          width:${opt.nat.w * s}px; height:${opt.nat.h * s}px; max-width:none;"></div>`;
    }
    return `<img class="fw-shot" src="${shot}" style="${shell}
      object-fit:${opt.fit || 'cover'}; object-position:top center;">`;
  };

  // laptop mockup: tra ve {html, screen:{x,y,w,h}} de canh dat anh vao dung o
  FW.laptop = (box) => {
    const bw = box.w, scrW = Math.round(bw * 0.845), scrH = Math.round(scrW * 0.6);
    const scrX = box.x + Math.round((bw - scrW) / 2), scrY = box.y + Math.round(bw * 0.035);
    const baseY = scrY + scrH + 12;
    return {
      screen: {x: scrX, y: scrY, w: scrW, h: scrH},
      html: `
        <div style="position:absolute; left:${scrX - 14}px; top:${scrY - 14}px;
          width:${scrW + 28}px; height:${scrH + 28}px; background:#DFE5E8;
          border-radius:16px; box-shadow:0 30px 70px rgba(19,60,70,.28);"></div>
        <div style="position:absolute; left:${box.x}px; top:${baseY}px; width:${bw}px; height:17px;
          background:linear-gradient(#E9EEF0,#C9D2D6); border-radius:0 0 14px 14px;"></div>
        <div style="position:absolute; left:${box.x + bw / 2 - 52}px; top:${baseY}px;
          width:104px; height:7px; background:#AEBAC0; border-radius:0 0 7px 7px;"></div>`,
    };
  };

  // ---- NHAN VAO CON SO (luat Lien 18/10/2026) ---------------------------------
  // Lam toi ca man tru vung so, khoanh vong cyan, roi keo so ra chu to kem 1 cau nghia.
  // focus = {x,y,w,h} TOA DO TREN ANH GOC; scale = ti le anh da thu nho.
  // `org` = goc toa do anh (da tinh ca phan phong); `box` chi dung de biet vung anh.
  FW.focus = (brand, org, focus, scale, box) => {
    const C = brand.colors;
    const fx = org.x + focus.x * scale, fy = org.y + focus.y * scale;
    const fw = focus.w * scale, fh = focus.h * scale;
    const pad = 10;
    // mot the duy nhat: box-shadow lan rong 9999px lam toi CA KHUNG, chua o so lai sang
    return `
      <div class="fw-hole" style="position:absolute; left:${fx - pad}px; top:${fy - pad}px;
        width:${fw + pad * 2}px; height:${fh + pad * 2}px; border-radius:8px;
        box-shadow:0 0 0 9999px rgba(12,32,38,.62); opacity:0;"></div>
      <div class="fw-ring" style="position:absolute; left:${fx - pad}px; top:${fy - pad}px;
        width:${fw + pad * 2}px; height:${fh + pad * 2}px; border-radius:8px;
        border:3px solid ${C.primary}; box-shadow:0 0 0 5px rgba(0,187,206,.26);
        opacity:0; z-index:55;"></div>`;
  };

  FW.callout = (brand, x, y, number, meaning, w) => {
    const C = brand.colors, F = brand.fonts;
    return `<div class="fw-callout" style="position:absolute; left:${x}px; top:${y}px;
      width:${w || 620}px; opacity:0; z-index:58;">
      <div style="font-family:${F.heading}; font-weight:700; font-size:92px; line-height:1;
        color:${C.primary};">${number}</div>
      ${meaning ? `<div style="font-size:28px; color:${C.text_heading}; margin-top:14px;
        line-height:1.35; font-weight:500;">${meaning}</div>` : ''}</div>`;
  };

  // ---- nhip chung: fade/truot nhe, hieu ung chi phuc vu noi dung --------------
  FW.inUp = (tl, sel, at, opt = {}) =>
    tl.from(sel, {opacity: 0, y: opt.y || 26, duration: opt.d || 0.7, ease: 'power3.out',
                  stagger: opt.stagger || 0}, at);

  window.FW = FW;
})();
