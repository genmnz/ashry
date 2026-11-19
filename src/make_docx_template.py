#!/usr/bin/env python3
"""Generate paper/template.docx, the reference document pandoc styles the thesis with.

A reference document is normally a binary dropped into the repository, which
nobody can review and nobody can change safely. This generates it from code
instead, so every typographic decision below is visible, explained and
adjustable in one place, and the file can be rebuilt from scratch.

`src/build_thesis.py` passes `--reference-doc paper/template.docx` whenever the
file exists, so running this script is the whole of the Word typography step.

The choices, and why:

* **Body 10.5pt Cambria, single spaced, 3pt after each paragraph.** A thesis
  is often typed double spaced, which exists to leave room for a marker's pen
  on paper and costs roughly forty per cent of the page count. This one is read
  on screen and presented from. Cambria has a large x-height, so it stays
  comfortable at this size. If an institution requires double spacing, run with
  THESIS_LINE_SPACING=2.0 and nothing else needs touching.
* **Margins 2.0cm, 2.3cm on the binding edge.** Every setting here was chosen
  by building the thesis, converting it to PDF with LibreOffice and counting
  the pages; the margins turned out to be the largest lever by far, because a
  millimetre either way reflows fifteen wide tables with it.
* **Sans-serif headings against a serif body.** The contrast makes the
  structure scannable, which matters in a document with six levels of numbered
  heading. Chapters start on a new page, which costs about eleven pages and is
  worth it.
* **Tables at 8pt, the bibliography at 9pt with a hanging indent.** Several
  tables here are eight columns wide; at body size they wrap and become
  unreadable. The reference entries are given their own style so that
  `src/build_thesis.py` can set them in two columns, which a list of short
  ragged entries wants.
* **No colour.** The document has to survive monochrome printing, so emphasis
  is carried by weight and size alone.
"""
from __future__ import annotations

import os

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "paper", "template.docx")

BODY_FONT = "Cambria"
HEAD_FONT = "Calibri"
MONO_FONT = "Consolas"

# Each of these can be overridden from the environment for a single run, e.g.
#   THESIS_LINE_SPACING=2.0 python3 src/make_docx_template.py
# which is how the settings below were chosen: build, convert to PDF with
# LibreOffice, count the pages, repeat.
def _num(name, default):
    return type(default)(os.environ.get(name, default))


BODY_SIZE = _num("THESIS_BODY_SIZE", 10.5)
LINE_SPACING = _num("THESIS_LINE_SPACING", 1.0)
SPACE_AFTER = _num("THESIS_SPACE_AFTER", 3.0)
TABLE_SIZE = _num("THESIS_TABLE_SIZE", 8.0)
PAGE_BREAK_CHAPTERS = os.environ.get("THESIS_CHAPTER_BREAKS", "1") == "1"
MARGIN = _num("THESIS_MARGIN", 2.0)
BIND_MARGIN = _num("THESIS_BIND_MARGIN", 2.3)

# (style name, size pt, bold, space before pt, space after pt)
HEADINGS = [
    ("Title",     20, True,  0,  14),
    ("Heading 1", 16, True,  0,   9),
    ("Heading 2", 13, True, 13,   5),
    ("Heading 3", 11.5, True, 10,  4),
    ("Heading 4", 10.5, True, 9,   3),
    ("Heading 5", 10.5, True, 8,   3),
    ("Heading 6", 10, True,  8,    3),
]


def set_font(style, name, size=None, bold=None, italic=None, colour=True):
    f = style.font
    f.name = name
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if colour:
        f.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    # python-docx sets only the latin font; east-asian and complex-script runs
    # fall back to the document default unless these are set too, which is how
    # a stray Calibri appears in the middle of a serif paragraph.
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def page_number_footer(section):
    """A centred PAGE field in the footer.

    Word stores a page number as a field, not as text, so it has to be built
    from the three runs Word expects: begin, instruction, end.
    """
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    # A field is three elements: a w:fldChar of type "begin", the instruction
    # itself, and a w:fldChar of type "end". The element name is w:fldChar for
    # both ends; naming them anything else leaves the reader with nothing but
    # the instruction run, which is why a malformed field prints "PAGE".
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for el in (begin, instr, end):
        run._r.append(el)
    set_font_run(run, BODY_FONT, 9)


def set_font_run(run, name, size):
    run.font.name = name
    run.font.size = Pt(size)
    rpr = run._r.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def main():
    doc = Document()

    for s in doc.sections:
        s.top_margin = Cm(MARGIN)
        s.bottom_margin = Cm(MARGIN)
        s.left_margin = Cm(BIND_MARGIN)      # binding edge
        s.right_margin = Cm(MARGIN)
        page_number_footer(s)

    normal = doc.styles["Normal"]
    set_font(normal, BODY_FONT, BODY_SIZE)
    pf = normal.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = LINE_SPACING
    pf.space_after = Pt(SPACE_AFTER)
    pf.space_before = Pt(0)
    pf.widow_control = True

    for name, size, bold, before, after in HEADINGS:
        try:
            st = doc.styles[name]
        except KeyError:
            continue
        set_font(st, HEAD_FONT, size, bold)
        st.font.italic = False
        p = st.paragraph_format
        p.space_before = Pt(before)
        p.space_after = Pt(after)
        p.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.line_spacing = 1.0
        p.keep_with_next = True       # never leave a heading alone at a page foot
        p.page_break_before = False

    # Chapters start on a new page; pandoc maps "# " to Heading 1.
    if PAGE_BREAK_CHAPTERS:
        doc.styles["Heading 1"].paragraph_format.page_break_before = True

    for name, size in (("Source Code", TABLE_SIZE), ("Verbatim Char", TABLE_SIZE)):
        try:
            set_font(doc.styles[name], MONO_FONT, size)
        except KeyError:
            pass

    for name in ("Caption", "Image Caption", "Table Caption"):
        try:
            st = doc.styles[name]
        except KeyError:
            continue
        set_font(st, BODY_FONT, 9)
        st.font.italic = True
        st.paragraph_format.space_before = Pt(4)
        st.paragraph_format.space_after = Pt(10)
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # "Compact" is the style pandoc gives every item of a tight list, which in
    # this document means most of the lists in the body. It belongs at body
    # size with a little less space after it, not at table size.
    try:
        c = doc.styles["Compact"]
        set_font(c, BODY_FONT, BODY_SIZE)
        cp = c.paragraph_format
        cp.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        cp.line_spacing = LINE_SPACING
        cp.space_after = Pt(max(1.0, SPACE_AFTER - 2))
    except KeyError:
        pass

    # The bibliography, set smaller and tighter with a hanging indent. The
    # style has to exist in the reference document for pandoc's
    # custom-style div to resolve to it.
    from docx.enum.style import WD_STYLE_TYPE
    try:
        bib = doc.styles.add_style("Bibliography Entry", WD_STYLE_TYPE.PARAGRAPH)
    except Exception:
        bib = doc.styles["Bibliography Entry"]
    set_font(bib, BODY_FONT, 9)
    bp = bib.paragraph_format
    bp.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    bp.line_spacing = 1.0
    bp.space_after = Pt(2)
    bp.space_before = Pt(0)
    bp.left_indent = Cm(0.7)
    bp.first_line_indent = Cm(-0.7)

    try:
        q = doc.styles["Quote"]
        set_font(q, BODY_FONT, BODY_SIZE)
        q.font.italic = True
        q.paragraph_format.left_indent = Cm(1.0)
    except KeyError:
        pass

    # Table text has to be set on the table styles pandoc actually uses, and
    # pandoc writes its tables with the "Table" style, falling back to
    # "Table Grid". Setting Normal alone does not reach them.
    for name in ("Table", "Table Grid", "Table Normal"):
        try:
            set_font(doc.styles[name], BODY_FONT, TABLE_SIZE)
        except KeyError:
            continue

    # A one-row sample table makes the style concrete in the reference file,
    # which is what pandoc copies from.
    t = doc.add_table(rows=1, cols=1)
    try:
        t.style = doc.styles["Table Grid"]
    except KeyError:
        pass
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    cell.text = ""
    set_font_run(cell.paragraphs[0].add_run(""), BODY_FONT, TABLE_SIZE)

    doc.save(OUT)
    print(f"wrote {OUT}")
    print(f"  body    {BODY_FONT} {BODY_SIZE}pt, line spacing {LINE_SPACING}, "
          f"{SPACE_AFTER}pt after")
    print(f"  headings {HEAD_FONT}, chapters break to a new page")
    print(f"  tables  {TABLE_SIZE}pt; margins {MARGIN}cm with a {BIND_MARGIN}cm binding edge; "
          "centred page numbers")


if __name__ == "__main__":
    main()
