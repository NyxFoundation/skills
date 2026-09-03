/* Six beats: idle dashboard → the user starts the job → rows work through →
   the one row that fails → the detail drawer (the "aha") → fixed + confirmed.
   Replace the copy, keep the shape. Every run() must be replayable from reset(). */
const ROWS = ['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10','r11','r12'];
const BAD = 'r5';

D.define([
  { name: 'idle', run: async () => {
      D.count('#k1v', 128); D.count('#k2v', 42); D.text('#k3v', '0'); D.count('#k4v', 96, v => v + '%');
  }},

  { name: 'start', run: async () => {
      D.cta('Running…', true); D.busy(true); D.msg(`run started · ${ROWS.length} records`);
      D.pill('r1', 'run', 'checking'); await D.sleep(700);
      D.pill('r1', 'ok', 'passed'); D.pill('r2', 'run', 'checking');
  }},

  { name: 'progress', run: async () => {
      for (const [ok, next] of [['r2','r3'], ['r3','r4'], ['r4','r5']]) {
        D.pill(ok, 'ok', 'passed'); D.pill(next, 'run', 'checking'); await D.sleep(550);
      }
      D.cls('#k2', 'lit'); D.count('#k2v', 46);
  }},

  { name: 'fail', run: async () => {
      D.pill(BAD, 'bad', 'failed'); D.lit(BAD); D.cls('#k3', 'lit'); D.count('#k3v', 1);
      D.toast('1 record needs attention', 'bad'); D.msg('1 failing');
      /* the rest of the queue keeps moving — the tool did not stop the world */
      for (const id of ROWS.slice(5)) { D.pill(id, 'ok', 'passed'); await D.sleep(160); }
  }, gap: 400 },

  { name: 'detail', run: async () => {
      D.drawer(true); await D.sleep(2200);                  // hold: the drawer is the payload
  }},

  { name: 'fixed', run: async () => {
      D.q('#dOk').style.display = 'block';
      D.busy(true); D.msg('applying fix…'); await D.sleep(1500);
      D.pill(BAD, 'ok', 'passed'); D.lit(BAD, false); D.busy(false);
      D.text('#k3v', '0'); D.cls('#k3', 'lit', false);
      await D.sleep(600); D.drawer(false); D.cta('Run check'); D.msg(`all ${ROWS.length} passing`);
      D.toast('All records passing', '', 0);
  }},
], () => {   /* reset: put every mutable thing back */
  D.stage.className = 'stage';
  ROWS.forEach(id => { D.pill(id, '', 'queued'); D.lit(id, false); });
  D.cls('#k2', 'lit', false); D.cls('#k3', 'lit', false);
  D.text('#k1v', '0'); D.text('#k2v', '0'); D.text('#k3v', '0'); D.text('#k4v', '0');
  D.q('#dOk').style.display = 'none'; D.q('#toast').className = 'toast';
  D.cta('Run check'); D.msg('idle'); D.caption(null);
});
D.replay();
