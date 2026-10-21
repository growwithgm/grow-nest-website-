// Render the hero (nest settled, headline visible) as the 1200x630 share image.
//
//   python3 -m http.server 8080          # in the repo root, in another terminal
//   npm i -D playwright && npx playwright install chromium
//   node tools/make-og-image.mjs [http://localhost:8080/]
//
// Writes assets/img/og-image.png.

import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';

const url = process.argv[2] || 'http://localhost:8080/';
const out = fileURLToPath(new URL('../assets/img/og-image.png', import.meta.url));

const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
// let the dots gather into the nest
await page.waitForTimeout(4000);
await page.screenshot({ path: out });
await browser.close();
console.log('wrote', out);
