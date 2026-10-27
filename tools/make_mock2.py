"""祝福・呪いの見せ方 第2案（AppleのLiquid Glass／HIGの考え方に沿った案）を mocks/state-visual-v2.html に生成する。
実行: cd tools && LINESEED_DIR=fonts/ python3 -I make_mock2.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_common import *

ROWS = [
 dict(cat='巻物', name='おはらいの巻物', st='n', other='買値 600', hint=True),
 dict(cat='草・種', name='毒消し草', st='n', other='買値 600'),
 dict(cat='巻物', name='混乱の巻物', st='b', other='買値 600'),
 dict(cat='草・種', name='薬草', st='b', other='買値 80'),
 dict(cat='杖', name='ただの杖', st='c', other='買値 435', extra='回数 5'),
 dict(cat='腕輪', name='胃縮小の腕輪', st='c', other='買値 3,045'),
]

def row(r, idea):
    st = r['st']; inner = ICON[r['cat']]
    hint = '<span class="tag tag-hint">使うと選択画面</span>' if r.get('hint') else ''
    extra = f'<span>{r["extra"]}</span>' if r.get('extra') else ''
    label = ''
    if idea == 'B':                     # 前回案B（参考）: 淡いタグ
        label = f'<span class="tag tag-{st}">{STN[st]}</span>'
    elif st != 'n':
        glyph = svg(GLYPH[st], 'st-glyph') if idea in ('B2', 'H') else ''
        label = f'<span class="st-text st-text-{st}">{glyph}{STN[st]} {MULT[st]}</span>'
    gut = ''
    if idea in ('G', 'I'):
        gut = (f'<span class="gut gut-{st}">{svg(GLYPH[st], "")}</span>' if st != 'n' else '<span class="gut" aria-hidden="true"></span>')
    return (f'<li class="rg-list-row st-{st}">{gut}<div><p class="rg-list-title"><span class="nm">{svg(inner)}<span>{r["name"]}</span></span>{hint}</p>'
            f'<div class="rg-list-copy"><span class="var">{label}<span>{r["other"]}</span>{extra}</span></div></div>'
            f'<button class="rg-button judge" type="button">{CHECK}判断完了</button></li>')

def list_html(idea):
    if idea == 'F':                      # 状態ごとの内側グループ（grouped style）
        out = '<div class="grps">'
        for st in ('n', 'b', 'c'):
            rs = [r for r in ROWS if r['st'] == st]
            title = STN[st] + ('' if st == 'n' else f'（買値・売値とも{MULT[st]}）')
            out += (f'<section class="grp grp-{st}"><h3 class="grp-head">{svg(GLYPH[st], "grp-glyph")}<span>{title}</span><span class="n">{len(rs)}件</span></h3>'
                    f'<ul class="grp-rows">{"".join(row(r, idea) for r in rs)}</ul></section>')
        return out + '</div>'
    return '<ul>' + ''.join(row(r, idea) for r in ROWS) + '</ul>'

IDEAS = [
 ('B', '案B（前回・参考）', '前回の案B。行の背景と左端の帯をはっきり染め、淡いタグも残しています。'),
 ('B2', '案B2：Bをガラスの作法に寄せる', '同じ「行を色づける」方向を、控えめにしました。帯は廃止し、ごく薄い色の面と細い縁、丸みのある角で包みます。色だけに頼らないよう、ベル／ドクロの形と「祝福 ×2」の文字を、塗らずに添えます。'),
 ('G', '案G：行頭のインジケーター列', '行の先頭に、幅の決まった列を設けます。祝福・呪いの行だけ、色つきの丸にベル／ドクロが入ります。行の背景は変えないので静かです。縦に並べたとき、列に沿って目が止まります。'),
 ('F', '案F：状態ごとのグループ', 'HIGの「グループ化した一覧」の作法です。通常・祝福・呪いを、それぞれ内側のグループに分け、見出しにアイコン・状態・倍率を置きます。行は無彩色で、色は見出しだけに使います。'),
 ('H', '案H：種別タイルの色替え', '先頭の種別アイコンのタイルが、状態に応じて金・紫に変わります。形で種別、色で状態を表します。名前の横には、アイコンと文字だけの無塗りのラベルを添えます。'),
 ('I', '案I：B2＋G（おすすめ）', '案B2の控えめな色づけに、案Gの行頭インジケーターを足します。面の色・形・文字の3つで伝わり、色が見えにくくても区別できます。通常の行は何も足さず、静かなままです。'),
]

CSS = '''
:root { --st-b-solid:#9a6200; --st-b-on:#fff; --st-b-text:#6b4300; --st-b-wash:rgba(217,154,26,.11); --st-b-wash2:rgba(217,154,26,.24); --st-b-line:rgba(217,154,26,.38);
        --st-c-solid:#6a3fb0; --st-c-on:#fff; --st-c-text:#4a2a86; --st-c-wash:rgba(138,91,214,.10); --st-c-wash2:rgba(138,91,214,.22); --st-c-line:rgba(138,91,214,.34);
        --st-n-text:#566a82; --edge-hi:rgba(255,255,255,.75);
        --old-b-tint:#fff3d6; --old-b-stripe:#d99a1a; --old-c-tint:#efe6fb; --old-c-stripe:#8a5bd6; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --st-b-solid:#e8b64a; --st-b-on:#2b1d00; --st-b-text:#f4d68a; --st-b-wash:rgba(232,182,74,.12); --st-b-wash2:rgba(232,182,74,.26); --st-b-line:rgba(232,182,74,.38);
  --st-c-solid:#a98be6; --st-c-on:#1d1033; --st-c-text:#d9c4f5; --st-c-wash:rgba(169,139,230,.15); --st-c-wash2:rgba(169,139,230,.28); --st-c-line:rgba(169,139,230,.40);
  --st-n-text:#9fb2c8; --edge-hi:rgba(255,255,255,.09);
  --old-b-tint:rgba(232,182,74,.14); --old-b-stripe:#e8b64a; --old-c-tint:rgba(169,139,230,.16); --old-c-stripe:#a98be6; } }
:root[data-theme="dark"] {
  --st-b-solid:#e8b64a; --st-b-on:#2b1d00; --st-b-text:#f4d68a; --st-b-wash:rgba(232,182,74,.12); --st-b-wash2:rgba(232,182,74,.26); --st-b-line:rgba(232,182,74,.38);
  --st-c-solid:#a98be6; --st-c-on:#1d1033; --st-c-text:#d9c4f5; --st-c-wash:rgba(169,139,230,.15); --st-c-wash2:rgba(169,139,230,.28); --st-c-line:rgba(169,139,230,.40);
  --st-n-text:#9fb2c8; --edge-hi:rgba(255,255,255,.09);
  --old-b-tint:rgba(232,182,74,.14); --old-b-stripe:#e8b64a; --old-c-tint:rgba(169,139,230,.16); --old-c-stripe:#a98be6; }
@media (prefers-contrast: more) { :root { --st-b-line:rgba(154,98,0,.85); --st-c-line:rgba(106,63,176,.85); } }

.mock-note { display: grid; gap: 10px; }
.mock-note p, .mock-note li { max-width: 72ch; }
.mock-note ul { display: grid; gap: 6px; padding-left: 1.2em !important; list-style: disc !important; }
.mock-theme { display: flex; flex-wrap: wrap; gap: 8px; }
.idea-head { display: grid; gap: 4px; margin-bottom: 4px; }
.idea-head p { font-size: 14px; color: var(--rg-muted); line-height: 1.7; }

/* 共通部品 */
.st-text { display: inline-flex; align-items: center; gap: 5px; font-size: 14px; font-weight: 700; }
.st-text-b { color: var(--st-b-text); } .st-text-c { color: var(--st-c-text); }
.st-glyph { width: 16px; height: 16px; stroke-width: 2.2; flex: none; }
.gut { width: 28px; height: 28px; border-radius: 50%; display: grid; place-items: center; flex: none; }
.gut svg { width: 16px; height: 16px; stroke-width: 2.2; }
.gut-b { background: var(--st-b-solid); color: var(--st-b-on); }
.gut-c { background: var(--st-c-solid); color: var(--st-c-on); }

/* B（前回） */
.idea-B .rg-list-row.st-b { background: var(--old-b-tint); box-shadow: inset 5px 0 0 var(--old-b-stripe); }
.idea-B .rg-list-row.st-c { background: var(--old-c-tint); box-shadow: inset 5px 0 0 var(--old-c-stripe); }
.idea-B .rg-list-row.st-b, .idea-B .rg-list-row.st-c { margin-inline: -12px; padding-inline: 20px 12px; border-top-color: transparent; border-radius: 12px; }

/* B2 / I : 薄い面＋細い縁＋丸み */
.idea-B2 .rg-list-row.st-b, .idea-I .rg-list-row.st-b { background: var(--st-b-wash); box-shadow: inset 0 0 0 1px var(--st-b-line), inset 0 1px 0 var(--edge-hi); }
.idea-B2 .rg-list-row.st-c, .idea-I .rg-list-row.st-c { background: var(--st-c-wash); box-shadow: inset 0 0 0 1px var(--st-c-line), inset 0 1px 0 var(--edge-hi); }
.idea-B2 .rg-list-row.st-b, .idea-B2 .rg-list-row.st-c, .idea-I .rg-list-row.st-b, .idea-I .rg-list-row.st-c { margin: 3px -10px; padding-inline: 10px; border-top-color: transparent; border-radius: 16px; }
.idea-B2 .rg-list-row.st-b + .rg-list-row, .idea-B2 .rg-list-row.st-c + .rg-list-row,
.idea-I .rg-list-row.st-b + .rg-list-row, .idea-I .rg-list-row.st-c + .rg-list-row { border-top-color: transparent; }

/* G / I : 行頭のインジケーター列 */
.idea-G .rg-list-row, .idea-I .rg-list-row { grid-template-columns: 28px minmax(0, 1fr) auto; gap: 12px; }

/* F : グループ */
.grps { display: grid; gap: 4px; }
.grp { margin-top: 14px; }
.grp-head { display: flex; align-items: center; gap: 8px; padding: 0 6px 8px; font-size: 14px; font-weight: 700; line-height: 1.5; }
.grp-head .n { margin-left: auto; font-weight: 400; color: var(--rg-muted); font-size: 13px; }
.grp-glyph { width: 24px; height: 24px; padding: 3px; border-radius: 50%; stroke-width: 2.2; flex: none; }
.grp-n .grp-head { color: var(--st-n-text); } .grp-n .grp-glyph { border: 1.5px solid var(--rg-control-border); }
.grp-b .grp-head { color: var(--st-b-text); } .grp-b .grp-glyph { background: var(--st-b-solid); color: var(--st-b-on); }
.grp-c .grp-head { color: var(--st-c-text); } .grp-c .grp-glyph { background: var(--st-c-solid); color: var(--st-c-on); }
.grp-rows { background: var(--rg-control); border: 1px solid var(--rg-border); border-radius: 18px; padding: 0 16px; }
.grp-rows .rg-list-row:first-child { border-top: 0; }

/* H : タイルの色替え */
.idea-H .rg-list-row.st-b .cat-ico { background: var(--st-b-wash2); color: var(--st-b-text); box-shadow: 0 0 0 1.5px var(--st-b-line); }
.idea-H .rg-list-row.st-c .cat-ico { background: var(--st-c-wash2); color: var(--st-c-text); box-shadow: 0 0 0 1.5px var(--st-c-line); }
'''

SRC = [('Materials（Liquid Glassは操作・ナビゲーションの層で、コンテンツの層には使わない）', 'https://developer.apple.com/design/human-interface-guidelines/materials'),
       ('Color（色は控えめに。状態表示などの強調に絞り、色だけに頼らない）', 'https://developer.apple.com/design/human-interface-guidelines/color'),
       ('Lists and tables（行は読みやすく簡潔に。グループ化した一覧の作法）', 'https://developer.apple.com/design/human-interface-guidelines/lists-and-tables'),
       ('Accessibility（色だけでなく、形やアイコンでも伝える）', 'https://developer.apple.com/design/human-interface-guidelines/accessibility')]
links = ''.join(f'<li><a class="rg-link" href="{u}" target="_blank" rel="noopener noreferrer">{t}</a></li>' for t, u in SRC)

parts = ['<div class="rg-theme"><div class="rg-ambient" aria-hidden="true"></div>',
 '<header class="rg-nav"><div class="dock-brand"><h1 class="rg-brand">祝福・呪いの見せ方 第2案（モック）</h1><span class="rg-muted">AppleのLiquid Glass／HIGの考え方に沿った案。本体には未反映</span></div><span></span>',
 '<div class="mock-theme" role="group" aria-label="表示テーマ"><button class="rg-chip" type="button" data-theme-set="light">ライト</button><button class="rg-chip" type="button" data-theme-set="dark">ダーク</button><button class="rg-chip" type="button" data-theme-set="" aria-pressed="true">端末に合わせる</button></div></header>',
 '<main class="rg-page rg-stack">',
 '<section class="rg-surface mock-note"><h2 class="rg-heading">この案の考え方</h2>'
 '<p>前回の案Bに感じた違和感を、AppleのLiquid GlassとHIGの原則に照らして整理しました。</p>'
 '<ul>'
 '<li><strong>ガラスは操作の層、一覧の行はコンテンツの層。</strong>行を濃い色で塗ると、ガラスの面の上にさらに主張の強い面が重なり、階層が分かりにくくなります。行は静かに保ち、強調は小さく的確に行います。</li>'
 '<li><strong>色は状態表示のような、本当に強調が要る所だけに。</strong>HIGは、色の使いすぎは注意を散らすと述べています。祝福・呪いは通常の行より少ないので、例外だけに色を付けます。</li>'
 '<li><strong>色だけに頼らない。</strong>形（ベル／ドクロ）と文字（祝福 ×2）を必ず添えます。</li>'
 '<li><strong>一覧は読みやすく、グループは構造で見せる。</strong>色の塗り分けより、位置（行頭の列）やグループで見せるほうが、流し見に向きます。</li>'
 '</ul>'
 '<p class="rg-muted">6行は見比べやすいよう、価格の異なるものを混ぜています。実際の画面では同じ価格のものだけが並びます。</p></section>',
 '<div class="results-grid">']
for key, title, desc in IDEAS:
    parts.append(f'<section class="rg-surface idea-{key}"><div class="idea-head"><h2 class="rg-heading">{title}</h2><p>{desc}</p></div>{list_html(key)}</section>')
parts.append('</div>')
parts.append(f'<section class="rg-surface mock-note"><h2 class="rg-heading">参照したAppleのガイドライン</h2><ul>{links}</ul></section>')
parts.append('</main></div>')
parts.append('''<script>
(function(){ var root=document.documentElement; var btns=document.querySelectorAll('[data-theme-set]');
 btns.forEach(function(b){ b.addEventListener('click',function(){ var v=b.getAttribute('data-theme-set'); if(v) root.setAttribute('data-theme',v); else root.removeAttribute('data-theme');
  btns.forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true':'false'); }); }); });
})();
</script>''')
print(write_page('祝福・呪いの見せ方 第2案（モック）', CSS, '\n'.join(parts), '../mocks/state-visual-v2.html'))
