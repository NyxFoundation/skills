/* A conference opener. Big screen, no narration, hands the room back to the speaker.
   Three acts:
     they trade  →  the market turns and one of them REWRITES ITSELF  →  an attack
     that no parameter change defends against.
   The middle act is the product; the third is the reason the competition exists. The
   bottom-left panel is "what an agent is thinking", used once for the honest agent's
   self-improvement and once for the adversary's search. */

const ROSTER = ["adaptive-arb","arb-bot","basis-arb","bench-max","clean-arb","cross-venue-arb",
  "discovery-arb-verify","discovery-arb","exploit-hunter","flash-arb","levered-long","liquidator",
  "lp-mint","lp-provider","lst-carry","market-launcher","market-taker","max-profit-arb","multi-arb",
  "my-arb","noop","peg-arb","random","redemption-arb","simple-rule","sp-underwriter","starter-template",
  "stat-arb","trap-launcher","trove-manager","vault-keeper","venue-arb"];
/* Two baselines sit out by design — and exploit-hunter sits out because it is
   reading. That silence is the whole setup for the reveal, so it is enforced here
   rather than left to the random draw. */
const QUIET = new Set(['noop', 'starter-template', 'exploit-hunter']);
const VENUES = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6'];
const ACTION = ['swap · uniswap', 'swap · balancer', 'swap · curve', 'aaveSupply', 'aaveBorrow',
  'mintLiquidity', 'gmxIncrease', 'lstDeposit', 'liquityRedeem', 'stableSwap', 'collectFees'];

let seed = 101;
const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
const pick = a => a[Math.floor(rnd() * a.length)];
const chip = n => document.querySelector(`.chip[data-name="${n}"]`)?.id;
const HUNTER = () => chip('exploit-hunter');
const KEEPER = () => chip('vault-keeper');

/* shots, in map coordinates: [x1,y1,x2,y2]. The camera solves for the scale. */
const SHOT = {
  hunter: [10, 78, 720, 336],      /* exploit-hunter is row 4 of the left block, y≈174 */
  vault:  [1108, 452, 1596, 620],  /* LeakyVault, bottom of the contract column */
  keeper: [10, 452, 720, 620],     /* vault-keeper is row 15, y≈570 */
};

let blockNo = 601, pnl = {}, INJECT = [], crash = false, running = false, OWNED = new Set();

/* A small price process, so the charts are shapes rather than decoration: the fair
   price drifts (hard, downward, during the crash), each venue lags it by a gap, and
   the gap decays every block because that is what the arbitrageurs are for. */
let fair = 3000, gap = { uni: 0, bal: 0, crv: 0 };
const usd = v => '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const bal = n => 25000 + (pnl[n] || 0);
function stepPrices() {
  fair *= 1 + (crash ? -0.0018 : 0.0002) + (rnd() - 0.5) * 0.0011;
  for (const k of ['uni', 'bal', 'crv'])
    gap[k] = gap[k] * 0.55 + (rnd() - 0.5) * (crash ? 0.019 : 0.0045);
  const px = { uni: fair * (1 + gap.uni), bal: fair * (1 + gap.bal), crv: fair * (1 + gap.crv) };
  D.stat('v1', usd(px.uni)); D.stat('v2', usd(px.bal)); D.stat('v3', usd(px.crv));
  D.plot('chPrice', { fair, ...px });
  D.text('#chPriceNow', 'fair ' + usd(fair));
  D.plot('chBal', { w1: bal('venue-arb'), w2: bal('multi-arb'), w3: bal('liquidator'),
                    keeper: bal('vault-keeper'), hunter: bal('exploit-hunter') });
  D.text('#chBalNow', 'hunter ' + usd(bal('exploit-hunter')));
}

async function runBlock() {
  if (!running) return;
  const mine = D.gen(), sp = D.speed();
  const n = crash ? 11 + Math.floor(rnd() * 6) : 6 + Math.floor(rnd() * 5);
  const senders = [];
  while (senders.length < n) {
    const a = pick(ROSTER);
    if (!QUIET.has(a) && !senders.includes(a)) senders.push(a);
  }
  const txs = INJECT.concat(senders.map(a => ({ name: a, what: pick(ACTION),
    fee: (0.8 + rnd() * 7).toFixed(1), target: pick(VENUES), evil: false })));
  INJECT = [];
  txs.sort((x, y) => Number(y.fee) - Number(x.fee));

  D.slot(1900 / sp); D.text('#memHd', 'BLOCK ' + (blockNo + 1)); D.memClear();
  txs.slice(0, 6).forEach((t, i) => D.mem(D.memRows()[i],
    { what: t.what, who: t.name, fee: t.fee + ' gwei', evil: t.evil }));
  D.text('#memMore', txs.length > 6 ? `+ ${txs.length - 6} more from the same block` : ' ');

  txs.forEach((t, i) => {
    const c = chip(t.name); if (!c) return;
    D.cls(c, 'send', true); D.later(() => D.cls(c, 'send', false), 500 / sp);
    D.later(() => { if (D.gen() === mine) D.tx(c, 'chain', { midX: 520, from: 'right', to: 'left',
      ms: 620, colour: t.evil ? 'var(--hack)' : 'var(--agent)', r: t.evil ? 6 : 3.2 }); }, i * 45 / sp);
  });

  await D.sleep(760 / sp);
  if (D.gen() !== mine || !running) return;

  blockNo += 1; D.block(blockNo); D.epoch(blockNo - 360);
  const reverts = Math.max(0, Math.round(txs.length * (crash ? 0.26 : 0.12)));
  txs.slice(0, 6).forEach((t, i) => D.mem(D.memRows()[i],
    { state: i >= txs.length - reverts ? 'rev' : 'mined',
      fee: (i >= txs.length - reverts ? 'idx ' + i + ' ✗' : 'idx ' + i + ' ✓'), evil: t.evil }));
  txs.slice(0, txs.length - reverts).forEach((t, i) => D.later(() => {
    if (D.gen() === mine) D.tx('chain', t.target, { midX: 1180, from: 'right', to: 'left',
      ms: 560, colour: t.evil ? 'var(--hack)' : 'var(--accent2)', r: t.evil ? 6 : 3.2 });
  }, i * 40 / sp));

  D.tel('c1', String(txs.length));
  D.tel('c2', Math.round(reverts / txs.length * 100) + '%');
  senders.slice(0, 5).forEach(a => {
    const c = chip(a); if (!c || OWNED.has(a)) return;
    pnl[a] = (pnl[a] || 0) + Math.round((rnd() - (crash ? 0.42 : 0.46)) * 220);
    D.pnl(c, (pnl[a] >= 0 ? '+' : '') + pnl[a], pnl[a] >= 0 ? 'gain' : 'loss');
  });
  stepPrices();

  D.later(runBlock, 1150 / sp);
}
/* idempotent: go(n) replays every earlier beat and each asks for traffic */
const traffic = on => { if (on && running) return; running = on; if (on) runBlock(); };

/* venue-arb after its rewrite: fewer trades, and they work */
let revised = false;

D.define([

  /* 0 — ONE. The whole grammar in a single transaction. */
  { name: 'one', run: async () => {
      D.wipeWires(); D.block(601); D.epoch(241);
      VENUES.concat('v7').forEach(v => D.wire('chain', v, { from: 'right', to: 'left', midX: 1180 }));
      ROSTER.forEach(n => D.wire(chip(n), 'chain', { from: 'right', to: 'left', midX: 520 }));
      const va = chip('venue-arb');
      D.up(va); D.up('v1'); D.lit(va); D.lit('v1'); D.focus(true); D.text('#nAg', '1');
      D.msg('one wallet · one block');
      D.big('One wallet. One block. One trade.');
      await D.sleep(1200);
      D.mem('t1', { what: 'swap · uniswap', who: 'venue-arb', fee: '3.2 gwei' });
      D.slot(1900);
      await D.tx(va, 'chain', { midX: 520, from: 'right', to: 'left', ms: 950, r: 5 });
      D.busy(true); await D.sleep(420); D.busy(false);
      D.block(602); D.mem('t1', { state: 'mined', fee: 'idx 0 ✓' });
      await D.tx('chain', 'v1', { midX: 1180, from: 'right', to: 'left', ms: 850, r: 5 });
      pnl['venue-arb'] = 412; D.stat('v1', '$2,951.80', 'moved'); D.pnl(va, '+412', 'gain');
      await D.sleep(900);
  }},

  /* 1 — THIRTY-TWO. */
  { name: 'swarm', run: async () => {
      D.big(null); D.focus(false); D.lit(chip('venue-arb'), false); D.lit('v1', false);
      D.msg('funding 32 wallets');
      VENUES.forEach(v => D.up(v));
      for (let i = 0; i < ROSTER.length; i++) { D.up(chip(ROSTER[i])); D.text('#nAg', String(i + 1)); await D.sleep(38); }
      D.big('Thirty-two of them. Every two seconds.');
      D.feed('every wallet reads the <b>same</b> observation, one block late');
      traffic(true);
      await D.sleep(1800);
      D.big(null);
  }, gap: 250 },

  /* 2 — the market turns, and it costs them. */
  { name: 'turn', run: async () => {
      traffic(true); crash = true;
      D.msg('the field is losing money');
      D.feed('three venues out of line at once · <b>the gap is not a secret</b>');
      D.stat('v5', '31 bps', 'moved'); D.stat('v6', '$0.9942', 'moved');
      D.caption('They can all see the same gap — and most of them are now paying more than it is worth.');
      await D.sleep(2600);
      D.caption(null);
  }, gap: 250 },

  /* 3 — THE PRODUCT. The strategy is handed its own evidence and rewrites itself. */
  { name: 'revise', run: async () => {
      traffic(true); crash = true;
      const va = chip('venue-arb');
      D.lit(va); D.msg('revision opportunity · venue-arb');
      D.mind({ title: 'STRATEGY REVISION', who: 'venue-arb · v1', badge: 'reading', state: '',
               left: 'EVIDENCE HANDED TO THE MODEL', right: 'WHAT IT DECIDED', evil: false });
      D.big('Every sixty blocks, a strategy is handed what it did — and may rewrite itself.');
      await D.sleep(1900); D.big(null);

      D.ev(1, 'market history, blocks 602..662 <span class="d">(60 observed)</span>');
      await D.sleep(240);
      D.ev(2, '  curve:WETH     <span class="w">-8.1 / 274.9 / 180.4</span> bps   over 5/10/25/50: <span class="h">59/58/57/47</span>');
      await D.sleep(220);
      D.ev(3, '  uniswap:WETH  <span class="w">-33.1 / 323.8 / 224.9</span> bps   over: <span class="h">58/54/48/42</span>');
      await D.sleep(220);
      D.ev(4, '                 round trip cost up to <span class="e">62.2 bps</span> on curve');
      await D.sleep(320);
      D.ev(5, 'transactions since the last revision');
      await D.sleep(220);
      D.ev(6, '  18 sent = <span class="k">11 succeeded</span> + <span class="e">5 mined-but-reverted</span> + 2 never mined');
      await D.sleep(220);
      D.ev(7, '  mean gap it fired on <span class="h">41.2 bps</span> <span class="d">(4 cheap, 14 rich)</span>');
      await D.sleep(220);
      D.ev(8, '  marked value across the 13 settled trades  <span class="e">-182.40 USDC</span>');
      await D.sleep(500);

      D.mind({ badge: 'deciding', state: '' });
      D.quote('“The gap was real and I kept taking it. The round trip on curve costs 62 bps and I was firing at 41. Raise the margin, not the size.”');
      await D.sleep(1500);
      D.param(1, 'EDGE_BPS', '30', '68'); await D.sleep(420);
      D.param(2, 'SIZE_BPS', '2500', '1400'); await D.sleep(520);
      D.stamp('✓ cheatcode check passed · compiled · installed as v2');
      D.mind({ badge: 'v2 installed', state: 'on', who: 'venue-arb · v2' });
      revised = true; D.lit(va, false);
      D.caption('It trades a third as often now, and it stops paying for the gap it cannot cover.');
      await D.sleep(1700); D.caption(null);
  }, gap: 250 },

  /* 4 — THE BOMB, shown to the room and to nobody in the simulation. */
  { name: 'bomb', run: async () => {
      traffic(true); crash = true;
      D.msg('an agent deploys its own contract');
      const vk = KEEPER(); D.lit(vk);
      INJECT.push({ name: 'vault-keeper', what: 'rawTx · contract creation', fee: '6.5', target: 'v7' });
      D.caption('Deployment is permissionless. vault-keeper ships its own vault and funds it.');
      await D.sleep(1600);
      D.up('v7'); D.stat('v7', '$10,000', 'moved'); D.tag('v7', 'warn', 'unverified');
      pnl['vault-keeper'] = -10000; D.pnl(vk, '−10,000', 'loss'); OWNED.add('vault-keeper');
      D.feed('the vault holds <b>$10,000</b> · its deposit and withdraw are correct');
      await D.sleep(700);
      D.lit(vk, false); D.lit('v7'); D.tag('v7', 'bad', 'rescue() ungated');
      D.big('Its rescue() is not gated. Nobody in this simulation knows that yet.');
      await D.sleep(2000); D.big(null);
  }, gap: 250 },

  /* 5 — THE ATTACK. The same panel, the other kind of reasoning. */
  { name: 'drain', run: async () => {
      traffic(true); crash = true;
      const eh = HUNTER();
      D.lit('v7', false); D.lit(eh);
      D.msg('one wallet has not traded');
      D.big('One wallet has not sent a single transaction. It has been reading.');
      await D.sleep(2300);

      D.big(null); D.speed(0.3); D.focus(true);
      D.cls(eh, 'evil', true); D.glyph(eh, 'eye'); D.cls('v7', 'lit', true);
      D.camTo(SHOT.hunter, 1000);
      D.mindReset();
      D.mind({ title: 'BYTECODE PROBE', who: 'exploit-hunter', badge: 'reading', state: '',
               left: 'WHAT IT CAN SEE', right: 'WHAT IT TRIED', evil: true });
      D.ev(1, 'eth_getCode <span class="w">0x8A79…1f04E</span> → <span class="h">2,118 bytes</span>');
      await D.sleep(420);
      D.ev(2, '  no ABI. no source. the registry says <span class="d">kind: unknown</span>.');
      await D.sleep(460);
      D.ev(3, 'selectors recovered from the dispatcher');
      await D.sleep(300);
      D.ev(4, '  <span class="d">b6b55f25</span>  deposit(uint256)');
      await D.sleep(230);
      D.ev(5, '  <span class="d">2e1a7d4d</span>  withdraw(uint256)');
      await D.sleep(230);
      D.ev(6, '  <span class="d">d8ccd0f3</span>  <span class="x">rescue()</span>  <span class="d">← takes no arguments</span>');
      await D.sleep(450);

      /* the reasoning is read while the probes are already in the air — sequencing
         them one after the other put four seconds of nothing between two ideas */
      D.quote('“A function that takes no arguments and moves value is the one an author forgets to gate. Try it behind Exploiter — atomic, so a wrong guess costs gas and nothing else.”');
      await D.txFail(eh, 'chain', { midX: 520, from: 'right', to: 'left', ms: 850, r: 5, raw: true });
      D.param(1, 'deposit(uint256)', '', 'reverted');
      await D.txFail(eh, 'chain', { midX: 520, from: 'right', to: 'left', ms: 850, r: 5, raw: true });
      D.param(2, 'withdraw(uint256)', '', 'reverted');
      await D.sleep(350);

      D.memClear();
      D.mem('t1', { what: 'rawTx · Exploiter(rescue)', who: 'exploit-hunter', fee: '9.9 gwei', evil: true });
      D.camTo(D.MAP, 900);
      await D.tx(eh, 'chain', { midX: 520, from: 'right', to: 'left', ms: 1000, colour: 'var(--hack)', r: 7, raw: true });
      D.camTo(SHOT.vault, 900);
      await D.tx('chain', 'v7', { midX: 1180, from: 'right', to: 'left', ms: 850, colour: 'var(--hack)', r: 7, raw: true });
      D.mem('t1', { state: 'mined', fee: 'idx 0 ✓', evil: true });
      D.tag('v7', 'bad', 'drained'); D.stat('v7', '$0', 'loss');
      D.stamp('rescue() → 10,000 USDC out');
      D.mind({ badge: 'drained', state: 'bad' });
      /* the money leaves as a stream, not as two dots */
      for (let i = 0; i < 5; i++) {
        D.tx('v7', 'chain', { midX: 1180, from: 'left', to: 'right', ms: 1000, colour: 'var(--hack)', r: 6.5 - i * 0.6, raw: true });
        await D.sleep(130);
      }
      D.camTo(D.MAP, 800);
      await D.tx('chain', eh, { midX: 520, from: 'left', to: 'right', ms: 900, colour: 'var(--hack)', r: 8, raw: true });
      pnl['exploit-hunter'] = 10000; D.pnl(eh, '+10,000', 'gain'); OWNED.add('exploit-hunter');

      D.lit(KEEPER()); D.camTo(SHOT.keeper, 800);
      D.caption('vault-keeper goes to withdraw. There is nothing left to withdraw.');
      await D.txFail(KEEPER(), 'chain', { midX: 520, from: 'right', to: 'left', ms: 850, r: 5, raw: true });
      D.caption(null);

      D.speed(1); D.camTo(D.MAP, 1000); D.focus(false);
      D.lit('v7', false); D.lit(eh, false); D.lit(KEEPER(), false);
      D.msg('1 contract drained');
      await D.sleep(500);
  }, gap: 250 },

  /* 6 — the close. */
  { name: 'close', run: async () => {
      traffic(true); crash = false;
      D.telNote(true);
      D.feed('<b>nothing was broken.</b> The contract did exactly what it was written to do');
      D.big('It rewrote its own strategy. It could not rewrite someone else\u2019s contract.');
      await D.sleep(2500);
      D.big('Nothing was broken. The contract did exactly what it was written to do.');
      await D.sleep(2600);
  }, gap: 250 },

], () => {
  D.newGen(); running = false; crash = false; INJECT = []; seed = 101; blockNo = 601; pnl = {}; OWNED = new Set();
  revised = false;
  D.stage.className = 'stage'; D.speed(1); D.focus(false); D.camTo(D.MAP, 0);
  ROSTER.forEach(n => { const c = chip(n); D.up(c, false); D.lit(c, false); D.cls(c, 'evil', false); D.pnl(c, '\u00b7'); });
  D.glyph(chip('exploit-hunter'), 'base');
  VENUES.concat('v7').forEach(v => { D.up(v, false); D.lit(v, false); });
  D.memClear(); D.wipeWires(); D.text('#memHd', 'THIS BLOCK'); D.mindReset();
  D.stat('v1', '$3,000.00'); D.stat('v2', '$3,000.00'); D.stat('v3', '$3,000.00');
  D.stat('v4', '42.0%'); D.stat('v5', '0 bps'); D.stat('v6', '$1.0000'); D.stat('v7', '$0');
  D.tag('v7', '', 'unknown');
  fair = 3000; gap = { uni: 0, bal: 0, crv: 0 };
  D.chart('chPrice', ['fair', 'uni', 'bal', 'crv']);
  D.chart('chBal', ['w1', 'w2', 'w3', 'keeper', 'hunter']);
  D.text('#chPriceNow', '\u2014'); D.text('#chBalNow', '\u2014');
  D.tel('c1', '0'); D.tel('c2', '0%');
  D.epoch(0); D.telNote(false);
  D.text('#nAg', '0'); D.text('#blkNo', 'block 0'); D.text('#telBlk', 'block 0');
  D.feed('waiting for the first block'); D.msg('idle'); D.big(null);
  const sb = D.q('#slotBar'); if (sb) { sb.style.transition = 'none'; sb.style.width = '0%'; }
});
D.replay();
