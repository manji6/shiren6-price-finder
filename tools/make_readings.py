"""アイテム名の読み仮名（ひらがな）を tools/readings.json に生成する。名前 → "読み1|読み2"（別の読みは | で区切る）。
辞書ライブラリ（pykakasi）で下書きを作り、ゲームでの呼び方と違うものを OVERRIDES で直す。
実行: pip install pykakasi && cd tools && python3 -I make_readings.py"""
import json
from pykakasi import kakasi

OVERRIDES = {
    # 草（〜そう）。「くさ」と打つ人も多いので、別の読みとして残す
    '混乱草': 'こんらんそう|こんらんくさ', '睡眠草': 'すいみんそう|すいみんくさ', '目つぶし草': 'めつぶしそう|めつぶしくさ',
    'めぐすり草': 'めぐすりそう|めぐすりくさ', 'すばやさ草': 'すばやさそう|すばやさくさ', 'パワーアップ草': 'ぱわーあっぷそう|ぱわーあっぷくさ',
    '高飛び草': 'たかとびそう|たかとびくさ', 'くねくね草': 'くねくねそう|くねくねくさ', 'いやし草': 'いやしそう|いやしくさ',
    'かぐわし草': 'かぐわしそう|かぐわしくさ', 'ドラゴン草': 'どらごんそう|どらごんくさ', '無敵草': 'むてきそう|むてきくさ',
    '毒消し草': 'どくけしそう|どくけしくさ', 'しあわせ草': 'しあわせそう|しあわせくさ',
    '弾きよけの腕輪': 'はじきよけのうでわ', '身代わりの杖': 'みがわりのつえ', '変化の壺': 'へんげのつぼ|へんかのつぼ',
    '魔物部屋の巻物': 'まものべやのまきもの|まものへやのまきもの', '真空斬りの巻物': 'しんくうぎりのまきもの|しんくうきりのまきもの',
    '天の恵みの巻物': 'てんのめぐみのまきもの|あめのめぐみのまきもの', '地の恵みの巻物': 'ちのめぐみのまきもの|つちのめぐみのまきもの',
    '諸刃の腕輪': 'もろはのうでわ|もろばのうでわ', '土塊の杖': 'つちくれのつえ|どかいのつえ',
}

def build(names):
    k = kakasi(); out = {}
    for n in names:
        out[n] = OVERRIDES.get(n) or ''.join(x['hira'] for x in k.convert(n))
    return out

if __name__ == '__main__':
    items = json.load(open('items.json', encoding='utf8'))
    names = [i['name'] for i in items if not i['known']]
    out = build(names)
    missing = [n for n in OVERRIDES if n not in out]
    assert not missing, f'OVERRIDES にあるが対象外の名前: {missing}'
    json.dump(out, open('readings.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(len(out), '件')
