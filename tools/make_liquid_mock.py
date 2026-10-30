"""Liquid Glass版の動くモックを mocks/liquid-glass.html に生成する。
実際のアプリ（public/index.html）に、liquid.css と背景のドット絵を重ねるだけなので、検索・判断完了などは本物と同じに動く。
実行: cd tools && python3 -I make_liquid_mock.py"""
import base64, os, re
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, '..')
html = open(os.path.join(root, 'public/index.html'), encoding='utf8').read()
css = open(os.path.join(here, 'liquid.css'), encoding='utf8').read()

def data_uri(name):
    b = open(os.path.join(root, 'mocks/assets', f'bg-{name}.png'), 'rb').read()
    return 'url(data:image/png;base64,' + base64.b64encode(b).decode() + ')'
scene_vars = ':root {' + ''.join(f' --scene-{n}: {data_uri(n)};' for n in ('dungeon', 'meadow', 'night')) + ' }\n'

# モック用の整形: 計測タグ・正規URL・OGPを外し、検索に載らないようにする
html = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\n?', '', html, flags=re.S)
html = re.sub(r'<link rel="canonical"[^>]*>\n?', '', html)
html = re.sub(r'<meta property="og:[^>]*>\n?|<meta name="twitter:[^>]*>\n?', '', html)
html = html.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
html = re.sub(r'<title>.*?</title>', '<title>シレン6 値段識別（Liquid Glass モック）</title>', html, count=1)
html = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', html, flags=re.S)
assert html.count('</style>') == 1
html = html.replace('</style>', scene_vars + css + '\n</style>')
amb = '<div class="rg-ambient" aria-hidden="true"></div>'
assert html.count(amb) == 1
html = html.replace(amb, '<div class="lg-scene" aria-hidden="true"></div>')
switch = '''<div class="lg-switch" role="group" aria-label="背景の切り替え（モック）"><span>背景</span>
<button type="button" data-scene="dungeon" aria-pressed="true">石畳の部屋</button><button type="button" data-scene="meadow" aria-pressed="false">草原</button><button type="button" data-scene="night" aria-pressed="false">夜の部屋</button></div>
<script>(function(){var r=document.documentElement,b=document.querySelectorAll('.lg-switch [data-scene]');r.setAttribute('data-scene','dungeon');
b.forEach(function(x){x.addEventListener('click',function(){r.setAttribute('data-scene',x.getAttribute('data-scene'));b.forEach(function(y){y.setAttribute('aria-pressed',y===x?'true':'false');});});});})();</script>
'''
assert html.count('</body>') == 1
html = html.replace('</body>', switch + '</body>')
open(os.path.join(root, 'mocks/liquid-glass.html'), 'w', encoding='utf8').write(html)
print(len(html))
