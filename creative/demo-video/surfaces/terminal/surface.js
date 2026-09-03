/* ===== surface helpers: terminal ===== */
(() => {
  /* run-plan row state: 'run' (spinner) | 'ok' | 'bad' | null (pending).
     dur is the right-aligned timing — nobody believes a step that took no time. */
  D.step = (id, state, dur) => {
    const el = D.q(id); if (!el) return;
    el.classList.remove('run', 'ok', 'bad');
    if (state) el.classList.add(state);
    if (dur !== undefined) el.querySelector('b').textContent = dur;
  };
  /* a progress bar inside a terminal line: D.tline(D.barline('b1','building')) then D.fill('b1', 100) */
  D.barline = (id, label) => `<span class="d">${label}</span>  <span class="bar"><i id="${id}"></i></span>`;
  D.fill = (id, pct) => { const el = D.q(id); if (el) el.style.width = pct + '%'; };
  /* reveal the result card in the run panel */
  D.card = (on = true) => D.cls('#sum', 'lit', on);
})();
