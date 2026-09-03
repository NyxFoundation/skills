/* ===== surface helpers: webapp ===== */
(() => {
  /* status pill on a table row: D.pill('r3','run','checking…') */
  D.pill = (rowId, kind, label) => {
    const p = D.q(rowId)?.querySelector('.pill'); if (!p) return;
    p.className = 'pill' + (kind ? ' ' + kind : '');
    if (label !== undefined) p.textContent = label;
  };
  /* right-hand detail drawer */
  D.drawer = (on = true) => D.cls(D.stage, 'drawer-open', on);
  /* bottom-right toast; kind 'bad' turns the dot red. Auto-hides after ms (0 = keep). */
  D.toast = (text, kind = '', ms = 2600) => {
    D.text('#toastMsg', text);
    const t = D.q('#toast'); t.className = 'toast on' + (kind ? ' ' + kind : '');
    if (ms) D.later(() => t.classList.remove('on'), ms);
  };
  /* header button state while the tool works */
  D.cta = (label, busy = false) => { D.text('#cta', label); D.cls('#cta', 'busy', busy); };
})();
