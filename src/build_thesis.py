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
        "### 5.2.2 Nobody is close to the ceiling",
        "**Figure 5.2** The ceiling varies 1.38-fold across 24 proteins; the "
        "fraction of it achieved varies 628-fold. A property with this little "
        "variation cannot explain an outcome with that much."),
    "fig6_charge_hydropathy": (
        "## 6.2 The positive result: disulfide density",
        "**Figure 6.1** Charge-hydropathy placement of the panel. The caseins fall "
        "on the disordered side of the Uversky boundary, as expected; Chapter 6 "
        "nevertheless finds that predicted disorder carries no association with "
        "titre among the proteins that have one."),
    "fig5_tea_cost": (
        "## 8.3 What actually drives the cost",
        "**Figure 8.1** Production cost against titre at four levels of realised "
        "carbon efficiency. The curves are nearly superimposed: titre moves the "
        "cost, carbon efficiency barely does."),
}


def assemble() -> str:
    parts: list[str] = []
    for name in CHAPTERS:
        text = (PAPER / name).read_text()
        for fig, (anchor, caption) in FIGURES.items():
            if anchor in text:
                img = f"\n\n![{caption}](../results/figures/{fig}.png)\n\n{caption}\n"
                # place the figure after the anchor's paragraph block
                idx = text.index(anchor) + len(anchor)
                nxt = text.find("\n## ", idx)
                nxt = len(text) if nxt == -1 else nxt
                text = text[:nxt] + img + text[nxt:]
        parts.append(text)
    return "\n\n---\n\n".join(parts)


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
                                              "--toc-depth=3",
                                              "--embed-resources"]),
                            ("docx", "docx", ["--toc"] + (
                                ["--reference-doc", str(TEMPLATE)]
                                if TEMPLATE.exists() else []))):
        target = OUT / f"thesis.{ext}"
        cmd = ["pandoc", str(md_path), "-f", "markdown", "-t", fmt,
               "-o", str(target), "--resource-path", str(PAPER)] + extra
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            print(f"  wrote {target} ({target.stat().st_size // 1024} KB)")
        except subprocess.CalledProcessError as exc:
            print(f"  {fmt} failed: {exc.stderr.decode()[:300]}")
        except FileNotFoundError:
            print("  pandoc not available")


if __name__ == "__main__":
    main()
