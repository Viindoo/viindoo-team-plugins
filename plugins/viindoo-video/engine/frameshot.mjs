// Chup 1 khung TINH trang thai cuoi cua 1 scene -> PNG. Dung cho nen demoframe.
// node frameshot.mjs --scene demoframe --data <file.json> --out <file.png> [--width 1920 --height 1080]
import {readFileSync} from 'node:fs';
import path from 'node:path';
import {loadBrand} from './src/brand.js';
import {ROOT, GSAP_FILE, loadPuppeteer, chromePath, resolveArg} from './src/env.js';

const puppeteer = loadPuppeteer();
const CHROME = chromePath();
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return (i !== -1 && process.argv[i + 1]) ? process.argv[i + 1] : d; };

const scene = arg('scene', 'demoframe');
if (!arg('data') || !arg('out')) { console.error('Can --data <file.json> va --out <file.png>'); process.exit(2); }
const data = JSON.parse(readFileSync(resolveArg(arg('data')), 'utf8'));
const out = resolveArg(arg('out'));
const W = parseInt(arg('width', '1920'), 10), H = parseInt(arg('height', '1080'), 10);

const brand = loadBrand();
const template = readFileSync(path.join(ROOT, 'src/template.html'), 'utf8');
const gsapSrc = readFileSync(GSAP_FILE, 'utf8');
const sceneSrc = readFileSync(path.join(ROOT, 'src/scenes/_fw.js'), 'utf8') + '\n'
  + readFileSync(path.join(ROOT, `src/scenes/${scene}.js`), 'utf8');

const browser = await puppeteer.launch({executablePath: CHROME, headless: true,
  args: ['--no-sandbox', '--disable-gpu', '--force-color-profile=srgb', '--hide-scrollbars']});
try {
  const page = await browser.newPage();
  await page.setViewport({width: W, height: H, deviceScaleFactor: 1});
  await page.setContent(template, {waitUntil: 'load'});
  await page.evaluate((wf, w, h) => {
    const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = wf; document.head.appendChild(l);
    const s = document.getElementById('stage'); s.style.width = w + 'px'; s.style.height = h + 'px';
  }, brand.fonts.webfont, W, H);
  await page.addScriptTag({content: gsapSrc});
  await page.addScriptTag({content: sceneSrc});
  await page.evaluate(() => new Promise((res) => { const t = setTimeout(res, 4000);
    try { document.fonts.ready.then(() => { clearTimeout(t); res(); }); } catch { clearTimeout(t); res(); } }));
  await page.evaluate((sc, d, b) => {
    const stage = document.getElementById('stage');
    const tl = window.SCENES[sc](stage, d, b, window.gsap); tl.time(tl.duration());
  }, scene, data, brand);
  await page.screenshot({path: out, clip: {x: 0, y: 0, width: W, height: H}});
  console.log('OK ' + out);
} finally { await browser.close(); }
