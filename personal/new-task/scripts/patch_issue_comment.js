#!/usr/bin/env node
/**
 * GitHub の issue コメント（または issue 本文）を、マーカー区間の差し替えで安全に更新する。
 *
 * 長文を `gh issue comment --body` にシェル経由で渡すと、バッククォートや `$` の展開、
 * 引用符の食い違いで壊れる。このスクリプトは gh api で本文を取得し、Node の文字列操作で
 * 置換し、JSON を stdin から PATCH するので、本文がシェルを一度も通らない。
 *
 * Usage:
 *   # 区間差し替え（--between は繰り返せる）
 *   node patch_issue_comment.js --endpoint repos/OWNER/REPO/issues/comments/ID \
 *     --between "## 見出し" "## 次の見出し" --with-file new_section.md --dry-run
 *
 *   # 本文まるごと差し替え
 *   node patch_issue_comment.js --endpoint repos/OWNER/REPO/issues/123 --body-file full.md
 *
 *   # 正規表現置換（--flags 既定 gm）
 *   node patch_issue_comment.js --endpoint ... --regex "^成果の測定(.*)$" --with "#### 成果の測定\$1"
 *
 * --dry-run を付けると PATCH せず、置換前後の文字数と該当箇所の前後 80 字だけを出す。
 * 破壊的な更新なので、まず --dry-run で確認してから本実行すること。
 */
const { execFileSync } = require("node:child_process");
const { readFileSync } = require("node:fs");

function parseArgs(argv) {
  const opts = { edits: [], dryRun: false, endpoint: null, bodyFile: null };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      const v = argv[i + 1];
      if (v === undefined) throw new Error(`${arg} に値がない`);
      i += 1;
      return v;
    };
    switch (arg) {
      case "--endpoint":
        opts.endpoint = next();
        break;
      case "--body-file":
        opts.bodyFile = next();
        break;
      case "--between": {
        const start = next();
        const end = next();
        opts.edits.push({ kind: "between", start, end });
        break;
      }
      case "--regex":
        opts.edits.push({ kind: "regex", pattern: next(), flags: "gm" });
        break;
      case "--flags": {
        const last = opts.edits.at(-1);
        if (!last || last.kind !== "regex") throw new Error("--flags は --regex の直後に置く");
        last.flags = next();
        break;
      }
      case "--with": {
        const last = opts.edits.at(-1);
        if (!last) throw new Error("--with の前に --between か --regex が要る");
        last.replacement = next();
        break;
      }
      case "--with-file": {
        const last = opts.edits.at(-1);
        if (!last) throw new Error("--with-file の前に --between か --regex が要る");
        last.replacement = readFileSync(next(), "utf8");
        break;
      }
      case "--dry-run":
        opts.dryRun = true;
        break;
      default:
        throw new Error(`不明な引数: ${arg}`);
    }
  }
  if (!opts.endpoint) throw new Error("--endpoint は必須");
  if (!opts.bodyFile && opts.edits.length === 0) throw new Error("--body-file か --between/--regex のどれかが要る");
  return opts;
}

function applyBetween(body, { start, end, replacement }) {
  const startIndex = body.indexOf(start);
  if (startIndex < 0) throw new Error(`開始マーカーが見つからない: ${JSON.stringify(start.slice(0, 60))}`);
  const endIndex = end === "" ? body.length : body.indexOf(end, startIndex + start.length);
  if (endIndex < 0) throw new Error(`終了マーカーが見つからない: ${JSON.stringify(end.slice(0, 60))}`);
  if (body.indexOf(start, startIndex + start.length) >= 0) {
    throw new Error(`開始マーカーが複数ある。より長いマーカーを指定する: ${JSON.stringify(start.slice(0, 60))}`);
  }
  return body.slice(0, startIndex) + replacement + body.slice(endIndex);
}

function main() {
  const opts = parseArgs(process.argv);
  const response = JSON.parse(execFileSync("gh", ["api", opts.endpoint], { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 }));
  const before = response.body ?? "";
  let body = before;

  if (opts.bodyFile) {
    body = readFileSync(opts.bodyFile, "utf8");
  }
  for (const edit of opts.edits) {
    if (edit.replacement === undefined) throw new Error("--with / --with-file の指定漏れ");
    if (edit.kind === "between") {
      body = applyBetween(body, edit);
    } else {
      const re = new RegExp(edit.pattern, edit.flags);
      if (!re.test(body)) throw new Error(`正規表現に一致しない: ${edit.pattern}`);
      body = body.replace(new RegExp(edit.pattern, edit.flags), edit.replacement);
    }
  }

  if (body === before) {
    console.error("変更なし。マーカーと置換内容を確認する");
    return 1;
  }

  if (opts.dryRun) {
    let i = 0;
    while (i < before.length && i < body.length && before[i] === body[i]) i += 1;
    console.log(
      JSON.stringify(
        {
          endpoint: opts.endpoint,
          dry_run: true,
          length_before: before.length,
          length_after: body.length,
          first_difference_at: i,
          before_context: before.slice(Math.max(0, i - 40), i + 40),
          after_context: body.slice(Math.max(0, i - 40), i + 40),
        },
        null,
        2,
      ),
    );
    return 0;
  }

  const updated = JSON.parse(
    execFileSync("gh", ["api", "--method", "PATCH", opts.endpoint, "--input", "-"], {
      input: JSON.stringify({ body }),
      encoding: "utf8",
      maxBuffer: 32 * 1024 * 1024,
    }),
  );
  console.log(
    JSON.stringify(
      { id: updated.id, html_url: updated.html_url, updated_at: updated.updated_at, body_length: updated.body.length },
      null,
      2,
    ),
  );
  return 0;
}

try {
  process.exit(main());
} catch (err) {
  console.error(`エラー: ${err.message}`);
  process.exit(1);
}
