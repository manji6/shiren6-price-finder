"""Wikiの「武器」「盾」「印」ページから、武器・盾の値段計算に使うデータを tools/ws_data.json に作る。
使い方: python3 -I build_ws_data.py <UTF-8に変換済みのhtmlがあるフォルダ>   （weapon.html / shield.html / seal.html）
取得: curl -sS -L "https://shiren6.game-info.wiki/d/<EUC-JPでURLエンコードしたページ名>" | iconv -f EUC-JP -t UTF-8//IGNORE
"""
import re, sys, html, json, os

def text(path):
    t = open(path, encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    s = re.sub(r'</(tr|p|h\d|li|div)>', '\n', s)
    s = re.sub(r'</t[dh]>', ' | ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\n\s*\n+', '\n', html.unescape(s))

def items(path):
    s = text(path)
    s = s[:s.index('詳細説明')]
    out = []
    for m in re.finditer(r'^(.+?) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (.*?) \| (.*?) \| (.*?) \|', s, re.M):
        name, base, slots, buy, sell, reso, seal, note = m.groups()
        out.append(dict(n=name.strip(), base=int(base), slots=int(slots), buy=int(buy), sell=int(sell), seal=seal.strip() if seal.strip() != '-' else ''))
    return out

def seals(path):
    s = text(path)
    s = s[s.index('武器印 \nNo.'):]
    w, sh = s.split('盾印 \nNo.', 1)
    def rows(block, kind):
        out = []
        for m in re.finditer(r'^(\d+) \| (.+?) \| (.+?) \| (.+?) \| ([\d,]+)(?:\*\d+)? \| ([\d,]+) \| ', block, re.M):
            no, ab, name, src, buy, sell = m.groups()
            out.append(dict(k=kind, no=int(no), ab=ab.strip(), n=name.strip(), nat=(src.strip() == '天然'), buy=int(buy.replace(',', '')), sell=int(sell.replace(',', ''))))
        return out
    return rows(w, 'w'), rows(sh, 's')

if __name__ == '__main__':
    d = sys.argv[1]
    sw, ss = seals(os.path.join(d, 'seal.html'))
    data = dict(weapons=items(os.path.join(d, 'weapon.html')), shields=items(os.path.join(d, 'shield.html')), seals=sw + ss)
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(data, open(os.path.join(here, 'ws_data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('武器', len(data['weapons']), '盾', len(data['shields']), '武器印', len(sw), '盾印', len(ss))
