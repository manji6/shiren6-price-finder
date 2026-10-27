// X投稿用のBefore/After画像（1枚）を promo/update-summary.png に生成する。
// 実行: OLD_HTML=/path/to/old/index.html NODE_PATH=$(npm root -g) node tools/make_promo.js
// OLD_HTML は変更前のpublic/index.html（例: git show origin/main:public/index.html > old.html）
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os');
const root = path.resolve(__dirname, '..');
const OLD = process.env.OLD_HTML;
if (!OLD) throw new Error('OLD_HTML を指定してください');
const NEW = path.join(root, 'public/index.html');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'promo-'));
const fontDir = path.join(__dirname, 'fonts');
const PRICE = '40'; // 売値40: 草・種に 通常2件(高飛び草・くねくね草)と祝福2件(毒草・暴走の種)

// 実アプリの検索結果（売値側の最初の一覧）を撮る。行の位置も返す
async function shotList(browser, file, out) {
  const p = await browser.newPage({ viewport: { width: 720, height: 1100 }, deviceScaleFactor: 2, colorScheme: 'light' });
  await p.goto('file://' + file);
  await p.fill('#price', PRICE); await p.waitForTimeout(600);
  const ul = p.locator('#sec-sell ul').first();
  const b = await ul.boundingBox();
  const rows = await p.$$eval('#sec-sell ul:first-of-type .rg-list-row', rs => rs.map(r => { const x = r.getBoundingClientRect(); return [x.top, x.height]; }));
  const padX = 16, padTop = -2, padBottom = 10;
  const clip = { x: b.x - padX, y: b.y - padTop, width: b.width + padX * 2, height: b.height + padTop + padBottom };
  await p.screenshot({ path: out, clip });
  await p.close();
  return { w: clip.width, h: clip.height, rows: rows.map(([t, h]) => [t - clip.y, h]) };
}
const b64 = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');

function page(o) {
  const nums = o.rows.map((r, i) => `<span class="num" style="top:${((r[0] + r[1] / 2) / o.h * 100).toFixed(2)}%">${i + 1}</span>`).join('');
  const bell = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a5 5 0 0 0-5 5v3.5L5.5 15h13L17 11.5V8a5 5 0 0 0-5-5z"/><path d="M10 18.5a2 2 0 0 0 4 0"/></svg>';
  const skull = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5c-4 0-7 2.8-7 6.5 0 2.2 1 3.8 2.5 4.8V18h9v-3.2C18 13.8 19 12.2 19 10c0-3.7-3-6.5-7-6.5z"/><circle cx="9.2" cy="10.5" r="1.3"/><circle cx="14.8" cy="10.5" r="1.3"/><path d="M10.5 18v-2M13.5 18v-2"/></svg>';
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
@font-face{font-family:Seed;src:url(file://${fontDir}/LINESeedJP-Regular.woff2);font-weight:400}
@font-face{font-family:Seed;src:url(file://${fontDir}/LINESeedJP-Bold.woff2);font-weight:700}
*{box-sizing:border-box;margin:0}
html,body{width:1600px;height:900px;overflow:hidden}
body{font-family:Seed,"Noto Sans JP",sans-serif;color:#20344b;background:linear-gradient(135deg,#e9f1fb,#d6e5f6 60%,#eef5fc);position:relative}
.orb{position:absolute;border-radius:50%;border:1px solid #ffffffb0;background:linear-gradient(140deg,#ffffffb0,#9cc2ea65 40%,#7fb0e425 75%,#ffffff50)}
.o1{width:1300px;height:420px;right:-520px;top:430px;transform:rotate(-30deg)}
.o2{width:700px;height:300px;left:-340px;top:-190px;transform:rotate(-25deg)}
.head{position:absolute;left:80px;right:80px;top:44px}
.eyebrow{font-size:26px;font-weight:700;color:#1d579a;letter-spacing:.08em}
h1{margin-top:4px;font-size:60px;line-height:1.3;font-weight:700}
.sub{margin-top:6px;font-size:27px;color:#3d5169;line-height:1.6}
.cols{position:absolute;left:80px;right:80px;top:268px;display:grid;grid-template-columns:1fr 1fr;gap:96px;align-items:start}
.panel{display:grid;gap:12px;min-width:0}
.pill{justify-self:start;padding:5px 24px;border-radius:999px;font-size:25px;font-weight:700;letter-spacing:.06em}
.before .pill{background:#e1e8f1;color:#4d6078;border:1px solid #c5d2e2}
.after .pill{background:#2a6cb8;color:#fff;box-shadow:inset 0 1px 1px #ffffff70}
.shot{position:relative;border-radius:24px;box-shadow:0 22px 52px rgba(30,70,125,.16)}
.shot img{display:block;width:100%;height:auto;border-radius:24px}
.after .shot{outline:4px solid #2a6cb8;outline-offset:3px}
.num{position:absolute;left:-12px;transform:translateY(-50%);width:30px;height:30px;border-radius:50%;background:#2a6cb8;color:#fff;font-size:18px;font-weight:700;display:grid;place-items:center;box-shadow:0 0 0 3px #fff}
.cap{font-size:27px;font-weight:700;text-align:center;margin-top:2px}
.before .cap{color:#5a6c82}.after .cap{color:#1d579a}
.legend{display:flex;justify-content:center;align-items:center;gap:14px;font-size:21px;color:#3d5169;margin-top:-2px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:3px 14px 3px 10px;border-radius:999px;font-weight:700;font-size:21px}
.chip svg{width:20px;height:20px}
.cb{background:rgba(217,154,26,.18);color:#6b4300;box-shadow:inset 0 0 0 1.5px rgba(217,154,26,.45)}
.cc{background:rgba(138,91,214,.16);color:#4a2a86;box-shadow:inset 0 0 0 1.5px rgba(138,91,214,.4)}
.arrow{position:absolute;left:50%;top:${o.arrowTop}px;transform:translateX(-50%);width:76px;height:76px;border-radius:50%;background:#2a6cb8;color:#fff;display:grid;place-items:center;box-shadow:0 8px 24px rgba(30,70,125,.3);z-index:3}
.arrow svg{width:40px;height:40px}
.foot{position:absolute;left:80px;right:80px;bottom:28px;display:flex;justify-content:space-between;font-size:22px;color:#566a82}
.foot b{color:#1d579a}
</style></head><body><div class="orb o1"></div><div class="orb o2"></div>
<div class="head"><p class="eyebrow">シレン6 値段識別 アップデート</p><h1>${o.title}</h1><p class="sub">${o.sub}</p></div>
<div class="cols">
  <div class="panel before"><div class="pill">Before</div><div class="shot"><img src="${o.before}" alt=""></div><p class="cap">${o.capB}</p></div>
  <div class="panel after"><div class="pill">After</div><div class="shot"><img src="${o.after}" alt="">${nums}</div><p class="cap">${o.capA}</p>
    <div class="legend"><span class="chip cb">${bell}祝福 ×2</span><span class="chip cc">${skull}呪い ×0.87</span><span>呪いも紫で区別</span></div></div>
</div>
<div class="arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
<div class="foot"><span>風来のシレン6 非公式ファンツール</span><b>shiren6.amanohashi.date</b></div>
</body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  fs.mkdirSync(path.join(root, 'promo'), { recursive: true });
  const before = await shotList(browser, OLD, path.join(tmp, 'before.png'));
  const after = await shotList(browser, NEW, path.join(tmp, 'after.png'));
  const job = {
    title: '並び順と、祝福・呪いの見た目を改善',
    sub: '売値40の例です。通常の高飛び草とくねくね草が先に出て、祝福の毒草と暴走の種は後ろになりました。',
    before: b64(path.join(tmp, 'before.png')), after: b64(path.join(tmp, 'after.png')),
    capB: '祝福が先頭。区別は小さなタグだけ', capA: '通常が先。祝福は色・アイコン・背景で区別',
    rows: after.rows, h: after.h, arrowTop: 440,
  };
  const html = path.join(tmp, 'summary.html');
  fs.writeFileSync(html, page(job));
  const p = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(root, 'promo', 'update-summary.png') });
  await p.close();
  await browser.close();
  console.log('update-summary.png', 'before', JSON.stringify([before.w, before.h]), 'after', JSON.stringify([after.w, after.h]));
})();
