// X投稿用のBefore/After画像を promo/ に生成する。
// 実行: OLD_HTML=/path/to/old/index.html NODE_PATH=$(npm root -g) node tools/make_promo.js
// OLD_HTML は変更前のpublic/index.html（例: git show origin/main:public/index.html > old.html）
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os');
const root = path.resolve(__dirname, '..');
const OLD = process.env.OLD_HTML;
if (!OLD) throw new Error('OLD_HTML を指定してください');
const NEW = path.join(root, 'public/index.html');
const MOCK_OLD = path.join(root, 'mocks/state-visual.html');      // 現状(変更前)の行
const MOCK_NEW = path.join(root, 'mocks/state-visual-v3.html');   // 案H＋弱い面(変更後)の行
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'promo-'));
const fontDir = path.join(__dirname, 'fonts');

async function shotSection(browser, file, out) {
  const p = await browser.newPage({ viewport: { width: 720, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  await p.goto('file://' + file);
  await p.fill('#price', '20'); await p.waitForTimeout(600);
  const el = p.locator('#sec-sell');
  const box = await el.boundingBox();
  const rows = await p.$$eval('#sec-sell .rg-list-row', rs => rs.map(r => { const b = r.getBoundingClientRect(); return [b.top, b.height]; }));
  await el.screenshot({ path: out });
  await p.close();
  return { w: box.width, h: box.height, rows: rows.map(([t, h]) => [t - box.y, h]) };
}
async function shotRows(browser, file, sel, out) {
  const p = await browser.newPage({ viewport: { width: 1280, height: 1400 }, deviceScaleFactor: 2, colorScheme: 'light' });
  await p.goto('file://' + file); await p.waitForTimeout(500);
  await p.evaluate(s => { document.querySelectorAll(s + ' .rg-list-row').forEach((r, i) => { if (i % 2 === 1) r.style.display = 'none'; }); }, sel);
  const b = await p.locator(sel).boundingBox();
  const pad = 14;
  await p.screenshot({ path: out, clip: { x: b.x - pad, y: b.y - 6, width: b.width + pad * 2, height: b.height + 12 } });
  await p.close();
  return { w: b.width + pad * 2, h: b.height + 12 };
}
const b64 = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');

function page(o) {
  const nums = (o.rows || []).map((r, i) => `<span class="num" style="top:${((r[0] + r[1] / 2) / o.h * 100).toFixed(2)}%">${i + 1}</span>`).join('');
  const panel = (cls, label, img, cap, withNums) => `
    <div class="panel ${cls}">
      <div class="pill">${label}</div>
      <div class="shot"><img src="${img}" alt="">${withNums ? nums : ''}</div>
      <p class="cap">${cap}</p>
    </div>`;
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
@font-face{font-family:Seed;src:url(file://${fontDir}/LINESeedJP-Regular.woff2);font-weight:400}
@font-face{font-family:Seed;src:url(file://${fontDir}/LINESeedJP-Bold.woff2);font-weight:700}
*{box-sizing:border-box;margin:0}
html,body{width:1600px;height:900px;overflow:hidden}
body{font-family:Seed,"Noto Sans JP",sans-serif;color:#20344b;background:linear-gradient(135deg,#e9f1fb,#d6e5f6 60%,#eef5fc);position:relative}
.orb{position:absolute;border-radius:50%;border:1px solid #ffffffb0;background:linear-gradient(140deg,#ffffffb0,#9cc2ea65 40%,#7fb0e425 75%,#ffffff50)}
.o1{width:1300px;height:420px;right:-520px;top:430px;transform:rotate(-30deg)}
.o2{width:700px;height:300px;left:-340px;top:-190px;transform:rotate(-25deg)}
.wrap{position:absolute;inset:0;padding:54px 80px 0}
.eyebrow{font-size:26px;font-weight:700;color:#1d579a;letter-spacing:.08em}
h1{margin-top:6px;font-size:64px;line-height:1.3;font-weight:700}
.sub{margin-top:8px;font-size:28px;color:#3d5169;line-height:1.6}
.cols{position:absolute;left:80px;right:80px;top:282px;display:grid;grid-template-columns:1fr 1fr;gap:96px;align-items:start}
.panel{display:grid;gap:14px;justify-items:stretch;min-width:0}
.pill{justify-self:start;padding:6px 26px;border-radius:999px;font-size:26px;font-weight:700;letter-spacing:.06em}
.before .pill{background:#e1e8f1;color:#4d6078;border:1px solid #c5d2e2}
.after .pill{background:#2a6cb8;color:#fff;box-shadow:inset 0 1px 1px #ffffff70}
.shot{position:relative;border-radius:26px;overflow:visible;box-shadow:0 24px 56px rgba(30,70,125,.16)}
.shot img{display:block;width:100%;height:auto;border-radius:26px}
.after .shot{outline:4px solid #2a6cb8;outline-offset:3px}
.num{position:absolute;left:-9px;transform:translateY(-50%);width:30px;height:30px;border-radius:50%;background:#2a6cb8;color:#fff;font-size:18px;font-weight:700;display:grid;place-items:center;box-shadow:0 0 0 3px #fff}
.before .num{background:#7d8ea3}
.cap{font-size:28px;font-weight:700;text-align:center;margin-top:2px}
.before .cap{color:#5a6c82}.after .cap{color:#1d579a}
.arrow{position:absolute;left:50%;top:${o.arrowTop}px;transform:translateX(-50%);width:76px;height:76px;border-radius:50%;background:#2a6cb8;color:#fff;display:grid;place-items:center;box-shadow:0 8px 24px rgba(30,70,125,.3);z-index:3}
.arrow svg{width:40px;height:40px}
.foot{position:absolute;left:80px;right:80px;bottom:30px;display:flex;justify-content:space-between;font-size:22px;color:#566a82}
.foot b{color:#1d579a}
</style></head><body><div class="orb o1"></div><div class="orb o2"></div>
<div class="wrap"><p class="eyebrow">${o.eyebrow}</p><h1>${o.title}</h1><p class="sub">${o.sub}</p></div>
<div class="cols">${panel('before', 'Before', o.before, o.capB, false)}${panel('after', 'After', o.after, o.capA, o.numbers)}</div>
<div class="arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
<div class="foot"><span>風来のシレン6 非公式ファンツール</span><b>shiren6.amanohashi.date</b></div>
</body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  fs.mkdirSync(path.join(root, 'promo'), { recursive: true });
  // 画像1: 並び順（実際のアプリ。売値20）
  const oB = await shotSection(browser, OLD, path.join(tmp, 'ord-before.png'));
  const oA = await shotSection(browser, NEW, path.join(tmp, 'ord-after.png'));
  // 画像2: 見た目（同じ3行を、旧CSSと新CSSで描画）
  const vB = await shotRows(browser, MOCK_OLD, '.idea-0 ul', path.join(tmp, 'vis-before.png'));
  const vA = await shotRows(browser, MOCK_NEW, '.idea-Ha ul', path.join(tmp, 'vis-after.png'));
  const jobs = [
    { name: 'update-1-order.png', eyebrow: 'シレン6 値段識別 アップデート①', title: '同じ値段の候補を、通常→祝福→呪いの順に表示',
      sub: '売値20の例です。通常の毒草と暴走の種が先に出て、祝福の薬草は最後になりました。',
      before: b64(path.join(tmp, 'ord-before.png')), after: b64(path.join(tmp, 'ord-after.png')),
      capB: '祝福の薬草が先頭だった', capA: '通常が先、祝福は後ろ', rows: oA.rows, h: oA.h, numbers: true, arrowTop: 470 },
    { name: 'update-2-visual.png', eyebrow: 'シレン6 値段識別 アップデート②', title: '祝福・呪いを、色とアイコンで見分けやすく',
      sub: '先頭アイコンの色を変え、ベル・ドクロのアイコン付きラベルと薄い背景色を付けました。',
      before: b64(path.join(tmp, 'vis-before.png')), after: b64(path.join(tmp, 'vis-after.png')),
      capB: '淡い色の小さなタグ', capA: '色・アイコン・背景の3つで区別', numbers: false, arrowTop: 440 },
  ];
  for (const j of jobs) {
    const html = path.join(tmp, j.name + '.html');
    fs.writeFileSync(html, page(j));
    const p = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
    await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(root, 'promo', j.name) });
    await p.close();
    console.log(j.name);
  }
  await browser.close();
})();
