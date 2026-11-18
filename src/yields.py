#!/usr/bin/env python3
"""Maximum theoretical yield of recombinant protein per gram of substrate.

For each protein in the curated panel, insert the balanced synthesis reaction
into iMT1026v3, fix the substrate uptake, and maximise secretion.  Two regimes
are reported:

  * `nongrowth` - growth blocked, only the non-growth maintenance ATP demand
    is met.  This is the thermodynamic ceiling: g protein per g substrate if
    the whole carbon flux went to the product.
  * `coupled`   - growth fixed at a specified specific growth rate, so that
    the yield is what a producing, dividing culture could reach.

Carbon sources: glycerol, methanol, glycerol+methanol (the standard K. phaffii
two-phase process), and glucose.
"""
from __future__ import annotations

import json
import os
import sys

import cobra
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from protein_cost import (CostParams, ProteinSpec, build_reactions,  # noqa: E402
                          compute_cost)

MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "data", "models", "kphaffii_imt1026v3", "iMT1026v3.xml")

# g/mol of the substrates, for mass-basis yields
MW = {"glycerol": 92.09382, "methanol": 32.04186, "glucose": 180.15588}

SUBSTRATES = {
    # name -> {exchange id: mmol/gDW/h uptake}, and the matching biomass rxn
    "glycerol":   ({"Ex_glyc": 10.0}, "BIOMASS_glyc"),
    "methanol":   ({"Ex_meoh": 10.0}, "BIOMASS_meoh"),
    "glyc_meoh":  ({"Ex_glyc": 5.0, "Ex_meoh": 5.0}, "BIOMASS6040"),
    "glucose":    ({"Ex_glc_D": 10.0}, "BIOMASS_glyc"),
}


def load_model():
    import logging
    logging.disable(logging.CRITICAL)
    return cobra.io.read_sbml_model(MODEL)


def _configure(model, subs, biomass_rxn):
    """Open exactly one substrate set; select the matching biomass equation."""
    for rid in ("Ex_glyc", "Ex_meoh", "Ex_glc_D"):
        model.reactions.get_by_id(rid).lower_bound = 0.0
    for rid, up in subs.items():
        model.reactions.get_by_id(rid).lower_bound = -float(up)
    for rid in ("BIOMASS", "BIOMASS_glyc", "BIOMASS_meoh", "BIOMASS8020",
                "BIOMASS6040", "BIOMASS4060", "BIOMASS8020b", "BIOMASS6040b",
                "BIOMASS4060b"):
        if rid in model.reactions:
            model.reactions.get_by_id(rid).bounds = (0.0, 0.0)
    model.reactions.get_by_id(biomass_rxn).bounds = (0.0, 1000.0)
    model.reactions.get_by_id("Ex_o2").lower_bound = -1000.0


def substrate_g_per_h(subs):
    g = 0.0
    key = {"Ex_glyc": "glycerol", "Ex_meoh": "methanol", "Ex_glc_D": "glucose"}
    for rid, up in subs.items():
        g += up * MW[key[rid]] / 1000.0      # mmol/h * g/mol / 1000 = g/h
    return g


def max_yield(model, spec: ProteinSpec, params: CostParams,
              substrate: str, mu: float = 0.0):
    """g protein secreted per g substrate consumed, at growth rate `mu`."""
    subs, biomass_rxn = SUBSTRATES[substrate]
    with model:
        _configure(model, subs, biomass_rxn)
        cost, rxn, sink = build_reactions(model, spec, params)
        model.reactions.get_by_id("growth").bounds = (mu, mu)
        model.objective = sink
        sol = model.optimize()
        if sol.status != "optimal":
            return None
        v = sol.objective_value                # mmol protein / gDW / h
        # v is mmol/gDW/h; mass_da is g/mol, so mmol * g/mol / 1000 = g
        g_prot = v * cost.product_mass_da / 1000.0           # g/gDW/h
        g_sub = substrate_g_per_h(subs)
        return {
            "flux_mmol_gDW_h": v,
            "g_protein_per_gDW_h": g_prot,
            "Y_g_per_g": g_prot / g_sub if g_sub else None,
            "mass_da": cost.product_mass_da,
            "atp_per_mol": cost.atp,
            "atp_per_g": cost.atp_per_g,
            "carbon_per_g": cost.carbon_per_g,
            "status": sol.status,
        }
