"""
Assemble the thesis from its chapter files, inject the figures at the points
they are discussed, and render to Markdown, HTML and Word.

The chapters are written as separate files so they can be revised independently;
nothing is hand-assembled, so a regenerated figure or a corrected chapter always
propagates to the output document.
"""
from __future__ import annotations

import subprocess
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / "paper"
FIGS = REPO / "results" / "figures"
OUT = PAPER / "build"

CHAPTERS = [
    "01_front_matter.md",
    "02_introduction.md",
    "03_literature_review.md",
    "04_methods.md",
    "05_results_ceiling.md",
    "06_results_gap.md",
    "07_results_predictors.md",
    "08_results_engineering.md",
    "09_results_economics.md",
    "10_discussion.md",
    "11_appendices.md",
    "12_references.md",
]

# figure -> (anchor heading it follows, caption)
FIGURES = {
    "fig1_theoretical_yields": (
        "### 4.1.1 Why the proteins converge",
        "**Figure 4.1** Maximum theoretical yield of each panel protein on "
        "glycerol, glucose and methanol, computed in iMT1026v3 with an explicit "
        "sequence-derived synthesis reaction and the full post-translational load "
        "charged. The protein changes the ceiling by under 10%; the carbon source "
        "changes it by about 30%."),
    "fig2_ptm_cost": (
        "### 4.3.1 Phosphorylation is free",
        "**Figure 4.2** Yield penalty of the post-translational load on a "
        "polypeptide basis. Phosphorylation, however many sites, costs almost "
        "nothing; disulfide bonding is nearly free; glycosylation dominates."),
    "fig3_hypermannosylation": (
        "### 4.3.4 Hypermannosylation, and why reporting one yield number misleads",
        "**Figure 4.3** Yeast outer-chain extension scanned from the ER core "
        "glycan (Man9) to Man100. Solid lines: polypeptide yield, which falls. "
        "Dashed lines: glycoprotein mass yield, which rises. A process measured on "
        "the wrong basis looks better as it gets worse."),
    "fig4_efficiency_gap": (
        "### 5.2.1 The headline contrast",
        "**Figure 5.1** Best published titre against the stoichiometric ceiling of "
        "the same protein, at 350 g/L substrate loading, log scale. Labels give the "
        "gap in fold. No published process exceeds 8.3% of its own ceiling."),
    "fig7_ceiling_vs_achievement": (
        "### 5.2.3 Nobody is close to the ceiling",
        "**Figure 5.2** The ceiling against the fraction of it achieved, one "
        "point per protein using that protein's best record (n = 26). On this "
        "basis the ceiling varies 1.31-fold (log10 SD 0.029) and utilisation "
        "of it varies with a log10 SD of 0.851; the per-record figures in "
        "§5.2.2 are 1.26-fold, 0.0193 and 0.892. A property "
        "with this little variation cannot explain an outcome with that much."),
    "fig6_charge_hydropathy": (
        "## 6.2 The result that did not survive",
        "**Figure 6.1** Charge-hydropathy placement of the panel. The caseins "
        "fall on the disordered side of the Uversky boundary, as expected; "
        "Chapter 6 nevertheless finds that disorder as pre-specified carries no "
        "association with ceiling utilisation, and §6.5 records why the "
        "association found for an alternative statistic was not reported as a "
        "finding."),
    "fig5_tea_cost": (
        "## 8.3 What actually drives the cost",
        "**Figure 8.1** Production cost against titre at four levels of realised "
        "carbon efficiency. The curves are nearly superimposed: titre moves the "
        "cost, carbon efficiency barely does."),
}


def dense_bibliography(text: str) -> str:
    """Set the reference entries as their own, denser paragraph style.

    A bibliography is conventionally set smaller and tighter than the body, and
    this one is long. Pandoc passes a `custom-style` div straight through to a
    Word paragraph style, so each run of bullet entries becomes a block of
    "Bibliography Entry" paragraphs, which `src/make_docx_template.py` defines
    at 9pt with a hanging indent. The bullet goes with it, which is what a
    hanging indent replaces.
    """
    out: list[str] = []
    run: list[str] = []

    def flush() -> None:
        if not run:
            return
        out.append('::: {custom-style="Bibliography Entry"}\n')
        out.extend(run)
        out.append(":::\n")
        run.clear()

    for line in text.split("\n"):
        if line.startswith("- "):
            # a blank line between entries, or Markdown runs them into one
            # paragraph and the whole block arrives in Word as a single run-on
            run.append(line[2:] + "\n\n")
        else:
            flush()
            out.append(line + "\n")
    flush()
    return "".join(out)


def assemble() -> str:
    parts: list[str] = []
    for name in CHAPTERS:
        text = (PAPER / name).read_text()
        if name == "12_references.md":
            text = dense_bibliography(text)
        for fig, (anchor, caption) in FIGURES.items():
            if anchor in text:
                # The alt text is what pandoc turns into the figure's caption
                # paragraph, so it must not also be repeated as body text, and
                # the explicit width keeps a 220-dpi plot inside the text block
                # instead of being scaled to the full page.
                img = (f"\n\n![{caption}]"
                       f"(../results/figures/{fig}.png){{width=13.5cm}}\n")
                # place the figure after the anchor's paragraph block
                idx = text.index(anchor) + len(anchor)
                nxt = text.find("\n## ", idx)
                nxt = len(text) if nxt == -1 else nxt
                text = text[:nxt] + img + text[nxt:]
        parts.append(text)
    # Chapters are joined with a blank line, not a horizontal rule: the Word
    # template already starts each chapter on a new page, and a rule on top of
    # that leaves a stray line on an otherwise empty page.
    return "\n\n".join(parts)


def two_column_bibliography(path) -> str:
    """Set the reference list in two columns.

    A bibliography is a list of short, ragged entries, and a single column of
    them across a full page wastes most of each line and runs to several pages
    more than it needs. Two columns is the convention in journals for the same
    reason.

    Word stores column settings per section, so this inserts a section break on
    the References heading: everything up to and including the heading stays in
    the one-column section, and the entries after it fall into a two-column one.
    The heading's own "start on a new page" is cleared at the same time, because
    the section break already starts the page and the two together leave a blank
    page between them.
    """
    try:
        from docx import Document
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        import copy
    except ImportError:
        return "python-docx not installed; bibliography left in one column"

    doc = Document(str(path))
    body = doc.element.body
    body_sect = body.find(qn("w:sectPr"))
    if body_sect is None:
        return "no section properties found"

    target = None
    for para in doc.paragraphs:
        if para.style.name == "Heading 1" and para.text.strip().lower() == "references":
            target = para
            break
    if target is None:
        return "no References heading found"

    # the one-column section ends with the heading
    first = copy.deepcopy(body_sect)
    for existing in first.findall(qn("w:cols")):
        first.remove(existing)
    cols = OxmlElement("w:cols")
    cols.set(qn("w:num"), "1")
    first.append(cols)
    ppr = target._p.get_or_add_pPr()
    for brk in ppr.findall(qn("w:pageBreakBefore")):
        ppr.remove(brk)
    brk = OxmlElement("w:pageBreakBefore")
    brk.set(qn("w:val"), "false")
    ppr.append(brk)
    ppr.append(first)

    # everything after it is two columns with a 0.7cm gutter
    for existing in body_sect.findall(qn("w:cols")):
        body_sect.remove(existing)
    cols2 = OxmlElement("w:cols")
    cols2.set(qn("w:num"), "2")
    cols2.set(qn("w:space"), "397")      # twentieths of a point, ~0.7cm
    cols2.set(qn("w:equalWidth"), "1")
    body_sect.append(cols2)

    doc.save(str(path))
    return "references set in two columns"


# Without this the standalone HTML is titled "thesis" in the browser tab.
HTML_TITLE = ("Stoichiometric production ceilings and realised titres "
              "in recombinant food proteins")

INSTITUTION = PAPER / "00_institution.yaml"
TEMPLATE = PAPER / "template.docx"

# The order these appear on a title page, with the label used when the value is
# still unfilled. A null field renders as a bracketed placeholder so that it is
# visible on the page rather than silently missing.
TITLE_FIELDS = [
    ("author", "AUTHOR'S FULL NAME"),
    ("student_id", "STUDENT NUMBER"),
    ("degree", "DEGREE"),
    ("department", "DEPARTMENT"),
    ("faculty", "FACULTY"),
    ("institution", "INSTITUTION"),
    ("city", "CITY"),
    ("country", "COUNTRY"),
    ("supervisor", "SUPERVISOR"),
    ("co_supervisor", None),          # optional: omitted entirely when unset
    ("submission_month", "MONTH AND YEAR OF SUBMISSION"),
    ("academic_year", "ACADEMIC YEAR"),
]


def read_institution() -> dict:
    """Minimal YAML read: flat key: value pairs, no dependency on PyYAML."""
    out: dict[str, str | None] = {}
    if not INSTITUTION.exists():
        return out
    for line in INSTITUTION.read_text().splitlines():
        line = line.split("#")[0].rstrip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip().strip('"').strip("'")
        out[key.strip()] = None if value in ("", "null", "~") else value
    return out


def institutional_front_matter(inst: dict) -> str:
    """Title page, declaration and signature block from 00_institution.yaml."""
    def v(key: str, placeholder: str | None) -> str | None:
        val = inst.get(key)
        if val:
            return str(val)
        return f"[{placeholder}]" if placeholder else None

    lines = ["<div style=\"page-break-after: always\"></div>", "",
             "## Title page", ""]
    for key, placeholder in TITLE_FIELDS:
        got = v(key, placeholder)
        if got is None:
            continue
        label = key.replace("_", " ").title()
        lines.append(f"**{label}:** {got}")
        lines.append("")

    author = v("author", "AUTHOR'S FULL NAME")
    inst_name = v("institution", "INSTITUTION")
    lines += [
        "<div style=\"page-break-after: always\"></div>", "",
        "## Declaration", "",
        f"I, {author}, declare that this thesis is my own work and that all "
        "sources used have been acknowledged. The computational analysis, the "
        "code in the accompanying repository and the writing are my own. No "
        "part of this work has been submitted for any other degree or "
        f"qualification at {inst_name} or elsewhere.",
        "",
        "The analysis is entirely computational. No wet-laboratory work was "
        "performed, and no experimental data generated by the author is "
        "reported. Every quantitative result derives from the published sources "
        "cited and from the code in the accompanying repository, and is "
        "reproducible by the procedure in Appendix D.",
        "",
        "Signed: ______________________________    Date: __________________",
        "",
        f"{author}",
        "",
    ]
    sup = v("supervisor", "SUPERVISOR")
    lines += [
        "**Supervisor's approval.** I confirm that this thesis was prepared "
        "under my supervision and that it is submitted with my approval.",
        "",
        "Signed: ______________________________    Date: __________________",
        "",
        f"{sup}",
        "",
    ]
    if inst.get("co_supervisor"):
        lines += ["Signed: ______________________________    Date: "
                  "__________________", "", str(inst["co_supervisor"]), ""]
    lines.append("<div style=\"page-break-after: always\"></div>")
    lines.append("")
    return "\n".join(lines)


FIG_RE = re.compile(r"^\*\*(Figure [0-9]+\.[0-9]+)\*\*\s+(.+)$", re.M)
TAB_RE = re.compile(r"^\*\*(Table [0-9]+\.[0-9]+)\s+[—-]\s+(.+?)\*\*\s*$", re.M)


def _first_sentence(text: str, limit: int = 150) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    cut = text.find(". ")
    if 0 < cut < limit:
        return text[:cut]
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"


def front_lists(md: str) -> str:
    """A list of figures and a list of tables, read off the assembled text."""
    figs, seen = [], set()
    for num, rest in FIG_RE.findall(md):
        if num in seen:
            continue
        seen.add(num)
        figs.append((num, _first_sentence(rest)))
    tabs, seen = [], set()
    for num, rest in TAB_RE.findall(md):
        if num in seen:
            continue
        seen.add(num)
        tabs.append((num, _first_sentence(rest)))

    out = ["<div style=\"page-break-after: always\"></div>", "",
           "## List of figures", ""]
    out += [f"- **{n}** — {c}" for n, c in figs] or ["- (none)"]
    out += ["", "<div style=\"page-break-after: always\"></div>", "",
            "## List of tables", ""]
    out += [f"- **{n}** — {c}" for n, c in tabs] or ["- (none)"]
    out += ["", "<div style=\"page-break-after: always\"></div>", ""]
    print(f"  listed {len(figs)} figures and {len(tabs)} tables")
    return "\n".join(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inst = read_institution()
    md = assemble()
    # Insert the institutional pages after the document title, before the
    # abstract, which is where every template this is likely to meet puts them.
    front = institutional_front_matter(inst)
    marker = "\n## Abstract"
    if marker in md:
        md = md.replace(marker, "\n" + front + marker, 1)
    else:
        md = front + md
    # Lists of figures and tables go after the abstract and acknowledgements,
    # immediately before Chapter 1, which is where a thesis template puts them.
    ch1 = "\n# Chapter 1 "
    if ch1 in md:
        md = md.replace(ch1, "\n" + front_lists(md) + ch1, 1)
    unfilled = [k for k, ph in TITLE_FIELDS
                if ph and not inst.get(k)]
    if unfilled:
        print(f"  institutional fields still unfilled ({len(unfilled)}): "
              + ", ".join(unfilled))
        print("  -> they render as bracketed placeholders; fill "
              "paper/00_institution.yaml")
    else:
        print("  institutional front matter complete")
    md_path = OUT / "thesis.md"
    md_path.write_text(md)
    words = len(md.split())
    print(f"assembled {len(CHAPTERS)} chapters, {words:,} words -> {md_path}")
    if TEMPLATE.exists():
        print(f"  using institutional template {TEMPLATE}")

    for fmt, ext, extra in (("html", "html", ["--standalone", "--toc",
                                              "--toc-depth=2",
                                              "--embed-resources",
                                              "--css", str(PAPER / "thesis.css"),
                                              "--metadata", "title=" + HTML_TITLE]),
                            ("docx", "docx", ["--toc", "--toc-depth=2"] + (
                                ["--reference-doc", str(TEMPLATE)]
                                if TEMPLATE.exists() else []))):
        target = OUT / f"thesis.{ext}"
        cmd = ["pandoc", str(md_path), "-f", "markdown", "-t", fmt,
               "-o", str(target), "--resource-path", str(PAPER)] + extra
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            print(f"  wrote {target} ({target.stat().st_size // 1024} KB)")
            if fmt == "docx":
                print(f"  {two_column_bibliography(target)}")
        except subprocess.CalledProcessError as exc:
            print(f"  {fmt} failed: {exc.stderr.decode()[:300]}")
        except FileNotFoundError:
            print("  pandoc not available")


if __name__ == "__main__":
    main()
