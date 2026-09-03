/* ===== demo engine — surface-agnostic ==================================
   D.* helpers used by every storyboard. Surface packs extend D in
   surfaces/<name>/surface.js; storyboards only call D.
   Targets: any helper takes a bare id ("W1"), a selector (".ln.err"),
   or an Element. Bare words are read as ids.
   ====================================================================== */
const D = (() => {
  const q = t => t instanceof Element ? t
        : typeof t === 'string' ? document.querySelector(/^[\w-]+$/.test(t) ? '#' + t : t) : null;
  const qa = s => [...document.querySelectorAll(s)];
  const stage = document.getElementById('stage');

  if (new URLSearchParams(location.search).has('rec')) document.body.classList.add('rec');
  const wrap = document.querySelector('.stage-wrap');
  const scale = () => wrap.getBoundingClientRect().width / 1600;
  const fit = () => { stage.style.transform = `scale(${scale()})`; };
  addEventListener('resize', fit); fit();

  /* ---- timing: every timer is cancellable so stages can be re-run ---- */
  let timers = [];
  const later = (fn, ms) => timers.push(setTimeout(fn, ms));
  const clear = () => { timers.forEach(clearTimeout); timers = []; };
  const sleep = ms => new Promise(r => later(r, ms));

  /* ---- content ---- */
  /* type text into an element with human jitter; cps = chars per second */
  async function type(t, text, cps = 38) {
    const el = q(t); el.textContent = '';
    for (const ch of text) { el.textContent += ch; await sleep(1000 / cps + Math.random() * 30); }
    return el;
  }
  const text = (t, s) => { const el = q(t); if (el) el.textContent = s; return el; };
  const html = (t, s) => { const el = q(t); if (el) el.innerHTML = s; return el; };
  /* toggle any class; `lit` is the convention for "this element is now called out" */
  const cls = (t, name, on = true) => { const el = q(t); if (el) el.classList.toggle(name, on); return el; };
  const lit = (t, on = true) => cls(t, 'lit', on);
  const busy = (on = true) => stage.classList.toggle('busy', on);
  const msg = s => text('#stMsg', s);
  /* ticking number — never reveal a count instantly, animate it */
  function count(t, to, fmt = v => ' ' + v.toLocaleString()) {
    const el = q(t); let v = 0;
    const step = () => { v = Math.min(to, v + Math.max(1, Math.round(to / 90))); el.textContent = fmt(v); if (v < to) later(step, 16); };
    step();
  }
  /* narration caption under the chrome; caption(null) hides it */
  function caption(s) {
    const c = document.querySelector('.cap'); if (!c) return;
    if (s == null) { c.classList.remove('on'); return; }
    c.firstElementChild.textContent = s; c.classList.add('on');
  }

  /* ---- scrolling: put `target` `offset` px below the top of its scroller.
     Note scrollTop clamps at the bottom — give the scroller padding-bottom
     if the last lines must be reachable. onScroll lets a surface sync a minimap. ---- */
  let onScroll = null;
  function scrollTo(container, target, offset = 200) {
    const box = q(container), el = q(target); if (!box || !el) return;
    box.scrollTop = el.offsetTop - offset;
    if (onScroll) onScroll(box, el);
  }

  /* ---- terminal helpers (no-op unless the surface has a #term) ----
     spans: .p prompt  .d dim  .h highlight  .w warn  .e error  .k ok  .a accent */
  function tline(markup, termSel = '#term') {
    const t = q(termSel); if (!t) return null;
    const d = document.createElement('div'); d.className = 'ln2'; d.innerHTML = markup;
    t.appendChild(d); t.scrollTop = 1e9; return d;
  }
  function prompt({ id = 'cmd', user = 'project', branch = 'main', term = '#term' } = {}) {
    tline(`<span class="p">➜</span> <span class="a">${user}</span> <span class="d">git:(</span><span style="color:#f78166">${branch}</span><span class="d">)</span> <span id="${id}"></span><span class="caret"></span>`, term);
    return document.getElementById(id);
  }
  const endPrompt = (term = '#term') => { const c = q(term)?.querySelector('.caret'); if (c) c.remove(); };

  /* ---- connector between two elements, in stage coordinates ----
     The stage is transform:scale()d, so every getBoundingClientRect() value
     must be divided by the scale before it is used as an SVG coordinate.
     opts: from/to edge ('left'|'right'|'center'), midX (elbow column, stage px),
           dx/dy nudges. */
  function box(el) {
    const sr = stage.getBoundingClientRect(), s = scale(), r = q(el).getBoundingClientRect();
    return { left: (r.left - sr.left) / s, right: (r.right - sr.left) / s, top: (r.top - sr.top) / s, h: r.height / s, w: r.width / s };
  }
  function link(a, b, o = {}) {
    const svg = document.getElementById('link'); if (!svg) return;
    const A = box(a), B = box(b);
    const edge = (r, e) => e === 'right' ? r.right : e === 'center' ? r.left + r.w / 2 : r.left;
    const ax = edge(A, o.from ?? 'left') + (o.dx ?? 0), ay = A.top + A.h / 2;
    const bx = edge(B, o.to ?? 'right') + (o.dx2 ?? 0), by = B.top + B.h / 2;
    const kx = o.midX ?? (ax + bx) / 2;
    const dv = by - ay, r = Math.min(40, Math.abs(dv) / 2);
    const d = Math.abs(dv) < 8
      ? `M${ax},${ay} L${bx},${by}`
      : `M${ax},${ay} C${kx - 10},${ay} ${kx},${ay} ${kx},${ay + Math.sign(dv) * r} L${kx},${by - Math.sign(dv) * r} C${kx},${by} ${kx},${by} ${bx},${by}`;
    svg.querySelector('#lp').setAttribute('d', d);
    const c1 = svg.querySelector('#c1'), c2 = svg.querySelector('#c2');
    c1.setAttribute('cx', ax); c1.setAttribute('cy', ay); c2.setAttribute('cx', bx); c2.setAttribute('cy', by);
    svg.classList.add('open');
  }
  const unlink = () => document.getElementById('link')?.classList.remove('open');

  /* ---- stage runner ----
     stages = [{name, run: async () => {}, gap?: ms}] and one reset().
     Every run() must be replayable from reset() — that is what makes the
     numbered buttons, keyboard digits and snap.py work. ---- */
  let stages = [], resetFn = () => {};
  function define(list, reset) {
    stages = list; resetFn = reset || (() => {});
    const boxEl = document.getElementById('steps');
    if (boxEl) {
      boxEl.innerHTML = '';
      list.forEach((s, i) => {
        const b = document.createElement('button');
        b.textContent = `${i} ${s.name}`; b.dataset.step = i; b.onclick = () => go(i); boxEl.appendChild(b);
      });
      const r = document.createElement('button'); r.textContent = '↻ replay'; r.onclick = replay; boxEl.appendChild(r);
    }
    addEventListener('keydown', e => {
      if (e.key === 'r') replay();
      if (/^[0-9]$/.test(e.key) && +e.key < list.length) go(+e.key);
    });
    const tickEl = document.getElementById('tick'), t0 = performance.now();
    if (tickEl) setInterval(() => { tickEl.textContent = ((performance.now() - t0) / 1000).toFixed(1) + 's'; }, 100);
  }
  const mark = n => qa('#steps button').forEach(b => b.setAttribute('aria-current', b.dataset.step == n ? 'step' : ''));
  async function go(n) {
    clear(); mark(n); resetFn();
    for (let i = 0; i <= n; i++) { if (i > 0) await sleep(stages[i].gap ?? 600); await stages[i].run(); }
  }
  const replay = () => go(stages.length - 1);

  return { q, $: q, qa, stage, scale, box, sleep, later, clear, type, text, html, cls, lit, busy, msg, count, caption,
           scrollTo, set onScroll(f) { onScroll = f; }, tline, prompt, endPrompt, link, unlink, define, go, replay };
})();
