// OGP画像とアイコンを生成する（Playwrightが必要）: node make_images.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.resolve(__dirname, 'ogp.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.resolve(__dirname, '../public/og-image.png') });
  const svg = require('fs').readFileSync(path.resolve(__dirname, 'icon.svg'), 'utf8');
  const q = await b.newPage({ viewport: { width: 180, height: 180 } });
  await q.setContent('<style>*{margin:0}svg{width:180px;height:180px;display:block}</style>' + svg);
  await q.screenshot({ path: path.resolve(__dirname, '../public/apple-touch-icon.png') });
  await b.close();
})();
