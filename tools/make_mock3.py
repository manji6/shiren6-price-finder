"""案Hをベースに、行の薄い面の強さを比べる第3弾のモックを mocks/state-visual-v3.html に生成する。
実行: cd tools && LINESEED_DIR=fonts/ python3 -I make_mock3.py"""
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

def row(r):
    st = r['st']
    hint = '<span class="tag tag-hint">使うと選択画面</span>' if r.get('hint') else ''
    extra = f'<span>{r["extra"]}</span>' if r.get('extra') else ''
    label = f'<span class="st-text st-text-{st}">{svg(GLYPH[st], "st-glyph")}{STN[st]} {MULT[st]}</span>' if st != 'n' else ''
    return (f'<li class="rg-list-row st-{st}"><div><p class="rg-list-title"><span class="nm">{svg(ICON[r["cat"]])}<span>{r["name"]}</span></span>{hint}</p>'
            f'<div class="rg-list-copy"><span class="var">{label}<span>{r["other"]}</span>{extra}</span></div></div>'
            f'<button class="rg-button judge" type="button">{CHECK}判断完了</button></li>')

IDEAS = [
 ('H', '案H（そのまま）', '先頭の種別タイルの色だけで状態を表します。行の背景は変えません。いちばん静かな見た目です。'),
 ('Ha', '案H＋弱い面', '案Hに、ごく薄い色の面だけを足しました。縁はなく、面は行の高さに沿った丸い形です。気づきやすさを少し足す程度です。'),
 ('Hb', '案H＋薄い面と細い縁', '案Hに、案B2と同じ強さの薄い面と細い縁を足しました。いちばん目立ちますが、案B2よりタイルの色替えが加わる分、少し賑やかです。'),
]

CSS = '''
:root { --st-b-solid:#9a6200; --st-b-text:#6b4300; --st-b-wash:rgba(217,154,26,.11); --st-b-weak:rgba(217,154,26,.07); --st-b-wash2:rgba(217,154,26,.24); --st-b-line:rgba(217,154,26,.38);
        --st-c-solid:#6a3fb0; --st-c-text:#4a2a86; --st-c-wash:rgba(138,91,214,.10); --st-c-weak:rgba(138,91,214,.06); --st-c-wash2:rgba(138,91,214,.22); --st-c-line:rgba(138,91,214,.34);
        --edge-hi:rgba(255,255,255,.75); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --st-b-text:#f4d68a; --st-b-wash:rgba(232,182,74,.12); --st-b-weak:rgba(232,182,74,.08); --st-b-wash2:rgba(232,182,74,.26); --st-b-line:rgba(232,182,74,.38);
  --st-c-text:#d9c4f5; --st-c-wash:rgba(169,139,230,.15); --st-c-weak:rgba(169,139,230,.10); --st-c-wash2:rgba(169,139,230,.28); --st-c-line:rgba(169,139,230,.40);
  --edge-hi:rgba(255,255,255,.09); } }
:root[data-theme="dark"] {
  --st-b-text:#f4d68a; --st-b-wash:rgba(232,182,74,.12); --st-b-weak:rgba(232,182,74,.08); --st-b-wash2:rgba(232,182,74,.26); --st-b-line:rgba(232,182,74,.38);
  --st-c-text:#d9c4f5; --st-c-wash:rgba(169,139,230,.15); --st-c-weak:rgba(169,139,230,.10); --st-c-wash2:rgba(169,139,230,.28); --st-c-line:rgba(169,139,230,.40);
  --edge-hi:rgba(255,255,255,.09); }
@media (prefers-contrast: more) { :root { --st-b-line:rgba(154,98,0,.85); --st-c-line:rgba(106,63,176,.85); } }
.mock-note { display: grid; gap: 10px; } .mock-note p { max-width: 72ch; }
.mock-theme { display: flex; flex-wrap: wrap; gap: 8px; }
.idea-head { display: grid; gap: 4px; margin-bottom: 4px; } .idea-head p { font-size: 14px; color: var(--rg-muted); line-height: 1.7; }
.st-text { display: inline-flex; align-items: center; gap: 5px; font-size: 14px; font-weight: 700; }
.st-text-b { color: var(--st-b-text); } .st-text-c { color: var(--st-c-text); }
.st-glyph { width: 16px; height: 16px; stroke-width: 2.2; flex: none; }
/* H: タイルの色替え（共通） */
.rg-list-row.st-b .cat-ico { background: var(--st-b-wash2); color: var(--st-b-text); box-shadow: 0 0 0 1.5px var(--st-b-line); }
.rg-list-row.st-c .cat-ico { background: var(--st-c-wash2); color: var(--st-c-text); box-shadow: 0 0 0 1.5px var(--st-c-line); }
/* 面を足す案 */
.idea-Ha .rg-list-row.st-b, .idea-Hb .rg-list-row.st-b, .idea-Ha .rg-list-row.st-c, .idea-Hb .rg-list-row.st-c { margin: 3px -10px; padding-inline: 10px; border-top-color: transparent; border-radius: 16px; }
.idea-Ha .rg-list-row.st-b { background: var(--st-b-weak); } .idea-Ha .rg-list-row.st-c { background: var(--st-c-weak); }
.idea-Hb .rg-list-row.st-b { background: var(--st-b-wash); box-shadow: inset 0 0 0 1px var(--st-b-line), inset 0 1px 0 var(--edge-hi); }
.idea-Hb .rg-list-row.st-c { background: var(--st-c-wash); box-shadow: inset 0 0 0 1px var(--st-c-line), inset 0 1px 0 var(--edge-hi); }
.idea-Hb .rg-list-row.st-b .cat-ico { box-shadow: 0 0 0 1.5px var(--st-b-line); } .idea-Hb .rg-list-row.st-c .cat-ico { box-shadow: 0 0 0 1.5px var(--st-c-line); }
.idea-Ha .rg-list-row.st-b + .rg-list-row, .idea-Ha .rg-list-row.st-c + .rg-list-row, .idea-Hb .rg-list-row.st-b + .rg-list-row, .idea-Hb .rg-list-row.st-c + .rg-list-row { border-top-color: transparent; }
'''

parts = ['<div class="rg-theme"><div class="rg-ambient" aria-hidden="true"></div>',
 '<header class="rg-nav"><div class="dock-brand"><h1 class="rg-brand">祝福・呪いの見せ方 第3案（モック）</h1><span class="rg-muted">案Hをベースに、行の面の強さを比較</span></div><span></span>',
 '<div class="mock-theme" role="group" aria-label="表示テーマ"><button class="rg-chip" type="button" data-theme-set="light">ライト</button><button class="rg-chip" type="button" data-theme-set="dark">ダーク</button><button class="rg-chip" type="button" data-theme-set="" aria-pressed="true">端末に合わせる</button></div></header>',
 '<main class="rg-page rg-stack">',
 '<section class="rg-surface mock-note"><h2 class="rg-heading">見比べ方</h2><p>3案とも、先頭の種別タイルの色替えと、名前の横の「アイコン＋文字」のラベルは同じです。違うのは、行の背景だけです。縦にスクロールして流し見したときに、祝福・呪いの行がどれだけ目に入るかで選んでください。</p><p class="rg-muted">6行は見比べやすいよう、価格の異なるものを混ぜています。実際の画面では同じ価格のものだけが並びます。</p></section>',
 '<div class="results-grid">']
for key, title, desc in IDEAS:
    parts.append(f'<section class="rg-surface idea-{key}"><div class="idea-head"><h2 class="rg-heading">{title}</h2><p>{desc}</p></div><ul>{"".join(row(r) for r in ROWS)}</ul></section>')
parts.append('</div></main></div>')
parts.append('''<script>
(function(){ var root=document.documentElement; var btns=document.querySelectorAll('[data-theme-set]');
 btns.forEach(function(b){ b.addEventListener('click',function(){ var v=b.getAttribute('data-theme-set'); if(v) root.setAttribute('data-theme',v); else root.removeAttribute('data-theme');
  btns.forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true':'false'); }); }); });
})();
</script>''')
print(write_page('祝福・呪いの見せ方 第3案（モック）', CSS, '\n'.join(parts), '../mocks/state-visual-v3.html'))
