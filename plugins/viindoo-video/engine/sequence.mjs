// Viindoo Motion - noi nhieu canh thanh 1 video dai (motion-graphics).
// Dung:  node sequence.mjs --seq <seq.json> --out <video.mp4> [--no-variants]
//   Duong dan tuong doi tinh tu thu muc dang dung; --out mac dinh $VIINDOO_VIDEO_WORKDIR/output/.
//
// seq JSON = { title?, width?, height?, fps?, scenes:[{scene, data, duration}] }
//   duration (giay) = do dai canh; qua phan animation thi khung cuoi tu giu.
// Ket qua: <out> (16:9) + ban doc 9:16 + vuong 1:1 (tru khi --no-variants).
import {readFileSync, mkdirSync, rmSync, existsSync, readdirSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {loadBrand} from './src/brand.js';
import {ROOT, OUTPUT_DIR, GSAP_FILE, loadPuppeteer, chromePath, makeTmpDir, resolveArg} from './src/env.js';

const puppeteer = loadPuppeteer();
const CHROME = chromePath();

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  if (i !== -1 && i + 1 < process.argv.length && !process.argv[i + 1].startsWith('--'))
    return process.argv[i + 1];
  return def;
}
const flag = (name) => process.argv.includes('--' + name);

const seqArg = arg('seq', null);
if (!seqArg) { console.error('Thieu --seq <file seq.json>. Mau: ' + path.join(ROOT, 'samples/seq-mau.json')); process.exit(2); }
const seqPath = resolveArg(seqArg);
const seq = JSON.parse(readFileSync(seqPath, 'utf8'));
const out = arg('out', null) ? resolveArg(arg('out'))
  : path.join(OUTPUT_DIR, path.basename(seqPath).replace(/\.json$/, '') + '.mp4');
const W = parseInt(arg('width', String(seq.width || 1920)), 10);
const H = parseInt(arg('height', String(seq.height || 1080)), 10);
const FPS = parseInt(arg('fps', String(seq.fps || 60)), 10);  // chuan forwarder: 60fps
const makeVariants = !flag('no-variants');
const segDir = arg('segdir', null);          // giu tung segment vao thu muc nay
const onlyArg = arg('only', null);           // chi render cac index nay (0-based, phay)
const onlySet = onlyArg ? new Set(onlyArg.split(',').map(s => parseInt(s, 10))) : null;
const noConcat = flag('no-concat');

const brand = loadBrand();
const template = readFileSync(path.join(ROOT, 'src/template.html'), 'utf8');
const gsapSrc = readFileSync(GSAP_FILE, 'utf8');

// nap source tung loai canh (unique) + file dung chung _fw.js (chrome kieu forwarder)
const sceneTypes = [...new Set(seq.scenes.map(s => s.scene))];
const fwSrc = readFileSync(path.join(ROOT, 'src/scenes/_fw.js'), 'utf8');
// Canh 3D (ten bat dau bang fw3d) can three.js ban co dinh, nap offline tu vendor/.
const THREE_SRC = path.join(ROOT, 'vendor/three-0.160.0.min.js');
const sceneSrcMap = Object.fromEntries(
  sceneTypes.map(t => [t, (t.startsWith('fw3d') ? readFileSync(THREE_SRC, 'utf8') + '\n' : '') +
    fwSrc + '\n' + readFileSync(path.join(ROOT, `src/scenes/${t}.js`), 'utf8')]));

// Nhung anh (shot/image/bg) thanh data URI de canh tu lam toi/khoanh/keo so bang CSS,
// khoi phai overlay bang ffmpeg. Duong dan tuong doi tinh tu thu muc chua file seq.
const MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
              '.webp': 'image/webp', '.svg': 'image/svg+xml'};
function embedImages(d, baseDir) {
  if (!d || typeof d !== 'object') return d;
  for (const [k, v] of Object.entries(d)) {
    if (v && typeof v === 'object') { embedImages(v, baseDir); continue; }
    if (typeof v !== 'string') continue;
    const isImgKey = /^(shot|image|img|icon|photo|bg)$/.test(k);
    if (!isImgKey || v.startsWith('data:')) continue;
    const p = path.isAbsolute(v) ? v : path.resolve(baseDir, v);
    if (!existsSync(p)) { console.warn(`[seq] khong thay anh: ${p}`); continue; }
    const mime = MIME[path.extname(p).toLowerCase()];
    if (!mime) { console.warn(`[seq] dinh dang anh la: ${p}`); continue; }
    d[k] = `data:${mime};base64,${readFileSync(p).toString('base64')}`;
  }
  return d;
}
const seqDir = path.dirname(path.resolve(seqPath));
for (const s of seq.scenes) embedImages(s.data, seqDir);

// Thu muc lam viec RIENG cho tung luot chay (co PID trong ten).
// Vi sao (24/10/2026): truoc day la duong dan co dinh `.seqwork` va dong duoi XOA SACH no
// luc khoi dong. Hai luot render chay chong nhau thi luot sau xoa mat khung hinh cua luot
// truoc -> ca hai cung chet voi ENOENT giua chung. Co PID thi khong con dung nhau.
// Nam trong $VIINDOO_VIDEO_WORKDIR/.tmp, khong ghi vao thu muc plugin.
const workDir = makeTmpDir('seqwork');
mkdirSync(path.dirname(out), {recursive: true});
const pad5 = (n) => String(n).padStart(5, '0');
const pad2 = (n) => String(n).padStart(2, '0');
const ffmpeg = (args) => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...args], {stdio: 'inherit'});

console.log(`[seq] ${seq.title || seqPath}  ${W}x${H}@${FPS}  ${seq.scenes.length} canh  brand=${brand.source}`);

const browser = await puppeteer.launch({
  executablePath: CHROME, headless: true, protocolTimeout: 180000,
  // --enable-unsafe-swiftshader: Chrome moi chi cho WebGL phan mem (canh 3D fw3d*) khi co co nay.
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--enable-unsafe-swiftshader',
    '--force-color-profile=srgb', '--hide-scrollbars'],
});

const segFiles = [];
try {
  const page = await browser.newPage();
  await page.setViewport({width: W, height: H, deviceScaleFactor: 1});
  await page.setContent(template, {waitUntil: 'load'});
  await page.evaluate((wf, w, h) => {
    const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = wf;
    document.head.appendChild(l);
    const s = document.getElementById('stage'); s.style.width = w + 'px'; s.style.height = h + 'px';
  }, brand.fonts.webfont, W, H);
  await page.addScriptTag({content: gsapSrc});
  for (const t of sceneTypes) await page.addScriptTag({content: sceneSrcMap[t]});
  await page.evaluate(() => new Promise((res) => {
    const done = () => res(); const t = setTimeout(done, 4000);
    try { document.fonts.ready.then(() => { clearTimeout(t); done(); }); } catch { clearTimeout(t); done(); }
  }));

  if (segDir) mkdirSync(resolveArg(segDir), {recursive: true});
  for (let si = 0; si < seq.scenes.length; si++) {
    if (onlySet && !onlySet.has(si)) continue;
    const sc = seq.scenes[si];
    const framesDir = path.join(workDir, `f${pad2(si)}`);
    mkdirSync(framesDir, {recursive: true});

    const tlDur = await page.evaluate((scene, d, b) => {
      const stage = document.getElementById('stage');
      const tl = window.SCENES[scene](stage, d, b, window.gsap);
      window.__tl = tl; tl.time(0); return tl.duration();
    }, sc.scene, sc.data, brand);

    const total = sc.duration != null ? parseFloat(sc.duration) : tlDur;
    const frames = Math.max(1, Math.round(total * FPS));
    console.log(`[seq] canh ${si + 1}/${seq.scenes.length} ${sc.scene} - ${total.toFixed(1)}s (${frames} khung)`);

    for (let i = 0; i < frames; i++) {
      const t = Math.min(total, i / FPS);
      await page.evaluate((tt) => { window.__tl.time(tt); }, t);
      await page.screenshot({path: path.join(framesDir, `f${pad5(i)}.png`),
        clip: {x: 0, y: 0, width: W, height: H}});
    }

    const seg = path.join(workDir, `seg${pad2(si)}.mp4`);
    ffmpeg(['-framerate', String(FPS), '-i', path.join(framesDir, 'f%05d.png'),
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium',
      '-r', String(FPS), seg]);
    segFiles.push(seg);
    if (segDir) {
      const dest = path.join(resolveArg(segDir), `seg${pad2(si)}.mp4`);
      execFileSync('cp', [seg, dest]);
      console.log(`[seq]   -> ${dest}`);
    }
    rmSync(framesDir, {recursive: true, force: true});
  }

  if (noConcat) { console.log('[seq] no-concat: xong cac segment.'); }
  else {
  // concat tat ca segment (cung codec/params -> copy duoc)
  const listFile = path.join(workDir, 'list.txt');
  writeFileSync(listFile, segFiles.map(f => `file '${f}'`).join('\n'));
  ffmpeg(['-f', 'concat', '-safe', '0', '-i', listFile, '-c', 'copy', out]);
  console.log(`[seq] OK  ${out}`);
  }

  if (makeVariants && !noConcat) {
    const base = out.replace(/\.mp4$/, '');
    ffmpeg(['-i', out, '-vf', 'scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', `${base}-9x16.mp4`]);
    ffmpeg(['-i', out, '-vf', 'scale=1080:-2,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=white',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', `${base}-1x1.mp4`]);
    console.log(`[seq] OK  ${base}-9x16.mp4 , ${base}-1x1.mp4`);
  }
} finally {
  await browser.close();
  rmSync(workDir, {recursive: true, force: true});
}
