/* ===== surface helpers: ide ===== */
(() => {
  /* minimap: random code-shaped bars, viewport rect synced to the editor scroll */
  const mm = D.q('#mm'), vp = D.q('#vp');
  if (mm) {
    for (let i = 0; i < 74; i++) {
      const d = document.createElement('i');
      d.style.width = (20 + Math.random() * 50) + '%';
      d.style.opacity = .5 + Math.random() * .5;
      mm.appendChild(d);
    }
    mm.appendChild(vp);
    D.onScroll = (pre, el) => { if (pre.id === 'mainPre') vp.style.top = (8 + (el.offsetTop / pre.scrollHeight) * (pre.clientHeight - 140)) + 'px'; };
  }

  /* keep line numbers honest after an inserted line (d = +1 / -1) */
  D.renumber = (preId, insertId, d) => {
    let after = false;
    D.qa('#' + preId + ' .ln').forEach(l => {
      if (after) { const i = l.querySelector('i'); i.textContent = (+i.textContent) + d; }
      if (l.id === insertId) after = true;
    });
  };
  /* switch the side pane's info block: 0 waiting / 1 failing / 2 passing */
  D.info = n => ['iv0', 'iv1', 'iv2'].forEach((id, i) => D.cls(id, 'on', i === n));
  /* dashed connector from a side-pane line to a main-editor line, routed down the minimap column */
  D.crossLink = (aId, bId) => D.link(aId, bId, { from: 'left', to: 'right', dx: 1, midX: D.box('#mainEd').right - 88, dx2: -88 });
  /* problem counters in the status bar */
  D.problems = (err, warn) => { D.text('#pcnt', String(err + warn)); D.html('#stErr', `⊗ ${err} &nbsp;⚠ ${warn}`); };
  /* bottom panel tab: 'term' | 'problems' */
  D.panel = which => {
    D.cls('#tTerm', 'on', which === 'term'); D.cls('#tProb', 'on', which === 'problems');
    D.cls(D.stage, 'probs', which === 'problems');
  };
})();
