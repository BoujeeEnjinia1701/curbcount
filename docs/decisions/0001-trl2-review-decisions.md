---
doc_id: CBC-DDR-001
title: CurbCount TRL 2 review decisions
project: CurbCount
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (v0.2). On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Items D1 to D7 and O2 are now decided as recommended; O1 had no recommendation and remains "Proposed, awaiting Amish". CBC-DDR-002 records what changed in the repo.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", each with options and, for seven of them, a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CurbCount items one by one. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. No item is recorded as decided or approved by Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CBC-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided (adopted for TRL 3 in v0.1, decided by Amish in v0.2).*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Budget | Option (a): raise `budget_usd` to $275. Applied in v0.2: `budget_usd` is now $275 (see O2 and CBC-DDR-002). | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Sensor | Option A, the 32 x 24 thermal array, for the first build; 60 GHz mmWave radar studied as a hot-climate variant. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Power | A FieldNode "high-load" variant (20 W panel, second 6 Ah cell), raised with the FieldNode project rather than changing FieldNode here. Since CBC-DDR-002 it applies only to the ESP32-S3 fallback; the baseline uses standard FieldNode power. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Processor | ESP32-S3 in the sensor head first; tracking on FieldNode's STM32WL alone studied at TRL 3 (CBC-CAL-001, section F). The study was done, and CBC-DDR-002 makes the STM32WL the baseline, with the ESP32-S3 as fallback. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Count interval and classes | 15-minute bins; three classes (pedestrian, cyclist or micromobility, motor vehicle), each by two directions. | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Calibration mode | Frames may be shown on a laptop only through a physical jumper in the sensor head, never over the radio. | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Public notice | A notice plate on each pole saying what is counted and linking to this repository (BOM line 13). | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that were open in v0.1.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and street (city transport department, residents' group or university). No recommendation was made. | Proposed, awaiting Amish |
| O2 | The budget figure (D1). The TRL 3 review recommended option (b): $275 with the STM32WL-only design (about $253). `budget_usd` is now $275. | Decided by Amish, 2026-09-25: go with recommendation |

No reworded pitch or problem line was recommended at TRL 2, so `project.yaml` and `README.md` keep the existing wording.

## Consequences

- CBC-PRB-001, CBC-PRC-001 and CBC-REQ-001 move to v0.3. The design choices above are described as "adopted for TRL 3, open for Amish's review" instead of "proposed". The street design case in CBC-REQ-001 now uses a 2.0 m bike lane, to match the R6 target.
- CBC-CAL-001 led to three design changes within these decisions, all at massing level and all open for Amish's review: (1) the thermal array is turned 90 degrees so that its 110 degree axis spans the street, with the view tilted 7.5 degrees toward the road instead of 10 degrees, which makes R6 (coverage) met on paper; (2) the panel mount becomes aluminium and the saddle plates thinner, because the steel mount alone came to 5.7 kg; (3) the FieldNode enclosure takes its TRL 3 size (150 x 90 x 200 mm) and a CurbCount saddle plate, since FieldNode's V-block kit seats only 40 to 60 mm poles.
- CBC-CAL-001 shows that R13 (cost) is not met even against the recommended $275 ($290.00), that R7 (counting in hot weather) is not met on paper, and that R4 is not met as written although its privacy aim is. The follow-up proposals are in `docs/REVIEW.md` and await Amish; this record does not decide them.
- v0.2: the three CBC-CAL-001 design changes above, and the follow-up proposals from the TRL 3 review, were accepted by Amish on 2026-09-25 with the rest of the recommendations; see CBC-DDR-002.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
