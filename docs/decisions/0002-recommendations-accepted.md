---
doc_id: CBC-DDR-002
title: CurbCount recommendations accepted
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
  change: Record the recommendations accepted by Amish on 2026-09-25 and what changed in the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Amish accepted every recommendation in `docs/REVIEW.md` and CBC-DDR-001 on 2026-09-25. Items with no recommendation stay open.

## Context

The TRL 2 and TRL 3 review notes (`docs/REVIEW.md`, both sessions of 2026-09-25) and CBC-DDR-001 left items marked "Proposed, awaiting Amish" or "Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review". On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that carried a recommendation is therefore decided as recommended; where a recommendation named one of several options, that option is the decision. TRL 4 remains on hold by Amish's instruction, and the repo stays at `trl: 3`.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` and CBC-DDR-001. They are not repeated here.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item (source) | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | D1 to D7 (CBC-DDR-001) | Decided as recommended: $275 budget, thermal array first with radar as hot-climate variant, FieldNode high-load variant raised with FieldNode, ESP32-S3 first with the STM32WL study, 15-minute bins and three classes, jumper-only calibration, public notice plate | CBC-DDR-001 v0.2 statuses updated; D3 and D4 are refined by items 3 and 4 below |
| 2 | Three CBC-CAL-001 v0.1 design changes (REVIEW, TRL 3): array turned 90 degrees, aluminium pole-top mount, FieldNode TRL 3 enclosure on a CurbCount saddle | Decided as made | No further change |
| 3 | O2 and REVIEW TRL 3 item 2, budget | Option (b): $275 with the STM32WL-only design | `budget_usd` $150 to $275 in `project.yaml`; R13 target $150 to $275 (budget); BOM $290.00 to $253.00, R13 not met to met on paper |
| 4 | REVIEW TRL 3 item 3, move tracking to the STM32WL | Baseline for the first build; ESP32-S3 head as fallback | BOM line 11 (ESP32-S3, $12) removed and lines 12 to 14 renumbered 11 to 13; one cell instead of two ($9 off); FieldNode's 6 W panel ($14) instead of the 20 W panel ($30); pole-top mount hinge plate 140 x 180 to 140 x 160 mm; `cad/src/model.py` (no processor part, one cell, 290 x 200 x 17 mm panel), STEP and STL re-exported; CBC-DWG-001 Rev P1 to P2; concept media re-rendered (blueprint CBC-DWG-010 Rev P2 to P3); head load 241 to 92 mW, draw 6.43 to 2.47 Wh/day, autonomy 4.78 days on two cells to 6.22 days on one |
| 5 | REVIEW TRL 3 item 4, R7 and the sensor for hot climates | Option (a) now: the thermal build is for temperate sites, stated in R7; option (b), bring the radar variant forward, applies to any hot partner city | R7 restated (survive -20 to +50 °C; count at temperate sites, air up to 20 °C; hot sites use radar); status not met to at risk. Radar design work waits for a partner city (O1) |
| 6 | REVIEW TRL 3 item 5, restate R4 | Adopt: 8 px/m or less at head height, below the IEC 62676-4 detection level of 25 px/m | R4 restated; not met as written (0.22 m ground pixel against 0.25 m) to met on paper (7.6 px/m for a 1.75 m person; 8.5 px/m for a 2.0 m person) |
| 7 | REVIEW TRL 3 item 6, R11 mass | Keep 6 kg and meet it through item 4 | R11 unchanged at 6 kg; mass 6.02 to 4.44 kg, at risk to met on paper |
| 8 | REVIEW TRL 3 item 7, payload | Pack the record into 10 bytes (six 12-bit counters and a status byte) | R5 target states the 10-byte record; payload 14 to 10 bytes; SF9 uplink 226 to 206 ms; US915 DR0 uplink fits (371 ms, 10 of 11 bytes); R15 at risk to met on paper |
| 9 | REVIEW TRL 3 item 8, raise with FieldNode | Decided; recorded as cross-repo actions in `docs/REVIEW.md`, FieldNode not edited | None in this repo |

Pitch and problem: no rewording was recommended, so `project.yaml` and `README.md` keep the existing pitch and problem lines.

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and street (city transport department, residents' group or university). No recommendation was made. | Proposed, awaiting Amish |

The side-arm panel mount for poles with a lantern on top was a suggestion, not a recommendation, and is not applied.

## Consequences

- Controlled documents revised: CBC-PRB-001 v0.4, CBC-PRC-001 v0.4, CBC-REQ-001 v0.4, CBC-CAL-001 v0.2, CBC-DDR-001 v0.2; CBC-DWG-001 Rev P2.
- Requirement status (CBC-CAL-001 v0.2): 0 not met (was 3), 3 at risk (R1, R2, R7), 4 not verifiable at TRL 3, 7 met on paper, 1 met by design.
- Pole loading from the panel falls from 170 N to 52 N at 35 m/s, and the moment at the pole base from 933 N·m to 283 N·m.
- The calibration jumper (DDR-001 D6) moves from the head to FieldNode's service header, because the head no longer has a processor.
- Deferred as TRL 4 work, on hold by Amish's instruction: profiling the fixed-point tracker on the STM32WL, I²C over the 2 m cable on a pole, window and array noise measurements, and any radar build. None has been started.
