"""
Thesis figures. One file, one style, every figure regenerated from the CSVs in
results/tables so that nothing in the manuscript is hand-drawn.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
TABLES = REPO / "results" / "tables"
FIGS = REPO / "results" / "figures"

INK = "#1d1d1f"
GRID = "#d9d9de"
PALETTE = {
    "dairy-casein": "#3b6ea5",
    "dairy-whey": "#5aa9a3",
    "egg": "#d6a243",
    "heme": "#b4553f",
    "reference": "#8a8a92",
}
LABEL = {
    "alpha_s1_casein": "αS1-casein", "alpha_s2_casein": "αS2-casein",
    "beta_casein": "β-casein", "kappa_casein": "κ-casein",
    "beta_lactoglobulin": "β-lactoglobulin", "alpha_lactalbumin": "α-lactalbumin",
    "ovalbumin": "ovalbumin", "leghemoglobin_c2": "leghemoglobin C2",
    "lactoferrin_bovine": "lactoferrin",
}


def style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GRID)
    ax.tick_params(colors=INK, labelsize=9, length=3, color=GRID)
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("title",):
        pass


def save(fig, name: str) -> None:
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGS / f"{name}.png", dpi=220, bbox_inches="tight",
                facecolor="white")
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {name}")


def fig_yields() -> None:
    df = pd.read_csv(TABLES / "protein_yields.csv")
    df = df[(df.atp_per_bond == 4.3) & (df.charge_ptms)
            & (df.get("mannose_per_glycan", 9.0) == 9.0)]
    piv = df.pivot_table(index="protein", columns="substrate",
                         values="g_protein_per_g_substrate")
    piv = piv.loc[[k for k in LABEL if k in piv.index]]

    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    x = range(len(piv))
    w = 0.26
    for i, (sub, colour) in enumerate((("glycerol", "#3b6ea5"),
                                       ("glucose", "#5aa9a3"),
                                       ("methanol", "#b4553f"))):
        if sub not in piv:
            continue
        ax.bar([xi + (i - 1) * w for xi in x], piv[sub], width=w,
               label=sub, color=colour, edgecolor="white", lw=0.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels([LABEL[i] for i in piv.index], rotation=35, ha="right")
    ax.set_ylabel("maximum theoretical yield\n(g protein / g substrate)")
    ax.set_title("Stoichiometric ceiling barely distinguishes the proteins;\n"
                 "the carbon source does", color=INK, fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=9)
    style(ax)
    save(fig, "fig1_theoretical_yields")


def fig_ptm_cost() -> None:
    df = pd.read_csv(TABLES / "ptm_cost.csv")
    df = df[df.substrate == "glycerol"].set_index("protein")
    df = df.loc[[k for k in LABEL if k in df.index]]

    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    colours = [PALETTE.get(c, "#8a8a92") for c in df.category]
    ax.bar([LABEL[i] for i in df.index], df.ptm_polypeptide_penalty_pct,
           color=colours, edgecolor="white", lw=0.5)
    for i, (name, r) in enumerate(df.iterrows()):
        tag = []
        if r.disulfides:
            tag.append(f"{int(r.disulfides)} S-S")
        if r.n_glyc:
            tag.append(f"{int(r.n_glyc)} N-glyc")
        if r.phosphoserines:
            tag.append(f"{int(r.phosphoserines)} pSer")
        if r.haem:
            tag.append("haem")
        ax.text(i, r.ptm_polypeptide_penalty_pct + 0.15, ", ".join(tag), ha="center",
                fontsize=7, color=INK, rotation=0)
    ax.set_ylabel("yield penalty of the\npost-translational load (%)")
    ax.set_title("Phosphorylation is free; glycosylation costs polypeptide yield",
                 color=INK,
                 fontsize=11, loc="left")
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")
    style(ax)
    save(fig, "fig2_ptm_cost")


def fig_glycan() -> None:
    path = TABLES / "glycan_scenarios.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for i, (prot, sub) in enumerate(df.groupby("protein")):
        sub = sub.sort_values("mannose_per_glycan")
        colour = f"C{i}"
        ax.plot(sub.mannose_per_glycan, sub.g_polypeptide_per_g_substrate,
                marker="o", ms=4, lw=1.9, color=colour,
                label=f"{LABEL.get(prot, prot)} — polypeptide")
        ax.plot(sub.mannose_per_glycan, sub.g_protein_per_g_substrate,
                marker="s", ms=3.5, lw=1.2, ls="--", color=colour, alpha=0.75,
                label=f"{LABEL.get(prot, prot)} — glycoprotein mass")
    ax.set_xlabel("mannose residues per N-glycan")
    ax.set_ylabel("maximum theoretical yield\n(g protein / g glycerol)")
    ax.set_title("Hypermannosylation raises the mass yield and destroys the\n"
                 "protein yield", color=INK, fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=7.5, ncol=1)
    style(ax)
    save(fig, "fig3_hypermannosylation")


def fig_gap() -> None:
    path = TABLES / "efficiency_gap.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    df = df[df.substrate_loading_g_L == 350.0]
    best = df.sort_values("titer_g_L", ascending=False).groupby("protein").head(1)
    best = best.sort_values("fraction_of_ceiling")

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    y = range(len(best))
    ax.barh(list(y), best.ceiling_g_L, color="#e4e7ec", edgecolor="white",
            label="stoichiometric ceiling")
    ax.barh(list(y), best.titer_g_L, color="#3b6ea5", edgecolor="white",
            label="best published titre")
    for i, r in enumerate(best.itertuples()):
        ax.text(r.ceiling_g_L * 1.02, i, f"{r.gap_fold:.0f}×", va="center",
                fontsize=8, color=INK)
    ax.set_yticks(list(y))
    ax.set_yticklabels([LABEL.get(p, p) for p in best.protein])
    ax.set_xscale("log")
    ax.set_xlabel("g / L (log scale), at 350 g/L substrate loading")
    ax.set_title("Published titres sit one to three orders of magnitude\n"
                 "below the stoichiometric ceiling", color=INK, fontsize=11,
                 loc="left")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.yaxis.grid(False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    save(fig, "fig4_efficiency_gap")


def fig_tea() -> None:
    path = TABLES / "tea_titer_yield_grid.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for yfrac, sub in df.groupby("yield_frac_of_theoretical"):
        sub = sub.sort_values("titer_g_L")
        ax.plot(sub.titer_g_L, sub.cost_usd_per_kg, marker="o", ms=4, lw=1.8,
                label=f"{yfrac:.0%} of theoretical yield")
    ax.axhline(20, color="#b4553f", ls="--", lw=1.2)
    ax.text(df.titer_g_L.max(), 21, "$20/kg commodity target", ha="right",
            fontsize=8, color="#b4553f")
    ax.set_xlabel("titre (g/L)")
    ax.set_ylabel("production cost (USD / kg)")
    ax.set_yscale("log")
    ax.set_title("Titre, not carbon efficiency, sets the cost", color=INK,
                 fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=8)
    style(ax)
    save(fig, "fig5_tea_cost")


def fig_features() -> None:
    path = TABLES / "target_features.csv"
    if not path.exists():
        return
    df = pd.read_csv(path).set_index("protein")
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for prot, r in df.iterrows():
        colour = PALETTE.get(r.category, "#8a8a92")
        ax.scatter(r.scaled_hydropathy, abs(r.net_charge_per_res), s=70,
                   color=colour, edgecolor="white", zorder=3)
        ax.annotate(LABEL.get(prot, prot), (r.scaled_hydropathy,
                                            abs(r.net_charge_per_res)),
                    textcoords="offset points", xytext=(6, 4), fontsize=8,
                    color=INK)
    xs = [0.30, 0.65]
    ax.plot(xs, [2.785 * x - 1.151 for x in xs], color="#b4553f", lw=1.3,
            ls="--")
    ax.text(0.615, 2.785 * 0.615 - 1.151 + 0.01, "Uversky boundary", fontsize=8,
            color="#b4553f", ha="right")
    ax.set_xlabel("mean scaled hydropathy")
    ax.set_ylabel("absolute mean net charge per residue")
    ax.set_title("The caseins fall on the disordered side of the\n"
                 "charge-hydropathy boundary", color=INK, fontsize=11, loc="left")
    style(ax)
    save(fig, "fig6_charge_hydropathy")


def main() -> None:
    print("figures:")
    for fn in (fig_yields, fig_ptm_cost, fig_glycan, fig_gap, fig_tea,
               fig_features):
        try:
            fn()
        except Exception as exc:  # pragma: no cover
            print(f"  skipped {fn.__name__}: {exc}")


if __name__ == "__main__":
    main()
