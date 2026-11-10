// Viindoo Motion - bo render clip data-driven, mien phi + agent tu chay.
// GSAP (animation) + Chrome headless (chup tung khung) + FFmpeg (xuat).
//
// Dung:  node render.mjs --scene kpi --data <data.json> --out <video.mp4>
//   Duong dan tuong doi tinh tu thu muc dang dung; --out mac dinh $VIINDOO_VIDEO_WORKDIR/output/<scene>.mp4.
// Tuy chon: --width 1920 --height 1080 --fps 30 --duration <giay> --no-variants
//
// Ket qua: <out> (16:9) + ban doc 9:16 + vuong 1:1 (tru khi --no-variants).
import {readFileSync, mkdirSync, rmSync, existsSync, readdirSync} from 'node:fs';
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

const scene = arg('scene', 'kpi');
if (!arg('data', null)) { console.error('Thieu --data <file data.json>'); process.exit(2); }
const dataPath = resolveArg(arg('data'));
const out = arg('out', null) ? resolveArg(arg('out')) : path.join(OUTPUT_DIR, `${scene}.mp4`);
const W = parseInt(arg('width', '1920'), 10);
const H = parseInt(arg('height', '1080'), 10);
const FPS = parseInt(arg('fps', '30'), 10);
const durOverride = arg('duration', null);
const makeVariants = !flag('no-variants');

const brand = loadBrand();
const data = JSON.parse(readFileSync(dataPath, 'utf8'));
const template = readFileSync(path.join(ROOT, 'src/template.html'), 'utf8');
const gsapSrc = readFileSync(GSAP_FILE, 'utf8');
const sceneSrc = readFileSync(path.join(ROOT, 'src/scenes/_fw.js'), 'utf8') + '\n'
  + readFileSync(path.join(ROOT, `src/scenes/${scene}.js`), 'utf8');

const framesDir = makeTmpDir('frames');
mkdirSync(path.dirname(out), {recursive: true});

const pad5 = (n) => String(n).padStart(5, '0');

function ffmpeg(args) {
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...args], {stdio: 'inherit'});
}

console.log(`[viindoo-motion] scene=${scene} ${W}x${H}@${FPS}  brand=${brand.source}`);

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: true,
  protocolTimeout: 120000,
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
    '--force-color-profile=srgb', '--hide-scrollbars'],
});

try {
  const page = await browser.newPage();
  await page.setViewport({width: W, height: H, deviceScaleFactor: 1});
  await page.setContent(template, {waitUntil: 'load'});

  // nhung webfont brand (link stylesheet, nhanh hon @import) + set kich thuoc stage
  await page.evaluate((wf, w, h) => {
    const l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = wf;
    document.head.appendChild(l);
    const s = document.getElementById('stage');
    s.style.width = w + 'px'; s.style.height = h + 'px';
  }, brand.fonts.webfont, W, H);

  await page.addScriptTag({content: gsapSrc});
  await page.addScriptTag({content: sceneSrc});

  // cho font tai, nhung CO GIOI HAN: khong co mang thi fallback Helvetica/Arial, van render
  await page.evaluate(() => new Promise((res) => {
    const done = () => res();
    const t = setTimeout(done, 4000);
    try { document.fonts.ready.then(() => { clearTimeout(t); done(); }); }
    catch { clearTimeout(t); done(); }
  }));
  const duration = await page.evaluate((sc, d, b) => {
    const stage = document.getElementById('stage');
    const tl = window.SCENES[sc](stage, d, b, window.gsap);
    window.__tl = tl;
    tl.time(0);
    return tl.duration();
  }, scene, data, brand);

  const total = durOverride ? parseFloat(durOverride) : duration;
  const frames = Math.max(1, Math.round(total * FPS));
  console.log(`[viindoo-motion] duration=${total.toFixed(2)}s -> ${frames} frames`);

  for (let i = 0; i < frames; i++) {
    const t = Math.min(total, i / FPS);
    await page.evaluate((tt) => { window.__tl.time(tt); }, t);
    await page.screenshot({
      path: path.join(framesDir, `f${pad5(i)}.png`),
      clip: {x: 0, y: 0, width: W, height: H},
    });
    if (i < 3 || i % 30 === 0) console.log(`[viindoo-motion]   frame ${i + 1}/${frames}`);
  }
  console.log(`[viindoo-motion] captured ${readdirSync(framesDir).length} frames`);

  // encode master 16:9
  ffmpeg(['-framerate', String(FPS), '-i', path.join(framesDir, 'f%05d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out]);
  console.log(`[viindoo-motion] OK  ${out}`);

  if (makeVariants) {
    const base = out.replace(/\.mp4$/, '');
    // 9:16 doc (letterbox nen trang)
    ffmpeg(['-i', out, '-vf',
      'scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', `${base}-9x16.mp4`]);
    // 1:1 vuong
    ffmpeg(['-i', out, '-vf',
      'scale=1080:-2,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=white',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', `${base}-1x1.mp4`]);
    console.log(`[viindoo-motion] OK  ${base}-9x16.mp4 , ${base}-1x1.mp4`);
  }
} finally {
  await browser.close();
  rmSync(framesDir, {recursive: true, force: true});
}
