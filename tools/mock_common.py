"""モック生成の共通部品。アプリ本体(template.html)と同じCSS・行マークアップを使うための補助。"""
import re, io, os, base64
from fontTools import subset
from fontTools.ttLib import TTFont

def app_css():
    tpl = open('template.html', encoding='utf8').read()
    return re.search(r'<style>(.*?)</style>', tpl, re.S).group(1)

ICON = {
 '巻物': '<path d="M8 4h11v13a3 3 0 0 1-3 3H6a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3h2z"/><path d="M12.5 9H16M12.5 12.5H16"/>',
 '草・種': '<path d="M5 19c0-8.5 5-14 14-14 0 9-5.5 14-14 14z"/><path d="M5 19l8-8"/>',
 '腕輪': '<circle cx="12" cy="14" r="6"/><path d="M12 2.5l2.3 2.7L12 8 9.7 5.2z"/>',
 '杖': '<path d="M4.5 19.5L14 10"/><path d="M17.5 2.5l1.3 2.7 2.7 1.3-2.7 1.3-1.3 2.7-1.3-2.7-2.7-1.3 2.7-1.3z"/>',
}
BELL = '<path d="M12 3a5 5 0 0 0-5 5v3.5L5.5 15h13L17 11.5V8a5 5 0 0 0-5-5z"/><path d="M10 18.5a2 2 0 0 0 4 0"/>'
SKULL = '<path d="M12 3.5c-4 0-7 2.8-7 6.5 0 2.2 1 3.8 2.5 4.8V18h9v-3.2C18 13.8 19 12.2 19 10c0-3.7-3-6.5-7-6.5z"/><circle cx="9.2" cy="10.5" r="1.3"/><circle cx="14.8" cy="10.5" r="1.3"/><path d="M10.5 18v-2M13.5 18v-2"/>'
DOT = '<circle cx="12" cy="12" r="4.5"/>'
GLYPH = {'b': BELL, 'c': SKULL, 'n': DOT}
STN = {'n': '通常', 'b': '祝福', 'c': '呪い'}
MULT = {'b': '×2', 'c': '×0.87'}
CHECK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="10" r="8"/><path d="M6.5 10.2l2.5 2.5 4.5-5"/></svg>'

def svg(inner, cls='cat-ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

def write_page(title, extra_css, body, out, head_extra='', robots='noindex', gtm=False):
    html = ('<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + (open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gtm.html'), encoding='utf8').read() if gtm else '') + f'<meta name="robots" content="{robots}">\n<title>{title}</title>\n{head_extra}<style>' + app_css() + extra_css + '</style>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
    chars = set(html) | set(chr(c) for c in range(0x20, 0x7f)) | {chr(c) for c in range(0x3040, 0x3100)}
    kit = os.environ.get('LINESEED_DIR', 'fonts/')
    def sub(fn):
        opt = subset.Options(); opt.flavor = 'woff2'; opt.layout_features = ['*']; opt.notdef_outline = True
        f = TTFont(kit + fn); s = subset.Subsetter(opt); s.populate(unicodes=[ord(c) for c in chars if ord(c) > 0x1f]); s.subset(f)
        b = io.BytesIO(); f.flavor = 'woff2'; f.save(b); return base64.b64encode(b.getvalue()).decode()
    html = html.replace('/*FONT_REG*/', sub('LINESeedJP-Regular.woff2')).replace('/*FONT_BOLD*/', sub('LINESeedJP-Bold.woff2'))
    open(out, 'w', encoding='utf8').write(html)
    return len(html)
