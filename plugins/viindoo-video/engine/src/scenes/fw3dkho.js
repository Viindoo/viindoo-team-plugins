// Scene: fw3dkho - MO PHONG 3D kho tu dong: bang chuyen, cong RFID, tu PLC, du lieu chay ve
// man hinh Viindoo (so ton kho tang khi cong doc the). Lien 09/11/2026: "dang mo hinh mo phong 3D"
// cho doan RFID / bang chuyen / PLC - cac phan nay TICH HOP THEO THIET KE RIENG cua tung doanh
// nghiep, nen goc canh LUON co nhan "Mo phong - tich hop theo thiet ke rieng".
//
// Can three.js (sequence.mjs tu nap vendor/three-0.160.0.min.js cho canh ten fw3d*) va WebGL
// phan mem (co --enable-unsafe-swiftshader). Moi khung la ham THUAN cua thoi gian t: timeline
// gsap chi day state.t, render() dung lai toan canh tu t -> tua toi lui deu cho ra cung mot hinh.
//
// data = {
//   tag?:        nhan goc ("Mo phong - tich hop theo thiet ke rieng"),
//   labels?:     {rfid, plc, conveyor, screen},
//   stockLabel?: chu tren man hinh ("Ton kho"),
//   unit?:       don vi sau so ("thung"),
//   stockStart?: so ton ban dau (mac dinh 1186),
//   duration?:   do dai canh (mac dinh 9)
// }
(function () {
  window.SCENES = window.SCENES || {};
  window.SCENES['fw3dkho'] = function (stage, data, brand, gsap) {
    const THREE = window.THREE;
    const C = brand.colors, F = brand.fonts, FW = window.FW;
    const W = 1920, H = 1080;
    const DUR = data.duration || 9;
    const L = Object.assign({rfid: 'Cổng RFID', plc: 'Tủ PLC', conveyor: 'Băng chuyền',
      screen: 'Viindoo'}, data.labels || {});
    const TAG = data.tag || 'Mô phỏng - tích hợp theo thiết kế riêng';
    const STOCK_LABEL = data.stockLabel || 'Tồn kho';
    const UNIT = data.unit || 'thùng';
    const STOCK0 = data.stockStart != null ? data.stockStart : 1186;
    const col = (h) => new THREE.Color(h);

    // ---------- khung HTML: canvas 3D + logo + nhan goc + nhan bam theo vat the ----------
    stage.innerHTML = FW.page(brand, `
      <canvas id="k3d" width="${W}" height="${H}" style="position:absolute;inset:0;"></canvas>
      <div id="k3fade" style="position:absolute;inset:0;background:${C.white};"></div>
      <div style="position:absolute;top:30px;left:46px;width:224px;height:72px;border-radius:14px;background:rgba(255,255,255,.96);box-shadow:0 8px 24px rgba(33,39,43,.12);"></div>
      ${FW.logoCorner(brand, 40)}
      <div id="k3tag" style="position:absolute; right:64px; bottom:56px; padding:12px 22px;
        border-radius:999px; background:rgba(255,255,255,.92); border:2px solid ${C.primary};
        font-family:${F.heading}; font-weight:600; font-size:24px; color:${C.text_heading};
        box-shadow:0 8px 24px rgba(33,39,43,.10);">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;
          background:${C.primary};margin-right:10px;vertical-align:middle;"></span>${TAG}</div>
      ${['rfid', 'plc', 'conveyor'].map(k => `<div class="k3lbl" id="k3l-${k}"
        style="position:absolute; left:0; top:0; transform:translate(-50%,-100%);
        padding:10px 18px; border-radius:10px; background:${C.text_heading}; color:#fff;
        font-family:${F.heading}; font-weight:600; font-size:24px; white-space:nowrap;
        opacity:0; box-shadow:0 10px 26px rgba(33,39,43,.22);">${L[k]}
        <div style="position:absolute;left:50%;bottom:-9px;margin-left:-9px;width:0;height:0;
          border-left:9px solid transparent;border-right:9px solid transparent;
          border-top:9px solid ${C.text_heading};"></div></div>`).join('')}
      <svg id="k3tline" width="${W}" height="${H}" style="position:absolute;inset:0;pointer-events:none;opacity:0">
        <line id="k3tl" x1="0" y1="0" x2="0" y2="0" stroke="${C.primary}" stroke-width="3"/>
        <circle id="k3tc" cx="0" cy="0" r="7" fill="${C.primary}"/></svg>
      <div id="k3tab" style="position:absolute; right:150px; top:250px; width:520px; height:340px; opacity:0;
        border-radius:30px; background:#21272B; padding:18px; box-shadow:0 24px 60px rgba(33,39,43,.30);">
        <div style="width:100%;height:100%;border-radius:16px;background:#fff;position:relative;overflow:hidden;
          font-family:${F.heading};">
          <div style="height:10px;background:${C.primary};"></div>
          <div style="position:absolute;left:28px;top:30px;height:36px;">${FW.logo(brand, 34)}</div>
          <div style="position:absolute;left:30px;top:96px;font-weight:600;font-size:28px;color:#6B6D70;">${STOCK_LABEL}</div>
          <div id="k3tnum" style="position:absolute;left:26px;top:128px;font-weight:700;font-size:110px;line-height:1;color:#21272B;">${STOCK0.toLocaleString('vi-VN')}</div>
          <div style="position:absolute;left:30px;top:252px;font-weight:600;font-size:28px;color:${C.primary};">${UNIT}</div>
        </div></div>`, {grid: false});

    const canvas = stage.querySelector('#k3d');
    const renderer = new THREE.WebGLRenderer({canvas, antialias: true, preserveDrawingBuffer: true});
    renderer.setPixelRatio(1);
    renderer.setSize(W, H, false);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.NoToneMapping;

    const scene = new THREE.Scene();
    scene.background = col('#F3F6F7');

    // camera truc giao goc isometric, truot nhe trong suot canh
    const VIEW = 15.5;
    const cam = new THREE.OrthographicCamera(-VIEW * W / H / 2, VIEW * W / H / 2, VIEW / 2, -VIEW / 2, 0.1, 200);

    // anh sang mem + bong do
    scene.add(new THREE.HemisphereLight(0xffffff, 0xe6eef0, 1.55));
    const sun = new THREE.DirectionalLight(0xffffff, 1.25);
    sun.position.set(-12, 22, 14);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    Object.assign(sun.shadow.camera, {left: -20, right: 20, top: 20, bottom: -20, near: 1, far: 70});
    sun.shadow.radius = 4;
    sun.shadow.bias = -0.0005;
    scene.add(sun);

    const mat = (c, o = {}) => new THREE.MeshStandardMaterial(Object.assign({color: col(c), roughness: 0.7, metalness: 0.05}, o));
    const box = (w, h, d, m, x, y, z, shadow = true) => {
      const me = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
      me.position.set(x, y, z); me.castShadow = shadow; me.receiveShadow = true;
      scene.add(me); return me;
    };

    // ---------- QUANG CANH NHA XUONG / KHO (Lien 09/11: thay nen trang trong) ----------
    // san be tong sang, vach di bo teal, hai buc tuong + khung thep, cua nhap hang, ke cao,
    // xe nang + pallet, den nha xuong. Tong trang + teal Viindoo.
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), mat('#EDF1F2', {roughness: 0.95}));
    floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
    const lineM = mat(C.primary, {roughness: 0.6});
    const fl = (w, d, x, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, 0.012, d), lineM);
      m.position.set(x, 0.006, z); m.receiveShadow = true; scene.add(m); };
    fl(30, 0.12, -1, 3.4); fl(30, 0.12, -1, -2.9);            // loi di hai ben bang chuyen
    fl(0.12, 12, -13.2, -3.8);                                 // vach truoc cua nhap hang
    for (let i = 0; i < 6; i++) fl(0.7, 0.12, -14.6 + i * 0.0, -8.6 + i * 1.6);  // vach cheo khu xe nang
    const wallM = mat('#F8FAFA', {roughness: 0.9});
    const bandM = mat(C.primary, {roughness: 0.6});
    const steelM = mat('#C9D3D6', {metalness: 0.4, roughness: 0.45});
    const WZ = -11.2, WX = -15.6, WH = 7.2;
    box(32, WH, 0.3, wallM, 0, WH / 2, WZ, false);            // tuong sau
    box(0.3, WH, 26, wallM, WX, WH / 2, 1.8, false);           // tuong trai
    box(32, 0.5, 0.32, bandM, 0, 0.25, WZ + 0.02, false);      // chan tuong teal
    box(0.32, 0.5, 26, bandM, WX + 0.02, 0.25, 1.8, false);
    for (let x = -14; x <= 15; x += 4.6) box(0.4, WH, 0.4, steelM, x, WH / 2, WZ + 0.3, false);   // cot thep
    for (let z = -9; z <= 14; z += 4.6) box(0.4, WH, 0.4, steelM, WX + 0.3, WH / 2, z, false);
    box(32, 0.35, 0.4, steelM, 0, WH - 0.2, WZ + 0.3, false);  // dam mai
    box(0.4, 0.35, 26, steelM, WX + 0.3, WH - 0.2, 1.8, false);
    // cua nhap hang (cua cuon) tren tuong trai
    const DZ = -4.8;
    box(0.12, 4.4, 4.6, mat('#DCE3E5', {metalness: 0.3, roughness: 0.5}), WX + 0.2, 2.2, DZ, false);
    for (let y = 0.3; y < 4.4; y += 0.32) box(0.14, 0.04, 4.5, mat('#C3CDD0'), WX + 0.24, y, DZ, false);
    box(0.3, 0.3, 5.2, bandM, WX + 0.25, 4.55, DZ, false);
    box(0.5, 0.5, 0.25, mat('#2C3338'), WX + 0.35, 0.4, DZ - 2.45, false);   // dem chan cua
    box(0.5, 0.5, 0.25, mat('#2C3338'), WX + 0.35, 0.4, DZ + 2.45, false);
    // den nha xuong (den treo cao)
    const lampM = new THREE.MeshStandardMaterial({color: col('#FFFFFF'), emissive: col('#FFFFFF'), emissiveIntensity: 0.9});
    for (const [lx, lz] of [[-9, -9.6], [-3, -9.6], [2, -9.6]]) {
      box(0.03, 1.2, 0.03, steelM, lx, WH - 0.8, lz, false);
      const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.75, 0.45, 24, 1, true), mat('#AEB9BD', {metalness: 0.5, side: THREE.DoubleSide}));
      sh.position.set(lx, WH - 1.55, lz); scene.add(sh);
      const bulb = new THREE.Mesh(new THREE.CircleGeometry(0.7, 24), lampM);
      bulb.rotation.x = Math.PI / 2; bulb.position.set(lx, WH - 1.76, lz); scene.add(bulb);
    }
    // xe nang + pallet canh cua nhap hang
    const fk = new THREE.Group(); fk.position.set(-12.2, 0, -0.6); fk.rotation.y = -0.5; scene.add(fk);
    const fkPart = (w, h, d, m, x, y, z) => { const me = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
      me.position.set(x, y, z); me.castShadow = true; me.receiveShadow = true; fk.add(me); return me; };
    const fkBody = mat(C.primary, {roughness: 0.45}), fkDark = mat('#2C3338', {roughness: 0.7});
    fkPart(1.4, 0.9, 2.2, fkBody, 0, 0.75, 0);
    fkPart(1.3, 0.12, 1.3, fkDark, 0, 2.55, -0.1);
    for (const sx of [-0.6, 0.6]) for (const sz of [-0.6, 0.45]) fkPart(0.08, 1.8, 0.08, fkDark, sx, 1.65, sz);
    fkPart(0.12, 2.6, 0.12, fkDark, -0.35, 1.3, 1.2); fkPart(0.12, 2.6, 0.12, fkDark, 0.35, 1.3, 1.2);
    fkPart(0.14, 0.06, 1.2, mat('#8C969A'), -0.3, 0.12, 1.85); fkPart(0.14, 0.06, 1.2, mat('#8C969A'), 0.3, 0.12, 1.85);
    for (const [wx, wz] of [[-0.72, -0.7], [0.72, -0.7], [-0.72, 0.7], [0.72, 0.7]]) {
      const wh = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.28, 20), fkDark);
      wh.rotation.z = Math.PI / 2; wh.position.set(wx, 0.32, wz); wh.castShadow = true; fk.add(wh);
    }
    const palM = mat('#C9A27A', {roughness: 0.85});
    for (const [px, pz, n] of [[-12.6, -8.2, 2], [-10.8, -8.2, 1]]) {
      box(1.3, 0.16, 1.3, palM, px, 0.08, pz);
      for (let i = 0; i < n; i++) box(1.15, 0.8, 1.15, mat(i % 2 ? '#D8B48C' : '#CDA67C'), px, 0.56 + i * 0.82, pz);
    }

    // ---------- bang chuyen ----------
    const CX0 = -11, CX1 = 9, CZ = 0, CW = 1.6, CH = 0.95;
    const frameM = mat('#E3E9EB', {metalness: 0.3, roughness: 0.45});
    const beltM = mat('#2C3338', {roughness: 0.85});
    box(CX1 - CX0, 0.18, CW + 0.25, frameM, (CX0 + CX1) / 2, CH - 0.05, CZ);
    const belt = box(CX1 - CX0, 0.05, CW, beltM, (CX0 + CX1) / 2, CH + 0.06, CZ, false);
    for (let x = CX0 + 0.6; x < CX1; x += 2.2) {
      box(0.12, CH - 0.1, 0.12, frameM, x, (CH - 0.1) / 2, CZ - CW / 2);
      box(0.12, CH - 0.1, 0.12, frameM, x, (CH - 0.1) / 2, CZ + CW / 2);
    }
    // vach teal hai mep bang chuyen
    box(CX1 - CX0, 0.06, 0.06, mat(C.primary, {roughness: 0.4}), (CX0 + CX1) / 2, CH + 0.06, CZ - CW / 2 - 0.12, false);
    box(CX1 - CX0, 0.06, 0.06, mat(C.primary, {roughness: 0.4}), (CX0 + CX1) / 2, CH + 0.06, CZ + CW / 2 + 0.12, false);
    // vach chay tren mat bang (thay chuyen dong cua bang)
    const stripeM = mat('#3B444A', {roughness: 0.8});
    const stripes = [];
    for (let i = 0; i < 26; i++) stripes.push(box(0.08, 0.012, CW - 0.05, stripeM, 0, CH + 0.09, CZ, false));

    // ---------- thung hang ----------
    const SPEED = 1.6, GAP = 2.5, GATE_X = -1.2, NBOX = 11, PRE = 9.5;
    const cartonM = mat('#D8B48C', {roughness: 0.8});
    const tapeM = mat(C.primary, {roughness: 0.5});
    const tagM = mat('#FFFFFF', {roughness: 0.4});
    const boxes = [];
    for (let k = 0; k < NBOX; k++) {
      const g = new THREE.Group();
      const b = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.8, 1.0), cartonM);
      b.position.y = 0.4; b.castShadow = true; b.receiveShadow = true; g.add(b);
      const tp = new THREE.Mesh(new THREE.BoxGeometry(1.01, 0.81, 0.18), tapeM); tp.position.y = 0.4; g.add(tp);
      const tg = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.24, 0.02), tagM);
      tg.position.set(0.18, 0.45, 0.51); g.add(tg);
      g.position.set(0, CH + 0.085, CZ);
      scene.add(g); boxes.push(g);
    }
    const boxX = (k, t) => CX0 + SPEED * t + PRE - GAP * k;          // vi tri thung k luc t
    const readT = (k) => (GATE_X - CX0 - PRE + GAP * k) / SPEED;      // luc thung k qua cong

    // ---------- cong RFID ----------
    const gateM = mat('#FFFFFF', {roughness: 0.35, metalness: 0.1});
    const glowM = new THREE.MeshStandardMaterial({color: col(C.primary), emissive: col(C.primary),
      emissiveIntensity: 0.15, roughness: 0.3});
    const GH = 3.1;
    box(0.32, GH, 0.32, gateM, GATE_X, GH / 2, CZ - CW / 2 - 0.55);
    box(0.32, GH, 0.32, gateM, GATE_X, GH / 2, CZ + CW / 2 + 0.55);
    box(0.36, 0.34, CW + 1.5, gateM, GATE_X, GH, CZ);
    const pan1 = box(0.06, 1.9, 0.26, glowM, GATE_X + 0.17, 1.65, CZ - CW / 2 - 0.55, false);
    const pan2 = box(0.06, 1.9, 0.26, glowM, GATE_X + 0.17, 1.65, CZ + CW / 2 + 0.55, false);
    const pan3 = box(0.06, 0.16, CW + 1.1, glowM, GATE_X + 0.19, GH, CZ, false);
    // vong song doc the (ve tren mat phang dung)
    const ringM = new THREE.MeshBasicMaterial({color: col(C.primary), transparent: true, opacity: 0, side: THREE.DoubleSide});
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.9, 1.0, 64), ringM);
    ring.rotation.y = Math.PI / 2; ring.position.set(GATE_X, 1.55, CZ); scene.add(ring);
    const beamM = new THREE.MeshBasicMaterial({color: col(C.primary), transparent: true, opacity: 0, depthWrite: false});
    const beam = new THREE.Mesh(new THREE.BoxGeometry(0.5, GH - 0.25, CW + 0.9), beamM);
    beam.position.set(GATE_X, (GH - 0.25) / 2 + 0.05, CZ); scene.add(beam);

    // ---------- tu PLC ----------
    const PLC = new THREE.Vector3(-7.5, 0, -4.2);
    box(1.5, 2.6, 0.9, mat('#EEF2F3', {roughness: 0.5, metalness: 0.2}), PLC.x, 1.3, PLC.z);
    box(1.32, 2.3, 0.04, mat('#E2E8EA', {roughness: 0.4}), PLC.x, 1.35, PLC.z + 0.47);
    box(0.08, 2.3, 0.05, mat(C.primary), PLC.x - 0.55, 1.35, PLC.z + 0.49, false);
    const leds = [];
    for (let i = 0; i < 4; i++) {
      const lm = new THREE.MeshStandardMaterial({color: col('#00B365'), emissive: col('#00B365'), emissiveIntensity: 0.2});
      leds.push(box(0.12, 0.12, 0.04, lm, PLC.x - 0.2 + i * 0.2, 2.15, PLC.z + 0.5, false));
    }
    box(0.7, 0.45, 0.04, mat('#2C3338'), PLC.x + 0.15, 1.55, PLC.z + 0.5, false);
    // cap tu PLC toi bang chuyen (duong thap sat san)
    const cableCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(PLC.x + 0.4, 0.12, PLC.z + 0.4), new THREE.Vector3(PLC.x + 1.6, 0.06, -1.6),
      new THREE.Vector3(-5.5, 0.06, CZ - CW / 2 - 0.3), new THREE.Vector3(-5.5, 0.6, CZ - CW / 2 - 0.15)]);
    const cable = new THREE.Mesh(new THREE.TubeGeometry(cableCurve, 40, 0.05, 8), mat('#5B656B'));
    cable.castShadow = true; scene.add(cable);

    // ---------- man hinh Viindoo ----------
    const SCR = new THREE.Vector3(6.4, 0, -4.6);
    const scrG = new THREE.Group(); scrG.position.copy(SCR); scrG.rotation.y = 0.62; scene.add(scrG);
    const inG = (m) => { scene.remove(m); m.position.sub(SCR); scrG.add(m); return m; };
    inG(box(0.25, 1.9, 0.25, mat('#D5DDE0', {metalness: 0.4, roughness: 0.4}), SCR.x, 0.95, SCR.z));
    inG(box(1.4, 0.08, 0.9, mat('#D5DDE0', {metalness: 0.4, roughness: 0.4}), SCR.x, 0.04, SCR.z));
    inG(box(4.3, 2.75, 0.16, mat('#21272B', {roughness: 0.5}), SCR.x, 3.25, SCR.z));
    const tc = document.createElement('canvas'); tc.width = 1024; tc.height = 640;
    const tx = tc.getContext('2d');
    const tex = new THREE.CanvasTexture(tc); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
    const face = new THREE.Mesh(new THREE.PlaneGeometry(4.05, 2.53),
      new THREE.MeshBasicMaterial({map: tex, toneMapped: false}));
    face.position.set(0, 3.25, 0.085); scrG.add(face);
    const logoImg = new Image();
    if (brand.logo && brand.logo.svg) {
      logoImg.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(brand.logo.svg);
    }
    let lastDrawKey = '';
    function drawScreen(count, bump, on) {
      const key = count + '|' + bump.toFixed(2) + '|' + on.toFixed(2) + '|' + (logoImg.complete ? 1 : 0);
      if (key === lastDrawKey) return; lastDrawKey = key;
      tx.fillStyle = '#FFFFFF'; tx.fillRect(0, 0, 1024, 640);
      tx.globalAlpha = on;
      tx.fillStyle = C.primary; tx.fillRect(0, 0, 1024, 14);
      if (logoImg.complete && logoImg.naturalWidth) {
        const h = 64, w = h * logoImg.naturalWidth / logoImg.naturalHeight;
        tx.drawImage(logoImg, 56, 52, w, h);
      }
      tx.fillStyle = '#6B6D70'; tx.font = `600 52px ${F.heading}`;
      tx.fillText(STOCK_LABEL, 60, 220);
      const s = 1 + 0.12 * bump;
      tx.save(); tx.translate(56, 455); tx.scale(s, s);
      tx.fillStyle = '#21272B'; tx.font = `700 230px ${F.heading}`;
      tx.fillText(count.toLocaleString('vi-VN'), 0, 0); tx.restore();
      tx.fillStyle = C.primary; tx.font = `600 54px ${F.heading}`;
      tx.fillText(UNIT, 62, 560);
      // vach "song" nho: so lan doc vua nhan
      tx.fillStyle = 'rgba(0,187,206,' + (0.25 + 0.6 * bump) + ')';
      tx.beginPath(); tx.arc(940, 96, 18, 0, Math.PI * 2); tx.fill();
      tx.globalAlpha = 1;
      tex.needsUpdate = true;
    }

    // ---------- duong du lieu: cong RFID -> man hinh, tu PLC -> man hinh ----------
    const dataM = new THREE.MeshStandardMaterial({color: col(C.primary), emissive: col(C.primary),
      emissiveIntensity: 0.25, transparent: true, opacity: 0.55, roughness: 0.4});
    const curveGate = new THREE.CatmullRomCurve3([
      new THREE.Vector3(GATE_X, GH + 0.2, CZ), new THREE.Vector3(GATE_X + 1.2, GH + 2.0, -1.0),
      new THREE.Vector3(SCR.x - 2.4, GH + 1.9, SCR.z + 1.6), new THREE.Vector3(SCR.x - 1.55, 3.9, SCR.z + 1.15)]);
    const curvePlc = new THREE.CatmullRomCurve3([            // cap mang chay sat san (Lien: khong sat dinh ke)
      new THREE.Vector3(PLC.x + 0.45, 0.35, PLC.z + 0.5), new THREE.Vector3(PLC.x + 0.9, 0.08, PLC.z + 1.4),
      new THREE.Vector3(-2.0, 0.08, -2.45), new THREE.Vector3(3.6, 0.08, -2.45),
      new THREE.Vector3(SCR.x - 0.9, 0.08, SCR.z + 0.9), new THREE.Vector3(SCR.x - 0.15, 0.3, SCR.z + 0.15)]);
    const tubeGate = new THREE.Mesh(new THREE.TubeGeometry(curveGate, 80, 0.035, 8), dataM);
    const tubePlc = new THREE.Mesh(new THREE.TubeGeometry(curvePlc, 80, 0.035, 8), dataM.clone());
    scene.add(tubeGate, tubePlc);
    const pulseM = new THREE.MeshStandardMaterial({color: col(C.primary), emissive: col(C.primary), emissiveIntensity: 1.2});
    const pulses = [];
    for (let i = 0; i < 6; i++) {
      const p = new THREE.Mesh(new THREE.SphereGeometry(0.13, 20, 14), pulseM);
      p.visible = false; scene.add(p); pulses.push(p);
    }
    const plcPulses = [];
    for (let i = 0; i < 4; i++) {
      const p = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), pulseM);
      p.visible = false; scene.add(p); plcPulses.push(p);
    }

    // ---------- ke hang phia sau (boi canh kho) ----------
    const rackM = mat('#CFD8DB', {metalness: 0.3, roughness: 0.5});
    const rackBeamM = mat(C.primary, {roughness: 0.45});
    const stockM = [mat('#D8B48C'), mat('#CDA67C'), mat('#E2C29E')];
    [[-7.2, -8.9], [-3.2, -8.9], [0.8, -8.9], [4.8, -8.9]].forEach(([rx, rz], ri) => {
      for (const dx of [-1.7, 1.7]) for (const dz of [-0.6, 0.6]) box(0.12, 5.6, 0.12, rackM, rx + dx, 2.8, rz + dz);
      for (const y of [0.25, 1.65, 3.05, 4.45]) {
        box(3.5, 0.1, 0.12, rackBeamM, rx, y, rz + 0.6, false);
        box(3.5, 0.1, 0.12, rackBeamM, rx, y, rz - 0.6, false);
        box(3.5, 0.05, 1.2, rackM, rx, y + 0.02, rz, false);
        for (let j = 0; j < 3; j++) {
          if ((ri + j + Math.round(y)) % 4 === 3) continue;
          box(0.95, 0.75, 0.95, stockM[(j + ri) % 3], rx - 1.1 + j * 1.1, y + 0.43, rz);
        }
      }
    });

    // ---------- NHAN VIEN KHO cam MAY TINH BANG (Lien 09/11 yeu cau) ----------
    // low-poly gon: mu bao ho trang, ao phan quang teal soc bac, quan xam dam. Dung truoc bang
    // chuyen, quay mat vao bang chuyen (camera nhin qua vai thay man may tinh bang). Man may tinh
    // bang dung CHUNG texture voi man lon -> so ton kho tang dong bo.
    const WKP = new THREE.Vector3(2.0, 0, 2.55);
    const wk = new THREE.Group(); wk.position.copy(WKP); wk.rotation.y = 2.62;   // nghieng ngang so voi camera: thay nguoi nghieng + man may tinh bang scene.add(wk);
    const wp = (geo, m, x, y, z, rx = 0, ry = 0, rz = 0) => { const me = new THREE.Mesh(geo, m);
      me.position.set(x, y, z); me.rotation.set(rx, ry, rz); me.castShadow = true; me.receiveShadow = true; wk.add(me); return me; };
    const skinM = mat('#E7C3A3', {roughness: 0.75}), pantM = mat('#3A4247', {roughness: 0.8});
    const vestM = mat(C.primary, {roughness: 0.55}), shirtM = mat('#F4F6F7', {roughness: 0.8});
    const reflM = mat('#E9EEF0', {metalness: 0.6, roughness: 0.25}), bootM = mat('#2C3338', {roughness: 0.7});
    // chan + giay
    wp(new THREE.CapsuleGeometry(0.15, 0.78, 6, 12), pantM, -0.17, 0.55, 0);
    wp(new THREE.CapsuleGeometry(0.15, 0.78, 6, 12), pantM, 0.17, 0.55, 0);
    wp(new THREE.BoxGeometry(0.26, 0.14, 0.42), bootM, -0.17, 0.07, 0.07);
    wp(new THREE.BoxGeometry(0.26, 0.14, 0.42), bootM, 0.17, 0.07, 0.07);
    // than: ao trong + ao phan quang + soc
    wp(new THREE.CapsuleGeometry(0.33, 0.55, 8, 16), shirtM, 0, 1.43, 0);
    wp(new THREE.CapsuleGeometry(0.345, 0.45, 8, 16), vestM, 0, 1.42, 0);
    wp(new THREE.CylinderGeometry(0.352, 0.352, 0.07, 20), reflM, 0, 1.26, 0);
    wp(new THREE.CylinderGeometry(0.352, 0.352, 0.07, 20), reflM, 0, 1.5, 0);
    // co + dau + mu bao ho
    wp(new THREE.CylinderGeometry(0.09, 0.1, 0.12, 12), skinM, 0, 1.96, 0);
    wp(new THREE.SphereGeometry(0.2, 20, 16), skinM, 0, 2.17, 0.0);
    wp(new THREE.SphereGeometry(0.235, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2), mat('#FFFFFF', {roughness: 0.35}), 0, 2.22, 0);
    wp(new THREE.CylinderGeometry(0.3, 0.3, 0.03, 24), mat('#FFFFFF', {roughness: 0.35}), 0, 2.22, 0.05);
    wp(new THREE.BoxGeometry(0.47, 0.035, 0.05), bandM, 0, 2.3, 0.0);
    // tay: canh tay tren buong xuong, cang tay dua ra truoc giu may tinh bang o ngang nguc
    for (const sx of [-1, 1]) {
      wp(new THREE.CapsuleGeometry(0.085, 0.42, 6, 10), vestM, sx * 0.4, 1.55, 0.03, 0.15, 0, sx * 0.12);
      wp(new THREE.CapsuleGeometry(0.075, 0.36, 6, 10), shirtM, sx * 0.3, 1.28, 0.27, -1.25, 0, sx * -0.25);
      wp(new THREE.SphereGeometry(0.075, 12, 10), skinM, sx * 0.19, 1.35, 0.47);
    }
    // may tinh bang: vo xam dam + mat man hinh dung texture man lon, nghieng len de nhin
    const tab = new THREE.Group(); tab.position.set(0, 1.32, 0.55); tab.rotation.set(-1.15, Math.PI, 0, "YXZ"); wk.add(tab);
    const tabBody = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.38, 0.03), mat('#21272B', {roughness: 0.4}));
    tabBody.castShadow = true; tab.add(tabBody);
    const tabFace = new THREE.Mesh(new THREE.PlaneGeometry(0.51, 0.33), new THREE.MeshBasicMaterial({map: tex, toneMapped: false}));
    tabFace.position.z = 0.017; tab.add(tabFace);

    // ---------- chieu vi tri 3D -> pixel de dat nhan HTML ----------
    const v = new THREE.Vector3();
    const toPx = (p) => { v.copy(p).project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; };
    const lblEls = {rfid: stage.querySelector('#k3l-rfid'), plc: stage.querySelector('#k3l-plc'),
      conveyor: stage.querySelector('#k3l-conveyor')};
    const lblPos = {rfid: new THREE.Vector3(GATE_X, GH + 0.45, CZ), plc: new THREE.Vector3(PLC.x, 2.85, PLC.z),
      conveyor: new THREE.Vector3(4.4, CH + 0.2, CZ + CW / 2)};
    const lblIn = {rfid: 1.3, plc: 1.9, conveyor: 2.5};
    const fadeEl = stage.querySelector('#k3fade');
    const tagEl = stage.querySelector('#k3tag');

    const ease = (x) => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
    const clamp01 = (x) => Math.max(0, Math.min(1, x));

    function render(t) {
      // camera: truot vong nhe, roi tu giay PUSH0 day vao nhan vien kho de thay man may tinh bang
      const PUSH0 = DUR - 3.6, pu = ease((t - PUSH0) / 2.6);
      const a = THREE.MathUtils.degToRad(38 + 9 * ease(t / DUR));
      const r = 30, el = 21 - 1.5 * ease(t / DUR);
      cam.position.set(Math.sin(a) * r - 0.5, el, Math.cos(a) * r);
      const lk = new THREE.Vector3(-0.2, 2.3, -2.6).lerp(new THREE.Vector3(WKP.x + 0.6, 1.6, WKP.z - 0.6), pu);
      cam.position.add(lk.clone().sub(new THREE.Vector3(-0.2, 2.3, -2.6)));
      cam.lookAt(lk);
      cam.zoom = (1.1 + 0.08 * ease(t / DUR)) * (1 + 1.25 * pu);
      cam.updateProjectionMatrix();
      tagEl.dataset.pu = pu;

      // vach tren bang chuyen chay theo toc do thung
      const off = (SPEED * t) % 0.8;
      stripes.forEach((s, i) => { s.position.x = CX0 + 0.2 + i * 0.8 + off; s.visible = s.position.x < CX1 - 0.1; });

      // thung hang + dem so doc
      let count = STOCK0, lastRead = -99;
      boxes.forEach((g, k) => {
        const x = boxX(k, t);
        g.visible = x > CX0 + 0.3 && x < CX1 - 0.4;
        g.position.x = x;
        const tr = readT(k);
        if (tr >= 0.2 && tr <= t) { count++; lastRead = Math.max(lastRead, tr); }
      });

      // cong sang khi vua doc
      const since = t - lastRead;
      const glow = since >= 0 && since < 1.4 ? Math.exp(-since * 2.0) : 0;
      beam.material.opacity = 0.22 * glow;
      [pan1, pan2, pan3].forEach(p => { p.material.emissiveIntensity = 0.18 + 2.2 * glow; });
      ring.material.opacity = since >= 0 && since < 0.9 ? 0.75 * (1 - since / 0.9) : 0;
      const rs = 0.6 + 1.6 * clamp01(since / 0.9); ring.scale.set(rs, rs, rs);

      // xung du lieu tu cong -> man hinh (bat dau luc doc, chay 1.1s)
      let pi = 0;
      boxes.forEach((g, k) => {
        const tr = readT(k); const u = (t - tr) / 1.1;
        if (tr >= 0.2 && u >= 0 && u <= 1 && pi < pulses.length) {
          const p = pulses[pi++]; p.visible = true; p.position.copy(curveGate.getPointAt(ease(u)));
        }
      });
      for (; pi < pulses.length; pi++) pulses[pi].visible = false;
      // xung deu tu PLC (trang thai bang chuyen) moi 0.9s
      plcPulses.forEach((p, i) => {
        const u = ((t * 0.6) + i / plcPulses.length) % 1;
        p.visible = t > 1.2; p.position.copy(curvePlc.getPointAt(u));
      });
      // den PLC nhap nhay theo nhip co dinh
      leds.forEach((l, i) => { l.material.emissiveIntensity = (Math.floor(t * 3 + i * 1.7) % 3 === 0) ? 1.6 : 0.25; });

      // man hinh: so tang + nay nhe khi vua tang (tre 1.1s cho xung toi noi)
      let shown = STOCK0, bump = 0;
      boxes.forEach((g, k) => {
        const ta = readT(k) + 1.1;
        if (readT(k) >= 0.2 && ta <= t) { shown++; const d = t - ta; if (d < 0.45) bump = Math.max(bump, 1 - d / 0.45); }
      });
      drawScreen(shown, bump, clamp01((t - 0.4) / 0.6));

      // nhan HTML
      for (const k of Object.keys(lblEls)) {
        const [px, py] = toPx(lblPos[k]);
        const o = clamp01((t - lblIn[k]) / 0.5);
        lblEls[k].style.left = px + 'px'; lblEls[k].style.top = (py - 14 - 10 * (1 - o)) + 'px';
        lblEls[k].style.opacity = o * (1 - pu);
      }
      const tabEl = stage.querySelector('#k3tab'), tline = stage.querySelector('#k3tline');
      const tabO = clamp01((t - (DUR - 2.9)) / 0.5);
      tabEl.style.opacity = tabO; tabEl.style.transform = `scale(${0.92 + 0.08 * tabO})`;
      stage.querySelector('#k3tnum').textContent = shown.toLocaleString('vi-VN');
      const tw = new THREE.Vector3(); tab.getWorldPosition(tw);
      const [tpx, tpy] = toPx(tw);
      const r0 = tabEl.getBoundingClientRect(), sr = stage.getBoundingClientRect();
      const sx = W / sr.width;
      tline.style.opacity = tabO;
      const lx2 = (r0.left - sr.left) * sx, ly2 = (r0.top - sr.top + r0.height / 2) * sx;
      const ln = stage.querySelector('#k3tl'); ln.setAttribute('x1', tpx); ln.setAttribute('y1', tpy);
      ln.setAttribute('x2', lx2); ln.setAttribute('y2', ly2);
      const cc = stage.querySelector('#k3tc'); cc.setAttribute('cx', tpx); cc.setAttribute('cy', tpy);
      fadeEl.style.opacity = 1 - clamp01(t / 0.7);
      tagEl.style.opacity = clamp01((t - 0.8) / 0.6);

      renderer.render(scene, cam);
    }

    const state = {t: 0};
    const tl = gsap.timeline({paused: true});
    tl.to(state, {t: DUR, duration: DUR, ease: 'none', onUpdate: () => render(state.t)});
    render(0);
    return tl;
  };
})();
