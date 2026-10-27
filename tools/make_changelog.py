"""changelog.json から更新履歴ページ public/changelog/index.html を生成する。
実行: cd tools && LINESEED_DIR=fonts/ python3 -I make_changelog.py"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_common import write_page

BASE = 'https://shiren6.amanohashi.date'
entries = json.load(open('changelog.json', encoding='utf8'))

def jp_date(s):
    y, m, d = s.split('-')
    return f'{int(y)}年{int(m)}月{int(d)}日'

rows = ''.join(
    f'<div class="rg-document-row"><h2 class="rg-heading"><time datetime="{e["date"]}">{jp_date(e["date"])}</time></h2>'
    f'<div class="rg-copy"><ul class="changes">{"".join("<li>" + html.escape(i) + "</li>" for i in e["items"])}</ul></div></div>'
    for e in entries)

body = ('<div class="rg-theme"><div class="rg-ambient" aria-hidden="true"></div>'
        '<header class="rg-nav"><div class="dock-brand"><h1 class="rg-brand">更新履歴</h1><span class="rg-muted">シレン6 値段識別</span></div><span></span>'
        '<a class="rg-button" href="/">値段識別に戻る</a></header>'
        f'<main class="rg-page rg-stack"><section class="rg-surface" aria-label="更新履歴">{rows}</section>'
        '<footer class="site-foot rg-muted"><p>風来のシレン6の非公式ファンツールです。ゲーム内の名称・データの権利は、それぞれの権利者に帰属します。</p></footer></main></div>')

css = '''
a.rg-button { text-decoration: none; }
.rg-theme .changes { display: grid; gap: 8px; padding-left: 1.3em; list-style: disc; }
.site-foot { padding: 4px 4px 0; text-align: center; }
'''
desc = 'シレン6 値段識別の更新履歴です。'
head = (f'<meta name="description" content="{desc}">\n<link rel="canonical" href="{BASE}/changelog/">\n'
        '<meta name="color-scheme" content="light dark">\n'
        '<meta name="theme-color" content="#eaf1fa" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#0d1622" media="(prefers-color-scheme: dark)">\n'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '<meta property="og:type" content="website">\n<meta property="og:locale" content="ja_JP">\n'
        f'<meta property="og:site_name" content="シレン6 値段識別">\n<meta property="og:url" content="{BASE}/changelog/">\n'
        f'<meta property="og:title" content="更新履歴｜シレン6 値段識別">\n<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:image" content="{BASE}/og-image.png">\n<meta name="twitter:card" content="summary_large_image">\n')
os.makedirs('../public/changelog', exist_ok=True)
print(write_page('更新履歴｜シレン6 値段識別', css, body, '../public/changelog/index.html', head, 'index, follow'))
