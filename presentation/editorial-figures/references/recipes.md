# Figure recipes

Copy-pasteable patterns for each archetype. All assume `style.py` is in the
working directory and imported as `S`:

```python
import style as S
```

Every recipe builds a figure with `S.new(...)`, draws with `S.t / S.rrect /
S.arrow / S.chip`, adds a headline with `S.title_block(...)`, and writes a PNG
with `S.save(fig, "name.png")`. Adapt the data lists/dicts; keep the structure.

## Contents
1. [Divergence (two diverging curves)](#1-divergence)
2. [Radial convergence (hub and spokes)](#2-radial-convergence)
3. [Stat-card dashboard (evidence grid)](#3-stat-card-dashboard)
4. [Concept flow (inputs to engine to outputs)](#4-concept-flow)
5. [Calendar timeline (day strip + event bars)](#5-calendar-timeline)
6. [Donut + horizontal bars (composition + channels)](#6-donut--bars)
7. [Zoning / floor plan (tinted zone boxes)](#7-zoning--floor-plan)

Universal conventions are repeated at the [bottom](#conventions). The most
common bug: **filled shapes hide text** — give labels a higher `zorder` than the
patch they sit on (e.g. a filled `Circle(z=4)` needs its label at `zorder=5+`).

---

## 1. Divergence

**When:** one quantity falls while another rises (cost up vs down, supply vs
demand). The crossover + widening gap carries the argument. Use a real (non-off)
axis. Curves should be smooth logistic S-curves, labelled at their right ends —
never with a legend box.

```python
def divergence(out="fig_divergence.png"):
    fig, ax = S.new(10.4, 6.4, axis_off=False, xlim=(0, 11.5), ylim=(0, 1.04))
    x = S.np.linspace(0, 10, 400)
    down = 0.08 + 0.86 / (1 + S.np.exp((x - 4.2) * 0.95))   # high -> low
    up   = 0.08 + 0.86 / (1 + S.np.exp(-(x - 5.0) * 0.85))  # low  -> high
    ax.fill_between(x, down, up, where=(up >= down), color=S.RUST, alpha=0.10,
                    zorder=1, interpolate=True)             # the "gap"
    ax.plot(x, down, color=S.SLATE, lw=3.0, zorder=3, solid_capstyle="round")
    ax.plot(x, up,   color=S.RUST,  lw=3.3, zorder=3, solid_capstyle="round")
    i = int(S.np.argmin(S.np.abs(down - up)))               # crossover
    ax.plot([x[i]], [(down[i] + up[i]) / 2], "o", color=S.INK, ms=6.5, zorder=5)
    ax.axvline(x[i], color=S.FAINT, lw=1.0, ls=(0, (2, 3)), zorder=1)
    S.t(ax, 10.18, down[-1], "生成コスト", fp="bold", size=14, color=S.SLATE, va="center")
    S.t(ax, 10.18, up[-1],   "検証コスト", fp="bold", size=14, color=S.RUST,  va="center")
    S.t(ax, 6.7, 0.90, "検証ギャップ", fp="bold", size=13, color=S.RUST, ha="center")
    S.arrow(ax, (6.7, 0.815), (8.1, 0.60), color=S.RUST_L, lw=1.5, ms=11, rad=-0.22)
    S.t(ax, x[i], 0.025, "転換点", fp="med", size=10.5, color=S.MUTED, ha="center", va="bottom")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(S.FAINT); ax.spines["bottom"].set_linewidth(1.1)
    ax.set_xlabel("時間・普及 →", fontproperties=S.F["med"], fontsize=11.5, color=S.SOFT, labelpad=9)
    ax.set_ylabel("コスト（相対）", fontproperties=S.F["med"], fontsize=11.5, color=S.SOFT, labelpad=10)
    fig.subplots_adjust(top=0.80, left=0.085, right=0.90, bottom=0.13)
    S.title_block(fig, "見出し", "サブ見出し。")
    return S.save(fig, out)
```

---

## 2. Radial convergence

**When:** several domains/streams converge into one unifying concept ("these are
not separate things"). A dark center disc + satellite cards + inward arrows.
Place 6 satellites on a hexagon (angles 90, 30, -30, -90, -150, 150).

```python
def convergence(center=("Agentic", "Economy", "Security"),
                caption="= 検証可能なデジタル経済",
                domains=(("AI", "生成・判断・自律化", S.SLATE),
                         ("デジタル", "金融サービス",   S.TEAL),
                         ("Web3 /", "オンチェーン金融", S.GOLD),
                         ("サイバー", "セキュリティ",   S.RUST),
                         ("耐量子暗号", "",            S.PLUM),
                         ("経済安全保障", "",          S.OLIVE)),
                out="fig_convergence.png"):
    fig, ax = S.new(9.4, 9.4, xlim=(-1.30, 1.30), ylim=(-1.42, 1.30))
    ax.set_aspect("equal")
    R, CR = 0.95, 0.40
    bw, bh = 0.62, 0.30
    for (l1, l2, c), a in zip(domains, (90, 30, -30, -90, -150, 150)):
        rad = S.np.deg2rad(a); px, py = R * S.np.cos(rad), R * S.np.sin(rad)
        S.arrow(ax, (px, py), (CR * S.np.cos(rad) * 1.02, CR * S.np.sin(rad) * 1.02),
                color=S.FAINT, lw=1.7, ms=12, z=2)
        S.rrect(ax, px - bw/2, py - bh/2, bw, bh, fc=S.CARD, ec=S.HAIR, lw=1.3, rs=0.07, z=3)
        ax.add_patch(S.Circle((px - bw/2 + 0.10, py + bh/2 - 0.085), 0.028, color=c, zorder=4))
        if l2:
            S.t(ax, px, py + 0.045, l1, fp="bold", size=12.5, color=S.INK, ha="center", va="center")
            S.t(ax, px, py - 0.065, l2, fp="med",  size=11.5, color=S.SOFT, ha="center", va="center")
        else:
            S.t(ax, px, py, l1, fp="bold", size=13, color=S.INK, ha="center", va="center")
    ax.add_patch(S.Circle((0, 0), CR, color=S.INK, zorder=4))
    for dy, line in zip((0.118, 0.0, -0.118), center):           # NOTE z=6 (above disc)
        S.t(ax, 0, dy, line, fp="ssemi", size=17, color=S.PAPER, ha="center", va="center", zorder=6)
    S.t(ax, 0, -CR - 0.24, caption, fp="bold", size=13, color=S.INK, ha="center", va="center", zorder=6)
    fig.subplots_adjust(top=0.83, bottom=0.04, left=0.04, right=0.96)
    S.title_block(fig, "見出し", "サブ見出し。", x=0.06, y=0.965)
    return S.save(fig, out)
```

---

## 3. Stat-card dashboard

**When:** a set of headline numbers / evidence ("Global Evidence Snapshot").
Grid of cards, each with: accent rule, category tag, big hero number, optional
sub line (put YoY / deltas in `S.RUST` to signal rising risk), 2-line
descriptor, source. Drive everything from a list of dicts.

```python
def dashboard(cards, ncol=4, out="fig_dashboard.png"):
    # card dict keys: acc, tag, hero, hsize, yoy(None ok), ycol, desc("a\nb"), src
    fig, ax = S.new(12.8, 7.3)
    L = Rm = 0.5; gap = 0.34; pad = 0.30
    cw = (12.8 - L - Rm - (ncol - 1) * gap) / ncol
    top, bot, rgap = 6.85, 0.45, 0.5
    nrow = (len(cards) + ncol - 1) // ncol
    ch = (top - bot - rgap * (nrow - 1)) / nrow
    for i, c in enumerate(cards):
        col, row = i % ncol, i // ncol
        x = L + col * (cw + gap); y = top - ch - row * (ch + rgap); ty = y + ch
        S.rrect(ax, x, y, cw, ch, fc=S.CARD, ec=S.HAIR, lw=1.2, rs=0.09, z=1)
        ax.plot([x + pad, x + pad + 0.55], [ty - 0.30] * 2, color=c["acc"], lw=3.2,
                solid_capstyle="round", zorder=3)
        S.t(ax, x + pad, ty - 0.42, c["tag"], fp="med", size=10, color=S.MUTED, va="top")
        S.t(ax, x + pad, ty - 0.90, c["hero"], fp="black", size=c["hsize"], color=S.INK, va="top")
        hh = c["hsize"] / 72.0
        if c.get("yoy"):
            ny = ty - 0.90 - hh - 0.12
            S.t(ax, x + pad, ny, c["yoy"], fp="bold", size=11.5, color=c.get("ycol", S.SOFT), va="top")
            dy = ny - 0.30
        else:
            dy = ty - 0.90 - hh - 0.20
        S.t(ax, x + pad, dy, c["desc"], fp="reg", size=10.5, color=S.SOFT, va="top", linespacing=1.42)
        S.t(ax, x + pad, y + 0.30, c["src"], fp="med", size=8.8, color=S.MUTED, va="center")
    fig.subplots_adjust(top=0.80, bottom=0.03, left=0.0, right=1.0)
    S.title_block(fig, "見出し", "サブ見出し。", x=0.045, y=0.965)
    return S.save(fig, out)

# example row:
#   dict(acc=S.RUST, tag="デジタル金融犯罪", hero="$16.6B", hsize=38,
#        yoy="前年比 +33%", ycol=S.RUST, desc="インターネット犯罪の\n年間報告損失（2024）",
#        src="FBI IC3 2024")
# hero sizing: plain numbers 40-44; "$16.6B"~38; long strings ("9.19-27")~31;
# short phrases ("管理不能")~26.
```

---

## 4. Concept flow

**When:** an input set feeds a process/engine that yields observed outputs
(submitted agents -> managed arena -> evaluation axes). Three columns, two
bundled arrows, a serif caption at the bottom.

```python
def concept_flow(left_title, agents, center_name, center_sub, dynamics,
                 right_title, axes_list, caption, out="fig_flow.png"):
    fig, ax = S.new(12.8, 7.1)
    # LEFT — inputs
    lx = 1.55
    S.t(ax, lx, 5.95, left_title, fp="bold", size=12.5, color=S.INK, ha="center", va="center", linespacing=1.4)
    ys = S.np.linspace(5.05, 2.05, len(agents))
    for lab, ay in zip(agents, ys):
        ax.add_patch(S.Circle((lx, ay), 0.21, fc=S.CARD, ec=S.SLATE, lw=1.8, zorder=3))
        S.t(ax, lx, ay, lab, fp="med", size=10, color=S.SLATE, ha="center", va="center", zorder=4)
    S.arrow(ax, (lx + 0.55, 3.55), (4.15, 3.55), color=S.SOFT, lw=2.2, ms=15)
    # CENTER — engine/arena
    ax0, ay0, aw, ah = 4.25, 1.40, 4.55, 4.55; cx = ax0 + aw / 2
    S.rrect(ax, ax0, ay0, aw, ah, fc="#FBFAF6", ec=S.SLATE_L, lw=1.6, rs=0.14, z=1)
    S.t(ax, cx, ay0 + ah - 0.45, center_name, fp="black", size=24, color=S.INK, ha="center", va="center")
    S.t(ax, cx, ay0 + ah - 0.90, center_sub, fp="med", size=11.5, color=S.SOFT, ha="center", va="center")
    pts = [(cx-1.15, ay0+2.55), (cx+1.15, ay0+2.62), (cx-0.55, ay0+1.95), (cx+0.62, ay0+1.92)]
    for a, b in [(0,1),(0,2),(2,3),(1,3)]:
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], color=S.SLATE_L, lw=1.0, alpha=0.7, zorder=2)
    for px, py in pts:
        ax.add_patch(S.Circle((px, py), 0.13, fc=S.SLATE, ec="none", zorder=3))
    cwid, chei, cg = 0.92, 0.40, 0.16; sx = cx - (3 * cwid + 2 * cg) / 2
    for k, d in enumerate(dynamics[:6]):
        r, cc = k // 3, k % 3
        S.chip(ax, sx + cc*(cwid+cg), ay0 + 0.75 - r*(chei+0.14), cwid, chei, d, size=10.5)
    S.arrow(ax, (ax0 + aw, 3.55), (9.55, 3.55), color=S.SOFT, lw=2.2, ms=15)
    # RIGHT — outputs / axes
    rx, rw = 9.7, 2.95
    S.t(ax, rx, 5.95, right_title, fp="bold", size=12.5, color=S.INK, ha="left", va="center")
    oy, oh, og = 5.35, 0.50, 0.115
    for o in axes_list:
        S.rrect(ax, rx, oy - oh, rw, oh, fc=S.CARD, ec=S.HAIR, lw=1.1, rs=0.16, z=2)
        ax.add_patch(S.Circle((rx + 0.22, oy - oh/2), 0.045, color=S.RUST, zorder=3))
        S.t(ax, rx + 0.40, oy - oh/2, o, fp="med", size=10.3, color=S.INK, ha="left", va="center")
        oy -= (oh + og)
    S.t(ax, 6.4, 0.58, caption, fp="smed", size=12.5, color=S.SLATE, ha="center", va="center")
    fig.subplots_adjust(top=0.81, bottom=0.02, left=0.0, right=1.0)
    S.title_block(fig, "見出し", "サブ見出し。", x=0.045, y=0.965)
    return S.save(fig, out)
```

---

## 5. Calendar timeline

**When:** positioning an event within a date window (a day strip with weekday /
holiday colouring, Gantt-style event bars, an optional bracket). Use Python
`datetime` for weekdays; pass a holidays dict so jp holidays are coloured and
tagged. **Verify holiday dates with WebSearch first** (see conventions).

```python
import datetime
def calendar_timeline(year, month, day_start, day_end, events, holidays=None,
                      bracket=None, callouts=(), out="fig_timeline.png"):
    # events: list of (i0, i1, color, label, is_hero)  -- i = day index from day_start
    # holidays: {day:int -> name:str};  bracket: (i0, i1, label)
    # callouts: list of (text, color)
    holidays = holidays or {}
    days = list(range(day_start, day_end + 1)); n = len(days)
    wd = ["月", "火", "水", "木", "金", "土", "日"]
    fig, ax = S.new(12.8, 6.6)
    gx0, gx1 = 2.7, 12.5; cw = (gx1 - gx0) / n
    cellx = lambda i: gx0 + i * cw
    cx = lambda i: gx0 + (i + 0.5) * cw
    for i in range(n + 1):
        ax.plot([cellx(i)] * 2, [1.95, 5.2], color=S.HAIR, lw=1.0, zorder=1)
    cy0, cy1 = 4.35, 5.18
    for i, d in enumerate(days):
        wkd = datetime.date(year, month, d).weekday()
        hol = d in holidays
        if hol or wkd == 6:   bg, tc = "#F4E8E3", S.RUST
        elif wkd == 5:        bg, tc = "#E9EEF3", S.SLATE
        else:                 bg, tc = S.CARD, S.INK
        S.rrect(ax, cellx(i) + 0.05, cy0, cw - 0.10, cy1 - cy0, fc=bg, ec=S.HAIR, lw=1.0, rs=0.06, z=2)
        S.t(ax, cx(i), cy0 + (cy1 - cy0) * 0.62, str(d), fp="black", size=17, color=tc, ha="center", va="center", zorder=3)
        S.t(ax, cx(i), cy0 + (cy1 - cy0) * 0.22, (wd[wkd] + "・祝") if hol else wd[wkd],
            fp="med", size=9.5, color=tc, ha="center", va="center", zorder=3)
    if bracket:
        i0, i1, lab = bracket
        bx0, bx1, by = cellx(i0) + 0.05, cellx(i1 + 1) - 0.05, 5.42
        ax.plot([bx0, bx1], [by, by], color=S.RUST_L, lw=1.6, zorder=2)
        for bx in (bx0, bx1): ax.plot([bx, bx], [by, by - 0.09], color=S.RUST_L, lw=1.6, zorder=2)
        S.t(ax, (bx0 + bx1) / 2, by + 0.09, lab, fp="bold", size=11, color=S.RUST, ha="center", va="bottom")
    yrows = [3.55, 2.88, 2.18]; hh = 0.46
    for (i0, i1, col, lab, hero), y in zip(events, yrows):
        x0, x1 = cellx(i0) + 0.06, cellx(i1 + 1) - 0.06
        S.rrect(ax, x0, y, x1 - x0, hh, fc=col, ec=(S.RUST if hero else "none"),
                lw=(2.0 if hero else 0), rs=0.08, z=3)
        S.t(ax, (x0 + x1) / 2, y + hh / 2, lab, fp="bold", size=12, color=S.PAPER, ha="center", va="center", zorder=4)
    cy = 1.45
    for text, col in callouts:
        S.t(ax, gx0, cy, text, fp="med", size=11, color=col, ha="left", va="center"); cy -= 0.43
    fig.subplots_adjust(top=0.81, bottom=0.03, left=0.0, right=1.0)
    S.title_block(fig, "見出し", "サブ見出し。", x=0.045, y=0.965)
    return S.save(fig, out)
```

---

## 6. Donut + bars

**When:** a composition (donut, center total) beside ranked channels
(horizontal bars). For range data, size wedges/bars by the midpoint and label
the range; add a footnote saying so.

```python
def donut_bars(segments, channels, total_label, out="fig_donut_bars.png"):
    # segments: list of (name, value, range_str, color)
    # channels: list of (name, value, range_str)
    fig, ax = S.new(12.8, 6.9)
    def header(x, s):
        S.t(ax, x, 6.30, s, fp="bold", size=13, color=S.INK, ha="left", va="center")
        ax.plot([x, x + 0.85], [6.06, 6.06], color=S.SLATE, lw=2.6, solid_capstyle="round", zorder=3)
    # donut
    header(0.45, "参加者構成")
    cxp, cyp, rad = 2.45, 3.05, 1.5; tot = sum(s[1] for s in segments); ang = 90.0
    for _, v, _, c in segments:
        ext = 360 * v / tot
        ax.add_patch(S.Wedge((cxp, cyp), rad, ang - ext, ang, width=rad * 0.42, fc=c, ec=S.PAPER, lw=2.2, zorder=2))
        ang -= ext
    S.t(ax, cxp, cyp + 0.16, "目標", fp="med", size=12, color=S.SOFT, ha="center", va="center", zorder=3)
    S.t(ax, cxp, cyp - 0.24, total_label, fp="black", size=23, color=S.INK, ha="center", va="center", zorder=3)
    lx, ly, lh = 4.35, 5.05, 0.515
    for name, v, rng, c in segments:
        ax.add_patch(S.FancyBboxPatch((lx, ly - 0.13), 0.26, 0.26,
            boxstyle="round,pad=0,rounding_size=0.05", fc=c, ec="none", zorder=2))
        S.t(ax, lx + 0.44, ly + 0.015, name, fp="med", size=10.8, color=S.INK, ha="left", va="center")
        S.t(ax, lx + 0.44, ly - 0.205, rng, fp="reg", size=9.2, color=S.MUTED, ha="left", va="center")
        ly -= lh
    ax.plot([7.05, 7.05], [0.55, 5.7], color=S.HAIR, lw=1.2, zorder=1)
    # bars
    header(7.45, "集客チャネル")
    bx0, bx1 = 7.45, 12.15; maxv = max(c[1] for c in channels)
    by, rowh = 5.05, 0.80
    for name, v, rng in channels:
        S.t(ax, bx0, by + 0.11, name, fp="med", size=10.6, color=S.INK, ha="left", va="bottom")
        S.rrect(ax, bx0, by - 0.33, (bx1 - bx0) * v / maxv, 0.29, fc=S.SLATE, ec="none", lw=0, rs=0.05, z=2)
        S.t(ax, bx0 + (bx1 - bx0) * v / maxv + 0.12, by - 0.185, rng, fp="med", size=9.6, color=S.SOFT, ha="left", va="center")
        by -= rowh
    S.t(ax, 0.45, 0.32, "数値は想定レンジ。円グラフは各レンジの中央値で作図。", fp="reg", size=9.5, color=S.MUTED, ha="left", va="center")
    fig.subplots_adjust(top=0.81, bottom=0.03, left=0.0, right=1.0)
    S.title_block(fig, "見出し", "サブ見出し。", x=0.045, y=0.965)
    return S.save(fig, out)
```

---

## 7. Zoning / floor plan

**When:** a schematic plan (rooms / zones), not architectural — sized by
importance, tinted by function, with an entrance arrow and feature chips. Keep
**symmetric inner padding**: if the left zone insets 0.30 from the container,
right zones must end 0.30 before the container's right border (a common miss).

```python
def zoning(zones, feats=(), entrance=None, out="fig_zoning.png"):
    # zones: list of (x, y, w, h, name, sub, fill, edge)  -- name may contain "\n"
    # feats: list of (label, width);  entrance: (x, label)
    fig, ax = S.new(12.8, 7.0)
    S.rrect(ax, 0.4, 1.05, 12.0, 4.75, fc="#FBFAF6", ec=S.SLATE_L, lw=1.6, rs=0.10, z=1)
    for x, y, w, h, name, sub, fc, ec in zones:
        S.rrect(ax, x, y, w, h, fc=fc, ec=ec, lw=1.3, rs=0.09, z=2)
        ny = y + h/2 + (0.17 if sub else 0)
        S.t(ax, x + w/2, ny, name, fp="bold", size=13, color=S.INK, ha="center", va="center", zorder=3, linespacing=1.3)
        if sub:
            S.t(ax, x + w/2, y + h/2 - 0.22, sub, fp="med", size=10.5, color=S.SOFT, ha="center", va="center", zorder=3)
    if entrance:
        ex, elab = entrance
        S.arrow(ax, (ex, 0.66), (ex, 1.28), color=S.SOFT, lw=2.2, ms=14, z=3)
        S.t(ax, ex, 0.50, elab, fp="med", size=10.3, color=S.SOFT, ha="center", va="top")
    fx = 0.70
    for label, w in feats:
        S.chip(ax, fx, 0.42, w, 0.40, label, size=9.8, rs=0.18); fx += w + 0.22
    fig.subplots_adjust(top=0.82, bottom=0.02, left=0.0, right=1.0)
    S.title_block(fig, "見出し", "サブ見出し。", x=0.045, y=0.965)
    return S.save(fig, out)

# Tint a zone fill from a base colour with S.lighten(S.SLATE, 0.86), etc.
```

---

## Conventions

These apply to every figure; they are what make the set look deliberate.

- **Output:** `S.save()` writes dpi=200, `bbox_inches="tight"`, paper-coloured,
  to the current working directory (or `$EDITORIAL_FIGURES_OUTDIR` if set). Then
  report the saved file paths back to the user.
- **Sizes:** wide diagrams 12.8 in; square radial 9.4; divergence ~10.4 x 6.4.
- **Headline:** always `S.title_block(fig, head, sub)` — serif-bold head, soft
  sans sub. Headlines state the takeaway, not the topic ("生成は安く、検証は
  高くなる", not "コスト比較").
- **Colour discipline:** paper + ink carry it; `SLATE` is the cool/neutral
  default; `RUST` is reserved for *rising risk* or sparing emphasis; reach for
  `CAT[...]` only when you must distinguish categories. Avoid rainbow.
- **Z-order:** text must sit above any filled patch it overlaps. Filled
  `Circle`/`Wedge` default to a high zorder — give their labels `zorder=5–6`.
- **No overlaps:** anchor stacked text with `va="top"` and explicit y steps;
  budget hero height as `pt/72` data units before placing the line below it.
- **Label at the source:** annotate curves at their ends and wedges via a
  legend list — avoid detached legends that force eye travel.
- **Padding symmetry:** equal inner margins; for the zoning container, match
  left and right insets.
- **Data honesty:** before drawing dates, prices, rankings, or "current"
  facts, use `WebSearch` to confirm them (Japanese public holidays, equinox-based
  dates, FX, leadership all drift). Label ranges as ranges; cite a source on
  every stat card; note when wedges use midpoints.
- **Always view, then fix:** after `save`, open the PNG with the `Read` tool and
  check Japanese glyphs (no □ tofu), overlaps, hidden text, and balance. Most
  defects are invisible until rendered. Iterate before delivering.
