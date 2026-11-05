"""「分かったアイテムを入れる方法」の動くモックを mocks/judge-input.html に生成する。
実行: cd tools && python3 -I make_judge_mock.py   （先に assemble.py で public/index.html を作っておく）
public/index.html の画面に、judge_mock.css / judge_mock.js を重ねるだけ。検索・判断完了などは本物と同じに動く。"""
import os, re
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, '..')
html = open(os.path.join(root, 'public/index.html'), encoding='utf8').read()
css = open(os.path.join(here, 'judge_mock.css'), encoding='utf8').read()
js = open(os.path.join(here, 'judge_mock.js'), encoding='utf8').read()
html = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\n?', '', html, flags=re.S)
html = re.sub(r'<link rel="canonical"[^>]*>\n?|<meta property="og:[^>]*>\n?|<meta name="twitter:[^>]*>\n?', '', html)
html = re.sub(r'<link rel="preload"[^>]*>\n?', '', html)
html = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', html, flags=re.S)
html = html.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
html = re.sub(r'<title>.*?</title>', '<title>シレン6 値段識別（入力方法のモック）</title>', html, count=1)
# 背景画像は /bg/ の絶対パス。ファイルとして単体で開いても出るよう、モックでは画像を内蔵する
import base64
def bg(name): return 'url(data:image/png;base64,' + base64.b64encode(open(os.path.join(root, 'public/bg', name + '.png'), 'rb').read()).decode() + ')'
html = html.replace('url(/bg/meadow.png)', bg('meadow')).replace('url(/bg/night.png)', bg('night'))
assert html.count('</style>') == 1 and html.count('</body>') == 1
import json
readings = json.load(open(os.path.join(here, 'readings.json'), encoding='utf8'))   # 名前 → 読み仮名（ひらがな）。make_readings.py で生成
html = html.replace('</style>', css + '\n</style>').replace('</body>', '<script>window.JM_READINGS=' + json.dumps(readings, ensure_ascii=False) + ';</script><script>' + js + '</script>\n</body>')
open(os.path.join(root, 'mocks/judge-input.html'), 'w', encoding='utf8').write(html)
print(len(html))
