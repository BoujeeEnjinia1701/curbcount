---
doc_id: CBC-DDR-004
title: CurbCount concept options and the STEM fixes of the kit 1.9.1 upgrade
project: CurbCount
doc_type: Design decision record
version: '0.1'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-10-31'
  author: Amish Chadha
  change: Concept selection between the thermal array head (A) and the 60 GHz radar head (B), both proposed to Amish; the duty-cycle fix for option B decided under the standing instruction; the cold-charging question proposed
---

# 0004: Concept options and STEM fixes (kit 1.9.1 upgrade)

- **Date:** 2026-10-31
- **Status:** proposed. Items C1 and C2 were made under Amish's standing instruction of 2026-10-23 (fix rule); items O1 to O4 are **Proposed, awaiting Amish**.

## Context

The kit 1.9.1 upgrade asked for a STEM check, at least two concept options scored against the user requirements, and detailed CAD for every option. The current design (thermal array head, tracked on FieldNode's STM32WL, one cell and a 6 W panel) is option A and is unchanged. Amish decided on 2026-09-25 (CBC-DDR-002) that the thermal build is for temperate sites and that a 60 GHz radar variant comes forward for hot-climate partner cities; that variant is option B here. The scoring is in CBC-OPT-001 and the checks are in CBC-STM-001.

## Options considered

**Concept selection (O2).**

1. Keep A as the build and B as the hot-climate variant. A scores 121 and B 110 of 165 (73.3 % and 66.7 %), a gap of 9.1 %. Changes nothing already decided. Costs: B stays unproven on price and rules.
2. Carry B forward for all sites. Radar is blind to nothing the thermal array is blind to, but the module price is unknown (CBC-MKT-001), 60 GHz rules are to assess (CBC-REG-001 G9) and it needs a 20 W panel, two cells and duty cycling to close the energy balance.
3. Design a combined head. Not scored; it would add the cost of both sensors on a 275 USD target that A already uses up to 1.00 USD of.

**Cold charging (O1).** A LiFePO4 cell must not be charged below 0 degrees C; FieldNode's NTC lockout stops charging; with the box about 3 K above the air in shaded winter sun, charging stops at about -3 degrees C by the estimate and nearer 0 degrees C allowing for thermal lag (STM S8, independent review).

1. Limit the claim to sites where the winter air stays above about 0 degrees C and state it in the requirements (done in PR-010, at risk). No cost; the counter cannot serve a cold winter.
2. Ask the FieldNode project for a heated cell pocket. Keeps the claim; adds a heater load to a 6 W panel in weak winter sun and changes the shared core.
3. Use a low-temperature-rated cell. Keeps the claim; changes BOM line 3 and the FieldNode core, price to assess.

**Option B energy (C1).** Radar always on: 32.0 Wh/day against 14.5 Wh/day stored (fails). Frame bursts at 0.4 W average: 10.7 Wh/day, 2.9 days without sun but only 2.0 days at -20 degrees C against 3 required (fails). Bursts at 0.25 W average: 6.7 Wh/day and 3.2 days at -20 degrees C, but 2.6 days once the end-of-life 80 % is applied as well (the independent review; fails). Bursts at 0.2 W average (one in six): 5.3 Wh/day, 5.8 days, 3.2 days at -20 degrees C and end of life (passes on paper). A bigger panel or a third cell would pass too but raise cost and mass.

**Vehicle frames (O3).** The independent review showed that CAL-001 C1 treats a car as a point at road level: at the warm hood, 1.0 m up, the field along the street is shorter and a car at 50 km/h gives 3.2 frames, not 4.2 (against 4 needed). Options: (1) 32 Hz subpages with 1 MHz I2C, 6.4 frames, noise up by the square root of 2 (recovered by track averaging), pull-up down to 644 ohm; (2) say vehicle counts are not met; (3) a vehicle sensor on option B only.

**Option B shared core (O4).** The 20 W panel pushes 5.0 A against FieldNode's 1.5 A charger setting (S28), and the shared cell is above its charge limit on hot days without a shield (S26). Options: (1) FieldNode's high-load variant (raised in CBC-DDR-001 D3) plus the shield; (2) keep B as a study only.

**Model fidelity (C2).** Rebuild `cad/src/model.py` to the kit 1.9 interface with every bolt, nut, screw and hole as a separate part, and a second option, without changing any design dimension.

## Decision

- **C1 (decided under the standing instruction, 2026-10-23):** option B's radar runs in frame bursts for about 0.2 W average (one burst in six), with two cells and a 20 W panel; the working principle, pitch and scope are unchanged. The burst rate the tracker needs is to be profiled at TRL 4. Amish can reverse it.
- **C2 (decided under the same instruction as a modelling change only):** `PARAMS` and `derived()` are identical to the kit 1.7 model (checked by comparing the two files), so no design dimension changed. The model now has 127 parts for option A and 128 for option B, all fasteners individual, with countersinks, clearance holes, crush spacers, a panel frame with lip holes, and a bolt and nut for each joint. The fixings follow the build plan (countersunk M4 screws for the V-saddles and cap disc, M5 countersunk screws for the clips); the washers of an earlier modelling attempt were left out because the BOM lists none.
- **O1 (Proposed, awaiting Amish):** recommend option 1 now (limit the claim to cool sites, done in the requirements) and raise options 2 and 3 with the FieldNode project, because the fix belongs in the shared core.
- **O3 (Proposed, awaiting Amish):** recommend option 1; it is a firmware and bus setting but changes the shared FieldNode sensor port speed, so FieldNode must agree. Until then PR-001 and PR-003 stay at risk with 3.2 frames at the hood.
- **O4 (Proposed, awaiting Amish, only if option B is carried forward):** recommend option 1, argued in the FieldNode project.
- **O2 (Proposed, awaiting Amish):** the options are within 10 %, so no pick is made. If he wants a lean, option 1 (A as the build, B as the hot-climate variant).

## Consequences

- If O2 option 1: nothing in the design changes; option B stays modelled and checked as a variant.
- If O1 option 2 or 3 is chosen: BOM line 3 or the FieldNode enclosure changes, the energy rows in CAL-001 E are rerun and PR-010 moves to met on paper.
- C1 adds a profiling task for TRL 4 (on hold) and the risk F17 in CBC-RSK-001.
- C2 means the drawings, STL and step files were regenerated; mass reads 5.24 kg in `sizing.py` (modelled volumes plus catalogue masses of bought parts) and 4.8 kg in `cad/fidelity.json` (modelled volumes); the 0.44 kg difference is not itemised and the 6 kg limit is met either way.
