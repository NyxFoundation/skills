// Proposal generator skeleton — docx-js
//   npm install docx && node make_docx.js
// Replace the CONTENT section. The helpers above it are the reusable part.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, HeadingLevel, BorderStyle,
  Footer, Header, PageNumber, PageBreak, VerticalAlign, LevelFormat, ImageRun,
} = require("docx");

// ─────────────────────────────────────────────── design tokens
const FONT = { ascii: "Yu Gothic", eastAsia: "Yu Gothic", hAnsi: "Yu Gothic", cs: "Yu Gothic" };
const MONO = { ascii: "Consolas", eastAsia: "MS Gothic", hAnsi: "Consolas", cs: "Consolas" };
const NAVY = "1F3864", HDRFILL = "1F3864", SUBFILL = "D9E2F3", LIGHT = "F2F5FA";
const GREY = "595959", RED = "C00000";
const USABLE = 9638;                       // A4 portrait, 20 mm margins, in DXA
const HAIR = { style: BorderStyle.SINGLE, size: 2, color: "AAB7CF" };
const CELLBORDER = { top: HAIR, bottom: HAIR, left: HAIR, right: HAIR };

const body = [];
const push = (...x) => x.forEach((e) => body.push(e));

// ─────────────────────────────────────────────── helpers
function p(text, opt = {}) {
  const runs = Array.isArray(text) ? text : [{ t: text }];
  return new Paragraph({
    alignment: opt.align,
    spacing: { before: opt.before ?? 60, after: opt.after ?? 60, line: opt.line ?? 300 },
    children: runs.map((r) => new TextRun({
      text: r.t, bold: r.b || opt.bold, color: r.c || opt.color || "000000",
      size: (r.size || opt.size || 10.5) * 2, font: FONT,
    })),
  });
}

// heading + explicit outlineLevel + explicit formatting.
// All three are required: `heading` alone loses the design, custom paragraphStyles are ignored.
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, outlineLevel: 0,
    spacing: { before: 400, after: 180 }, keepNext: true,
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 4 } },
    children: [new TextRun({ text, bold: true, size: 30, color: NAVY, font: FONT })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, outlineLevel: 1,
    spacing: { before: 280, after: 120 }, keepNext: true,
    children: [new TextRun({ text, bold: true, size: 23, color: NAVY, font: FONT })],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3, outlineLevel: 2,
    spacing: { before: 200, after: 90 }, keepNext: true,
    children: [new TextRun({ text, bold: true, size: 20, color: "2E4E8F", font: FONT })],
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "dots", level },
    spacing: { before: 40, after: 40, line: 290 },
    children: [new TextRun({ text, size: 21, font: FONT })],
  });
}
function note(text) {
  return new Paragraph({
    spacing: { before: 80, after: 160 },
    children: [new TextRun({ text, size: 18, color: GREY, font: FONT })],
  });
}
function caption(text) {
  return new Paragraph({
    spacing: { before: 60, after: 200 },
    children: [new TextRun({ text, size: 16, color: GREY, font: FONT })],
  });
}
function spacer(h = 120) {
  return new Paragraph({ spacing: { after: h }, children: [new TextRun({ text: "", font: FONT })] });
}

function cellPara(text, opt = {}) {
  // one Paragraph per line — "\n" inside a TextRun does nothing
  return String(text).split("\n").map((ln, i) => new Paragraph({
    alignment: opt.align || AlignmentType.LEFT,
    spacing: { before: i === 0 ? 40 : 10, after: 40, line: 260 },
    children: [new TextRun({
      text: ln, bold: opt.bold, color: opt.color || "000000",
      size: (opt.size || 9) * 2, font: FONT,
    })],
  }));
}

// widths are relative; they are scaled to USABLE. aligns: array of "c" | undefined
function table(headers, rows, widths, opt = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  const w = widths.map((x) => Math.round(x * USABLE / total));
  const aligns = opt.aligns || [];
  const cell = (txt, i, isHead, shade) => new TableCell({
    width: { size: w[i], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: isHead ? HDRFILL : (shade || "FFFFFF") },
    margins: { top: 40, bottom: 40, left: 90, right: 90 },
    verticalAlign: VerticalAlign.CENTER,
    borders: CELLBORDER,
    children: cellPara(txt, {
      bold: isHead || (opt.shadeFirstCol && i === 0),
      color: isHead ? "FFFFFF" : undefined,
      size: opt.size || 9,
      align: isHead ? AlignmentType.CENTER
                    : (aligns[i] === "c" ? AlignmentType.CENTER : AlignmentType.LEFT),
    }),
  });
  const trs = [];
  if (headers) {
    trs.push(new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, i, true)) }));
  }
  rows.forEach((r) => trs.push(new TableRow({
    children: r.map((c, i) => cell(c, i, false, opt.shadeFirstCol && i === 0 ? SUBFILL : "FFFFFF")),
  })));
  return new Table({ columnWidths: w, width: { size: USABLE, type: WidthType.DXA }, rows: trs });
}

function code(lines, opt = {}) {
  const arr = Array.isArray(lines) ? lines : lines.split("\n");
  return new Table({
    columnWidths: [USABLE], width: { size: USABLE, type: WidthType.DXA },
    rows: [new TableRow({ children: [new TableCell({
      width: { size: USABLE, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, color: "auto", fill: "F5F7FA" },
      margins: { top: 120, bottom: 120, left: 180, right: 120 },
      borders: {
        top: HAIR, bottom: HAIR, right: HAIR,
        left: { style: BorderStyle.SINGLE, size: 12, color: NAVY },
      },
      children: arr.map((ln) => new Paragraph({
        spacing: { before: 0, after: 0, line: 240 },
        children: [new TextRun({ text: ln === "" ? " " : ln, size: (opt.size || 8) * 2, font: MONO })],
      })),
    })] })],
  });
}

// widthIn in inches; transformation is px @96dpi
function figure(pngPath, widthIn, imgW, imgH) {
  const px = Math.round(widthIn * 96);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 160, after: 60 },
    children: [new ImageRun({
      type: "png", data: fs.readFileSync(pngPath),
      transformation: { width: px, height: Math.round(px * imgH / imgW) },
    })],
  });
}

// Phase-level Gantt as a table. Colour + glyph so it survives B&W printing.
function ganttTable(days, weekOf, bars, gates, nameW = 2900) {
  const cw = [nameW].concat(new Array(days.length).fill(Math.floor((USABLE - nameW) / days.length)));
  const c = (txt, i, fill, bold, color, size) => new TableCell({
    width: { size: cw[i], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: fill || "FFFFFF" },
    margins: { top: 20, bottom: 20, left: 20, right: 20 },
    verticalAlign: VerticalAlign.CENTER, borders: CELLBORDER,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 10, after: 10 },
      children: [new TextRun({ text: txt, bold, color: color || "000000",
                               size: (size || 6) * 2, font: FONT })],
    })],
  });
  const rows = [
    new TableRow({ tableHeader: true, children: [c("", 0, HDRFILL)]
      .concat(days.map((d, i) => c(weekOf[i], i + 1, HDRFILL, true, "FFFFFF", 6.5))) }),
    new TableRow({ tableHeader: true, children: [c("フェーズ", 0, SUBFILL, true, "000000", 8)]
      .concat(days.map((d, i) => c(d, i + 1, SUBFILL, true, "000000", 6))) }),
  ];
  bars.forEach(([name, s, e, color]) => {
    const cells = [new TableCell({
      width: { size: cw[0], type: WidthType.DXA },
      margins: { top: 30, bottom: 30, left: 80, right: 40 },
      verticalAlign: VerticalAlign.CENTER, borders: CELLBORDER,
      children: [new Paragraph({ spacing: { before: 10, after: 10 },
        children: [new TextRun({ text: name, size: 15, font: FONT })] })],
    })];
    for (let d = 1; d <= days.length; d++) {
      const on = d >= s && d <= e;
      cells.push(c(on ? "■" : "", d, on ? color : "FFFFFF", false, NAVY, 6));
    }
    rows.push(new TableRow({ children: cells }));
  });
  const g = [new TableCell({
    width: { size: cw[0], type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: SUBFILL },
    margins: { top: 30, bottom: 30, left: 80, right: 40 },
    verticalAlign: VerticalAlign.CENTER, borders: CELLBORDER,
    children: [new Paragraph({ spacing: { before: 10, after: 10 },
      children: [new TextRun({ text: "承認ゲート", bold: true, size: 15, font: FONT })] })],
  })];
  for (let d = 1; d <= days.length; d++) {
    g.push(c(gates[d] || "", d, gates[d] ? RED : "FFFFFF", true, gates[d] ? "FFFFFF" : "000000", 5.5));
  }
  rows.push(new TableRow({ children: g }));
  return new Table({ columnWidths: cw, width: { size: USABLE, type: WidthType.DXA }, rows });
}

// ═══════════════════════════════════════════════ CONTENT — replace below
const CLIENT = "○○株式会社";
const TITLE = "○○のご提案";
const SUBTITLE = "サブタイトル";
const DATE = "20XX 年 X 月 X 日";
const VENDOR = "貴社名";

const cover = [
  new Paragraph({ spacing: { before: 2600 }, children: [new TextRun({ text: "", font: FONT })] }),
  new Paragraph({ spacing: { after: 900 },
    children: [new TextRun({ text: `${CLIENT}　御中`, size: 28, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    border: { top: { style: BorderStyle.SINGLE, size: 14, color: NAVY, space: 14 } },
    children: [new TextRun({ text: TITLE, bold: true, size: 40, color: NAVY, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 1600 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 14, color: NAVY, space: 14 } },
    children: [new TextRun({ text: SUBTITLE, size: 22, color: GREY, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 100 },
    children: [new TextRun({ text: DATE, size: 21, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.RIGHT,
    children: [new TextRun({ text: VENDOR, bold: true, size: 24, font: FONT })] }),
  new Paragraph({ children: [new PageBreak()] }),
];

// 静的目次（TOC フィールドは読み手が更新しないと出ず、Google Docs では描画されない）
push(h1("目次"));
[["1.", "ご提案の背景"], ["2.", "ご提案の概要"], ["3.", "実施内容"],
 ["4.", "成果物"], ["5.", "実施体制"], ["6.", "スケジュール"],
 ["7.", "お見積り"], ["付録 A", "用語"], ["付録 B", "出典"]]
  .forEach(([n, t]) => push(new Paragraph({
    spacing: { before: 70, after: 70 }, indent: { left: 400 },
    children: [new TextRun({ text: n + "　", bold: true, size: 21, color: NAVY, font: FONT }),
               new TextRun({ text: t, size: 21, font: FONT })],
  })));
push(new Paragraph({ children: [new PageBreak()] }));

push(h1("1. ご提案の背景"));
push(h2("1.1　これまでの経緯"));
push(p("本文。です・ます調、短文。メタ記述・改訂履歴・社内事情は書かない。"));

push(h1("2. ご提案の概要"));
push(table(["項目", "内容"], [
  ["期間", "X 週間（実働 XX 営業日）"],
  ["対象範囲", "…"],
  ["主な成果物", "N 点（…）"],
  ["御社ご負担", "会議ご出席 合計 XX 時間。合計 XX 人日"],
], [180, 620], { shadeFirstCol: true }));

push(h1("6. スケジュール"));
push(ganttTable(
  ["10/05", "10/06", "10/07", "10/08", "10/09"],
  ["第1週", "", "", "", ""],
  [["第 0 フェーズ　準備", 1, 2, "8FAADC"],
   ["第 1 フェーズ　実施", 2, 5, "A9D18E"]],
  { 2: "G0", 5: "G1" }
));
push(note("数字は日付です。日程は営業日通番を正とし、日付は参考値です。"));

// 図：mermaid やコードブロックではなく、レンダリング済み画像を貼る
// push(figure("fig_xxx.png", 6.35, 2032, 2135));
// push(caption("説明のために作成した例です。"));

// ═══════════════════════════════════════════════ document
const doc = new Document({
  creator: VENDOR, title: TITLE, description: SUBTITLE,
  numbering: { config: [{ reference: "dots", levels: [
    { level: 0, format: LevelFormat.BULLET, text: "・", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 480, hanging: 240 } } } },
    { level: 1, format: LevelFormat.BULLET, text: "－", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 900, hanging: 240 } } } },
  ] }] },
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  sections: [
    { properties: { page: { size: { width: 11906, height: 16838 },
        margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } } },
      children: cover },
    { properties: { page: { size: { width: 11906, height: 16838 },
        margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } } },
      headers: { default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "AAB7CF", space: 4 } },
        children: [new TextRun({ text: TITLE, size: 16, color: GREY, font: FONT })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY, font: FONT })] })] }) },
      children: body },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("proposal.docx", buf);
  console.log("saved, bytes =", buf.length);
});
