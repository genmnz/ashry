# Merged secretion-titer corpus

Input rows: 356
Merged rows: 306
Rows carrying a numeric mg/L value: 297

## Input provenance

- `titers_eggheme.tsv`: 61 rows
- `titers_fungal.tsv`: 100 rows
- `titers_host_panel.csv`: 109 rows
- `titers_kpdairy.tsv`: 54 rows
- `titers_target_proteins.csv`: 32 rows

## Rows per protein (merged)

- other: 107
- ovalbumin: 25
- lactoferrin: 24
- lysozyme: 20
- interferon: 17
- serum albumin: 13
- beta-lactoglobulin: 10
- leghemoglobin: 10
- myoglobin: 10
- collagen: 7
- kappa-casein: 7
- protein fragment or single domain: 7
- alpha-lactalbumin: 6
- phytase: 6
- chymosin: 5
- ovomucoid: 5
- xylanase: 5
- avidin: 4
- glucoamylase: 3
- haemoglobin: 3
- brazzein: 2
- casein macropeptide (fragment): 2
- osteopontin: 2
- alpha-s1-casein: 1
- alpha-s2-casein: 1
- beta-casein: 1
- cellobiohydrolase I: 1
- ovotransferrin: 1
- transferrin: 1

## Rows per host (merged)

- Komagataella phaffii: 140
- Trichoderma reesei: 48
- Aspergillus niger: 26
- Escherichia coli: 18
- Saccharomyces cerevisiae: 17
- Aspergillus oryzae: 14
- Thermothelomyces heterothallica: 11
- Aspergillus awamori: 7
- other: 6
- Kluyveromyces lactis: 5
- Bacillus subtilis: 4
- Ogataea polymorpha: 4
- Kluyveromyces marxianus: 3
- Yarrowia lipolytica: 2
- Neurospora crassa: 1

## Deduplication (33 groups collapsed)

- `alpha-lactalbumin` in Komagataella phaffii at 113.4 mg/L: kept `titers_host_panel-9` (high), folded in 1 other record(s): titers_target_proteins-8
- `alpha-lactalbumin` in Komagataella phaffii at 5.2 mg/L: kept `kpdairy-7` (high), folded in 2 other record(s): titers_host_panel-8;titers_target_proteins-7
- `alpha-lactalbumin` in Komagataella phaffii at 56.3 mg/L: kept `kpdairy-8` (high), folded in 2 other record(s): titers_host_panel-7;titers_target_proteins-6
- `beta-lactoglobulin` in Komagataella phaffii at 13880.0 mg/L: kept `kpdairy-1` (high), folded in 2 other record(s): titers_host_panel-1;titers_target_proteins-1
- `beta-lactoglobulin` in Saccharomyces cerevisiae at 1.1 mg/L: kept `kpdairy-3` (high), folded in 1 other record(s): titers_target_proteins-3
- `beta-lactoglobulin` in Trichoderma reesei at 1000.0 mg/L: kept `kpdairy-6` (high), folded in 3 other record(s): titers_host_panel-92;titers_target_proteins-2;fungal-1
- `brazzein` in Trichoderma reesei at 1300.0 mg/L: kept `fungal-14` (high), folded in 1 other record(s): titers_host_panel-97
- `casein macropeptide (fragment)` in Komagataella phaffii at 1020.0 mg/L: kept `titers_host_panel-10` (high), folded in 2 other record(s): titers_target_proteins-29;kpdairy-16
- `interferon` in Trichoderma reesei at 2400.0 mg/L: kept `fungal-25` (high), folded in 1 other record(s): titers_host_panel-94
- `kappa-casein` in Aspergillus oryzae at 0.2 mg/L: kept `fungal-11` (high), folded in 2 other record(s): fungal-12;titers_target_proteins-28
- `lactoferrin` in Komagataella phaffii at 1200.0 mg/L: kept `titers_host_panel-6` (high), folded in 1 other record(s): titers_target_proteins-17
- `lactoferrin` in Komagataella phaffii at 2.0 mg/L: kept `kpdairy-31` (high), folded in 2 other record(s): titers_host_panel-18;titers_target_proteins-26
- `lactoferrin` in Komagataella phaffii at 232.6 mg/L: kept `kpdairy-25` (high), folded in 2 other record(s): titers_host_panel-16;titers_target_proteins-22
- `lactoferrin` in Komagataella phaffii at 2800.0 mg/L: kept `kpdairy-19` (high), folded in 2 other record(s): titers_host_panel-17;titers_target_proteins-25
- `lactoferrin` in Trichoderma reesei at 1349.5 mg/L: kept `fungal-8` (high), folded in 2 other record(s): titers_host_panel-95;titers_target_proteins-18
- `lactoferrin` in Trichoderma reesei at 368.5 mg/L: kept `fungal-7` (high), folded in 2 other record(s): titers_host_panel-96;titers_target_proteins-19
- `lactoferrin` in Yarrowia lipolytica at 3140.0 mg/L: kept `kpdairy-24` (high), folded in 2 other record(s): titers_host_panel-100;titers_target_proteins-20
- `lactoferrin` in Yarrowia lipolytica at 409.9 mg/L: kept `titers_host_panel-101` (high), folded in 2 other record(s): titers_target_proteins-21;kpdairy-23
- `leghemoglobin` in Kluyveromyces marxianus at 7270.0 mg/L: kept `titers_host_panel-102` (high), folded in 1 other record(s): titers_target_proteins-16
- `leghemoglobin` in Komagataella phaffii at 1652.7 mg/L: kept `titers_host_panel-5` (high), folded in 1 other record(s): titers_target_proteins-15
- `leghemoglobin` in Komagataella phaffii at 3500.0 mg/L: kept `eggheme-1` (high), folded in 2 other record(s): titers_host_panel-2;titers_target_proteins-13
- `leghemoglobin` in Komagataella phaffii at 6000.0 mg/L: kept `titers_host_panel-3` (high), folded in 1 other record(s): titers_target_proteins-14
- `lysozyme` in Komagataella phaffii at 3500.0 mg/L: kept `eggheme-48` (high), folded in 1 other record(s): titers_host_panel-13
- `other` in Komagataella phaffii at 1300.0 mg/L: kept `titers_host_panel-71` (high), folded in 1 other record(s): titers_host_panel-72
- `other` in Trichoderma reesei at 47.4 mg/L: kept `fungal-55` (high), folded in 1 other record(s): titers_host_panel-98
- `other` in Trichoderma reesei at 508.0 mg/L: kept `fungal-51` (high), folded in 1 other record(s): titers_host_panel-99
- `ovalbumin` in Escherichia coli at 3700.0 mg/L: kept `eggheme-21` (high), folded in 1 other record(s): titers_target_proteins-10
- `ovalbumin` in Escherichia coli at 42.0 mg/L: kept `eggheme-20` (high), folded in 1 other record(s): titers_target_proteins-11
- `ovalbumin` in Trichoderma reesei at 2000.0 mg/L: kept `fungal-3` (high), folded in 3 other record(s): eggheme-34;titers_host_panel-93;titers_target_proteins-9
- `ovotransferrin` in Komagataella phaffii at 97.0 mg/L: kept `titers_host_panel-90` (medium), folded in 1 other record(s): eggheme-41
- `protein fragment or single domain` in Komagataella phaffii at 15.7 mg/L: kept `kpdairy-34` (high), folded in 1 other record(s): titers_host_panel-21
- `serum albumin` in Komagataella phaffii at 1000.0 mg/L: kept `kpdairy-40` (high), folded in 1 other record(s): titers_host_panel-23
- `serum albumin` in Komagataella phaffii at 17470.0 mg/L: kept `kpdairy-35` (high), folded in 1 other record(s): titers_host_panel-24
