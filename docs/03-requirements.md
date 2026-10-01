---
doc_id: CBC-REQ-001
title: CurbCount requirements
project: CurbCount
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (numbered, measurable requirements with targets and concept status)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from CBC-CAL-001; design case bike lane 2.0 m to match R6; decisions from CBC-DDR-001 reflected; proposed restatements of R4 and R11 noted
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-30'
  author: Amish Chadha
  change: Status figures from CBC-CAL-001 v0.3 after the design for construction (CBC-DDR-003); no status changed
---

# CurbCount requirements

These requirements are targets for concept review and must be revised with a co-design partner before the design is frozen. The design choices behind them (thermal array, tracking on FieldNode's STM32WL with standard FieldNode power, 15-minute bins and three classes in a 10-byte record, jumper-only calibration, public notice) were decided by Amish on 2026-09-25 (CBC-DDR-001 and CBC-DDR-002). Version 0.4 applies his decisions: R4 is restated in pixels per meter at head height, R7 is restated for temperate sites, R13 follows the new $275 budget, and R11 stays at 6 kg. Version 0.5 takes its figures from CBC-CAL-001 v0.3, after the design for construction (CBC-DDR-003); no status changed. Status is taken from the calculation note CBC-CAL-001 v0.3; "met on paper" means met by calculation only. No requirement is **not met**. Three are at risk (R1, R2, R7) and four cannot be shown at TRL 3 (R3, R10, R12, R14).

Design case: one counter on a 114 mm pole 0.45 m behind the curb, sensor window 4.3 m above the road, a 3 m sidewalk, a 2.0 m bike lane and one 3.5 m traffic lane.

Table 1. Requirements.

| ID | Requirement | Target | Verification | Status (CBC-CAL-001 v0.3) |
| --- | --- | --- | --- | --- |
| R1 | Count pedestrians, cyclists (including micromobility) and motor vehicles in the nearest lane, by direction along the street | 3 classes x 2 directions | Test against manual counts | At risk: 4.2 frames for a car at 50 km/h, 4 assumed needed |
| R2 | Count accuracy for pedestrians and cyclists | Within ±10 % of manual counts per hour at flows up to 600 per hour per direction | Field comparison with manual counts | At risk: random merging alone loses 6.5 %; groups add more |
| R3 | Count accuracy for motor vehicles in the nearest lane | Within ±15 % of manual counts per hour | Field comparison | Not verifiable at TRL 3 (4.2 frames, 3.4 px smear) |
| R4 | Privacy: no image, audio or identifier leaves the device; frames held only in RAM; sensor unable to resolve faces or plates | 8 px/m or less at head height for a 1.75 m person, below the IEC 62676-4 detection level of 25 px/m (restated in v0.4; was a ground pixel of 0.25 m or larger) | Design review, firmware audit, geometry | Met on paper: 7.6 px/m (8.5 px/m for a 2.0 m person) |
| R5 | Output format | 15-minute counts per class and direction in an open, documented 10-byte record (six 12-bit counters and a status byte) over LoRaWAN | Design review | Met by design |
| R6 | Coverage from one pole | Full width of a 3 m sidewalk, a 2 m bike lane and the nearest lane | Geometry, field check | Met on paper with the array turned 90 degrees: -4.45 to 8.34 m across |
| R7 | Operating range | Survive -20 °C to +50 °C; count at temperate sites (design days with air up to 20 °C). Hot-climate sites use the mmWave radar variant (restated in v0.4; was counting with air up to 35 °C) | Thermal chamber, seasonal field test | At risk: on the mild design day sunlit pavement hides pedestrians for 10.2 h with single frames, 3.2 h with track averaging; shaded 0 h |
| R8 | Autonomy without sun | 3 days of continuous counting | Energy budget, bench test | Met on paper: 6.22 days on one cell (4.36 at -20 °C) |
| R9 | Energy neutral in winter | At 1.5 peak sun hours with street shading derating | Energy budget, field log | Met on paper: FieldNode's 6 W panel stores 4.4 Wh/day against 2.47 Wh/day |
| R10 | Ingress protection | IP65 for the enclosure and the sensor head | Spray test | Not verifiable at TRL 3 |
| R11 | Mass on the pole | 6 kg or less | Weighing | Met on paper: 5.26 kg with the parts added for construction (4.44 kg in v0.4; 6.02 kg with the 20 W panel) |
| R12 | Installation | Two trained people, 60 min, no drilling, welding or pole wiring; withstands 35 m/s gusts | Timed trial, bracket calculation | Not verifiable at TRL 3: 59 min estimate; wind and fit met on paper |
| R13 | Parts cost | $275 or less per counter (`budget_usd`; was $150) | Priced BOM | Met on paper: $274.00 (margin $1.00) |
| R14 | Service life | 5 years outdoors with one battery change | Design review, UV-stable materials | Not verifiable at TRL 3 |
| R15 | Radio use | Within EU868 1 % duty cycle and the US915 dwell limits | Airtime calculation | Met on paper: 0.82 s/h at SF9; 371 ms at US915 DR0 |

Table 2. Assumptions behind the targets.

| Assumption | Value | Source or basis |
| --- | --- | --- |
| Walking speed | 1.0 to 1.5 m/s | Typical design range (estimate) |
| Cyclist speed | up to 25 km/h | Typical urban maximum (estimate) |
| Vehicle speed in the nearest lane | up to 50 km/h | Common urban limit (estimate) |
| Peak sun hours, winter design case | 1.5 h | Mid-latitude winter (estimate) |
| Street shading and dust derating | 40 % | Estimate, to be checked on real poles |
| Temperate design day | Air 10 to 20 °C | CBC-CAL-001 section D |
