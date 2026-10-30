"""SFC（スーパーファミコン）風のドット絵の背景を生成する。すべてオリジナルの絵で、既存ゲームの画像は使っていない。
実行: cd tools && python3 -I make_bg.py   → ../public/bg/{meadow,night}.png（336x192, 16x16タイル21x12枚）
CSS側で image-rendering: pixelated により拡大して使う。"""
import os, random
from PIL import Image, ImageDraw

T = 16; W, H = 21, 12
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'bg')
os.makedirs(OUT, exist_ok=True)

def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ---- SFC風の限られたパレット
P = dict(
    floor=hexc('#7b7f9e'), floor_hi=hexc('#9a9fbd'), floor_lo=hexc('#5c607d'), grout=hexc('#454866'),
    wall=hexc('#4a4f73'), wall_hi=hexc('#6a709a'), wall_lo=hexc('#323654'), mortar=hexc('#262944'), cap=hexc('#8a90b8'),
    grass=hexc('#58b04c'), grass_hi=hexc('#7acb5c'), grass_lo=hexc('#3f9440'), grass_dk=hexc('#2f7a38'),
    dirt=hexc('#c9a26a'), dirt_hi=hexc('#e0bd84'), dirt_lo=hexc('#a98250'),
    water=hexc('#4a8fd8'), water_hi=hexc('#8cc4f4'), water_lo=hexc('#336bb0'),
    trunk=hexc('#7a4a2a'), trunk_lo=hexc('#52301c'),
    ol=hexc('#2a1d2e'),
)

def noise_tile(im, tx, ty, base, hi, lo, rnd, density=0.10):
    d = ImageDraw.Draw(im)
    x0, y0 = tx * T, ty * T
    d.rectangle([x0, y0, x0 + T - 1, y0 + T - 1], fill=base)
    for _ in range(int(T * T * density)):
        x, y = rnd.randrange(T), rnd.randrange(T)
        d.point((x0 + x, y0 + y), fill=rnd.choice([hi, lo]))

def stone_floor(im, tx, ty, rnd):
    noise_tile(im, tx, ty, P['floor'], P['floor_hi'], P['floor_lo'], rnd, 0.07)
    d = ImageDraw.Draw(im); x0, y0 = tx * T, ty * T
    d.line([x0, y0 + T - 1, x0 + T - 1, y0 + T - 1], fill=P['grout'])
    d.line([x0 + T - 1, y0, x0 + T - 1, y0 + T - 1], fill=P['grout'])
    d.line([x0, y0, x0 + T - 2, y0], fill=P['floor_hi'])
    d.line([x0, y0, x0, y0 + T - 2], fill=P['floor_hi'])

def brick_wall(im, tx, ty, rnd, top=False):
    d = ImageDraw.Draw(im); x0, y0 = tx * T, ty * T
    d.rectangle([x0, y0, x0 + T - 1, y0 + T - 1], fill=P['wall'])
    for row in range(2):
        yy = y0 + row * 8
        d.line([x0, yy + 7, x0 + T - 1, yy + 7], fill=P['mortar'])
        off = 0 if row == 0 else 8
        for bx in (off, off + 8):
            xx = x0 + (bx % 16)
            d.line([xx, yy, xx, yy + 7], fill=P['mortar'])
        d.line([x0, yy, x0 + T - 1, yy], fill=P['wall_hi'])
        for _ in range(6):
            d.point((x0 + rnd.randrange(T), yy + rnd.randrange(1, 7)), fill=rnd.choice([P['wall_hi'], P['wall_lo']]))
    if top:
        d.rectangle([x0, y0, x0 + T - 1, y0 + 1], fill=P['cap'])

def torch(im, tx, ty):
    d = ImageDraw.Draw(im); x, y = tx * T + 4, ty * T + 1
    d.rectangle([x + 2, y + 8, x + 3, y + 13], fill=P['trunk']); d.rectangle([x + 1, y + 7, x + 4, y + 8], fill=P['trunk_lo'])
    for (dx, dy, c) in [(2, 0, '#ffe45e'), (1, 1, '#ffb43a'), (2, 1, '#fff2a0'), (3, 1, '#ffb43a'), (1, 2, '#ff8a2a'), (2, 2, '#ffd35a'), (3, 2, '#ff8a2a'), (1, 3, '#ff6a1e'), (2, 3, '#ffb43a'), (3, 3, '#ff6a1e'), (2, 4, '#ff6a1e')]:
        d.point((x + dx, y + dy + 2), fill=hexc(c))

def glow(im, cx, cy, r, color=(255, 190, 90), strength=0.55):
    """ドット絵らしく4段階に量子化した光の輪（SFCの陰影表現に近づける）"""
    px = im.load()
    for y in range(max(0, cy - r), min(im.height, cy + r)):
        for x in range(max(0, cx - r), min(im.width, cx + r)):
            dist = ((x - cx) ** 2 + ((y - cy) * 1.2) ** 2) ** 0.5
            if dist < r:
                t = (1 - dist / r); t = int(t * 4) / 4 * strength
                px[x, y] = mix(px[x, y], color, t)

def shadow(im, x, y, w):
    d = ImageDraw.Draw(im, 'RGBA'); d.ellipse([x, y, x + w, y + 3], fill=(20, 18, 40, 90))

def outline(d, pts, fill):
    d.polygon(pts, fill=fill, outline=P['ol'])

def scroll(im, x, y):
    d = ImageDraw.Draw(im); shadow(im, x, y + 11, 12)
    d.rectangle([x + 2, y + 2, x + 10, y + 9], fill=hexc('#f4e6c0'), outline=P['ol'])
    d.line([x + 4, y + 4, x + 8, y + 4], fill=hexc('#a0623a')); d.line([x + 4, y + 6, x + 8, y + 6], fill=hexc('#a0623a'))
    for rx in (x, x + 10):
        d.rectangle([rx, y + 1, rx + 2, y + 10], fill=hexc('#d9a35c'), outline=P['ol'])
        d.point((rx + 1, y + 3), fill=hexc('#f6d493'))

def herb(im, x, y):
    d = ImageDraw.Draw(im); shadow(im, x + 1, y + 11, 10)
    d.line([x + 6, y + 11, x + 6, y + 5], fill=P['grass_dk'])
    for (a, b) in [((x + 1, y + 4), (x + 6, y + 8)), ((x + 11, y + 4), (x + 6, y + 8)), ((x + 3, y + 1), (x + 6, y + 6)), ((x + 9, y + 1), (x + 6, y + 6))]:
        d.polygon([a, b, (a[0] + (1 if a[0] < 6 else -1), a[1] + 3)], fill=P['grass_hi'], outline=P['ol'])
    d.ellipse([x + 5, y + 3, x + 7, y + 6], fill=P['grass'], outline=P['ol'])

def pot(im, x, y):
    d = ImageDraw.Draw(im); shadow(im, x, y + 11, 13)
    d.ellipse([x + 1, y + 3, x + 12, y + 12], fill=hexc('#b5603a'), outline=P['ol'])
    d.rectangle([x + 4, y + 1, x + 9, y + 4], fill=hexc('#c97a4a'), outline=P['ol'])
    d.line([x + 4, y + 1, x + 9, y + 1], fill=hexc('#e6a066'))
    d.point((x + 3, y + 6), fill=hexc('#e6a066')); d.point((x + 3, y + 7), fill=hexc('#e6a066'))
    d.line([x + 4, y + 9, x + 9, y + 9], fill=hexc('#8a4326'))

def wand(im, x, y):
    d = ImageDraw.Draw(im); shadow(im, x, y + 11, 12)
    d.line([x + 1, y + 11, x + 9, y + 3], fill=P['ol'], width=3); d.line([x + 1, y + 11, x + 9, y + 3], fill=P['trunk'], width=1)
    for (dx, dy) in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        d.point((x + 10 + dx, y + 2 + dy), fill=hexc('#ffe45e'))
    d.point((x + 12, y + 0), fill=hexc('#fff2a0')); d.point((x + 8, y + 0), fill=hexc('#fff2a0'))

def stairs(im, tx, ty):
    d = ImageDraw.Draw(im); x0, y0 = tx * T, ty * T
    d.rectangle([x0, y0, x0 + T - 1, y0 + T - 1], fill=P['ol'])
    for i in range(5):
        c = mix(P['floor_lo'], P['floor_hi'], i / 4)
        d.rectangle([x0 + 1 + i, y0 + 1 + i * 3, x0 + T - 2, y0 + 3 + i * 3], fill=c)
        d.line([x0 + 1 + i, y0 + 3 + i * 3, x0 + T - 2, y0 + 3 + i * 3], fill=P['grout'])

def traveler(im, x, y):
    """笠をかぶった旅人（一般的な旅人の記号。特定キャラクターではない）"""
    d = ImageDraw.Draw(im); shadow(im, x - 1, y + 21, 14)
    d.polygon([(x + 6, y), (x - 1, y + 8), (x + 13, y + 8)], fill=hexc('#e8c27a'), outline=P['ol'])
    d.line([x + 2, y + 6, x + 10, y + 6], fill=hexc('#c99a52'))
    d.rectangle([x + 3, y + 8, x + 9, y + 12], fill=hexc('#f2cfa4'), outline=P['ol'])
    d.point((x + 5, y + 10), fill=P['ol']); d.point((x + 8, y + 10), fill=P['ol'])
    d.polygon([(x + 2, y + 13), (x + 10, y + 13), (x + 12, y + 20), (x, y + 20)], fill=hexc('#4a7fd0'), outline=P['ol'])
    d.line([x + 3, y + 15, x + 9, y + 15], fill=hexc('#7aa6ec'))
    d.rectangle([x + 3, y + 20, x + 5, y + 22], fill=P['trunk_lo']); d.rectangle([x + 7, y + 20, x + 9, y + 22], fill=P['trunk_lo'])

def dither_vignette(im, strength=0.35):
    px = im.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            dx = (x - w / 2) / (w / 2); dy = (y - h / 2) / (h / 2)
            t = max(0, (dx * dx + dy * dy) ** 0.5 - 0.55) * strength
            t = int(t * 6) / 6
            px[x, y] = mix(px[x, y], (10, 10, 30), min(t, .6))

def dungeon(night=False):
    rnd = random.Random(7 if not night else 11)
    im = Image.new('RGB', (W * T, H * T))
    for ty in range(H):
        for tx in range(W):
            if ty < 3: brick_wall(im, tx, ty, rnd, top=(ty == 0))
            else: stone_floor(im, tx, ty, rnd)
    # 壁の足元の影
    d = ImageDraw.Draw(im, 'RGBA'); d.rectangle([0, 3 * T, W * T, 3 * T + 5], fill=(15, 14, 36, 110))
    torches = [(3, 1), (10, 1), (17, 1)]
    for t in torches: torch(im, *t)
    stairs(im, 18, 8)
    scroll(im, 3 * T + 2, 6 * T + 2); herb(im, 6 * T + 1, 8 * T); pot(im, 9 * T, 6 * T + 3)
    wand(im, 12 * T + 1, 9 * T); traveler(im, 8 * T + 1, 4 * T + 6)
    for (tx, ty) in torches:
        glow(im, tx * T + 7, ty * T + 8, 62 if night else 44, strength=0.75 if night else 0.5)
    if night:
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b = px[x, y]
                lum = (r * .3 + g * .5 + b * .2)
                px[x, y] = mix((int(r * .38), int(g * .42), int(b * .62)), (r, g, b), min(1, max(0, (lum - 150) / 150)) * .55)
    dither_vignette(im, 0.5 if night else 0.3)
    return im

def meadow():
    rnd = random.Random(21)
    im = Image.new('RGB', (W * T, H * T))
    for ty in range(H):
        for tx in range(W):
            noise_tile(im, tx, ty, P['grass'], P['grass_hi'], P['grass_lo'], rnd, 0.10)
    d = ImageDraw.Draw(im)
    # 草の房
    for _ in range(90):
        x, y = rnd.randrange(W * T - 4), rnd.randrange(H * T - 4)
        d.line([x, y + 3, x, y + 1], fill=P['grass_dk']); d.line([x + 2, y + 3, x + 2, y + 1], fill=P['grass_dk']); d.point((x + 1, y + 2), fill=P['grass_hi'])
    # 道
    def path_y(x): return int(5.2 * T + 22 * __import__('math').sin(x / 46.0))
    for x in range(W * T):
        cy = path_y(x)
        for y in range(cy - 11, cy + 11):
            edge = abs(y - cy) > 8
            d.point((x, y), fill=P['dirt_lo'] if edge and rnd.random() < .6 else (P['dirt_hi'] if rnd.random() < .08 else P['dirt']))
    # 池
    d.ellipse([14 * T, 7 * T + 4, 19 * T, 11 * T + 8], fill=P['water_lo'])
    d.ellipse([14 * T + 3, 7 * T + 7, 19 * T - 3, 11 * T + 4], fill=P['water'])
    for (x, y) in [(15 * T + 6, 9 * T), (16 * T + 10, 9 * T + 8), (17 * T + 2, 8 * T + 10)]:
        d.line([x, y, x + 6, y], fill=P['water_hi'])
    # 花
    for _ in range(26):
        x, y = rnd.randrange(8, W * T - 8), rnd.randrange(8, H * T - 8)
        if abs(y - path_y(x)) < 14 or (14 * T - 4 < x < 19 * T + 4 and 7 * T < y < 12 * T): continue
        c = rnd.choice(['#ffffff', '#ffe45e', '#ff9ac0', '#c8a0ff'])
        d.point((x, y), fill=hexc(c)); d.point((x + 1, y), fill=hexc(c)); d.point((x, y + 1), fill=hexc(c)); d.point((x - 1, y), fill=hexc(c)); d.point((x, y - 1), fill=hexc(c))
        d.point((x, y), fill=hexc('#ffd35a'))
    # 木
    def tree(cx, cy):
        d.ellipse([cx - 9, cy + 12, cx + 9, cy + 17], fill=(30, 70, 40))
        d.rectangle([cx - 2, cy + 6, cx + 2, cy + 15], fill=P['trunk'], outline=P['ol'])
        for (rx, ry, r, c) in [(0, 0, 14, P['grass_lo']), (-4, -3, 11, P['grass']), (-2, -6, 7, P['grass_hi'])]:
            d.ellipse([cx + rx - r, cy + ry - r + 2, cx + rx + r, cy + ry + r + 2], fill=c, outline=P['ol'] if r == 14 else None)
        for (dx, dy) in [(-6, -4), (3, -8), (7, 0), (-1, 3)]:
            d.point((cx + dx, cy + dy), fill=P['grass_hi'])
    for (tx, ty) in [(2, 2), (5, 9), (9, 1), (12, 10), (19, 3), (0, 8)]:
        tree(tx * T + 8, ty * T + 4)
    dither_vignette(im, 0.22)
    return im

if __name__ == '__main__':
    for name, im in [('meadow', meadow()), ('night', dungeon(night=True))]:
        im.save(os.path.join(OUT, f'{name}.png'), optimize=True)
        print(name, im.size)
