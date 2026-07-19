---
name: latex-editing
description: |
  Edit, review, and clean up LaTeX source files. Covers AI-generated LaTeX corruption patterns,
  patch-tool pitfalls with escaped characters and macros, fallback editing strategies when patch fails,
  and systematic QA review for logical coherence and typesetting correctness.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [latex, editing, patching, cleanup, ai-corruption, typesetting, review, qa]
---

# LaTeX Editing

This skill covers common problems when AI agents edit LaTeX source files: corruption from automated updates, patch-tool failures due to escaping, and systematic review workflows.

---

## AI Cleanup — Fixing AI-Generated LaTeX Corruption

When an AI has updated LaTeX files, specific corruption patterns often appear.

### Common Corruption Patterns

1. **Escaped newlines (`\\n`)**: AI sometimes inserts literal backslash-n instead of a newline.
   - Fix: replace `\\n` with actual newline characters.

2. **Non-ASCII symbols**: Smart quotes, em-dashes, or Unicode math symbols may be inserted.
   - Fix: replace with LaTeX equivalents (`---`, `` ` `` ``, `""` for quotes; `\text{...}` for Unicode).

3. **Broken math environments**: AI may split `\begin{equation}` across lines or mismatch delimiters.
   - Fix: verify every `\begin{...}` has a matching `\end{...}`.

4. **Over-escaped backslashes**: AI may double-escape (`\\alpha` instead of `\alpha`).
   - Fix: audit math mode for `\\` sequences that should be `\`.

### Verification Steps

1. Run `pdflatex` or `latexmk` and check for errors.
2. Inspect the `.log` file for missing font or encoding warnings.
3. Diff against the last known-good version to spot unintended changes.

---

## Patch Pitfalls — Editing LaTeX with the Patch Tool

The `patch` tool (and Hermes's `patch` action) often fails on LaTeX because of:

1. **Escaped characters**: backslashes, braces, and dollar signs confuse fuzzy matching.
2. **Macros with parameters**: `\newcommand{...}` blocks may span multiple lines.
3. **Whitespace sensitivity**: LaTeX ignores most whitespace, but patch does not.

### Strategies

- **Use `replace_all=false`** (default) and provide extra context lines so the match is unique.
- **Quote the old_string carefully**: if it contains backslashes, double-escape in the JSON payload.
- **Prefer `sed` or Python** for single-line macro replacements when `patch` keeps failing.
- **Break large changes into smaller patches**: replace one environment at a time.

---

## Handling Patch Failures — Fallback Editing

When standard patch tools fail on LaTeX due to hidden characters, escaping, or complex formatting:

1. **Switch to line-numbered replacement**: use `read_file` to find exact line numbers, then use `write_file` with a Python script to surgically replace the region.
2. **Use Python's `re` module**: for pattern-based replacements that don't need exact text matching.
3. **Use `latexdiff` for review**: generate a visual diff of old vs new before committing.
4. **Preserve a backup**: always keep `.bak` before bulk edits.

### Example: Surgical Python Replacement
```python
with open('paper.tex') as f:
    lines = f.readlines()
# Replace lines 45-50
lines[44:50] = ['new content\n']
with open('paper.tex', 'w') as f:
    f.writelines(lines)
```

---

## Review QA — Systematic LaTeX Review

Review LaTeX source files for both logical coherence and correct technical typesetting, specifically detecting AI-generated artifacts.

### Checklist

- [ ] All citations resolve (`\cite{...}` keys exist in `.bib`)
- [ ] Figures and tables are referenced before they appear
- [ ] Math environments are balanced (no unclosed `$`, `\[`, `\begin`)
- [ ] No smart quotes or non-ASCII in math mode
- [ ] Section hierarchy is consistent (`\section` > `\subsection` > `\subsubsection`)
- [ ] Tables use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`) not vertical lines
- [ ] Algorithm environments compile without `algorithmicx` version mismatches
- [ ] No hard-coded figure widths that break two-column layouts

### AI Artifact Detection
- Search for `TODO`, `FIXME`, or placeholder text left by AI.
- Check for hallucinated citations — verify every `\cite` against the `.bib` file.
- Verify that rewritten sections still match the original meaning (semantic drift).
