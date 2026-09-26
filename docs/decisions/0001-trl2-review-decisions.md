---
doc_id: CBC-DDR-001
title: CurbCount TRL 2 review decisions
project: CurbCount
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items D1 to D7 are adopted for TRL 3 work pending Amish's review; items O1 and O2 remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", each with options and, for seven of them, a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CurbCount items one by one. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. No item is recorded as decided or approved by Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CBC-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3.*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Budget | Option (a): raise `budget_usd` to $275. Per the session instruction, `budget_usd` in `project.yaml` stays at $150; the $275 figure is recorded here and in `docs/REVIEW.md` as awaiting Amish, and CBC-CAL-001 states the cost against both figures. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Sensor | Option A, the 32 x 24 thermal array, for the first build; 60 GHz mmWave radar studied as a hot-climate variant. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Power | A FieldNode "high-load" variant (20 W panel, second 6 Ah cell), raised with the FieldNode project rather than changing FieldNode here. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Processor | ESP32-S3 in the sensor head first; tracking on FieldNode's STM32WL alone studied at TRL 3 (CBC-CAL-001, section F). | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | Count interval and classes | 15-minute bins; three classes (pedestrian, cyclist or micromobility, motor vehicle), each by two directions. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | Calibration mode | Frames may be shown on a laptop only through a physical jumper in the sensor head, never over the radio. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D7 | Public notice | A notice plate on each pole saying what is counted and linking to this repository (BOM line 13). | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and street (city transport department, residents' group or university). No recommendation was made. | Proposed, awaiting Amish |
| O2 | The $275 budget figure itself (D1): `budget_usd` is unchanged at $150 until Amish sets it. | Proposed, awaiting Amish |

No reworded pitch or problem line was recommended at TRL 2, so `project.yaml` and `README.md` keep the existing wording.

## Consequences

- CBC-PRB-001, CBC-PRC-001 and CBC-REQ-001 move to v0.3. The design choices above are described as "adopted for TRL 3, open for Amish's review" instead of "proposed". The street design case in CBC-REQ-001 now uses a 2.0 m bike lane, to match the R6 target.
- CBC-CAL-001 led to three design changes within these decisions, all at massing level and all open for Amish's review: (1) the thermal array is turned 90 degrees so that its 110 degree axis spans the street, with the view tilted 7.5 degrees toward the road instead of 10 degrees, which makes R6 (coverage) met on paper; (2) the panel mount becomes aluminium and the saddle plates thinner, because the steel mount alone came to 5.7 kg; (3) the FieldNode enclosure takes its TRL 3 size (150 x 90 x 200 mm) and a CurbCount saddle plate, since FieldNode's V-block kit seats only 40 to 60 mm poles.
- CBC-CAL-001 shows that R13 (cost) is not met even against the recommended $275 ($290.00), that R7 (counting in hot weather) is not met on paper, and that R4 is not met as written although its privacy aim is. The follow-up proposals are in `docs/REVIEW.md` and await Amish; this record does not decide them.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
