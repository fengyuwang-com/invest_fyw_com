/* FengInvest 研究库 · 阅读器脚本（原生 JS，零依赖） */
(function () {
  'use strict';

  var root = document.documentElement;
  var sidebar = document.getElementById('sidebar');
  var main = document.querySelector('.main-content');
  var menuToggle = document.getElementById('menuToggle');
  var closeBtn = document.getElementById('sidebarToggle');

  function openSidebar() {
    if (!sidebar) return;
    sidebar.classList.add('open');
    if (main) main.classList.add('sidebar-open');
  }
  function closeSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    if (main) main.classList.remove('sidebar-open');
  }
  if (menuToggle) menuToggle.addEventListener('click', openSidebar);
  if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeSidebar();
  });
  if (main) {
    main.addEventListener('click', function (e) {
      if (sidebar && sidebar.classList.contains('open') && !sidebar.contains(e.target)) closeSidebar();
    });
  }

  /* ---------- 主题 ---------- */
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var dark = root.getAttribute('data-theme') === 'dark';
      if (dark) {
        root.removeAttribute('data-theme');
        localStorage.setItem('feng_theme', 'light');
      } else {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem('feng_theme', 'dark');
      }
    });
  }

  /* ---------- 字号 ---------- */
  var fsButtons = document.querySelectorAll('[data-fs-set]');
  Array.prototype.forEach.call(fsButtons, function (btn) {
    btn.addEventListener('click', function () {
      var size = btn.getAttribute('data-fs-set');
      if (size === 'm') root.removeAttribute('data-fs');
      else root.setAttribute('data-fs', size);
      localStorage.setItem('feng_fs', size);
    });
  });

  /* ---------- 阅读进度 ---------- */
  var bar = document.getElementById('progressBar');
  var article = document.querySelector('.report-reader');
  if (bar) {
    if (article) {
      var update = function () {
        var rect = article.getBoundingClientRect();
        var total = rect.height - window.innerHeight + 120;
        var done = -rect.top + 120;
        var ratio = total > 0 ? done / total : (done > 0 ? 1 : 0);
        ratio = Math.max(0, Math.min(1, ratio));
        bar.style.transform = 'scaleX(' + ratio + ')';
      };
      window.addEventListener('scroll', update, { passive: true });
      window.addEventListener('resize', update);
      update();
    } else {
      bar.style.display = 'none';
    }
  }

  /* ---------- 报告筛选 ---------- */
  var chips = document.querySelectorAll('.chip[data-filter]');
  var list = document.getElementById('reportList');
  if (chips.length && list) {
    Array.prototype.forEach.call(chips, function (chip) {
      chip.addEventListener('click', function () {
        Array.prototype.forEach.call(chips, function (c) { c.classList.remove('active'); });
        chip.classList.add('active');
        var filter = chip.getAttribute('data-filter');
        var rows = list.querySelectorAll('.report-row');
        Array.prototype.forEach.call(rows, function (row) {
          var show = true;
          if (filter.indexOf('market:') === 0) show = row.getAttribute('data-market') === filter.slice(7);
          else if (filter.indexOf('decision:') === 0) show = row.getAttribute('data-decision') === filter.slice(9);
          row.style.display = show ? '' : 'none';
        });
      });
    });
  }

  /* ---------- 站内搜索 ---------- */
  var input = document.getElementById('searchInput');
  var results = document.getElementById('searchResults');
  if (input && results) {
    var index = null;
    var loading = false;

    function loadIndex(cb) {
      if (index) { cb(); return; }
      if (loading) { return; }
      loading = true;
      var s = document.createElement('script');
      s.src = '/search-index.js';
      s.onload = function () {
        index = window.FENG_SEARCH_INDEX || [];
        cb();
      };
      s.onerror = function () {
        results.innerHTML = '<p class="search-hint">搜索索引加载失败，请刷新页面重试。</p>';
      };
      document.head.appendChild(s);
    }

    function esc(s) {
      return String(s).replace(/[&<>"']/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    }

    function highlight(text, terms) {
      var out = esc(text);
      terms.forEach(function (t) {
        if (!t) return;
        var safe = esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        out = out.replace(new RegExp('(' + safe + ')', 'gi'), '<mark>$1</mark>');
      });
      return out;
    }

    function search() {
      var q = input.value.trim().toLowerCase();
      if (!q) {
        results.innerHTML = '<p class="search-hint">输入关键词开始搜索。</p>';
        return;
      }
      var terms = q.split(/\s+/).filter(Boolean);
      var hits = [];
      index.forEach(function (item) {
        var title = (item.title || '').toLowerCase();
        var text = ((item.text || '') + ' ' + (item.excerpt || '')).toLowerCase();
        var score = 0;
        var all = true;
        terms.forEach(function (t) {
          if (title.indexOf(t) >= 0) score += 10;
          if ((item.excerpt || '').toLowerCase().indexOf(t) >= 0) score += 4;
          if (text.indexOf(t) >= 0) score += 2;
          if (title.indexOf(t) < 0 && text.indexOf(t) < 0) all = false;
        });
        if (all) hits.push({ item: item, score: score });
      });
      hits.sort(function (a, b) { return b.score - a.score; });
      hits = hits.slice(0, 40);
      if (!hits.length) {
        results.innerHTML = '<p class="search-hint">没有找到「' + esc(input.value.trim()) + '」。试试公司名、代码或更短的关键词。</p>';
        return;
      }
      results.innerHTML = hits.map(function (h) {
        var it = h.item;
        return '<a class="search-item" href="' + esc(it.url) + '">' +
          '<div class="si-title">' + highlight(it.title, terms) +
          '<span class="si-cat">' + esc(it.cat || '') + '</span></div>' +
          '<div class="si-excerpt">' + highlight(it.excerpt || '', terms) + '</div></a>';
      }).join('');
    }

    var timer = null;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        loadIndex(search);
      }, 120);
    });
    var params = new URLSearchParams(location.search);
    if (params.get('q')) {
      input.value = params.get('q');
      loadIndex(search);
    }
  }
})();
