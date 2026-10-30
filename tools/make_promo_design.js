// X投稿用の画像（デザイン刷新＋「名前[数]」表記）を promo/update-2026-10-30.png に生成する。
// 実行: OLD_HTML=/path/to/old/index.html NODE_PATH=$(npm root -g) node tools/make_promo_design.js
// OLD_HTML は変更前のpublic/index.html。変更後は現在の public/index.html。サーバーは不要（背景は /bg/ なので、簡易サーバーで配信して撮る）
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os'), http = require('http');
const root = path.resolve(__dirname, '..');
const OLD = process.env.OLD_HTML; if (!OLD) throw new Error('OLD_HTML を指定してください');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'promo-'));
const fontDir = path.join(__dirname, 'fonts');
const VW = 800, VH = 460; // 撮影する範囲（幅・高さ）
const PRICE = '520'; // 売値520: 杖・壺（回数・容量つき）の候補が並ぶ

// public/ を簡易配信（/bg/ の背景画像を読むため）。変更前のHTMLは同じサーバーの別パスで配る
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  let f = u === '/__old__/' ? OLD : path.join(root, 'public', u.endsWith('/') ? u + 'index.html' : u);
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': f.endsWith('.png') ? 'image/png' : 'text/html; charset=utf-8' }); res.end(d); });
});

async function shot(browser, url, out) {
  const p = await browser.newPage({ viewport: { width: VW, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
  await p.route(/googletagmanager\.com|google-analytics\.com/, r => r.abort());
  await p.goto(url, { waitUntil: 'load' });
  await p.fill('#price', PRICE); await p.waitForTimeout(900);
  const clip = { x: 0, y: 0, width: VW, height: VH };
  const rects = await p.evaluate(() => {
    const r = e => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; };
    const nav = document.querySelector('.rg-nav');
    const name = document.querySelector('#sec-sell .rg-list-title .nm span:last-child');
    const row = name.closest('.rg-list-row');
    const countEl = [...row.querySelectorAll('.rg-list-copy .var > span')].find(s => /回数|容量/.test(s.textContent));
    return { nav: r(nav), name: r(name), count: countEl ? r(countEl) : null };
  });
  await p.screenshot({ path: out, clip });
  await p.close();
  return rects;
}
const b64 = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');

function page(o) {
  const pct = (x, y) => `left:${(x / VW * 100).toFixed(2)}%;top:${(y / VH * 100).toFixed(2)}%`;
  const badge = (n, x, y, cls = '') => `<span class="num ${cls}" style="${pct(x, y)}">${n}</span>`;
  const bn = o.before, an = o.after;
  const beforeBadges = bn.count ? badge('②', bn.count[0] + bn.count[2] + 36, bn.count[1] + bn.count[3] / 2, 'grey') : '';
  const afterBadges = badge('①', 26, an.nav[1] + an.nav[3] + 22) + badge('②', an.name[0] + an.name[2] + 34, an.name[1] + an.name[3] / 2);
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
@font-face{font-family:Seed;src:url(file://${fontDir}/LINESeedJP-Regular.woff2);font-weight:400}
@font-face{font-family:Seed;src:url(file://${fontDir}/LINESeedJP-Bold.woff2);font-weight:700}
*{box-sizing:border-box;margin:0}
html,body{width:1600px;height:900px;overflow:hidden}
body{font-family:Seed,"Noto Sans JP",sans-serif;color:#20344b;background:linear-gradient(135deg,#e9f1fb,#d6e5f6 60%,#eef5fc);position:relative}
.orb{position:absolute;border-radius:50%;border:1px solid #ffffffb0;background:linear-gradient(140deg,#ffffffb0,#9cc2ea65 40%,#7fb0e425 75%,#ffffff50)}
.o1{width:1300px;height:420px;right:-520px;top:430px;transform:rotate(-30deg)}
.o2{width:700px;height:300px;left:-340px;top:-190px;transform:rotate(-25deg)}
.head{position:absolute;left:80px;right:80px;top:40px}
.eyebrow{font-size:25px;font-weight:700;color:#1d579a;letter-spacing:.08em}
h1{margin-top:2px;font-size:58px;line-height:1.3;font-weight:700}
.sub{margin-top:4px;font-size:26px;color:#3d5169;line-height:1.6}
.cols{position:absolute;left:80px;right:80px;top:236px;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.panel{display:grid;gap:10px;min-width:0}
.pill{justify-self:start;padding:4px 22px;border-radius:999px;font-size:23px;font-weight:700;letter-spacing:.06em}
.before .pill{background:#e1e8f1;color:#4d6078;border:1px solid #c5d2e2}
.after .pill{background:#2a6cb8;color:#fff;box-shadow:inset 0 1px 1px #ffffff70}
.shot{position:relative;border-radius:22px;box-shadow:0 22px 52px rgba(30,70,125,.2);overflow:hidden}
.shot img{display:block;width:100%;height:auto}
.after .shot{outline:4px solid #2a6cb8;outline-offset:3px}
.num{position:absolute;transform:translate(-50%,-50%);min-width:34px;height:34px;padding:0 4px;border-radius:999px;background:#2a6cb8;color:#fff;font-size:22px;font-weight:700;display:grid;place-items:center;box-shadow:0 0 0 3px #fff,0 4px 12px rgba(0,0,0,.3)}
.num.grey{background:#7d8ea3}
.arrow{position:absolute;left:50%;top:${o.arrowTop}px;transform:translateX(-50%);width:76px;height:76px;border-radius:50%;background:#2a6cb8;color:#fff;display:grid;place-items:center;box-shadow:0 8px 24px rgba(30,70,125,.3);z-index:3}
.arrow svg{width:40px;height:40px}
.notes{position:absolute;left:80px;right:80px;bottom:62px;display:grid;gap:6px}
.notes p{font-size:25px;line-height:1.5;font-weight:700;color:#1d579a;display:flex;gap:10px;align-items:baseline}
.notes p b{display:inline-grid;place-items:center;min-width:32px;height:32px;border-radius:999px;background:#2a6cb8;color:#fff;font-size:20px;flex:none;transform:translateY(-1px)}
.foot{position:absolute;left:80px;right:80px;bottom:20px;display:flex;justify-content:space-between;font-size:20px;color:#566a82}
.foot b{color:#1d579a}
</style></head><body><div class="orb o1"></div><div class="orb o2"></div>
<div class="head"><p class="eyebrow">シレン6 値段識別 アップデート</p><h1>${o.title}</h1><p class="sub">${o.sub}</p></div>
<div class="cols">
  <div class="panel before"><div class="pill">Before</div><div class="shot"><img src="${o.beforeImg}" alt="">${beforeBadges}</div></div>
  <div class="panel after"><div class="pill">After</div><div class="shot"><img src="${o.afterImg}" alt="">${afterBadges}</div></div>
</div>
<div class="arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
<div class="notes">${o.notes.map((t, i) => `<p><b>${['①', '②'][i]}</b><span>${t}</span></p>`).join('')}</div>
<div class="foot"><span>風来のシレン6 非公式ファンツール</span><b>shiren6.amanohashi.date</b></div>
</body></html>`;
}

(async () => {
  await new Promise(r => server.listen(18997, '127.0.0.1', r));
  const browser = await chromium.launch();
  fs.mkdirSync(path.join(root, 'promo'), { recursive: true });
  const beforeR = await shot(browser, 'http://127.0.0.1:18997/__old__/', path.join(tmp, 'before.png'));
  const afterR = await shot(browser, 'http://127.0.0.1:18997/', path.join(tmp, 'after.png'));
  const job = {
    title: 'デザインを刷新し、杖・壺をゲームの表記に',
    sub: 'ガラスのような透明感のある見た目に。背景はスーパーファミコン風のドット絵です。',
    beforeImg: b64(path.join(tmp, 'before.png')), afterImg: b64(path.join(tmp, 'after.png')),
    before: beforeR, after: afterR, arrowTop: 440,
    notes: ['ガラス風のデザインに変更。背景はライトが草原、ダークが夜の部屋です。', '杖の回数・壺の容量を、ゲームと同じ「ただの杖[6]」の形で表示します。'],
  };
  const html = path.join(tmp, 'design.html');
  fs.writeFileSync(html, page(job));
  const p = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(root, 'promo', 'update-2026-10-30.png') });
  await browser.close(); server.close();
  console.log('update-2026-10-30.png', JSON.stringify({ before: beforeR.count && 'count有', after: !!afterR.name }));
})();
