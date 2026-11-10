// Cau hinh chung cho 3 loi vao (render.mjs, sequence.mjs, frameshot.mjs).
//
// Nguyen tac: engine nam trong thu muc plugin (chi doc), MOI THU GHI RA nam trong
// thu muc lam viec cua nguoi dung:
//   VIINDOO_VIDEO_WORKDIR   (mac dinh ~/viindoo-video)
//     output/               video xuat ra (mac dinh cua --out)
//     .engine-deps/         node_modules cua engine (setup.sh cai vao day)
//     .tmp/                 khung hinh tam trong luc render (tu xoa sau moi luot)
// Duong dan tuong doi tren dong lenh (--seq, --data, --out) tinh tu thu muc dang dung (cwd).
import {existsSync, mkdirSync} from 'node:fs';
import {createRequire} from 'node:module';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const expandHome = (p) => (p && p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : p);
export const WORKDIR = path.resolve(expandHome(process.env.VIINDOO_VIDEO_WORKDIR || '~/viindoo-video'));
export const OUTPUT_DIR = path.join(WORKDIR, 'output');

// Tim thu muc node_modules co gsap + puppeteer-core, theo thu tu:
// VIINDOO_VIDEO_DEPS -> <WORKDIR>/.engine-deps/node_modules -> <engine>/node_modules
function findNodeModules() {
  const tries = [
    process.env.VIINDOO_VIDEO_DEPS && path.resolve(expandHome(process.env.VIINDOO_VIDEO_DEPS)),
    path.join(WORKDIR, '.engine-deps', 'node_modules'),
    path.join(ROOT, 'node_modules'),
  ].filter(Boolean);
  for (const d of tries) {
    if (existsSync(path.join(d, 'gsap', 'package.json')) &&
        existsSync(path.join(d, 'puppeteer-core', 'package.json'))) return d;
  }
  console.error('[viindoo-video] Chua cai thu vien cho engine (gsap, puppeteer-core).\n' +
    `  Chay: bash "${path.join(ROOT, 'setup.sh')}"\n` +
    `  (cai vao ${path.join(WORKDIR, '.engine-deps')}), hoac dat VIINDOO_VIDEO_DEPS=<thu muc node_modules>.`);
  process.exit(2);
}
export const NODE_MODULES = findNodeModules();
export const GSAP_FILE = path.join(NODE_MODULES, 'gsap', 'dist', 'gsap.min.js');

export function loadPuppeteer() {
  const req = createRequire(path.join(NODE_MODULES, '..', 'package.json'));
  const m = req('puppeteer-core');
  return m.default || m;
}

// Chrome: CHROME_PATH, roi cac vi tri quen thuoc theo he dieu hanh.
export function chromePath() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const known = {
    darwin: ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
      '/Applications/Chromium.app/Contents/MacOS/Chromium'],
    linux: ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium',
      '/usr/bin/chromium-browser'],
    win32: ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'],
  }[process.platform] || [];
  const hit = known.find((p) => existsSync(p));
  if (hit) return hit;
  console.error('[viindoo-video] Khong thay Chrome. Dat CHROME_PATH=<duong dan file chay Chrome>.');
  process.exit(2);
}

// Thu muc tam rieng cho tung luot chay (co PID): hai luot render chay chong nhau khong xoa nham
// khung hinh cua nhau.
export function makeTmpDir(prefix) {
  const d = path.join(WORKDIR, '.tmp', `${prefix}-${process.pid}`);
  mkdirSync(d, {recursive: true});
  return d;
}

export const resolveArg = (p) => path.resolve(process.cwd(), expandHome(p));
