# Toolchain notes

Every pitfall here cost real time. On NixOS use `uv run --with ...` for Python and local `npm install`
for Node — see `devops/nixos-environment`.

---

## docx-js (Node)

```bash
npm init -y && npm install docx
node make_docx.js
```

### Heading outline levels — the one that looks fine and isn't

Custom-styled `Paragraph`s with a `TextRun` produce headings that **look** right but carry no outline
level. Word's navigation pane and Google Docs' outline stay empty.

```js
// ✗ looks correct, no outline
new Paragraph({ children: [new TextRun({ text, bold: true, size: 30, color: NAVY })] })
```

Adding `heading:` fixes the outline but docx-js's **default** heading style then takes over the
appearance (blue `2E74B5`, size 32). Defining your own `paragraphStyles` with `id: "Heading1"` does
**not** win — the built-in default is emitted instead.

The combination that works: `heading` + explicit `outlineLevel` + run/paragraph formatting set
directly (run-level always beats style-level).

```js
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    outlineLevel: 0,                       // explicit; do not rely on the style
    spacing: { before: 400, after: 180 },
    keepNext: true,
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 4 } },
    children: [new TextRun({ text, bold: true, size: 30, color: NAVY, font: FONT })],
  });
}
```

Verify in the output, do not assume:

```python
x = z.read("word/document.xml").decode()
print([(l, x.count(f'<w:outlineLvl w:val="{l}"')) for l in "012"])
print([(h, x.count(f'w:val="{h}"')) for h in ["Heading1", "Heading2", "Heading3"]])
```

### Table of contents

A `TableOfContents` field renders only after the reader updates fields, and Google Docs shows nothing.
For a document that ships to both, write a **static 目次** and rely on heading styles for navigation.

### Japanese fonts

```js
const FONT = { ascii: "Yu Gothic", eastAsia: "Yu Gothic", hAnsi: "Yu Gothic", cs: "Yu Gothic" };
```

Pass the object (not a string) to every `TextRun` and to `styles.default.document.run`.

### Tables

- Set `columnWidths` on the table **and** `width` on every cell, both `WidthType.DXA`.
  Percentages break in Google Docs
- `ShadingType.CLEAR`, never `SOLID` (renders black)
- A4 portrait with 20 mm margins → usable width **9638 DXA**. Scale a relative width array:
  `w = widths.map(x => Math.round(x * USABLE / sum))`
- Multi-line cell text: one `Paragraph` per line. `\n` inside a `TextRun` does nothing
- `tableHeader: true` on the header row so it repeats across pages

### Images

`ImageRun` requires `type`:

```js
new ImageRun({ type: "png", data: fs.readFileSync(path),
               transformation: { width: px, height: px * imgH / imgW } })
```

`transformation` is in pixels at 96 dpi. For a 6.35 in wide figure: `6.35 * 96 = 610`.

### Other

- `PageBreak` must be inside a `Paragraph`
- Never emit `•` literally — configure `numbering` with `LevelFormat.BULLET`
- Cover page in its own section so the header/footer starts on page 2

---

## openpyxl

```bash
uv run --quiet --with openpyxl python make_xlsx.py
```

### Formulas

openpyxl writes formulas with **no cached value**. Excel and Google Sheets recalculate on open, so
the delivered file is fine — but `data_only=True` reads back `None`, and previewers show blanks.
`scripts/recalc.py` (the `xlsx` skill) needs LibreOffice; if it is unavailable, say so when reporting
rather than claiming the numbers were verified.

Stick to Excel-2007-era functions (`SUM`, `ROUND`, `AVERAGE`, `SUMIFS`, `INDEX`/`MATCH`). Avoid
`XLOOKUP`, `FILTER`, `UNIQUE`, `SORT`.

### Conditional-formatting Gantt

Bars that follow the start/end columns instead of being painted once:

```python
gr = f"{first_day_col}{first_row}:{last_day_col}{last_row}"
# gates first, stopIfTrue, so they win over the phase colour
gw.conditional_formatting.add(gr, FormulaRule(
    formula=[f'AND($C{first_row}="ゲート",{L}${HDR}>=$H{first_row},{L}${HDR}<=$I{first_row})'],
    fill=PatternFill("solid", fgColor=GATE), stopIfTrue=True))
for phase, color in PHASE_COLOR.items():
    gw.conditional_formatting.add(gr, FormulaRule(
        formula=[f'AND($B{first_row}="{phase}",{L}${HDR}>=$H{first_row},{L}${HDR}<=$I{first_row})'],
        fill=PatternFill("solid", fgColor=color), stopIfTrue=True))
```

The formula is written relative to the range's **top-left cell**; `$` placement does the rest.
Put the day number (1..n) in the header row so `{L}${HDR}` can be compared numerically, and format it
as `'"D"0'` for display.

### Gotchas

- Merged cells: write the top-left anchor only; the rest are read-only `MergedCell`
- `freeze_panes` takes a **coordinate string** (`"L6"`), not a cell object — passing a `MergedCell`
  raises `TypeError: 'MergedCell' object is not iterable`
- Do not merge a phase band across the Gantt columns; fill those cells individually instead
- Rounding: `ROUND(x*0.15, 1)` gives 6.4 where the document says 6.5. Use
  `ROUND(x*rate*2, 0)/2` to land on clean half-days
- Mark input cells unmistakably: yellow fill `FFF2CC` + blue font `0000FF`, and list them in a legend

---

## matplotlib figures

Use `presentation/editorial-figures` for the house style. Specific to diagram work:

```bash
uv run --with matplotlib --with numpy --with uharfbuzz --with fonttools python fig.py
```

- **Open every PNG with the Read tool.** Overlaps, tofu glyphs, and overflow are invisible otherwise.
  Crop with PIL to inspect a region closely
- **Tofu glyphs** in Noto Sans CJK JP: `−` (U+2212), `≠`, `⊆`. Use `-`, `!=`, and prose
- **`va="center"` on multi-line text** occupies more vertical space than `lines × size × linespacing`
  suggests. If a block overflows its box, switch to a single line or `va="top"` with an explicit
  anchor — do not keep nudging the offset
- Manual layout beats auto layout for a known graph. Define lane x-coordinates and a row pitch as
  constants, then place everything relative to them
- Semantic colour only. Reserve the warning colour for the one thing the reader must look at
- Reproduce the source structure faithfully. A diagram that "cleans up" the real output misleads

---

## rclone / Google Drive

Token lives in the rclone config:

```bash
TOKEN=$(rclone config dump | python3 -c \
  "import json,sys; print(json.loads(json.load(sys.stdin)['gdrive']['token'])['access_token'])")
```

rclone refreshes it on use, so run an rclone command first if the token is stale.

### Upload originals

```bash
rclone copy file.docx gdrive: --drive-root-folder-id <FOLDER_ID> --tpslimit 2 -v
rclone lsjson gdrive: --drive-root-folder-id <FOLDER_ID> --tpslimit 2    # IDs + names
```

### Native Google Docs/Sheets

`--drive-import-formats docx,xlsx` **does not convert** (tested on rclone 1.72). Use the Drive API:

```bash
curl -s -X POST "https://www.googleapis.com/drive/v3/files/<FILE_ID>/copy?supportsAllDrives=true" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"...","mimeType":"application/vnd.google-apps.document","parents":["<FOLDER_ID>"]}'
```

`application/vnd.google-apps.spreadsheet` for xlsx.

Note: `rclone lsjson` shows a Google Doc **with an export extension appended** (`.docx`), so a native
Doc and a real `.docx` look identical in the listing. Distinguish by ID, and give the converted file
a distinct name.

### Updating without breaking the link

Once a Google Doc URL has been shared, keep it. Update in place — do not re-copy:

```bash
curl -s -X PATCH \
  "https://www.googleapis.com/upload/drive/v3/files/<DOC_ID>?uploadType=media&supportsAllDrives=true" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  --data-binary @proposal.docx
```

### Quota

403 `Quota exceeded ... Requests per minute` appears readily. Back off 2–5 minutes and retry in a
loop; do not hammer. `--tpslimit 2` on rclone calls helps.

---

## Codex CLI

```bash
codex exec --skip-git-repo-check -c model_reasoning_effort="high" "$(cat prompt.txt)" \
  < /dev/null > out.txt 2>&1
```

- `< /dev/null` mandatory (see `review-loop.md`)
- Run in the background and poll; high-effort runs on a long document take 5–15 minutes
- Output includes the tool-call trace; the report starts after the `tokens used` line:
  `awk '/tokens used/{f=1} f' out.txt`

---

## Environment checks worth doing up front

```bash
which node npm            # docx-js
uv --version              # Python deps
which soffice             # absent ⇒ no docx render check, no xlsx recalc — SAY SO
which dot mmdc            # usually absent; plan on matplotlib for diagrams
fc-list | grep -i "noto.*cjk" | head -3
which rclone && rclone listremotes
which codex
```

State the missing pieces in the final report rather than implying verification you could not perform.

---

## Markdown → docx で必ず踏む 3 つ

### 1. 折り返し行が 1 段落ずつ出る

markdown を行単位で処理する変換器は、**ソースの折り返しをそのまま段落の区切りにする**。
段落間の余白が全行に入り、ページ数が 3〜4 割ふくらむ。文が 2〜3 行に分断されて見えるので、
体裁も壊れる。67 ページのうち 10 ページ以上がこれだった。

**空行までを 1 段落にまとめてから流し込む。** 箇条書きの継続行（インデント行）も同様に吸収する。

```python
buf = [ln.strip()]
j = i + 1
while j < len(lines) and lines[j].strip():
    nxt = lines[j]
    if nxt.startswith(("#", "|", "> ", "```", "![")) or re.match(r"^\s*[-*\d]", nxt):
        break
    buf.append(nxt.strip()); j += 1
write_inline(p, "".join(buf))          # 和文なので連結時に空白を入れない
i = j
```

`preflight_check.py` が「句点で終わらない段落の比率」で検出する。25% を超えたら疑う。

### 2. インライン強調が行をまたぐと記号が出る

`**強調**` の正規表現は行をまたがない。markdown 側で折り返すと、アスタリスクがそのまま docx に出る。

- **強調は 1 行に収める。** 長い強調は文を分ける
- 生成後に `literal **` を数えて 0 を確認する。目視では見落とす

### 3. 見出しにアウトラインレベルが載らない

`add_heading()` のスタイルだけでは `w:outlineLvl` が付かず、**Word のナビゲーションウィンドウと
Google ドキュメントの目次が空になる**。python-docx でも明示的に足す。

```python
o = OxmlElement("w:outlineLvl"); o.set(qn("w:val"), str(level - 1))
h._p.get_or_add_pPr().append(o)
```

---

## 図: フォント名で Bold を信頼しない

CJK フォントが**可変フォント 1 本**で入っている環境（NixOS の `NotoSansCJK-VF.otf.ttc` など）では、
matplotlib の `font_manager` に **weight=100（Thin）としてしか登録されない**。
`fontweight="bold"` を指定しても効かず、全部の和文が極細で描かれる。

Google ドキュメントが取り込み時に画像の長辺を 2048px へ縮小するため、この細さでは線が飛び、
「画質は悪くないのに読めない」状態になる。**目視でも気づきにくい。**単体で見ると読めるからである。

確認と回避:

```bash
python3 -c "import matplotlib.font_manager as fm; \
  print({(f.name,f.weight) for f in fm.fontManager.ttflist if 'CJK' in f.name})"
```

静的ウェイトが無ければ、保存直前に全テキストを同色で縁取って太らせる。

```python
import matplotlib.patheffects as pe
from matplotlib.text import Text
for t in fig.findobj(Text):
    if t.get_text().strip() and not t.get_path_effects():
        t.set_path_effects([pe.withStroke(linewidth=t.get_fontsize() * 0.11,
                                          foreground=t.get_color())])
```

`assets/figure_preflight.py` が、使用フォントの weight と描画後の線の細さを報告する。

---

## Drive API は 403 を返す前提で書く

rclone の共有 OAuth クライアント経由だと、**正常なリクエストでも 403 が頻繁に返る**。
スコープの問題ではない。20 秒待って最大 15 回再試行する。

- **401 はトークン切れ。** `rclone lsd gdrive:` を 1 回叩けば更新されるので、API を叩く前に流す
- `files.list`（フォルダの列挙）は特に 403 になりやすい。`files.get` を ID 指定で使うほうが通る
- 既存ファイルの更新は ID 固定の `files.update`。URL・ファイル名・配置フォルダが変わらない
- 新規作成は multipart POST。`mimeType` に Google 形式を指定すると変換され、指定しなければ
  アップロードした形式のまま置かれる。**ガントを含む xlsx は変換しない**（塗り分けと列幅が崩れる）
