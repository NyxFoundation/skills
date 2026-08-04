---
name: arch-diagram
description: Generate a STATIC architecture/system diagram as a PNG asset using a Python (matplotlib) script stored in figures/, for slides that need one still figure — system architectures, attack-moment snapshots, protocol topologies, infra dependency maps. The style is "boxless architecture diagram" — floating icon+label entities, plain-text section headers, right-angle wiring with filled arrowheads, dashed ghost outlines for absent actors, and strict color semantics (red=attack path only). Trigger whenever the user asks for: "静的アーキ図", "アーキテクチャ図を生成/修正", "Python で図を作って", "matplotlib の図", "kelp_arch みたいな図", or when an existing figures/*.py-generated PNG needs a visibility/layout fix. NOT for morphing multi-phase animations (that is animated-concept-slide) and not for simple flowcharts a Mermaid block can express.
---

# Static architecture diagram (matplotlib → PNG)

One Python script in `figures/` renders one PNG into `public/images/`, which a slide
embeds with `<img src="/images/<name>.png" class="max-h-[440px] w-auto object-contain" />`.

**Reference implementation: `figures/kelp_arch.py`** (KelpDAO × LayerZero 1-of-1 DVN
事件, used by `slides/SL08b.md`). Read it before writing a new diagram — it encodes the
icon library, the primitives, and every layout decision below. Other live examples:
`figures/poe_arch.py`, `figures/scope_gap_chart.py`.

## When this pattern wins

- The slide needs **one still figure**: an architecture snapshot ("the moment of
  compromise"), a topology, a dependency map — no time progression on screen.
- The figure needs assets Slidev/Mermaid can't compose well: brand logos as node icons,
  precise routed wiring, per-entity color states.

Use something else when:
- States progress over time on the slide → `animated-concept-slide` (Vue + SVG phases).
- A plain flowchart/sequence suffices → Mermaid block in the slide.

## File & run conventions (hard rules)

- Script lives at **`figures/<name>.py`** — NEVER only in the session scratchpad
  (scratchpads die with the session; this rule exists because kelp_arch.py was nearly
  lost that way). Output goes to **`public/images/<name>_static.png`** via an absolute
  `OUT` path constant.
- Run with: `uv run --with matplotlib python3 figures/<name>.py`
  (system python has no matplotlib; uv is on PATH). Pillow for crop checks:
  `uv run --with pillow python3 -c ...`.
- Header comment in every script: how to regenerate + which slide consumes it.
- JP font: resolve from candidates `["Noto Sans CJK JP", "Noto Sans JP", "IPAexGothic",
  ...]` against `fm.fontManager.ttflist` (copy the snippet from kelp_arch.py).
  Ignore `findfont: Failed to find font weight` warnings — render is fine; always
  verify by eye, not by warnings.

## Canvas & font-size math (the #1 visibility trap)

Baseline geometry (copy from kelp_arch.py): `figsize=(13.4, 6.2), dpi=200`,
`xlim(0, 1260)`, ylim spanning ≈ 480-500 units, `bbox_inches="tight"`.

The deck's readability floor is **14 px at the 1280×720 canvas**. A PNG shown with
`max-h-[440px]` is scaled to `440/H_img` of its pixel height, and matplotlib text is
`fontsize/72*dpi` pixels tall. With this baseline (H_img ≈ 1200-1260 after tight crop):

```
canvas_px ≈ fontsize_pt * (dpi/72) * (440 / H_img) ≈ fontsize_pt * 1.0
```

→ **fontsize in pt ≈ resulting canvas px.** Floors: entity labels ≥ 15, sub-labels /
edge labels ≥ 13, section headers 15 (monospace bold), callout code 14, drain/大数字
13.5-16. Anything ≤ 12 pt is unreadable when projected. If the layout gets taller
(H_img grows), fonts must grow proportionally — recompute, don't eyeball.

## Design vocabulary (boxless style)

- **No enclosing boxes, no legends.** Entities are floating icon + bold label
  (+ optional sub-label) via `entity()`. Prefer ZERO section headers: fold scope into
  entity labels ("Karak RPC #1" not a "KARAK L2 RPC" header over "RPCサーバー #1"),
  and never restate an entity label as a header ("ETHEREUM" over "Ethereum Contract"
  is noise). `section()` exists only for grouping info that genuinely fits nowhere
  else — in practice a boundary band (below) usually does that job better.
- **Vendor/system boundary band** — the one legitimate "area" element, distinct from
  entity boxes: a large light-tinted dashed rounded rect (fill `#6366f1` alpha 0.05,
  edge `#94a3b8` dashed, zorder 1 behind everything) around a subsystem, with a brand
  logo + name at its top-left INSIDE corner. Use it to attribute a mechanism to a
  vendor (LayerZero around the DVN tier). Route flows so they CROSS the band's edges —
  the crossings say "messages/attacks pass through this layer". Any `on_line` label
  bbox sitting on the band must use the band's composited color (`#f7f7fe`), not
  white, or it shows as a white rectangle.
- **Icon shape = actor role, color = state.** Different roles must get different
  silhouettes (shield = verifier/DVN, server stack = RPC/infra, person = user, brand
  logo = contract). If two different roles share an icon, the viewer reads them as one
  tier — the shape channel is doing semantic work, don't waste it.
- **Wiring is right-angle** (vertical/horizontal only), filled arrowheads
  (`FancyArrowPatch(arrowstyle="-|>")` — never open/hand-drawn heads). Straight runs
  with `straight()`, multi-bend with `elbow_path()`.
- **Ghost = absent**: dashed outline icon (`ghost=True`), no fill, no connector — the
  *absence of a line* says "not responding". Ghost outline `#94a3b8`, but ghost **text**
  darker `#64748b` so it survives projection.
- **Color semantics** (fixed): red `#dc2626` = attack path / compromised / tampered
  ONLY; amber `#d97706` = degraded-but-alive sole path; gray = healthy/neutral;
  ghost = absent. **A victim that behaved correctly stays neutral-colored** — show
  damage with an explicit red loss label (e.g. `−116,500 rsETH（$292M）流出`) beside it,
  never by tinting the victim.
- **Logos as icons**: brand logos from `public/logos/` (fetch recipe in CLAUDE.md
  「実ロゴの取得」; use ≥256px source or it pixelates). A logo can BE the entity icon
  (Karak/Ethereum contracts) or brand a boundary band's corner (LayerZero). A logo
  adjacent to a label is READ as that label's subject — never park brand X's logo
  next to element Y (the original bug: KelpDAO's logo beside "ETHEREUM" read as an
  Ethereum logo). If a brand has no natural anchor in the diagram, leave it to the
  slide title. **Never hard-code `zoom` against a logo's pixel size** — compute it:
  `zoom = min(TARGET_H/h, MAX_W/w)` from `mpimg.imread(...).shape` (see
  figures/scope_gap_chart.py). A fixed zoom silently doubles the logo when someone
  swaps the file for a higher-res version — this happened.

## Layout rules distilled from iteration

1. **Lines must never strike through text.** Where a trunk line passes an entity's
   labels, give the labels an opaque white bbox (`entity(..., on_line=True)`) so the
   label *interrupts* the line — the standard "label sits on the wire" idiom.
2. **Merge parallel feeds into one trunk.** N sources → short verticals → one
   horizontal collector → junction dot (`Circle` r≈5) → single arrow into the target's
   edge. Two parallel verticals flanking a label column reads as clutter.
3. **Callout above its target, vertical leader — and boxless like everything else.**
   A config/code callout is a plain monospace text line (no filled panel, no border —
   a boxed callout is the one element that will look pasted-on next to floating
   entities). Highlight only the fatal token: red + larger + a thin red outline around
   that token alone, with the vertical dashed leader dropping from directly beneath it
   onto the target node's top edge. Ambiguous diagonal/elbow leaders get misread (the
   original bug: the arrow appeared to point at a logo).
4. **Cluster a resource pool under its consumer** (RPC servers under the DVN that polls
   them) so ownership is spatial, and **route colored wiring so it never encloses
   unrelated actors** — put the wired nodes adjacent to the trunk, ghosts outside the
   wiring's hull.
5. **Keep section headers out of wiring corridors** (the leader's x-lane), at the left
   edge of the row they head, vertically clear of other rows' labels.
6. Big-picture symmetry: main flow on one horizontal line (`MAIN_Y`), the hero node's
   x (`DVN_X`-style constant) shared by callout, leader, trunk, junction — one vertical
   axis of causality. Name these as constants; don't scatter magic numbers.

## One-shot recipe (follow this order for a new diagram)

Do NOT sketch freely and fix later — the reference quality comes from deciding in
this order, before writing coordinates:

1. **Copy `figures/kelp_arch.py`** as the starting file. Keep the imports, font
   resolution, palette, `entity()/section()/straight()/elbow_path()/icon_*` primitives
   and the figsize/xlim/ylim baseline verbatim. You are replacing the content below
   the `座標定数` marker, not the machinery.
2. **Inventory actors and assign each a role-shape**: user→person, contract→brand
   logo, verifier→shield, server/infra→server stack. New role → new silhouette
   (design it in the icon library section, ~radius s=20-24). No two roles share a
   shape.
3. **Assign states**: healthy/neutral (gray), sole-degraded-path (amber), attack path
   (red), absent (ghost dashed), victim (neutral + red loss label). Every color must
   be justified by a state, not by decoration.
4. **Fix the two axes**: `MAIN_Y` for the single left→right main flow; `HERO_X` for
   the hero node — callout, leader, trunk, junction all share this x. Write them as
   constants first.
5. **Place the supporting cast around those axes**: resource pool clustered under its
   consumer; ghosts flanking OUTSIDE any colored wiring; boundary band around exactly
   the subsystem a vendor owns, with its logo top-left inside.
6. **Wire**: right-angle only, filled arrowheads, merge parallel feeds into one trunk
   with a junction dot, callout leader = vertical drop from beneath the fatal token.
   Any line crossing a label → `on_line=True` with the correct backing color.
7. **Set font sizes from the table** (pt ≈ canvas px): entity 15 / sub 13.5 / edge
   label 13 / callout 14 / loss label 13.5. Never below 13.
8. Only then render and run the verification loop below. One or two crop-zoom checks
   should be cosmetic confirmation, not layout surgery — if the render needs
   structural fixes, a step above was skipped.

## Verification loop (mandatory)

1. `uv run --with matplotlib python3 figures/<name>.py`
2. `Read` the output PNG. Check: font floor, no line-through-text, arrowheads land on
   node edges, color semantics, no enclosure misreads, headers unambiguous.
3. Crop-zoom the risky region (junctions, arrow landings) with pillow and `Read` it.
4. Slide-level check per CLAUDE.md §11: `bun run build` → SPA server on :4002 →
   Firefox headless screenshot of the slide → `Read`: no overflow, no collision with
   sources footer / Merkle logo.
5. Update the slide's speaker-notes 【概念図の読み方】 to match the final geometry, and
   note the generating script path there.

## Examples

`examples/` に、実際に PR 原稿へ載せた対の図の生成スクリプトが入っている（Aladdin Security
共同研究の記事用）。ゼロから書き始める前にこの2本を読むと、上のレシピが具体形でわかる。

| ファイル | 何の図か |
|---|---|
| `examples/problem_translation_wall.py` | 問題図。「具体構造ごとに証明をゼロから独立探索していて、定理の在庫が構造の数だけ膨張する」状態 |
| `examples/solution_category_theory.py` | 解決図。抽象定理を圏論的中間表現として一度だけ証明し、各構造へ降ろす |

読みどころは figure そのものより**冒頭コメントの改訂経緯**。初版は「自然言語→Lean 命題の翻訳の壁を
圏論が埋める」という筋書きだったが、社内研究メモがそれを明示的に否定していた（formalization gap は
圏論化でも消えない）ため、図の主張ごと描き直している。**図は主張であり、裏が取れない主張は描かない。**

実行するときは冒頭の `OUT` を自分のリポジトリの `public/images/` に書き換える。

## Pitfalls

| 失敗 | 対処 |
|---|---|
| スクリプトを scratchpad にだけ置く | `figures/` にコミット。出力先は `public/images/` 絶対パス |
| フォント 11-12pt (旧 kelp_arch の敗因) | 上の換算式で 13pt 床、主要ラベル 15pt |
| 配線がラベルを貫通 | `on_line=True` 白 bbox か、合流トランクに再配線 |
| リーダー線の着地が曖昧 | 対象の真上から垂直ドロップ、ノード辺に矢じりを着地 |
| 被害者ノードを赤に塗る | 中立色+赤の損失ラベル。赤は攻撃経路専用 |
| 赤配線が無関係ノードを囲う | 配線対象をトランク隣接に置き、ゴーストは配線の外へ |
| favicon 128px ロゴ拡大でボケ | 256px 以上を取得 (`sz=256`) |
| エンティティラベルの言い直し見出し | 見出しゼロを基本に。スコープはラベルに畳み込む (Karak RPC #N) |
| 要素 X の隣に別ブランド Y のロゴ | X のロゴと誤読される。帰属は境界バンドの左上コーナーか、タイトルに任せる |
| callout を塗り+枠パネルにする | 図で唯一の「箱」になり浮く。プレーンなコード行+致命 token のみ強調 |
| 役割の違うアクターに同じアイコン | 形=役割 (シールド=検証者、サーバー=インフラ)。同形だと同一 tier に見える |
| ロゴ zoom をピクセル実寸に対し固定 | 高解像度版への差し替えでサイズが化ける。`min(TARGET_H/h, MAX_W/w)` で逆算 |
| バンド上の on_line ラベルが白 bbox | 白い四角が浮く。バンドの合成色 (#f7f7fe) を敷く |
| 2×2 グリッド・凡例・囲み枠 | 使わない。位置・矢印・形 (実線/破線) で読ませる |
| 警告 `font weight not found` で消耗 | 無害。目視確認のみを信じる |
