/* ===== surface helpers: world =====
   Bringing nodes online, wiring them, and — the part that makes it read as a
   simulation rather than an animation — running the traffic. */
(() => {
  const SVGNS = 'http://www.w3.org/2000/svg';
  const wire = () => document.getElementById('wire');
  const flow = () => document.getElementById('flow');
  /* bumped by reset(); every loop and every in-flight dot checks it and gives up */
  let gen = 0;
  D.newGen = () => { gen++; flow().innerHTML = ''; };
  D.gen = () => gen;

  const el = (n, a) => { const e = document.createElementNS(SVGNS, n); for (const k in a) e.setAttribute(k, a[k]); return e; };

  /* Geometry in MAP coordinates, read from the layout rather than from the screen.
     getBoundingClientRect() would be measured through the stage scale AND through
     the camera transform, so a push-in would slide every wire off its node. Offsets
     are untouched by transforms, which is exactly what a camera needs. */
  const cam = () => document.getElementById('cam');
  function mbox(t) {
    const e = D.q(t); if (!e) return { left: 0, top: 0, w: 0, h: 0 };
    let x = 0, y = 0, n = e;
    while (n && n !== cam()) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; }
    return { left: x, top: y, w: e.offsetWidth, h: e.offsetHeight };
  }
  D.mbox = mbox;

  /* The camera frames a RECTANGLE of the map, not a point and a zoom factor.
     Framing a point is how you end up with the two things the shot is about at
     opposite edges of the screen: on this map the adversary and its target are
     1,540px apart, so "scale 1.55 centred on the adversary" pushes the target
     clean out of frame. Give it what must be visible and let it solve for the
     scale. MAP is the whole board, which is what pulling back means. */
  const FRAME_W = 1600, FRAME_H = 620, MAX_SCALE = 1.7;
  D.MAP = [0, 0, FRAME_W, FRAME_H];
  D.camTo = (rect, ms = 900) => {
    const c = cam(); if (!c) return;
    const [x1, y1, x2, y2] = rect;
    const s = Math.min(MAX_SCALE, FRAME_W / Math.max(1, x2 - x1), FRAME_H / Math.max(1, y2 - y1));
    const tx = (FRAME_W - (x2 - x1) * s) / 2 - x1 * s;
    const ty = (FRAME_H - (y2 - y1) * s) / 2 - y1 * s;
    c.style.transition = ms ? `transform ${ms}ms cubic-bezier(.4,0,.2,1)` : 'none';
    c.style.transform = `translate(${tx}px,${ty}px) scale(${s})`;
  };
  D.cam = (o = {}) => D.camTo(D.MAP, o.ms ?? 900);
  /* the world's clock. 1 is real time; the drain runs at a quarter of it. */
  let speed = 1;
  D.speed = v => { if (v !== undefined) speed = v; return speed; };
  D.focus = (on = true) => D.cls(D.stage, 'focus', on);

  /* Elbow path between two boxes, in STAGE coordinates. Both SVG layers are
     children of .stage for exactly this reason — nested in .map every path came
     out 56px low. */
  function d(a, b, o = {}) {
    const A = mbox(a), B = mbox(b);
    /* mbox reports left/top/w/h; the right edge is derived here rather than stored,
       so there is one place that knows what an edge means. */
    const ax = (o.from === 'left' ? A.left : A.left + A.w), ay = A.top + A.h / 2;
    const bx = (o.to === 'right' ? B.left + B.w : B.left), by = B.top + B.h / 2;
    const kx = o.midX ?? (ax + bx) / 2;
    const dv = by - ay, r = Math.min(30, Math.abs(dv) / 2);
    return Math.abs(dv) < 5 ? `M${ax},${ay} L${bx},${by}`
      : `M${ax},${ay} C${kx - 10},${ay} ${kx},${ay} ${kx},${ay + Math.sign(dv) * r}` +
        ` L${kx},${by - Math.sign(dv) * r} C${kx},${by} ${kx},${by} ${bx},${by}`;
  }

  D.wire = (a, b, o = {}) => {
    const p = el('path', { d: d(a, b, o), class: o.cls || '' });
    p.dataset.pair = `${a}>${b}`; wire().appendChild(p); return p;
  };
  D.hot = (a, b, cls = 'hot') => {
    const p = wire().querySelector(`[data-pair="${a}>${b}"]`);
    if (p) p.setAttribute('class', cls); else D.wire(a, b, { cls });
  };
  D.wipeWires = () => { wire().innerHTML = ''; };

  /* One transaction travelling one wire. Await it to sequence on ARRIVAL — state
     must change when a transaction lands, not when it is sent. */
  D.tx = (a, b, o = {}) => new Promise(resolve => {
    const mine = gen;
    const path = el('path', { d: d(a, b, o), fill: 'none', stroke: 'none' });
    flow().appendChild(path);
    const len = path.getTotalLength(), colour = o.colour || 'var(--accent2)';
    const dot = el('circle', { r: o.r || 3.4, fill: colour, color: colour });
    flow().appendChild(dot);
    const ms = (o.ms || 900) / (o.raw ? 1 : speed), t0 = performance.now();
    const step = now => {
      if (mine !== gen) { dot.remove(); path.remove(); return; }
      const k = Math.min(1, (now - t0) / ms), pt = path.getPointAtLength(len * k);
      dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y);
      if (k < 1) requestAnimationFrame(step);
      else { dot.style.transition = 'opacity .25s'; dot.style.opacity = '0';
             D.later(() => { dot.remove(); path.remove(); }, 280); resolve(); }
    };
    requestAnimationFrame(step);
  });

  /* A transaction that goes out and does not take. It travels most of the way,
     turns, and comes back red. Two of these before the one that works is what
     makes the third one worth watching — a first-try success is not a story. */
  D.txFail = (a, b, o = {}) => new Promise(resolve => {
    const mine = gen;
    const path = el('path', { d: d(a, b, o), fill: 'none', stroke: 'none' });
    flow().appendChild(path);
    const len = path.getTotalLength();
    const dot = el('circle', { r: o.r || 4, fill: 'var(--agent)', color: 'var(--agent)' });
    flow().appendChild(dot);
    const turn = o.turn ?? 0.66, ms = (o.ms || 900) / (o.raw ? 1 : speed), t0 = performance.now();
    const step = now => {
      if (mine !== gen) { dot.remove(); path.remove(); return; }
      const e = (now - t0) / ms;
      const k = e <= 1 ? turn * e : Math.max(0, turn * (2 - e));
      const pt = path.getPointAtLength(len * k);
      dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y);
      if (e > 1) { dot.setAttribute('fill', 'var(--bad)'); dot.setAttribute('color', 'var(--bad)'); }
      if (e < 2) requestAnimationFrame(step);
      else { dot.remove(); path.remove(); resolve(); }
    };
    requestAnimationFrame(step);
  });

  /* ---- nodes ---- */
  D.up = (t, on = true) => D.cls(t, 'up', on);
  D.stat = (id, v, mood = '') => {
    D.text('#' + id + 'v', v);
    const n = D.q(id); if (n) { n.classList.remove('moved', 'gain', 'loss'); if (mood) n.classList.add(mood); }
  };
  D.tag = (id, kind, label) => {
    const t = D.q(id)?.querySelector('.tag'); if (!t) return;
    t.className = 'tag' + (kind ? ' ' + kind : ''); if (label !== undefined) t.textContent = label;
  };
  /* a wallet chip's running PnL */
  D.pnl = (chipId, text, mood = '') => {
    const c = D.q(chipId); if (!c) return;
    c.querySelector('.gp').textContent = text;
    c.classList.remove('gain', 'loss'); if (mood) c.classList.add(mood);
  };
  D.chipOf = name => document.querySelector(`.chip[data-name="${name}"]`)?.id;
  /* swap a node's category glyph — used once, when the wallet that has been reading
     stops looking like a baseline */
  D.glyph = (id, name) => {
    const u = D.q(id)?.querySelector('.ic use');
    if (u) u.setAttribute('href', '#ic-' + name);
  };

  /* ---- the chain ---- */
  D.block = n => {
    D.text('#blkNo', 'block ' + n.toLocaleString());
    D.text('#telBlk', 'block ' + n.toLocaleString());
    D.cls(D.stage, 'tick', true); D.later(() => D.cls(D.stage, 'tick', false), 200);
  };
  /* the slot gauge: one block of wall clock, filling. Restarted every block. */
  D.slot = ms => {
    const i = D.q('#slotBar'); if (!i) return;
    i.style.transition = 'none';
    i.style.width = '0%';
    /* Force the reflow. Without it the browser coalesces the 0% and the 100% into
       one style recalculation, never sees the start value, and the bar sits pinned
       at full for the whole run — a loading gauge that has visibly stopped. Setting
       the transition back on a requestAnimationFrame is not enough: rAF fires
       before the style flush, so both writes still land in the same recalc. */
    void i.offsetWidth;
    i.style.transition = `width ${ms}ms linear`;
    i.style.width = '100%';
  };
  D.mem = (id, o = {}) => {
    const r = D.q(id); if (!r) return;
    r.className = 'tx on' + (o.state ? ' ' + o.state : '') + (o.evil ? ' evil' : '');
    const put = (s, v) => { const n = r.querySelector(s); if (n && v !== undefined) n.textContent = v; };
    put('b', o.what); put('.who', o.who); put('.fee', o.fee);
  };
  D.memRows = () => ['t1', 't2', 't3', 't4', 't5', 't6'];
  D.memClear = () => { D.memRows().forEach(id => { const r = D.q(id); if (r) r.className = 'tx'; }); D.text('#memMore', ' '); };
  D.feed = h => D.html('#chainFeed', h);

  /* ---- the reasoning panel ---- */
  D.mind = (o = {}) => {
    if (o.title !== undefined) D.text('#mindTitle', o.title);
    if (o.who !== undefined) D.text('#mindWho', o.who);
    if (o.left !== undefined) D.text('#mkL', o.left);
    if (o.right !== undefined) D.text('#mkR', o.right);
    if (o.badge !== undefined) {
      D.text('#mindBadge', o.badge);
      const b = D.q('#mindBadge'); b.className = 'badge' + (o.state ? ' ' + o.state : '');
    }
    if (o.evil !== undefined) D.cls('#mind', 'evil', o.evil);
  };
  /* evidence lines, revealed one at a time — the order is the argument */
  D.ev = (n, markup) => { const e = D.q('e' + n); if (!e) return; e.innerHTML = markup; e.classList.add('on'); };
  D.evClear = () => { for (let i = 1; i <= 8; i++) { const e = D.q('e' + i); if (e) { e.className = 'ev'; e.innerHTML = '&nbsp;'; } } };
  D.quote = s => { D.text('#mQuote', s); D.cls('#mQuote', 'on', true); };
  /* the parameter that moved, and what it moved from */
  D.param = (n, name, from, to) => {
    const r = D.q('p' + n); if (!r) return;
    r.querySelector('.pn').textContent = name;
    r.querySelector('.pf').textContent = from;
    r.querySelector('.pt').textContent = to;
    r.classList.add('on');
  };
  D.stamp = s => { D.text('#mStamp', s); D.cls('#mStamp', 'on', true); };
  D.mindReset = () => {
    D.evClear();
    D.cls('#mQuote', 'on', false); D.text('#mQuote', ' ');
    ['p1','p2'].forEach(i => { const r = D.q('#' + i); if (r) r.className = 'prm'; });
    D.cls('#mStamp', 'on', false); D.text('#mStamp', ' ');
    D.mind({ title: 'STRATEGY REVISION', who: '—', badge: 'idle', state: '', evil: false,
             left: 'EVIDENCE HANDED TO THE MODEL', right: 'WHAT IT DECIDED' });
  };

  /* ---- history charts ----
     Autoscaled polylines over the last N blocks. The scale is shared across the
     series of one chart so the lines can be compared, and it is padded so a flat
     stretch does not fill the box. */
  const CH = {};
  D.chart = (id, keys, cap = 46) => {
    CH[id] = { keys, cap, data: Object.fromEntries(keys.map(k => [k, []])) };
    draw(id);
  };
  D.plot = (id, vals) => {
    const c = CH[id]; if (!c) return;
    for (const k of c.keys) {
      const v = vals[k];
      const a = c.data[k];
      a.push(v === undefined ? (a.length ? a[a.length - 1] : null) : v);
      if (a.length > c.cap) a.shift();
    }
    draw(id);
  };
  function draw(id) {
    const c = CH[id], svg = D.q('#' + id); if (!c || !svg) return;
    const W = 548, H = 84;
    let lo = Infinity, hi = -Infinity;
    for (const k of c.keys) for (const v of c.data[k]) if (v != null) { if (v < lo) lo = v; if (v > hi) hi = v; }
    if (!isFinite(lo)) { lo = 0; hi = 1; }
    const pad = (hi - lo) * 0.14 || Math.abs(hi) * 0.02 || 1;
    lo -= pad; hi += pad;
    /* While the window is filling, spread the points across the whole width; once it
       is full this is the same thing as scrolling. Right-aligning from the first
       block instead put three points in the last 5% of the box. */
    const len = Math.max(...c.keys.map(k => c.data[k].length), 0);
    const n = Math.max(2, len);
    for (const k of c.keys) {
      const a = c.data[k], p = svg.querySelector(`polyline[data-k="${k}"]`);
      if (!p) continue;
      const off = n - a.length;
      const pts = a.map((v, i) => v == null ? null
        : `${((i + off) / (n - 1) * W).toFixed(1)},${(H - (v - lo) / (hi - lo) * H).toFixed(1)}`)
        .filter(Boolean).join(' ');
      p.setAttribute('points', pts);
    }
  }
  D.chartReset = () => { for (const id in CH) D.chart(id, CH[id].keys, CH[id].cap); };

  /* ---- the strip under the charts ---- */
  D.tel = (cell, value) => D.text('#' + cell + 'v', value);
  D.epoch = (block, total = 720) => {
    D.text('#epBlk', block.toLocaleString());
    const b = D.q('#epBar'); if (b) b.style.width = Math.min(100, block / total * 100) + '%';
  };
  D.telNote = (on = true) => D.cls('#telNote', 'on', on);
  /* a caption at keynote size, for the two lines the room has to read */
  D.big = (s, on = true) => { D.caption(s); D.cls('.cap', 'big', on && s != null); };
})();
