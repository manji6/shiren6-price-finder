(function () {
  var A = window.ShirenApp; if (!A) return;
  var root = document.documentElement;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var CHECK = '<svg class="jm-check" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 10.5l3.5 3.5 7.5-8"/></svg>';
  // 検索用: 全角半角をそろえ、カタカナをひらがなにして比べる
  var norm = function (s) { return s.normalize('NFKC').toLowerCase().replace(/[ァ-ヶ]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0x60); }); };
  var hit = function (it, q) { return !q || norm(it.n).indexOf(norm(q)) >= 0; };
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
    '<input class="rg-input" id="jm-q" type="search" inputmode="search" enterkeyhint="search" autocomplete="off" placeholder="名前で探す（例：混乱、つえ）" aria-label="アイテム名で絞り込む">' +
    '<div class="rg-chips jm-tabs" id="jm-tabs" role="group" aria-label="種別"></div><div class="jm-grid" id="jm-grid"></div>' +
    '<div class="jm-foot"><span class="rg-muted" id="jm-count"></span><button class="rg-button" id="jm-done" type="button">完了</button></div>';
  ($('.rg-theme') || document.body).appendChild(dlg);   // フォントなどの指定が効くよう、ページの内側に置く
  function renderSheet() {
    var tabs = [['', 'すべて']].concat(A.cats.map(function (c) { return [c, c]; }));
    $('#jm-tabs').innerHTML = tabs.map(function (t) { var n = counts(t[0]); return '<button type="button" class="rg-chip" data-jm-tab="' + esc(t[0]) + '" aria-pressed="' + (tab === t[0]) + '">' + (t[0] ? A.ico(t[0]) : '') + t[1] + '<span class="chip-count">' + n[0] + '/' + n[1] + '</span></button>'; }).join('');
    var list = A.items.filter(function (i) { return (!tab || i.c === tab) && hit(i, q); });
    $('#jm-grid').innerHTML = list.length ? list.map(chip).join('') : '<p class="jm-empty">「' + esc(q) + '」に一致するアイテムはありません。</p>';
    var n = counts(''); $('#jm-count').textContent = '判断済み ' + n[0] + ' / ' + n[1];
  }
  $('#jm-open').addEventListener('click', function () { renderSheet(); dlg.showModal(); });
  $('#jm-close').addEventListener('click', function () { dlg.close(); }); $('#jm-done').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener('click', function (e) { var t = e.target.closest('[data-jm-tab]'); if (t) { tab = t.getAttribute('data-jm-tab'); renderSheet(); } });
  var qEl = $('#jm-q');
  qEl.addEventListener('compositionstart', function () { composing = true; }); qEl.addEventListener('compositionend', function () { composing = false; q = qEl.value; renderSheet(); });
  qEl.addEventListener('input', function (e) { if (composing || e.isComposing) return; q = qEl.value; renderSheet(); });

  /* ---------- B: 入力欄の切替（123 ⇄ 名前） ---------- */
  var price = $('#price'), pw = $('.price-wrap'), nameMode = false;
  var mode = document.createElement('button'); mode.type = 'button'; mode.className = 'rg-button jm-b-only jm-mode'; mode.setAttribute('aria-pressed', 'false'); mode.setAttribute('aria-label', '入力の種類を切り替える（数字／名前）'); mode.innerHTML = '<span>123</span>';
  pw.appendChild(mode);
  var sugg = document.createElement('div'); sugg.className = 'jm-sugg'; sugg.id = 'jm-sugg'; sugg.hidden = true; pw.appendChild(sugg);
  function setMode(on) {
    if (nameMode === on) return;
    price.value = ''; price.dispatchEvent(new Event('input', { bubbles: true }));  // 価格の検索を空に戻す（切り替え前の状態で）
    nameMode = on; root.classList.toggle('jm-name', on);
    mode.setAttribute('aria-pressed', on); mode.innerHTML = '<span>' + (on ? '名前' : '123') + '</span>';
    price.setAttribute('inputmode', on ? 'text' : 'numeric'); price.setAttribute('enterkeyhint', on ? 'search' : 'done');
    price.placeholder = on ? 'アイテム名（例：混乱）' : '値段を入力（例 400）'; price.removeAttribute('maxlength'); if (!on) price.setAttribute('maxlength', '9');
    sugg.hidden = true; price.focus();
  }
  mode.addEventListener('click', function () { setMode(!nameMode); });
  var bComposing = false;
  function suggest() {
    var v = price.value.trim(); if (!v) { sugg.hidden = true; return; }
    var all = A.items.filter(function (i) { return !A.isJudged(i.key) && hit(i, v); });
    sugg.hidden = false;
    sugg.innerHTML = all.length ? all.slice(0, 6).map(function (i) { return '<button type="button" class="jm-sug" data-jm-pick="' + esc(i.key) + '">' + A.ico(i.c) + '<span>' + esc(i.n) + '</span><em>判断済みにする</em></button>'; }).join('') + (all.length > 6 ? '<p class="jm-sug-note">ほか ' + (all.length - 6) + ' 件。もう少し入力して絞り込めます。</p>' : '')
      : '<p class="jm-sug-note">「' + esc(v) + '」に一致する未判断のアイテムはありません。</p>';
  }
  function pick(key) { A.set(key, true); price.value = ''; sugg.hidden = true; price.focus(); }
  sugg.addEventListener('click', function (e) { var t = e.target.closest('[data-jm-pick]'); if (t) pick(t.getAttribute('data-jm-pick')); });
  // 名前モードの間は、価格の検索（数字だけに整える処理）に入力を渡さない
  ['input', 'compositionstart', 'compositionend', 'keydown'].forEach(function (ev) {
    window.addEventListener(ev, function (e) {
      if (!nameMode || e.target !== price) return;
      e.stopPropagation();
      if (ev === 'compositionstart') bComposing = true;
      else if (ev === 'compositionend') { bComposing = false; suggest(); }
      else if (ev === 'input') { if (!bComposing && !e.isComposing) suggest(); }
      else if (ev === 'keydown') {
        if (e.key === 'Enter' && !e.isComposing) { e.preventDefault(); var f = $('.jm-sug', sugg); if (f) pick(f.getAttribute('data-jm-pick')); }
        if (e.key === 'Escape') { sugg.hidden = true; }
      }
    }, true);
  });
  document.addEventListener('click', function (e) { if (nameMode && !pw.contains(e.target)) sugg.hidden = true; });

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
  bar.innerHTML = '<span>入力方法</span><button type="button" data-v="A" aria-pressed="true">A シート</button><button type="button" data-v="B" aria-pressed="false">B 入力欄の切替</button><button type="button" data-v="C" aria-pressed="false">C 常設パネル</button>';
  document.body.appendChild(bar);
  function setVariant(v) { if (v !== 'B') setMode(false); if (dlg.open) dlg.close(); root.setAttribute('data-jm', v); bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v); }); }
  bar.addEventListener('click', function (e) { var b = e.target.closest('[data-v]'); if (b) setVariant(b.getAttribute('data-v')); });
  setVariant((location.hash.match(/jm=([ABC])/) || [])[1] || 'A');
})();
