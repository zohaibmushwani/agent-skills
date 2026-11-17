#!/usr/bin/env node
/**
 * Render HTML screens to portrait PNGs and extract a measured <id>.spec.json from the real DOM.
 *
 * Usage: node render_screens.mjs <design-dir> [--w 412] [--h 892] [--scale 2]
 *   Input : <design-dir>/html/<group>/<id>.html     (ids like home-01 or home-01.empty)
 *   Output: <design-dir>/screens/<group>/<id>.png and <id>.spec.json
 * Env: PLAYWRIGHT_MODULE (path to playwright's index.mjs/js if not installed locally), CHROME_PATH (chromium exe).
 *
 * What is measured (so audits judge the real thing, not the prompt):
 *   - every interactive element (a, button, input, [data-tap]) -> hit area w/h, y
 *   - every element with its own text -> computed font-size, colour, effective background
 *   Markup hints: data-id, data-primary, data-skip (ignore subtree, e.g. dimmed content behind a scrim).
 */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const root = path.resolve(args[0] || '.');
const opt = (k, d) => (args.includes(k) ? Number(args[args.indexOf(k) + 1]) : d);
const W = opt('--w', 412), H = opt('--h', 892), SCALE = opt('--scale', 2);

const pw = await import(process.env.PLAYWRIGHT_MODULE ? pathToFileURL(process.env.PLAYWRIGHT_MODULE).href : 'playwright');
const chromium = pw.chromium || pw.default.chromium;
const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });

function walk(dir) {
  return fs.existsSync(dir) ? fs.readdirSync(dir, { withFileTypes: true }).flatMap(e =>
    e.isDirectory() ? walk(path.join(dir, e.name)) : e.name.endsWith('.html') ? [path.join(dir, e.name)] : []) : [];
}

const extract = () => {
  const toHex = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(s => parseFloat(s));
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const hex = (o) => '#' + [o.r, o.g, o.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const blend = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 });
  const skipped = (el) => !!el.closest('[data-skip],[aria-hidden="true"]');
  const effBg = (el) => {
    let layers = [];
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null; // gradient/image: cannot judge
      const c = toHex(cs.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (const l of layers.reverse()) base = blend(l, base);
    return base;
  };
  const elements = [];
  const seen = new Map();
  const nameOf = (el, fallback) => {
    let id = el.getAttribute('data-id') || el.getAttribute('aria-label') || (el.textContent || '').trim().slice(0, 24) || fallback;
    id = id.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || fallback;
    const n = (seen.get(id) || 0) + 1; seen.set(id, n);
    return n > 1 ? `${id}-${n}` : id;
  };
  document.querySelectorAll('a,button,input,[data-tap]').forEach((el) => {
    if (skipped(el)) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    elements.push({
      id: nameOf(el, 'tap'), type: el.tagName === 'INPUT' ? 'input' : 'button', interactive: true,
      primary: el.hasAttribute('data-primary') || undefined,
      w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y), font: 0
    });
  });
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  for (let el = walker.nextNode(); el; el = walker.nextNode()) {
    if (skipped(el)) continue;
    const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
    if (!own) continue;
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    if (cs.visibility === 'hidden' || cs.display === 'none' || r.width === 0) continue;
    const bg = effBg(el), fgc = toHex(cs.color);
    const o = { id: nameOf(el, el.tagName.toLowerCase()), type: 'text', interactive: false, text: own.slice(0, 40),
      w: Math.round(r.width), h: Math.round(r.height), y: Math.round(r.y), font: Math.round(parseFloat(cs.fontSize)) };
    if (bg && fgc) { o.bg = hex(bg); o.fg = hex(fgc.a < 1 ? blend(fgc, bg) : fgc); }
    elements.push(o);
  }
  const overflowX = document.documentElement.scrollWidth > window.innerWidth;
  return { elements, overflowX, primaries: document.querySelectorAll('[data-primary]').length };
};

const files = walk(path.join(root, 'html')).sort();
if (!files.length) { console.error(`no html files under ${path.join(root, 'html')}`); process.exit(2); }
let n = 0;
for (const f of files) {
  const rel = path.relative(path.join(root, 'html'), f);
  const group = path.dirname(rel) === '.' ? 'misc' : path.dirname(rel);
  const id = path.basename(f, '.html');
  const outDir = path.join(root, 'screens', group);
  fs.mkdirSync(outDir, { recursive: true });
  await page.goto(pathToFileURL(f).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.screenshot({ path: path.join(outDir, `${id}.png`) });
  const m = await page.evaluate(extract);
  const spec = { id, title: id, group, mode: 'light', size: [W, H], primary_actions: m.primaries,
    overflowX: m.overflowX, elements: m.elements, generated_by: 'render_screens.mjs (measured from DOM)' };
  fs.writeFileSync(path.join(outDir, `${id}.spec.json`), JSON.stringify(spec, null, 1));
  n++;
  console.log(`rendered ${group}/${id}  (${m.elements.length} elements${m.overflowX ? ', HORIZONTAL OVERFLOW' : ''})`);
}
await browser.close();
console.log(`done: ${n} screens`);
