---
name: document-processing
description: |
  Extract, edit, and generate documents. Covers OCR and text extraction from PDFs/scanned files,
  natural-language PDF editing (nano-pdf), and PDF generation with Japanese text support (reportlab).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [documents, pdf, ocr, text-extraction, editing, reportlab, japanese]
    related_skills: [powerpoint, notion]
---

# Document Processing

This skill covers text extraction from documents, PDF editing, and PDF generation with internationalization support.

---

## OCR and Document Text Extraction

Extract text from PDFs and scanned documents using multiple strategies based on document type.

### Text-Based PDFs (selectable text)
Use `pymupdf` (PyMuPDF):
```python
import fitz  # PyMuPDF
doc = fitz.open("paper.pdf")
text = "\n".join(page.get_text() for page in doc)
```

### Scanned / Image-Based PDFs (needs OCR)
Use `marker-pdf`:
```bash
marker_single paper.pdf --output-dir /tmp/extracted/
```

### Remote PDFs
Use `web_extract` for URLs, or download first then process locally.

### DOCX Files
Use `python-docx`:
```python
from docx import Document
doc = Document("file.docx")
text = "\n".join(p.text for p in doc.paragraphs)
```

### Pitfalls
- `marker-pdf` requires significant memory for large documents.
- PyMuPDF may miss text in complex layouts (multi-column, tables).
- For PPTX extraction, use the `powerpoint` skill.

---

## Natural-Language PDF Editing (nano-pdf)

Edit PDFs by describing changes in natural language.

### Setup
```bash
pip install nano-pdf
```

### Usage
```bash
# Fix typos
nano-pdf edit document.pdf --instruction "Fix the typo 'recieve' to 'receive' on page 3"

# Update titles
nano-pdf edit document.pdf --instruction "Change the title on page 1 to 'New Title'"
```

### Pitfalls
- nano-pdf works best on text-based PDFs. Scanned/image PDFs need OCR first.
- Complex formatting (tables, multi-column) may not be preserved exactly.
- Always verify the output PDF visually before discarding the original.

---

## PDF Generation with Japanese Text (reportlab)

Generate PDFs with Japanese support on NixOS/Linux, avoiding common pitfalls with coordinate comparison and font loading.

### Setup
```bash
pip install reportlab
```

### Key Pitfalls
1. **Coordinate comparison**: reportlab uses exact float comparisons. Use `isSameIn()` or tolerant comparisons.
2. **Font loading**: Japanese fonts must be registered explicitly:
   ```python
   from reportlab.pdfbase import pdfmetrics
   from reportlab.pdfbase.ttfonts import TTFont
   pdfmetrics.registerFont(TTFont('JapaneseFont', '/path/to/NotoSansCJKJP-Regular.otf'))
   ```
3. **NixOS**: fonts may not be in standard paths. Use `fc-list` to discover available fonts.

### Example
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=A4)
c.setFont("JapaneseFont", 12)
c.drawString(100, 700, "日本語テキスト")
c.save()
```
