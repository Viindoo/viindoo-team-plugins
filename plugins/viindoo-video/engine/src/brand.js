// Brand resolver - doc tu brand-tokens.json cua plugin (<plugin>/brand/brand-tokens.json).
// Khong hardcode mau/font o day; chi fallback khi khong doc duoc file.
// Doi brand: sua <plugin>/brand/, KHONG sua o day. De duong dan bang BRAND_TOKENS / BRAND_LOGO.
import {readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const BRAND_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'brand');
const DEFAULT_TOKENS = process.env.BRAND_TOKENS || path.join(BRAND_DIR, 'brand-tokens.json');

// Logo chuan: file SVG goc trong SSOT brand assets (nét chữ riêng, KHONG go lai bang font).
// Nap san dang inline markup de canh nhung thang vao HTML.
function loadLogo(tokensPath) {
  const file = process.env.BRAND_LOGO ||
    path.join(BRAND_DIR, 'assets', 'logo-color.svg');
  try {
    const svg = readFileSync(file, 'utf8')
      .replace(/<\?xml[\s\S]*?\?>/g, '')
      .replace(/<!DOCTYPE[\s\S]*?>/gi, '')
      .trim();
    if (!svg.startsWith('<svg')) throw new Error('khong phai SVG');
    return {svg, source: file};
  } catch {
    return {svg: null, source: `fallback (khong doc duoc ${file})`};
  }
}

const FALLBACK = {
  colors: {
    primary: '#00BBCE', secondary: '#7F4282', grey: '#8F8F8F',
    grey_light_bg: '#F2F2F2', white: '#FFFFFF',
    text_heading: '#21272B', text_body: '#282F33', text_muted: '#6B6D70',
    success: '#00B365', warning: '#C99700', info: '#0099E6',
  },
  fonts: {
    heading: "Montserrat,'Helvetica Neue',Arial,sans-serif",
    body: "Roboto,'Helvetica Neue',Arial,sans-serif",
    webfont: 'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap',
  },
};

export function loadBrand(path = DEFAULT_TOKENS) {
  try {
    const t = JSON.parse(readFileSync(path, 'utf8'));
    return {
      colors: {...FALLBACK.colors, ...(t.colors || {})},
      fonts: {
        heading: t?.typography?.marketing?.heading_stack || FALLBACK.fonts.heading,
        body: t?.typography?.marketing?.body_stack || FALLBACK.fonts.body,
        webfont: t?.typography?.marketing?.webfont || FALLBACK.fonts.webfont,
      },
      logo: loadLogo(path),
      source: path,
    };
  } catch {
    return {...FALLBACK, logo: loadLogo(path),
      source: 'fallback (khong doc duoc brand-tokens.json)'};
  }
}
