"""「武器・盾」モードの画面モックを mocks/weapon-shield.html に生成する（実際のWikiデータで計算して動く）。
実行: cd tools && LINESEED_DIR=fonts/ python3 -I make_mock_ws.py
事前に build_ws_data.py で ws_data.json を作っておくこと。"""
import os, sys, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_common import *

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = open(os.path.join(HERE, 'ws_data.json'), encoding='utf8').read()
READ = open(os.path.join(HERE, 'ws_readings.json'), encoding='utf8').read()
# 名前検索（かな・カタカナ・ローマ字・長音のゆるさ）は、アプリ本体（template.html）のコードをそのまま使う
_tpl = open(os.path.join(HERE, 'template.html'), encoding='utf8').read()
SEARCH_JS = _tpl[_tpl.index('var kn = function'):_tpl.index('var HAY = {}')]

def png(name):
    return 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, '..', 'public', 'bg', name), 'rb').read()).decode()

SWORD = '<path d="M14.5 3.5h6v6l-9.5 9.5-6-6z"/><path d="M6.5 14.5l-2.5 2.5M9.5 17.5L7 20M3.5 20.5l2-2"/>'
SHIELD = '<path d="M12 3l7 2.5v6c0 4.4-3 7.4-7 9.5-4-2.1-7-5.1-7-9.5v-6z"/><path d="M12 7.5v10"/>'
STAR = '<path d="M12 3.2l2.6 5.5 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.5l6-.8z"/>'
SCROLL = ICON['巻物']

CSS = '''
[hidden] { display: none !important; }
:root { --scene-meadow: url(__MEADOW__); --scene-night: url(__NIGHT__);
        --st-b-solid:#9a6200; --st-b-text:#6b4300; --st-b-wash:rgba(217,154,26,.11); --st-b-weak:rgba(217,154,26,.07); --st-b-wash2:rgba(217,154,26,.24); --st-b-line:rgba(217,154,26,.38);
        --st-c-solid:#6a3fb0; --st-c-text:#4a2a86; --st-c-wash:rgba(138,91,214,.10); --st-c-weak:rgba(138,91,214,.06); --st-c-wash2:rgba(138,91,214,.22); --st-c-line:rgba(138,91,214,.34); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --st-b-text:#f4d68a; --st-b-wash:rgba(232,182,74,.12); --st-b-weak:rgba(232,182,74,.08); --st-b-wash2:rgba(232,182,74,.26); --st-b-line:rgba(232,182,74,.38);
  --st-c-text:#d9c4f5; --st-c-wash:rgba(169,139,230,.15); --st-c-weak:rgba(169,139,230,.10); --st-c-wash2:rgba(169,139,230,.28); --st-c-line:rgba(169,139,230,.40); } }
:root[data-theme="dark"] {
  --st-b-text:#f4d68a; --st-b-wash:rgba(232,182,74,.12); --st-b-weak:rgba(232,182,74,.08); --st-b-wash2:rgba(232,182,74,.26); --st-b-line:rgba(232,182,74,.38);
  --st-c-text:#d9c4f5; --st-c-wash:rgba(169,139,230,.15); --st-c-weak:rgba(169,139,230,.10); --st-c-wash2:rgba(169,139,230,.28); --st-c-line:rgba(169,139,230,.40); }

/* ---- モック操作用の帯（本実装には入れない） */
.mock-bar { width: min(1180px, 100%); margin: 0 auto 12px; padding: 10px 14px; display: flex; flex-wrap: wrap; align-items: center; gap: 8px; border-radius: 22px;
  border: 1px dashed var(--rg-control-border); background: var(--lg-glass-b); color: var(--rg-muted); font-size: 13px; }
.mock-bar b { color: var(--rg-text); margin-right: 4px; }
.mock-bar .rg-chip { min-height: 36px; padding: 4px 12px; font-size: 13px; }

/* ---- 上部のタブ「道具｜武器・盾」 */
.app-tabs { width: min(1180px, 100%); margin: 0 auto 12px; display: grid; justify-items: center; gap: 6px; }
.seg { display: inline-flex; padding: 4px; gap: 4px; border-radius: 999px; max-width: 100%;
  background: linear-gradient(165deg, var(--lg-glass-a), var(--lg-glass-b)); border: 1px solid var(--lg-edge);
  -webkit-backdrop-filter: blur(18px) saturate(1.7); backdrop-filter: blur(18px) saturate(1.7);
  box-shadow: inset 0 1px 0 var(--lg-spec), inset 0 -1px 0 var(--lg-edge-soft), 0 10px 28px var(--lg-shadow); }
.seg button { appearance: none; display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 44px; padding: 4px 20px; border: 0; border-radius: 999px; background: transparent;
  color: var(--rg-muted); font: inherit; font-size: 15px; font-weight: 700; cursor: pointer; white-space: nowrap; transition: background-color var(--rg-fast) ease, color var(--rg-fast) ease; }
.seg button[aria-pressed="true"], .seg button[aria-selected="true"] { background: linear-gradient(165deg, var(--lg-pressed-a), var(--lg-pressed-b)); color: var(--rg-chip-on-text);
  box-shadow: inset 0 1px 0 var(--lg-spec), 0 3px 10px rgba(42, 108, 184, .28); }
.seg button:focus-visible { outline: 2px solid var(--rg-accent); outline-offset: 1px; }
.seg svg { width: 22px; height: 22px; flex: none; }
.seg-lg button { min-height: 50px; padding-inline: 30px; font-size: 17px; }

/* ---- ナビ（武器・盾）：いま調べている条件を要約して出す */
.ws-inputs { justify-self: center; width: 100%; max-width: 720px; display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 12px; }
.pick-meta { font-size: 13.5px; color: var(--rg-muted); font-variant-numeric: tabular-nums; }

/* ---- 条件の面 */
.ws-panel { z-index: 5; display: grid; gap: 20px; }
.ws-top { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; }
.ws-hint { flex: 1 1 280px; min-width: 0; line-height: 1.7; }
.ws-field { display: grid; gap: 8px; min-width: 0; }
.ws-label { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 10px; font-size: 14px; font-weight: 700; color: var(--rg-accent-text); letter-spacing: .04em; }
.ws-label small { font-size: 12.5px; font-weight: 400; color: var(--rg-muted); letter-spacing: 0; }
.name-box { position: relative; }
.rg-theme .ws-input { height: 56px; min-height: 56px; line-height: 1.3; border-radius: 999px; padding: 8px 22px 8px 26px; font-size: 20px; font-weight: 700; background: var(--lg-input); border: 1px solid var(--lg-edge);
  box-shadow: inset 0 2px 8px rgba(10, 24, 60, .10), inset 0 1px 0 var(--lg-spec), 0 4px 14px rgba(8, 14, 38, .16); }
.rg-theme .ws-input.num { font-size: 28px; font-variant-numeric: tabular-nums; letter-spacing: .02em; padding-right: 54px; }
.rg-theme .ws-input.num::placeholder, .rg-theme .ws-input::placeholder { font-size: 16px; font-weight: 400; letter-spacing: 0; }
.rg-theme .ws-input:focus-visible { outline: 0; border-color: var(--rg-accent); box-shadow: 0 0 0 4px rgba(76, 147, 224, .32), inset 0 2px 8px rgba(10, 24, 60, .10), 0 6px 22px rgba(42, 108, 184, .35); }
.price-box { position: relative; }
.price-box .price-clear { right: 6px; }
.picked { display: flex; align-items: center; gap: 12px; height: 56px; min-height: 56px; padding: 6px 8px 6px 10px; border-radius: 999px; background: var(--lg-input); border: 1px solid var(--lg-edge);
  box-shadow: inset 0 1px 0 var(--lg-spec), 0 4px 14px rgba(8, 14, 38, .12); }
.picked .cat-ico { width: 38px; height: 38px; padding: 7px; border-radius: 14px; }
.picked-name { min-width: 0; flex: 1; font-size: 19px; line-height: 1.35; font-weight: 700; overflow-wrap: anywhere; }
.name-box .sugg { right: auto; width: max(100%, 380px); max-width: calc(100vw - 32px); }
.picked .rg-button { min-height: 40px; padding: 4px 14px; }
.sugg-head { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; padding: 4px 6px 8px; }
.sugg-head .rg-chip { min-height: 36px; padding: 2px 12px; font-size: 13px; }
.sug .cat-ico { flex: none; }
.sug .sug-main { display: grid; line-height: 1.4; }
.sug .sug-main small { font-size: 12.5px; font-weight: 400; color: var(--rg-muted); }

/* 神器の印 */
.seal-box { display: grid; gap: 10px; }
.seal-chips { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.seal-chips .rg-chip { min-height: 40px; padding: 4px 8px 4px 14px; }
.seal-chips .rg-chip svg { width: 16px; height: 16px; opacity: .8; }
.seal-chips .price { font-size: 12.5px; font-weight: 400; opacity: .85; font-variant-numeric: tabular-nums; }
.seal-chips .rg-chip.own { padding-right: 14px; cursor: default; }
.seal-add { min-height: 40px; padding: 4px 16px; }
.seal-panel { display: grid; gap: 10px; padding: 14px; border-radius: 24px; background: var(--rg-solid-surface); border: 1px solid var(--lg-edge); box-shadow: inset 0 1px 0 var(--lg-spec); }
.seal-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 6px; max-height: 300px; overflow: auto; padding: 2px; }
.seal-opt { appearance: none; display: flex; align-items: center; gap: 10px; min-height: 48px; padding: 6px 12px; border: 1px solid transparent; border-radius: 16px; background: transparent; color: var(--rg-text);
  font: inherit; font-size: 14.5px; font-weight: 700; text-align: left; cursor: pointer; }
.seal-opt:hover { background: var(--lg-input); }
.seal-opt:focus-visible { outline: 2px solid var(--rg-accent); outline-offset: 1px; }
.seal-opt[aria-pressed="true"] { background: var(--rg-chip-on-bg); border-color: var(--rg-chip-on-border); color: var(--rg-chip-on-text); }
.seal-opt:disabled { opacity: .45; cursor: default; }
.seal-opt .ab { flex: none; min-width: 34px; height: 28px; padding: 0 4px; display: grid; place-items: center; border-radius: 9px; background: var(--rg-chip-on-bg); color: var(--rg-chip-on-text); font-size: 12px; }
.seal-opt[aria-pressed="true"] .ab { background: var(--rg-solid-surface); color: var(--rg-accent-text); }
.seal-opt .nm2 { min-width: 0; display: grid; line-height: 1.35; }
.seal-opt small { font-size: 12px; font-weight: 400; color: var(--rg-muted); }
.seal-opt[aria-pressed="true"] small { color: inherit; opacity: .85; }
.tag-nat { color: var(--st-b-text); border-color: var(--st-b-line); background: var(--st-b-wash); font-weight: 700; }
.tag-jingi { color: var(--st-b-text); border-color: var(--st-b-line); background: var(--st-b-wash); }
.tag-jingi svg { width: 14px; height: 14px; margin-right: 4px; }

/* 結果の行：右に大きく強化値 */
.ws-res .plus { min-width: 84px; padding: 4px 16px; border-radius: 20px; text-align: center; font-size: 30px; line-height: 1.4; font-weight: 700; font-variant-numeric: tabular-nums;
  background: var(--rg-chip-on-bg); color: var(--rg-chip-on-text); }
.rg-list-row.st-c.ws-res .plus { background: var(--st-c-wash2); color: var(--st-c-text); box-shadow: 0 0 0 1.5px var(--st-c-line); }
.ws-res .ans { font-size: 1.15em; font-variant-numeric: tabular-nums; }
.rg-list-row.st-c .ans { color: var(--st-c-text); }
.res-ws { grid-column: 1 / -1; }
.ws-res .calc { color: var(--rg-muted); font-size: 13.5px; font-variant-numeric: tabular-nums; }
.near { margin-top: 10px; padding: 10px 14px; border-radius: 16px; background: var(--lg-input); font-size: 14px; color: var(--rg-muted); font-variant-numeric: tabular-nums; }
.near b { color: var(--rg-text); }
.near { display: grid; gap: 4px; }
.near p { font-size: 13px; }
.near-row { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 8px; }
.st-tag { flex: none; min-width: 3.2em; padding: 0 10px; border-radius: 999px; text-align: center; font-size: 12.5px; font-weight: 700; line-height: 1.7; background: var(--rg-chip-on-bg); color: var(--rg-chip-on-text); }
.st-tag.c { background: var(--st-c-wash2); color: var(--st-c-text); }
.hero-ws { grid-column: 1 / -1; display: grid; gap: 14px; }
.steps { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 4px; }
.steps li { padding: 14px 16px; border-radius: 20px; background: var(--lg-input); line-height: 1.7; }
.steps b { display: block; color: var(--rg-accent-text); }

/* 道具タブ（現行画面の置き場） */
.tool-ph { display: grid; gap: 12px; border-style: dashed; }
.tool-ph .rg-chips .rg-chip { cursor: default; }

/* モックの補足（本実装には入れない） */
.mock-note { width: min(1180px, 100%); margin: 0 auto; padding: 22px 26px; border-radius: 26px; border: 1px dashed var(--rg-control-border); background: var(--lg-glass-b); display: grid; gap: 8px; }
.mock-note ul { display: grid; gap: 6px; padding-left: 1.2em; list-style: disc; }
.mock-note li { line-height: 1.7; font-size: 14.5px; }

@media (max-width: 900px) { .steps { grid-template-columns: minmax(0, 1fr); } }
@media (max-width: 700px) {
  .ws-inputs { grid-column: 1 / -1; grid-row: 2; max-width: none; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 8px; }
  .rg-theme .ws-input { padding-inline: 14px; font-size: 16px; }
  .rg-theme .ws-input.num { font-size: 22px; padding-right: 44px; }
  .picked { gap: 8px; padding-left: 14px; }
  .picked .cat-ico { display: none; }
  .picked-name { font-size: 16px; }
  .picked .rg-button { min-height: 36px; padding: 2px 10px; font-size: 13px; }
  .price-box .price-clear { width: 40px; height: 40px; }
  .app-tabs .seg { width: 100%; }
  .app-tabs .seg button { flex: 1; padding-inline: 10px; }
  .ws-res .plus { min-width: 68px; font-size: 24px; padding-inline: 10px; }
}
'''.replace('__MEADOW__', png('meadow.png')).replace('__NIGHT__', png('night.png'))

BODY = '''
<div class="rg-theme" id="app">
  <div class="lg-scene" aria-hidden="true"></div>

  <div class="mock-bar" aria-label="モック操作用">
    <b>モック操作用</b>
    <button class="rg-chip" type="button" data-ex="n">通常（カタナ 1,300）</button>
    <button class="rg-chip" type="button" data-ex="c">呪い（カタナ 1,044）</button>
    <button class="rg-chip" type="button" data-ex="s">盾（鉄甲の盾 1,500）</button>
    <button class="rg-chip" type="button" data-ex="j">神器（カタナ＋印2つ 4,800）</button>
    <button class="rg-chip" type="button" data-ex="jc">神器の呪い（カタナ＋印2つ 3,654）</button>
    <button class="rg-chip" type="button" data-ex="m">マイナス呪い（カタナ 783）</button>
    <button class="rg-chip" type="button" data-ex="x">該当なし（カタナ 1,250）</button>
  </div>

  <div class="app-tabs">
    <div class="seg seg-lg" role="tablist" aria-label="調べるもの">
      <button type="button" role="tab" id="tab-tool" data-tab="tool" aria-selected="false">__SCROLL__道具</button>
      <button type="button" role="tab" id="tab-ws" data-tab="ws" aria-selected="true">__SWORD__武器・盾</button>
    </div>
  </div>

  <!-- 道具タブのナビ（現行どおり） -->
  <header class="rg-nav" id="nav-tool" hidden>
    <div class="dock-brand"><h1 class="rg-brand">シレン6 値段識別</h1><span class="rg-muted">判断済み 4 / 138</span></div>
    <div class="price-wrap">
      <label class="rg-visually-hidden" for="tool-price">ゲーム内で見えた売値または買値（ギタン）</label>
      <input class="rg-input price-input" id="tool-price" type="text" inputmode="numeric" autocomplete="off" maxlength="9" placeholder="値段を入力">
      <div class="mode-seg" role="group" aria-label="入力の種類"><button type="button" aria-pressed="true">価格</button><button type="button" aria-pressed="false">名前</button></div>
    </div>
    <button class="rg-button" type="button" disabled>リセット</button>
  </header>

  <!-- 武器・盾タブのナビ -->
  <header class="rg-nav" id="nav-ws">
    <div class="dock-brand"><h1 class="rg-brand">シレン6 値段識別</h1><span class="rg-muted">武器・盾の強化値</span></div>
    <div class="ws-inputs">
      <div class="name-box" id="name-box">
        <label class="rg-visually-hidden" for="ws-name">武器・盾の名前</label>
        <input class="rg-input ws-input" id="ws-name" type="text" autocomplete="off" spellcheck="false" placeholder="名前を入力（かたな、katana）" aria-controls="ws-sugg">
        <div class="picked" id="picked" hidden></div>
        <div class="sugg" id="ws-sugg" hidden></div>
      </div>
      <div class="price-box">
        <input class="rg-input ws-input num" id="ws-price" type="text" inputmode="numeric" autocomplete="off" maxlength="9" placeholder="買値を入力" aria-label="ゲーム内で見えた買値（ギタン）">
        <button class="price-clear" id="ws-clear" type="button" aria-label="入力した値段を消す" hidden><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M5 5l10 10M15 5L5 15"/></svg></button>
      </div>
    </div>
    <button class="rg-button" type="button" id="ws-reset">入力を消す</button>
  </header>

  <main class="rg-page rg-stack" id="view-tool" hidden>
    <section class="rg-surface tool-ph" aria-label="道具タブ">
      <h2 class="rg-heading">道具タブ（いまの画面がそのまま入ります）</h2>
      <p class="rg-muted">ここには、今までどおりの候補一覧・種別の絞り込み・判断済みの一覧が出ます。武器・盾タブに移っても、入力した値段と判断済みは消えません。</p>
      <div class="rg-chips"><span class="rg-chip" style="pointer-events:none">入力中の値段 <b id="tool-keep">—</b></span><span class="rg-chip" style="pointer-events:none">判断済み 4件</span></div>
    </section>
  </main>

  <main class="rg-page rg-stack" id="view-ws">
    <section class="rg-surface ws-panel" aria-label="調べる武器・盾の条件">
      <div class="ws-top">
        <div class="seg" role="group" aria-label="通常か神器か">
          <button type="button" data-g="n" aria-pressed="true">通常</button><button type="button" data-g="j" aria-pressed="false">__STAR__神器</button>
        </div>
      </div>
      <p class="pick-meta" id="pick-meta" hidden></p>
      <div class="seal-box" id="seal-box" hidden>
        <div class="ws-label"><span>付いている印</span><small id="seal-sum"></small></div>
        <div class="seal-chips" id="seal-chips"></div>
        <div class="seal-panel" id="seal-panel" hidden>
          <input class="rg-input" id="seal-q" type="text" autocomplete="off" spellcheck="false" placeholder="印の名前で絞り込み（例：会心、kaishin）" aria-label="印の名前で絞り込み">
          <div class="seal-list" id="seal-list"></div>
        </div>
      </div>
    </section>

    <div class="results-grid" id="ws-results"></div>

    <section class="rg-surface" aria-label="価格の見方">
      <div class="rg-document-row">
        <h2 class="rg-heading">計算のしくみ</h2>
        <div class="rg-copy">
          <p>通常の武器・盾は、買値が「基礎の買値＋100×強化値」です。最初から付いている印は、基礎の値段に含まれています。</p>
          <p>神器は、基礎の値段が2倍になり、追加で付いた印の値段が足されます。強化値の加算は2倍になりません。青神器・金神器の違いでも値段は変わりません。</p>
          <p>呪われていると、買値は合計が87%（小数点以下切り捨て）になります。祝福は、武器・盾にはありません。</p>
        </div>
      </div>
      <div class="rg-document-row">
        <h2 class="rg-heading">対象と制限</h2>
        <div class="rg-copy">
          <p>強化値は −9〜+99 を対象にしています。印を銀封印しても、印数を増やしても、値段は変わりません。</p>
          <p>値段が複数の候補に当たるときは、すべて並べます。売値は対象にしていません。</p>
        </div>
      </div>
    </section>

    <section class="mock-note" aria-label="モックの補足">
      <h2 class="rg-heading">モックの補足（本実装には出しません）</h2>
      <ul>
        <li>武器・盾の名前と基礎値段、印の値段は、シレン6 Wikiの「武器」「盾」「印」のページの値を使っています。印の値段はWikiの検証値（コミュニティ報告）で、確定情報ではありません。</li>
        <li>神器で、その武器に最初から付いている印が「基礎の値段×2」に含まれるかは、Wikiに明記がありません。このモックでは含まれる前提で、追加で付いた印だけを足しています。</li>
        <li>名前と印の検索は、既存の「かな・ローマ字でも探せる」仕組みと同じコードです。読みは辞書の下書きに手直しを加えたもので、印の読みは下書きのままです。</li>
        <li>売値からの判定は付けていません（お店で並んでいる買値だけを使います）。</li>
        <li>武器・盾には「判断完了」のような記録機能はつけていません。1つずつ強化値を調べて終わる使い方を想定しています。</li>
      </ul>
    </section>

    <footer class="site-foot rg-muted"><p>風来のシレン6の非公式ファンツールです。ゲーム内の名称・データの権利は、それぞれの権利者に帰属します。</p></footer>
  </main>
</div>

<script>
(function () {
  var D = __DATA__, R = __READ__;
  __SEARCH__
  var HAY = {}, HAYL = {};
  function hay(n) { if (!HAY[n]) { HAY[n] = kn(n) + '|' + kn(R[n] || ''); HAYL[n] = lite(HAY[n]); } }
  function nameHit(n, query) {
    var qn = kn(query); if (!qn) return true; hay(n);
    if (HAY[n].indexOf(qn) >= 0) return true;
    var ka = /[a-z]/.test(qn) ? kn(romaji2kana(qn)) : '';
    if (ka && HAY[n].indexOf(ka) >= 0) return true;
    return HAYL[n].indexOf(lite(qn)) >= 0 || !!(ka && HAYL[n].indexOf(lite(ka)) >= 0);
  }
  var $ = function (id) { return document.getElementById(id); };
  var fmt = function (n) { return Number(n).toLocaleString('ja-JP'); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var P = { w: '__SWORD_P__', s: '__SHIELD_P__', star: '__STAR_P__', x: '<path d="M6 6l12 12M18 6L6 18"/>' };
  function ico(inner, cls) { return '<svg class="' + (cls || 'cat-ico') + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + inner + '</svg>'; }
  var SKULL = '__SKULL__';
  var NMIN = -9, NMAX = 99, CURSE = 0.87;

  var S = { tab: 'ws', g: 'n', kind: '', pick: null, q: '', price: '', seals: [], sealOpen: false, sealQ: '', toolPrice: '400' };

  function item() { return S.pick ? (S.pick.k === 'w' ? D.weapons : D.shields)[S.pick.i] : null; }
  function sealsFor(k) { return D.seals.filter(function (s) { return s.k === k; }); }
  function sealBy(k, no) { return D.seals.filter(function (s) { return s.k === k && s.no === no; })[0]; }

  /* ---------- 計算 ---------- */
  function fixedPrice(it) {
    var sum = 0;
    S.seals.forEach(function (no) { var x = sealBy(S.pick.k, no); if (x) sum += x.buy; });
    return it.buy * (S.g === 'j' ? 2 : 1) + sum;
  }
  function priceOf(it, n, st) {
    var v = fixedPrice(it) + 100 * n;
    return st === 'c' ? Math.floor(v * CURSE) : v;
  }
  function solve(it, p) {
    var out = [];
    ['n', 'c'].forEach(function (st) {
      for (var n = NMIN; n <= NMAX; n++) if (priceOf(it, n, st) === p) { out.push({ st: st, n: n }); break; }
    });
    return out;
  }
  function near(it, p, st) {
    var lo = null, res = [];
    for (var n = NMIN; n <= NMAX; n++) if (priceOf(it, n, st) <= p) lo = n;
    [lo, lo === null ? NMIN : lo + 1].forEach(function (n) { if (n !== null && n >= NMIN && n <= NMAX) res.push({ n: n, v: priceOf(it, n, st) }); });
    return res;
  }
  var sgn = function (n) { return n >= 0 ? '+' + n : '−' + Math.abs(n); };

  /* ---------- 描画 ---------- */
  function renderTabs() {
    var ws = S.tab === 'ws';
    $('tab-ws').setAttribute('aria-selected', ws); $('tab-tool').setAttribute('aria-selected', !ws);
    $('view-ws').hidden = !ws; $('nav-ws').hidden = !ws; $('view-tool').hidden = ws; $('nav-tool').hidden = ws;
    $('tool-keep').textContent = S.toolPrice ? fmt(S.toolPrice) + ' ギタン' : '（なし）';
  }
  function renderPick() {
    var it = item(), box = $('picked');
    $('ws-name').hidden = !!it; box.hidden = !it;
   
    $('seal-box').hidden = !(S.g === 'j');
    if (it) {
      box.innerHTML = ico(S.pick.k === 'w' ? P.w : P.s) + '<span class="picked-name">' + esc(it.n) + '</span><button class="rg-button" type="button" id="re-pick" aria-label="名前を選び直す">変更</button>';
    }
    var pm = $('pick-meta'); pm.hidden = !it;
    if (it) { var kn2 = S.pick.k === 'w' ? '武器' : '盾'; pm.textContent = kn2 + '・基礎値 ' + it.base + '・印数 ' + it.slots + '・' + (S.g === 'j' ? '神器の買値 ' + fmt(it.buy * 2) + '（基本印のみ）' : kn2 + 'の買値 ' + fmt(it.buy)); }
  }
  function renderSugg() {
    var box = $('ws-sugg');
    if (S.pick || document.activeElement !== $('ws-name') && !S.q) { box.hidden = true; return; }
    var all = [], qq = S.q.trim();
    D.weapons.forEach(function (x, i) { all.push({ k: 'w', i: i, x: x }); }); D.shields.forEach(function (x, i) { all.push({ k: 's', i: i, x: x }); });
    var list = all.filter(function (e) { return (!S.kind || e.k === S.kind) && (!qq || nameHit(e.x.n, qq)); });
    var head = '<div class="sugg-head">' + [['', 'すべて'], ['w', '武器'], ['s', '盾']].map(function (c) { return '<button class="rg-chip" type="button" data-kind="' + c[0] + '" aria-pressed="' + (S.kind === c[0]) + '">' + c[1] + '</button>'; }).join('') + '</div>';
    var rows = list.slice(0, 7).map(function (e) {
      return '<button class="sug" type="button" data-pk="' + e.k + ':' + e.i + '">' + ico(e.k === 'w' ? P.w : P.s) + '<span class="sug-main"><span>' + esc(e.x.n) + '</span><small>基礎値 ' + e.x.base + '・印数 ' + e.x.slots + '</small></span><em>' + (S.g === 'j' ? '神器 ' + fmt(e.x.buy * 2) : fmt(e.x.buy)) + '</em></button>';
    }).join('');
    var note = list.length > 7 ? '<p class="sug-note">ほか ' + (list.length - 7) + '件。名前を入力して絞り込めます。</p>' : (list.length ? '' : '<p class="sug-note">該当する武器・盾がありません。</p>');
    box.innerHTML = head + rows + note; box.hidden = false;
  }
  function renderSeals() {
    if (S.g !== 'j') return;
    var it = item(), chips = $('seal-chips');
    var tb = 0;
    var own = it && it.seal ? sealsFor(S.pick.k).filter(function (x) { return x.n === it.seal; })[0] : null;
    var h = own ? '<span class="rg-chip own" aria-pressed="true">' + esc(own.n) + '<span class="price">基本の印</span></span>' : '';
    h += S.seals.map(function (no) {
      var s = sealBy(S.pick.k, no); tb += s.buy;
      return '<button class="rg-chip" type="button" data-rm="' + no + '" aria-label="印「' + esc(s.n) + '」を外す" aria-pressed="true">' + esc(s.n) + '<span class="price">+' + fmt(s.buy) + '</span>' + ico(P.x, 'i') + '</button>';
    }).join('');
    h += '<button class="rg-button seal-add" type="button" id="seal-toggle" ' + (it ? '' : 'disabled') + '>' + (S.sealOpen ? '閉じる' : '＋ 印を追加') + '</button>';
    chips.innerHTML = h;
    $('seal-sum').textContent = it ? (S.seals.length ? '強化値 0・呪いなしの買値：' + fmt(it.buy * 2 + tb) : '') : '先に名前を選んでください';
    $('seal-panel').hidden = !(S.sealOpen && it);
    if (S.sealOpen && it) {
      var q = S.sealQ.trim();
      $('seal-list').innerHTML = sealsFor(S.pick.k).filter(function (s) { return !q || nameHit(s.n, q) || kn(s.ab).indexOf(kn(q)) >= 0; }).map(function (s) {
        var own = it.seal && it.seal === s.n, on = S.seals.indexOf(s.no) >= 0;
        return '<button class="seal-opt" type="button" data-sno="' + s.no + '" aria-pressed="' + on + '"' + (own ? ' disabled' : '') + '><span class="ab">' + esc(s.ab) + '</span><span class="nm2"><span>' + esc(s.n) + (s.nat ? ' <span class="tag tag-nat">天然</span>' : '') + '</span><small>' + (own ? '基本の印として付いています' : '+' + fmt(s.buy) + ' ギタン') + '</small></span></button>';
      }).join('') || '<p class="rg-muted" style="padding:8px">該当する印がありません。</p>';
    }
  }
  function variantRow(it, v) {
    var cur = v.st === 'c', fx = fixedPrice(it), val = priceOf(it, v.n, v.st);
    var calc = fmt(fx) + (v.n < 0 ? ' − ' : ' + ') + 100 + ' × ' + Math.abs(v.n);
    calc = cur ? '(' + calc + ') × 0.87 ＝ ' + fmt(val) + '（小数点以下切り捨て）' : calc + ' ＝ ' + fmt(val);
    var jt = S.g === 'j' ? '<span class="tag tag-jingi">' + ico(P.star, 'i') + '神器</span>' : '';
    var word = '<b class="ans">' + sgn(v.n) + (cur ? '（呪い）' : '') + '</b>';
    return '<li class="rg-list-row ws-res ' + (cur ? 'st-c' : 'st-n') + '"><div><p class="rg-list-title"><span class="nm">' + ico(S.pick.k === 'w' ? P.w : P.s) + '<span>この値段の' + esc(it.n) + 'は ' + word + (cur ? '' : ' ') + 'です</span></span>' + jt + '</p>' +
      '<div class="rg-list-copy"><span class="var calc">' + calc + '</span></div></div>' +
      '<span class="plus" aria-hidden="true">' + sgn(v.n) + '</span></li>';
  }
  function renderResults() {
    var box = $('ws-results'), it = item(), p = S.price ? parseInt(S.price, 10) : null;
    $('ws-clear').hidden = !S.price;
    if (!it || p == null || isNaN(p)) {
      box.innerHTML = '<section class="rg-surface hero-ws"><h2 class="rg-heading">名前と値段から、強化値と呪いを調べます</h2>' +
        '<p class="rg-copy">ゲームで見えた武器・盾の名前を選び、買値を入力してください。' + (it ? '' : '先に名前を選ぶと、値段の入力欄で計算が始まります。') + '</p>' +
        '<ul class="steps"><li><b>1. 通常か神器かを選ぶ</b>神器のときは、付いている印も選びます。</li><li><b>2. 名前を選ぶ</b>かな・ローマ字でも探せます。</li><li><b>3. 買値を入れる</b>当てはまる強化値と、呪いの有無を出します。</li></ul></section>';
      return;
    }
    var vs = solve(it, p), body;
    if (vs.length) body = '<ul>' + vs.map(function (v) { return variantRow(it, v); }).join('') + '</ul>';
    else {
      var line = function (st) {
        var xs = near(it, p, st).filter(function (x) { return Math.abs(x.v - p) <= 150; });
        return xs.length ? '<span class="near-row"><span class="st-tag' + (st === 'c' ? ' c' : '') + '">' + (st === 'c' ? '呪い' : '通常') + '</span>' + xs.map(function (x) { return '<b>' + sgn(x.n) + '</b> のとき ' + fmt(x.v); }).join(' ／ ') + '</span>' : '';
      };
      body = '<p class="empty-box">買値が <strong>' + fmt(p) + '</strong> になる強化値はありません。</p>' +
        (near(it, p, 'n').concat(near(it, p, 'c')).some(function (x) { return Math.abs(x.v - p) <= 150; }) ?
          '<div class="near"><p>近い値（読み間違いや、印の選び漏れがないか確かめてください）</p>' + line('n') + line('c') + '</div>' :
          '<p class="near">この値段は、強化値 ' + sgn(NMIN) + '〜' + sgn(NMAX) + ' の範囲に近い値がありません。名前や印の選び間違いがないか確かめてください。</p>');
    }
    box.innerHTML = '<section class="rg-surface res-sec res-ws" aria-label="判定">' +
      '<h2 class="rg-heading res-head">' + esc(it.n) + (S.g === 'j' ? '（神器）' : '') + ' ・ 買値 <span class="res-num">' + fmt(p) + '</span><span class="res-count">' + vs.length + '件</span></h2>' + body + '</section>';
  }
  function renderAll() { renderTabs(); renderPick(); renderSugg(); renderSeals(); renderResults();
    document.querySelectorAll('.ws-top [data-g]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-g') === S.g)); }); }

  /* ---------- 操作 ---------- */
  function setPick(k, i) { S.pick = { k: k, i: i }; S.seals = []; S.q = ''; $('ws-name').value = ''; S.sealOpen = false; renderAll(); setTimeout(function () { $('ws-price').focus(); }, 0); }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('button'); if (!t) { if (!e.target.closest('#name-box')) { $('ws-sugg').hidden = true; } return; }
    if (t.dataset.tab) { S.tab = t.dataset.tab; renderTabs(); return; }
    if (t.dataset.g) { S.g = t.dataset.g; S.seals = []; S.sealOpen = false; renderAll(); return; }
    if (t.dataset.pk) { var a = t.dataset.pk.split(':'); setPick(a[0], +a[1]); return; }
    if (t.dataset.kind !== undefined && t.closest('#ws-sugg')) { S.kind = t.dataset.kind; renderSugg(); return; }
    if (t.id === 're-pick') { S.pick = null; S.seals = []; renderAll(); $('ws-name').focus(); return; }
    if (t.id === 'seal-toggle') { S.sealOpen = !S.sealOpen; renderSeals(); return; }
    if (t.dataset.rm) { S.seals = S.seals.filter(function (n) { return n !== +t.dataset.rm; }); renderAll(); return; }
    if (t.dataset.sno) { var no = +t.dataset.sno, ix = S.seals.indexOf(no); if (ix >= 0) S.seals.splice(ix, 1); else S.seals.push(no); renderSeals(); renderResults(); return; }
    if (t.id === 'ws-clear') { S.price = ''; $('ws-price').value = ''; renderAll(); $('ws-price').focus(); return; }
    if (t.id === 'ws-reset') { S.pick = null; S.seals = []; S.price = ''; S.q = ''; $('ws-price').value = ''; $('ws-name').value = ''; renderAll(); return; }
    if (t.dataset.ex) { example(t.dataset.ex); return; }
  });
  $('ws-name').addEventListener('input', function () { S.q = this.value; renderSugg(); });
  $('ws-name').addEventListener('focus', renderSugg);
  $('ws-price').addEventListener('input', function () { this.value = this.value.replace(/[^0-9]/g, ''); S.price = this.value; renderResults(); $('ws-clear').hidden = !S.price; });
  $('seal-q').addEventListener('input', function () { S.sealQ = this.value; renderSeals(); });
  $('tool-price').addEventListener('input', function () { this.value = this.value.replace(/[^0-9]/g, ''); S.toolPrice = this.value; });
  $('tool-price').value = S.toolPrice;
  function find(list, n) { for (var i = 0; i < list.length; i++) if (list[i].n === n) return i; return -1; }
  function example(id) {
    S.tab = 'ws'; S.sealOpen = false; S.seals = []; S.g = 'n'; var k = 'w', name = 'カタナ', price = '1300';
    if (id === 'c') price = '1044';
    if (id === 's') { k = 's'; name = '鉄甲の盾'; price = '1500'; }
    if (id === 'x') price = '1250';
    if (id === 'm') price = '783';
    if (id === 'j') { S.g = 'j'; price = '4800'; }
    if (id === 'jc') { S.g = 'j'; price = '3654'; }
    S.pick = { k: k, i: find(k === 'w' ? D.weapons : D.shields, name) };
    if (id === 'j' || id === 'jc') { S.seals = [5, 18]; S.sealOpen = false; }
    S.price = price; $('ws-price').value = price; S.q = ''; $('ws-name').value = ''; renderAll();
  }
  example('n');
})();
</script>
'''

body = (BODY.replace('__SWORD_P__', SWORD).replace('__SHIELD_P__', SHIELD).replace('__STAR_P__', STAR).replace('__SKULL__', SKULL)
        .replace('__SCROLL__', svg(SCROLL, 'tab-ico')).replace('__SWORD__', svg(SWORD, 'tab-ico')).replace('__STAR__', svg(STAR, 'tab-ico'))
        .replace('__DATA__', DATA).replace('__READ__', READ).replace('__SEARCH__', SEARCH_JS))

n = write_page('武器・盾モード モック', CSS, body, os.path.join(HERE, '..', 'mocks', 'weapon-shield.html'))
print('weapon-shield.html', n)
