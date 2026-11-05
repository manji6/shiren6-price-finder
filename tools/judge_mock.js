(function () {
  var A = window.ShirenApp; if (!A) return;
  var root = document.documentElement;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var CHECK = '<svg class="jm-check" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 10.5l3.5 3.5 7.5-8"/></svg>';
  // ---- 検索: 漢字の名前でも、読み（ひらがな）やローマ字でヒットさせる ----
  var R = window.JM_READINGS || {};
  // 全角半角をそろえ、カタカナをひらがなにし、長音（ー）と空白は無視する
  var kn = function (s) { return s.normalize('NFKC').toLowerCase().replace(/[ァ-ヶ]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0x60); }).replace(/[ー\s]/g, ''); };
  var RM = {};
  (function () {
    var rows = { '': 'あいうえお', k: 'かきくけこ', s: 'さしすせそ', t: 'たちつてと', n: 'なにぬねの', h: 'はひふへほ', m: 'まみむめも', r: 'らりるれろ', g: 'がぎぐげご', z: 'ざじずぜぞ', d: 'だぢづでど', b: 'ばびぶべぼ', p: 'ぱぴぷぺぽ' };
    Object.keys(rows).forEach(function (c) { for (var i = 0; i < 5; i++) RM[c + 'aiueo'[i]] = rows[c][i]; });
    RM.ya = 'や'; RM.yu = 'ゆ'; RM.yo = 'よ'; RM.wa = 'わ'; RM.wo = 'を';
    var small = { a: 'ゃ', u: 'ゅ', o: 'ょ' };
    ['k', 'g', 's', 'z', 't', 'd', 'n', 'h', 'b', 'p', 'm', 'r'].forEach(function (c) { ['a', 'u', 'o'].forEach(function (v) { RM[c + 'y' + v] = rows[c][1] + small[v]; }); });
    var alt = { si: 'し', shi: 'し', ti: 'ち', chi: 'ち', tu: 'つ', tsu: 'つ', hu: 'ふ', fu: 'ふ', zi: 'じ', ji: 'じ', sha: 'しゃ', shu: 'しゅ', sho: 'しょ', she: 'しぇ', cha: 'ちゃ', chu: 'ちゅ', cho: 'ちょ', che: 'ちぇ', ja: 'じゃ', ju: 'じゅ', jo: 'じょ', jya: 'じゃ', jyu: 'じゅ', jyo: 'じょ', fa: 'ふぁ', fi: 'ふぃ', fe: 'ふぇ', fo: 'ふぉ', xtu: 'っ', ltu: 'っ', xtsu: 'っ', ltsu: 'っ' };
    Object.keys(alt).forEach(function (k) { RM[k] = alt[k]; });
  })();
  // ローマ字 → ひらがな。変換の途中（最後の子音だけ打った状態など）でも、読める所までを返す
  function romaji2kana(s) {
    var out = '', i = 0;
    while (i < s.length) {
      var c = s[i], nx = s[i + 1];
      if (nx !== undefined && c === nx && /[bcdfghjklmpqrstvwxyz]/.test(c)) { out += 'っ'; i++; continue; }
      if (c === 'n') {
        if (nx === undefined || nx === "'") { out += 'ん'; i += (nx === undefined ? 1 : 2); continue; }
        if (nx === 'n') { var n2 = s[i + 2]; if (n2 === undefined || !/[aiueoy]/.test(n2)) { out += 'ん'; i += 2; } else { out += 'ん'; i++; } continue; }
        if (!/[aiueoy]/.test(nx)) { out += 'ん'; i++; continue; }
      }
      var tok = null;
      for (var len = 4; len >= 1; len--) { var seg = s.substr(i, len); if (RM[seg]) { tok = RM[seg]; i += len; break; } }
      if (tok !== null) { out += tok; continue; }
      if (c === '-') { out += 'ー'; i++; continue; }
      i++; // 変換の途中の子音などは読み飛ばす
    }
    return out;
  }
  // 長音をゆるく見る（ふういん ≒ ふいん、ごうせい ≒ ごせい）。お段・う段のあとの「う」と、え段のあとの「い」を無視する
  var lite = function (s) { return s.replace(/([おこそとのほもよろをごぞどぼぽょうくすつぬふむゆるぐずづぶぷゅ])う/g, '$1').replace(/([えけせてねへめれげぜでべぺ])い/g, '$1'); };
  var HAY = {}, HAYL = {};
  A.items.forEach(function (it) { HAY[it.key] = kn(it.n) + '|' + kn(R[it.n] || ''); HAYL[it.key] = lite(HAY[it.key]); });
  function hit(it, q) {
    if (!q) return true;
    var n = kn(q); if (!n) return true;
    var hay = HAY[it.key];
    if (hay.indexOf(n) >= 0) return true;
    var k = /[a-z]/.test(n) ? kn(romaji2kana(n)) : '';
    if (k && hay.indexOf(k) >= 0) return true;
    var hl = HAYL[it.key];
    return hl.indexOf(lite(n)) >= 0 || (k && hl.indexOf(lite(k)) >= 0);
  }
  // 前方一致（読みや名前の先頭が入力と同じ）を先に並べる
  function rank(it, q) {
    var n = kn(q), k = /[a-z]/.test(n) ? kn(romaji2kana(n)) : '';
    return HAY[it.key].split('|').some(function (p) { return (n && p.indexOf(n) === 0) || (k && p.indexOf(k) === 0); }) ? 0 : 1;
  }
  var chip = function (it) { var on = A.isJudged(it.key); return '<button type="button" class="rg-chip jm-chip" data-jm-key="' + esc(it.key) + '" aria-pressed="' + on + '">' + A.ico(it.c) + '<span>' + esc(it.n) + '</span>' + (on ? CHECK : '') + '</button>'; };
  var counts = function (cat) { var all = A.items.filter(function (i) { return !cat || i.c === cat; }); return [all.filter(function (i) { return A.isJudged(i.key); }).length, all.length]; };

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-jm-key]'); if (!t) return;
    var k = t.getAttribute('data-jm-key'); A.set(k, !A.isJudged(k));
  });

  /* ---------- A: シート ---------- */
  var tab = '', q = '', composing = false;
  var wrap = document.createElement('div'); wrap.className = 'jm-a-only'; wrap.id = 'jm-open-wrap';
  wrap.innerHTML = '<button class="rg-button" id="jm-open" type="button">アイテム名から判断済みにする</button>';
  $('.filter-surface').appendChild(wrap);
  var dlg = document.createElement('dialog'); dlg.className = 'rg-dialog jm-sheet'; dlg.setAttribute('aria-labelledby', 'jm-st');
  dlg.innerHTML = '<div class="jm-head"><h2 class="rg-heading" id="jm-st">判断済みにするアイテム</h2><button class="rg-button" id="jm-close" type="button">閉じる</button></div>' +
    '<input class="rg-input" id="jm-q" type="search" inputmode="search" enterkeyhint="search" autocomplete="off" placeholder="名前で探す（かな・ローマ字OK 例：こんらん、tsue）" aria-label="アイテム名で絞り込む">' +
    '<div class="rg-chips jm-tabs" id="jm-tabs" role="group" aria-label="種別"></div><div class="jm-grid" id="jm-grid"></div>' +
    '<div class="jm-foot"><span class="rg-muted" id="jm-count"></span><button class="rg-button" id="jm-done" type="button">完了</button></div>';
  ($('.rg-theme') || document.body).appendChild(dlg);   // フォントなどの指定が効くよう、ページの内側に置く
  function renderSheet() {
    var tabs = [['', 'すべて']].concat(A.cats.map(function (c) { return [c, c]; }));
    $('#jm-tabs').innerHTML = tabs.map(function (t) { var n = counts(t[0]); return '<button type="button" class="rg-chip" data-jm-tab="' + esc(t[0]) + '" aria-pressed="' + (tab === t[0]) + '">' + (t[0] ? A.ico(t[0]) : '') + t[1] + '<span class="chip-count">' + n[0] + '/' + n[1] + '</span></button>'; }).join('');
    var list = A.items.filter(function (i) { return (!tab || i.c === tab) && hit(i, q); });
    if (q) list = list.map(function (i, ix) { return [rank(i, q), ix, i]; }).sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; }).map(function (x) { return x[2]; });
    $('#jm-grid').innerHTML = list.length ? list.map(chip).join('') : '<p class="jm-empty">「' + esc(q) + '」に一致するアイテムはありません。</p>';
    var n = counts(''); $('#jm-count').textContent = '判断済み ' + n[0] + ' / ' + n[1];
  }
  $('#jm-open').addEventListener('click', function () { renderSheet(); dlg.showModal(); });
  $('#jm-close').addEventListener('click', function () { dlg.close(); }); $('#jm-done').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener('click', function (e) { var t = e.target.closest('[data-jm-tab]'); if (t) { tab = t.getAttribute('data-jm-tab'); renderSheet(); } });
  var qEl = $('#jm-q');
  qEl.addEventListener('compositionstart', function () { composing = true; }); qEl.addEventListener('compositionend', function () { composing = false; q = qEl.value; renderSheet(); });
  qEl.addEventListener('input', function () { q = qEl.value; renderSheet(); });   // 変換の途中でも絞り込む

  /* ---------- B: 入力欄の切替（価格 ⇄ 名前）。切り替えの見せ方を3案 ---------- */
  var price = $('#price'), pw = $('.price-wrap'), nav = $('.rg-nav'), nameMode = false;
  // 入力欄の中にスイッチやボタンが入る案（①②）では、ヒント文を短くして、隠れないようにする
  var phNum = function () { return root.getAttribute('data-jb') === '3' ? '値段を入力（例 400）' : '値段を入力'; };
  var phName = function () { return root.getAttribute('data-jb') === '3' ? '名前を入力（かな・ローマ字OK）' : '名前を入力'; };
  function refreshPlaceholder() { price.placeholder = nameMode ? phName() : phNum(); }
  var HINT = '<p class="jm-sug-note">読み（こんらん）やローマ字（konran）でも探せます。漢字に変換しなくてOKです。</p>';
  // ① 2択スイッチ（価格｜名前）: 入力欄の右に、どちらも文字で出す
  var seg = document.createElement('div'); seg.className = 'jm-seg'; seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', '入力の種類');
  seg.innerHTML = '<button type="button" data-m="num" aria-pressed="true">価格</button><button type="button" data-m="name" aria-pressed="false">名前</button>'; pw.appendChild(seg);
  // ② ボタン: 押すとどうなるかを、文で書く
  var btn2 = document.createElement('button'); btn2.type = 'button'; btn2.className = 'rg-button jm-btn2'; pw.appendChild(btn2);
  // ③ 入力欄の下のタブ（価格で探す｜名前で探す）
  var tabs3 = document.createElement('div'); tabs3.className = 'jm-tabs3'; tabs3.setAttribute('role', 'group'); tabs3.setAttribute('aria-label', '探し方');
  tabs3.innerHTML = '<button type="button" data-m="num" aria-pressed="true">価格で探す</button><button type="button" data-m="name" aria-pressed="false">名前で探す</button>'; nav.appendChild(tabs3);
  var sugg = document.createElement('div'); sugg.className = 'jm-sugg'; sugg.id = 'jm-sugg'; sugg.hidden = true; pw.appendChild(sugg);
  function syncUI() {
    [seg, tabs3].forEach(function (el) { el.querySelectorAll('[data-m]').forEach(function (b) { b.setAttribute('aria-pressed', (b.getAttribute('data-m') === 'name') === nameMode); }); });
    btn2.innerHTML = nameMode ? '<span class="jm-ico">123</span>価格に戻る' : '<span class="jm-ico">あ</span>名前で入力';
    btn2.setAttribute('aria-label', nameMode ? '価格の入力に戻す' : '名前で入力する');
  }
  function setMode(on) {
    if (nameMode === on) return;
    price.value = ''; price.dispatchEvent(new Event('input', { bubbles: true }));  // 価格の検索を空に戻す（切り替え前の状態で）
    nameMode = on; root.classList.toggle('jm-name', on); syncUI();
    price.setAttribute('inputmode', on ? 'text' : 'numeric'); price.setAttribute('enterkeyhint', on ? 'search' : 'done');
    refreshPlaceholder(); price.removeAttribute('maxlength'); if (!on) price.setAttribute('maxlength', '9');
    price.focus(); suggest();
  }
  [seg, tabs3].forEach(function (el) { el.addEventListener('click', function (e) { var b = e.target.closest('[data-m]'); if (b) setMode(b.getAttribute('data-m') === 'name'); }); });
  btn2.addEventListener('click', function () { setMode(!nameMode); });
  syncUI();
  var bComposing = false;
  function suggest() {
    var v = price.value.trim();
    if (!v) { if (nameMode) { sugg.hidden = false; sugg.innerHTML = HINT; } else sugg.hidden = true; return; }
    var all = A.items.filter(function (i) { return !A.isJudged(i.key) && hit(i, v); })
      .map(function (i, ix) { return [rank(i, v), ix, i]; }).sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; }).map(function (x) { return x[2]; });
    sugg.hidden = false;
    sugg.innerHTML = all.length ? all.slice(0, 6).map(function (i) { return '<button type="button" class="jm-sug" data-jm-pick="' + esc(i.key) + '">' + A.ico(i.c) + '<span>' + esc(i.n) + '</span><em>判断済みにする</em></button>'; }).join('') + (all.length > 6 ? '<p class="jm-sug-note">ほか ' + (all.length - 6) + ' 件。もう少し入力して絞り込めます。</p>' : '')
      : '<p class="jm-sug-note">「' + esc(v) + '」に一致する未判断のアイテムはありません。</p>';
  }
  function pick(key) { A.set(key, true); price.value = ''; price.focus(); suggest(); }
  sugg.addEventListener('click', function (e) { var t = e.target.closest('[data-jm-pick]'); if (t) pick(t.getAttribute('data-jm-pick')); });
  price.addEventListener('focus', function () { if (nameMode) suggest(); });
  // 名前モードの間は、価格の検索（数字だけに整える処理）に入力を渡さない。変換の途中でも、入力に合わせて候補を出す
  ['input', 'compositionstart', 'compositionend', 'keydown'].forEach(function (ev) {
    window.addEventListener(ev, function (e) {
      if (!nameMode || e.target !== price) return;
      e.stopPropagation();
      if (ev === 'compositionstart') bComposing = true;
      else if (ev === 'compositionend') { bComposing = false; suggest(); }
      else if (ev === 'input') suggest();
      else if (ev === 'keydown') {
        if (e.key === 'Enter' && !e.isComposing) { e.preventDefault(); var f = $('.jm-sug', sugg); if (f) pick(f.getAttribute('data-jm-pick')); }
        if (e.key === 'Escape') { sugg.hidden = true; }
      }
    }, true);
  });
  document.addEventListener('click', function (e) { if (nameMode && !pw.contains(e.target) && !nav.contains(e.target)) sugg.hidden = true; });

  /* ---------- C: 常設パネル ---------- */
  var panel = document.createElement('details'); panel.className = 'rg-surface jm-panel jm-c-only'; panel.open = true;
  panel.innerHTML = '<summary>判別したアイテムをメモ <span class="res-count" id="jm-pc"></span></summary><div class="jm-body" id="jm-pb"></div>';
  $('#judged-box').parentNode.insertBefore(panel, $('#judged-box'));
  function renderPanel() {
    $('#jm-pb').innerHTML = A.cats.map(function (c) { var n = counts(c); return '<div class="jm-group"><h3>' + A.ico(c).replace('class="cat-ico"', 'class="cat-ico" style="width:26px;height:26px;padding:4px;border-radius:8px"') + c + '<small>' + n[0] + ' / ' + n[1] + '</small></h3><div class="jm-grid">' + A.items.filter(function (i) { return i.c === c; }).map(chip).join('') + '</div></div>'; }).join('');
    var n = counts(''); $('#jm-pc').textContent = n[0] + ' / ' + n[1];
  }

  A.onChange(function () { if (dlg.open) renderSheet(); renderPanel(); if (nameMode && !sugg.hidden) suggest(); });
  renderPanel();

  /* ---------- 切り替えバー ---------- */
  var bar = document.createElement('div'); bar.className = 'jm-bar'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'モックの切り替え');
  bar.innerHTML = '<span>入力方法</span><button type="button" data-v="A" aria-pressed="true">A シート</button><button type="button" data-v="B" aria-pressed="false">B 入力欄の切替</button><button type="button" data-v="C" aria-pressed="false">C 常設パネル</button><span class="jm-bar-b">切替の見せ方</span><button type="button" class="jm-bar-b" data-jb="1" aria-pressed="true">① 2択</button><button type="button" class="jm-bar-b" data-jb="2" aria-pressed="false">② ボタン</button><button type="button" class="jm-bar-b" data-jb="3" aria-pressed="false">③ タブ</button>';
  document.body.appendChild(bar);
  function setVariant(v) { if (v !== 'B') setMode(false); if (dlg.open) dlg.close(); root.setAttribute('data-jm', v); bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v); }); }
  function setStyle(n) { root.setAttribute('data-jb', n); refreshPlaceholder(); bar.querySelectorAll('[data-jb]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-jb') === n); }); }
  bar.addEventListener('click', function (e) { var b = e.target.closest('[data-v]'); if (b) setVariant(b.getAttribute('data-v')); var s = e.target.closest('[data-jb]'); if (s) setStyle(s.getAttribute('data-jb')); });
  setStyle((location.hash.match(/jb=([123])/) || [])[1] || '1');
  setVariant((location.hash.match(/jm=([ABC])/) || [])[1] || 'A');
})();
