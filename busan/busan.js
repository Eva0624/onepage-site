/* 釜山之旅共用腳本：勾選／金額記憶、全部清除、搜尋按鈕 */
(function () {
  var page = document.body.getAttribute('data-page');
  if (!page) return;
  var KEY = 'busan.' + page;
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { state = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  function each(list, fn) { Array.prototype.forEach.call(list, fn); }

  /* 1. 勾選 */
  var boxes = document.querySelectorAll('input[type=checkbox][data-key]');
  function sync(cb) {
    var item = cb.closest('[data-item]');
    if (item) item.classList.toggle('done', cb.checked);
    var lab = cb.closest('.bought');
    if (lab) lab.classList.toggle('done', cb.checked);
  }
  function count() {
    var el = document.querySelector('[data-count]');
    if (!el) return;
    var n = 0;
    each(boxes, function (b) { if (b.checked) n++; });
    el.textContent = n + ' / ' + boxes.length;
  }
  each(boxes, function (cb) {
    var k = cb.getAttribute('data-key');
    cb.checked = (k in state) ? !!state[k] : cb.defaultChecked;
    sync(cb);
    cb.addEventListener('change', function () {
      state[k] = cb.checked;
      save();
      sync(cb);
      count();
    });
  });
  count();

  /* 2. 金額輸入與進度條（付款頁） */
  each(document.querySelectorAll('input[type=number][data-key]'), function (inp) {
    var k = inp.getAttribute('data-key');
    var limit = Number(inp.getAttribute('data-limit')) || 0;
    var wrap = inp.closest('.spend');
    if (k in state && state[k] !== null) inp.value = state[k];
    function render(store) {
      var v = Number(inp.value) || 0;
      if (store) { state[k] = v; save(); }
      if (!wrap) return;
      var pct = limit ? Math.min(100, v / limit * 100) : 0;
      wrap.querySelector('.bar-fill').style.width = pct + '%';
      wrap.querySelector('.spend-now').textContent = v.toLocaleString();
      wrap.querySelector('.spend-left').textContent = Math.max(0, limit - v).toLocaleString();
      wrap.classList.toggle('over', !!limit && v >= limit);
    }
    inp.addEventListener('input', function () { render(true); });
    render(false);
  });

  /* 3. 全部清除 */
  each(document.querySelectorAll('[data-reset]'), function (btn) {
    btn.addEventListener('click', function () {
      if (confirm('清除這一頁所有勾選與紀錄？')) {
        try { localStorage.removeItem(KEY); } catch (e) {}
        location.reload();
      }
    });
  });

  /* 4. 搜尋按鈕 */
  var ENG = {
    gimg:  { label: 'Google 圖片', q: 'en', url: 'https://www.google.com/search?tbm=isch&q=' },
    oy:    { label: 'Olive Young', q: 'en', url: 'https://global.oliveyoung.com/search?query=' },
    oykr:  { label: 'OY 韓國站',   q: 'ko', url: 'https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=' },
    naver: { label: 'Naver',       q: 'ko', url: 'https://search.naver.com/search.naver?query=' },
    nshop: { label: 'Naver 購物',  q: 'ko', url: 'https://search.shopping.naver.com/search/all?query=' },
    lotte: { label: '樂天 ON',     q: 'ko', url: 'https://www.lotteon.com/search/search/search.ecn?mallId=1&q=' }
  };
  var bodyEngines = document.body.getAttribute('data-engines') || 'gimg,naver';
  each(document.querySelectorAll('.pcard'), function (card) {
    var row = card.querySelector('.search-row');
    if (!row) return;
    var qEn = card.getAttribute('data-q-en') || '';
    var qKo = card.getAttribute('data-q-ko') || '';
    var engines = (card.getAttribute('data-engines') || bodyEngines).split(',');
    each(engines, function (id) {
      var e = ENG[id.trim()];
      if (!e) return;
      var q = e.q === 'ko' ? (qKo || qEn) : (qEn || qKo);
      if (!q) return;
      var a = document.createElement('a');
      a.className = 'sbtn sbtn-' + id.trim();
      a.target = '_blank';
      a.rel = 'noopener';
      a.href = e.url + encodeURIComponent(q);
      a.textContent = e.label;
      row.appendChild(a);
    });
  });
})();
