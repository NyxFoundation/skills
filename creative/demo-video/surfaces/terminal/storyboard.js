/* Six beats: idle → the command → the plan appears → work streams in →
   the finding (the reason anyone would run this) → the result card.
   Replace the copy, keep the shape. Every run() must be replayable from reset(). */
D.define([
  { name: 'idle', run: async () => { D.prompt({ user: '~/work/project' }); } },

  { name: 'cmd', run: async () => {
      await D.type('#cmd', 'tool run --all'); await D.sleep(400); D.endPrompt();
      D.busy(true); D.msg('starting…');
      D.tline('<span class="d">tool 0.4.1 · 8 workers · cache warm</span>');
  }},

  { name: 'plan', run: async () => {
      D.cls(D.stage, 'split'); await D.sleep(600);
      D.step('t1', 'run'); D.msg('1/4 running'); D.count('num', 12400);
  }},

  { name: 'work', run: async () => {
      D.tline('<span class="a">→</span> scanning <span class="h">128</span> files');
      await D.sleep(450); D.tline('  <span class="d">src/…            94 files   0.7s</span>');
      await D.sleep(300); D.tline('  <span class="d">packages/…       34 files   0.5s</span>');
      await D.sleep(400); D.step('t1', 'ok', '1.2s'); D.step('t2', 'run'); D.msg('2/4 running');
      D.tline(D.barline('b1', 'building index'));
      await D.sleep(120); D.fill('b1', 100);
      await D.sleep(1000); D.step('t2', 'ok', '0.9s'); D.step('t3', 'run'); D.msg('3/4 running');
      D.tline('<span class="a">→</span> checking <span class="h">41</span> rules');
      await D.sleep(400); D.tline('  <span class="k">✓</span> <span class="d">38 rules clean</span>');
      await D.sleep(350); D.tline('  <span class="d">2 rules skipped (no coverage)</span>');
  }},

  { name: 'finding', run: async () => {
      D.tline('<span class="w">●</span> <span class="h">src/handler.ts:82</span> <span class="d">— the one thing worth showing</span>');
      await D.sleep(900);
      D.tline('<div class="box kv">' +
              '<span class="d">why</span>  one sentence a practitioner would nod at<br>' +
              '<span class="d">fix</span>  <b>tool fix --id 3</b></div>');
      D.step('t3', 'bad', '2.1s'); D.msg('1 finding');
  }, gap: 500 },

  { name: 'result', run: async () => {
      await D.sleep(1800);                                   // hold: let the viewer read the box
      D.step('t3', 'ok', '2.1s'); D.step('t4', 'run');
      D.tline('<span class="a">→</span> applying fix <span class="d">(1 file)</span>');
      await D.sleep(700); D.tline('  <span class="d">src/handler.ts  +3 −1</span>');
      await D.sleep(500); D.step('t4', 'ok', '0.4s'); D.busy(false); D.msg('done');
      D.tline('<span class="a">→</span> re-running <span class="h">41</span> rules');
      await D.sleep(700);
      D.tline('<span class="k">✓</span> all checks pass <span class="d">(4.6s)</span>');
      D.tline('<span class="d">  41 rules · 128 files · 1 fix applied · 0 findings left</span>');
      D.text('#big', '4.6s'); D.text('#m1', '1 fixed'); D.text('#m2', '128 files'); D.card(true);
  }},
], () => {   /* reset: put every mutable thing back */
  D.stage.className = 'stage'; D.html('#term', ''); D.unlink();
  ['t1', 't2', 't3', 't4'].forEach(id => D.step(id, null, ''));
  D.card(false); D.text('#big', '—'); D.text('#m1', '—'); D.text('#m2', '—');
  D.msg('idle'); D.text('#num', '0'); D.caption(null);
});
D.replay();
