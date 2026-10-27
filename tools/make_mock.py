"""祝福・呪いの見た目の比較モックを mocks/state-visual.html に生成する。
実行: cd tools && LINESEED_DIR=fonts/ python3 -I make_mock.py
アプリ本体と同じCSS・同じ行マークアップを使い、状態の見せ方だけを変えて並べる。"""
import re, io, os, base64
from fontTools import subset
from fontTools.ttLib import TTFont

tpl = open('template.html', encoding='utf8').read()
css = re.search(r'<style>(.*?)</style>', tpl, re.S).group(1)

ICON = {
 '巻物': '<path d="M8 4h11v13a3 3 0 0 1-3 3H6a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3h2z"/><path d="M12.5 9H16M12.5 12.5H16"/>',
 '草・種': '<path d="M5 19c0-8.5 5-14 14-14 0 9-5.5 14-14 14z"/><path d="M5 19l8-8"/>',
 '腕輪': '<circle cx="12" cy="14" r="6"/><path d="M12 2.5l2.3 2.7L12 8 9.7 5.2z"/>',
 '杖': '<path d="M4.5 19.5L14 10"/><path d="M17.5 2.5l1.3 2.7 2.7 1.3-2.7 1.3-1.3 2.7-1.3-2.7-2.7-1.3 2.7-1.3z"/>',
}
BELL = '<path d="M12 3a5 5 0 0 0-5 5v3.5L5.5 15h13L17 11.5V8a5 5 0 0 0-5-5z"/><path d="M10 18.5a2 2 0 0 0 4 0"/>'
SKULL = '<path d="M12 3.5c-4 0-7 2.8-7 6.5 0 2.2 1 3.8 2.5 4.8V18h9v-3.2C18 13.8 19 12.2 19 10c0-3.7-3-6.5-7-6.5z"/><circle cx="9.2" cy="10.5" r="1.3"/><circle cx="14.8" cy="10.5" r="1.3"/><path d="M10.5 18v-2M13.5 18v-2"/>'
def svg(inner, cls='cat-ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
CHECK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="10" r="8"/><path d="M6.5 10.2l2.5 2.5 4.5-5"/></svg>'
STN = {'n': '通常', 'b': '祝福', 'c': '呪い'}
MULT = {'b': '×2', 'c': '×0.87'}

# 表示サンプル（価格は実データの値。並び順は「通常 → 祝福 → 呪い」）
ROWS = [
 dict(cat='巻物', name='おはらいの巻物', st='n', other='買値 600', hint=True),
 dict(cat='草・種', name='毒消し草', st='n', other='買値 600'),
 dict(cat='巻物', name='混乱の巻物', st='b', other='買値 600'),
 dict(cat='草・種', name='薬草', st='b', other='買値 80'),
 dict(cat='杖', name='ただの杖', st='c', other='買値 435', extra='回数 5'),
 dict(cat='腕輪', name='胃縮小の腕輪', st='c', other='買値 3,045'),
]

def row(r, idea):
    st = r['st']
    icon = svg(ICON[r['cat']])
    if idea == 'A' and st != 'n':
        icon = f'<span class="ico-wrap">{icon}<span class="corner corner-{st}">{svg(BELL if st=="b" else SKULL, "")}</span></span>'
    hint = '<span class="tag tag-hint">使うと選択画面</span>' if r.get('hint') else ''
    pill = ''
    if idea in ('C', 'E') and st != 'n':
        pill = f'<span class="pill pill-{st}">{svg(BELL if st=="b" else SKULL, "")}{STN[st]} {MULT[st]}</span>'
    tag = ''
    if idea in ('0', 'A', 'B'):
        tag = f'<span class="tag tag-{st}">{STN[st]}</span>'
    extra = f'<span>{r["extra"]}</span>' if r.get('extra') else ''
    cls = f'rg-list-row st-{st}'
    return (f'<li class="{cls}"><div><p class="rg-list-title"><span class="nm">{icon}<span>{r["name"]}</span></span>{pill}{hint}</p>'
            f'<div class="rg-list-copy"><span class="var">{tag}<span>{r["other"]}</span>{extra}</span></div></div>'
            f'<button class="rg-button judge" type="button">{CHECK}判断完了</button></li>')

def band(st):
    label = {'b': '祝福（買値・売値とも2倍）', 'c': '呪い（買値・売値とも0.87倍）'}[st]
    return f'<li class="state-band band-{st}">{svg(BELL if st=="b" else SKULL, "")}{label}</li>'

def list_html(idea):
    out = '<ul>'
    last = None
    for r in ROWS:
        if idea == 'D' and r['st'] != last and r['st'] != 'n':
            out += band(r['st'])
        last = r['st']
        out += row(r, idea)
    return out + '</ul>'

IDEAS = [
 ('0', '現状', '淡い色の小さなタグ。どの行が祝福・呪いかは、タグの文字を読まないと分かりません。'),
 ('A', '案A：ゲームのマークを重ねる', '種別アイコンの角に、ゲーム内と同じ「ベル（祝福）」「ドクロ（呪い）」を重ねます。プレイヤーが見慣れた記号で気づけます。タグは残します。'),
 ('B', '案B：行ごと色づける', '祝福は金、呪いは紫で、行の背景と左端の帯を染めます。文字を読まなくても、縦に流し見るだけで色の違いが目に入ります。'),
 ('C', '案C：濃いバッジ＋倍率', '祝福・呪いだけ、塗りつぶしの濃いバッジをアイテム名の横に付けます。ベル／ドクロのアイコンと「×2」「×0.87」入りです。通常にはタグを付けず、例外だけを目立たせます。'),
 ('D', '案D：区切りの帯', '並び順が通常→祝福→呪いなので、状態が変わる位置に帯の見出しを入れます。行ごとのタグは不要になり、行は今よりすっきりします。'),
 ('E', '案E：B＋Cの組み合わせ（おすすめ）', '行の色づけと濃いバッジを併用します。色が見えない人でも、アイコンと文字で区別できます。通常の行は何も付けず、静かなままです。'),
]

MOCK_CSS = '''
:root { --st-b-solid:#9a6200; --st-b-on:#fff; --st-b-tint:#fff3d6; --st-b-stripe:#d99a1a; --st-b-text:#6b4300;
        --st-c-solid:#6a3fb0; --st-c-on:#fff; --st-c-tint:#efe6fb; --st-c-stripe:#8a5bd6; --st-c-text:#4a2a86; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --st-b-solid:#e8b64a; --st-b-on:#2b1d00; --st-b-tint:rgba(232,182,74,.14); --st-b-stripe:#e8b64a; --st-b-text:#f4d68a;
  --st-c-solid:#a98be6; --st-c-on:#1d1033; --st-c-tint:rgba(169,139,230,.16); --st-c-stripe:#a98be6; --st-c-text:#d9c4f5; } }
:root[data-theme="dark"] {
  --st-b-solid:#e8b64a; --st-b-on:#2b1d00; --st-b-tint:rgba(232,182,74,.14); --st-b-stripe:#e8b64a; --st-b-text:#f4d68a;
  --st-c-solid:#a98be6; --st-c-on:#1d1033; --st-c-tint:rgba(169,139,230,.16); --st-c-stripe:#a98be6; --st-c-text:#d9c4f5; }
.mock-note { display: grid; gap: 8px; }
.mock-note p { max-width: 72ch; }
.mock-theme { display: flex; flex-wrap: wrap; gap: 8px; }
.idea-head { display: grid; gap: 4px; margin-bottom: 4px; }
.idea-head p { font-size: 14px; color: var(--rg-muted); line-height: 1.7; }
.rg-list-row.st-n { }
.ico-wrap { position: relative; display: inline-flex; flex: none; }
.corner { position: absolute; right: -6px; bottom: -6px; width: 20px; height: 20px; border-radius: 50%; display: grid; place-items: center; border: 2px solid var(--rg-solid-surface); }
.corner svg { width: 12px; height: 12px; stroke-width: 2.4; }
.corner-b { background: var(--st-b-solid); color: var(--st-b-on); }
.corner-c { background: var(--st-c-solid); color: var(--st-c-on); }
.pill { display: inline-flex; align-items: center; gap: 5px; padding: 1px 12px 1px 9px; border-radius: 999px; font-size: 14px; font-weight: 700; line-height: 1.7; white-space: nowrap; }
.pill svg { width: 16px; height: 16px; stroke-width: 2.2; flex: none; }
.pill-b { background: var(--st-b-solid); color: var(--st-b-on); }
.pill-c { background: var(--st-c-solid); color: var(--st-c-on); }
.idea-B .rg-list-row.st-b, .idea-E .rg-list-row.st-b { background: var(--st-b-tint); box-shadow: inset 5px 0 0 var(--st-b-stripe); }
.idea-B .rg-list-row.st-c, .idea-E .rg-list-row.st-c { background: var(--st-c-tint); box-shadow: inset 5px 0 0 var(--st-c-stripe); }
.idea-B .rg-list-row.st-b, .idea-B .rg-list-row.st-c, .idea-E .rg-list-row.st-b, .idea-E .rg-list-row.st-c { margin-inline: -12px; padding-inline: 20px 12px; border-top-color: transparent; border-radius: 12px; }
.state-band { display: flex; align-items: center; gap: 8px; margin-top: 16px; padding: 6px 14px; border-radius: 10px; font-size: 14px; font-weight: 700; }
.state-band svg { width: 18px; height: 18px; stroke-width: 2.2; flex: none; }
.band-b { background: var(--st-b-tint); color: var(--st-b-text); box-shadow: inset 5px 0 0 var(--st-b-stripe); }
.band-c { background: var(--st-c-tint); color: var(--st-c-text); box-shadow: inset 5px 0 0 var(--st-c-stripe); }
.idea-D .state-band + .rg-list-row { border-top-color: transparent; }
'''

parts = ['<div class="rg-theme"><div class="rg-ambient" aria-hidden="true"></div>',
 '<header class="rg-nav"><div class="dock-brand"><h1 class="rg-brand">祝福・呪いの見せ方（モック）</h1><span class="rg-muted">デザイン案の比較用。アプリ本体には反映していません</span></div><span></span>',
 '<div class="mock-theme" role="group" aria-label="表示テーマ"><button class="rg-chip" type="button" data-theme-set="light">ライト</button><button class="rg-chip" type="button" data-theme-set="dark">ダーク</button><button class="rg-chip" type="button" data-theme-set="" aria-pressed="true">端末に合わせる</button></div></header>',
 '<main class="rg-page rg-stack">',
 '<section class="rg-surface mock-note"><h2 class="rg-heading">見方</h2><p>同じ6行（通常2、祝福2、呪い2）を、案ごとに見せ方だけ変えて並べています。画面幅を狭めるとスマホの見え方も確認できます。上のボタンでダークモードも切り替えられます。</p><p class="rg-muted">価格は実データから取った値ですが、6行は見比べやすいよう価格の異なるものを1つの一覧に混ぜています。実際の画面では同じ価格のものだけが並びます。</p></section>',
 '<div class="results-grid">']
for key, title, desc in IDEAS:
    parts.append(f'<section class="rg-surface idea-{key}"><div class="idea-head"><h2 class="rg-heading">{title}</h2><p>{desc}</p></div>{list_html(key)}</section>')
parts.append('</div></main></div>')
parts.append('''<script>
(function(){ var root=document.documentElement; var btns=document.querySelectorAll('[data-theme-set]');
 btns.forEach(function(b){ b.addEventListener('click',function(){ var v=b.getAttribute('data-theme-set'); if(v) root.setAttribute('data-theme',v); else root.removeAttribute('data-theme');
  btns.forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true':'false'); }); }); });
})();
</script>''')
body = '\n'.join(parts)

html = ('<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex">\n<title>祝福・呪いの見せ方（モック）</title>\n<style>' + css + MOCK_CSS + '</style>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
chars = set(html) | set(chr(c) for c in range(0x20, 0x7f)) | {chr(c) for c in range(0x3040, 0x3100)}
kit = os.environ.get('LINESEED_DIR', 'fonts/')
def sub(fn):
    opt = subset.Options(); opt.flavor = 'woff2'; opt.layout_features = ['*']; opt.notdef_outline = True
    f = TTFont(kit + fn); s = subset.Subsetter(opt); s.populate(unicodes=[ord(c) for c in chars if ord(c) > 0x1f]); s.subset(f)
    b = io.BytesIO(); f.flavor = 'woff2'; f.save(b); return base64.b64encode(b.getvalue()).decode()
html = html.replace('/*FONT_REG*/', sub('LINESeedJP-Regular.woff2')).replace('/*FONT_BOLD*/', sub('LINESeedJP-Bold.woff2'))
open('../mocks/state-visual.html', 'w', encoding='utf8').write(html)
print(len(html))
