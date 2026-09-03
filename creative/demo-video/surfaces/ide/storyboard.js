/* Six beats: idle → run → first easy win → second pane → the real problem →
   the fix, verified. Replace the copy, keep the shape. Every run() must be
   replayable from reset(). */
D.define([
  { name: 'idle', run: async () => { D.prompt({ user: 'project' }); } },

  { name: 'run', run: async () => {
      D.busy(true); D.msg('analyzing…');
      await D.type('#cmd', 'tool analyze .'); await D.sleep(300); D.endPrompt();
      D.tline('<span class="a">→</span> reading <span class="h">2</span> files'); await D.sleep(400);
      D.tline('<span class="a">→</span> done <span class="d">(1.8s)</span>'); D.busy(false);
  }},

  { name: 'warn', run: async () => {
      D.msg('1 warning'); D.scrollTo('mainPre', 'W1', 200); D.lit('W1');
      D.tline('<span class="w">●</span> warning at <span class="h">main.ext:2</span>');
      D.count('num', 1234, v => ' −' + v.toLocaleString() + ' gas'); D.problems(0, 1);
  }},

  { name: 'spec', run: async () => { D.cls(D.stage, 'split'); D.info(0); await D.sleep(800); } },

  { name: 'error', run: async () => {
      D.lit('E1'); D.lit('S1'); D.cls('#peek1', 'open'); D.info(1);
      await D.sleep(300); D.crossLink('S1', 'E1');
      D.problems(1, 1); D.msg('1 error · fix available');
  }, gap: 500 },

  { name: 'fix', run: async () => {
      await D.sleep(2000);                                   // hold: let the viewer read the peek
      D.cls('#peek1', 'open', false); D.unlink();
      D.cls('#INS', 'open'); D.renumber('mainPre', 'INS', 1);
      await D.sleep(300); await D.type('#typed', 'inserted line of code', 60);
      D.lit('INS'); D.lit('E1', false);
      D.busy(true); D.msg('re-checking…'); await D.sleep(1400); D.busy(false); D.msg('all good'); D.info(2);
      D.cls('#p2', 'gone'); D.problems(0, 1);
      await D.sleep(800); D.panel('problems');
  }},
], () => {   /* reset: put every mutable thing back */
  D.stage.className = 'stage'; D.html('#term', ''); D.unlink();
  D.qa('.ln.lit').forEach(e => e.classList.remove('lit'));
  D.cls('#peek1', 'open', false);
  if (D.q('#INS').classList.contains('open')) { D.cls('#INS', 'open', false); D.renumber('mainPre', 'INS', -1); }
  D.text('#typed', ''); D.info(0); D.msg('idle'); D.text('#num', ''); D.problems(0, 0);
  D.cls('#p2', 'gone', false); D.panel('term'); D.q('#mainPre').scrollTop = 0; D.caption(null);
});
D.replay();
