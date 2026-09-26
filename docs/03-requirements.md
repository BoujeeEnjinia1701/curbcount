---
doc_id: CBC-REQ-001
title: CurbCount requirements
project: CurbCount
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
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
---

# CurbCount requirements

These requirements are targets for concept review and must be revised with a co-design partner before the design is frozen. The design choices behind them (thermal array, high-load FieldNode power, ESP32-S3 processor, 15-minute bins and three classes, jumper-only calibration, public notice) are adopted for TRL 3 under Amish's 2026-09-25 instruction and open for his review (CBC-DDR-001). Status is taken from the calculation note CBC-CAL-001; "met on paper" means met by calculation only. Three requirements are **not met**: R4 as written (the privacy aim is met), R7 in hot weather and R13 cost. Four are at risk (R1, R2, R11, R15) and four cannot be shown at TRL 3 (R3, R10, R12, R14).

Design case: one counter on a 114 mm pole 0.45 m behind the curb, sensor window 4.3 m above the road, a 3 m sidewalk, a 2.0 m bike lane and one 3.5 m traffic lane. (Version 0.2 used a 1.8 m bike lane; 2.0 m matches the R6 target.)

Table 1. Requirements.

| ID | Requirement | Target | Verification | Status (CBC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Count pedestrians, cyclists (including micromobility) and motor vehicles in the nearest lane, by direction along the street | 3 classes x 2 directions | Test against manual counts | At risk: 4.2 frames for a car at 50 km/h, 4 assumed needed |
| R2 | Count accuracy for pedestrians and cyclists | Within ±10 % of manual counts per hour at flows up to 600 per hour per direction | Field comparison with manual counts | At risk: random merging alone loses 6.5 %; groups add more |
| R3 | Count accuracy for motor vehicles in the nearest lane | Within ±15 % of manual counts per hour | Field comparison | Not verifiable at TRL 3 (4.2 frames, 3.4 px smear) |
| R4 | Privacy: no image, audio or identifier leaves the device; frames held only in RAM; sensor unable to resolve faces or plates | Ground pixel size 0.25 m or larger at the design height | Design review, firmware audit, geometry | **Not met as written:** smallest ground pixel 0.22 m. Privacy aim met: 8.5 px/m at head height against 250 px/m to identify (restatement proposed, awaiting Amish) |
| R5 | Output format | 15-minute counts per class and direction in an open, documented format over LoRaWAN | Design review | Met by design (14 bytes per bin) |
| R6 | Coverage from one pole | Full width of a 3 m sidewalk, a 2 m bike lane and the nearest lane | Geometry, field check | Met on paper with the array turned 90 degrees: -4.45 to 8.34 m across |
| R7 | Operating range | -20 °C to +50 °C; counting works with air up to 35 °C | Thermal chamber, hot-season field test | **Not met on paper:** on a hot design day pedestrians fall below detection contrast for 14.2 h (sunlit) to 24 h (shaded) |
| R8 | Autonomy without sun | 3 days of continuous counting | Energy budget, bench test | Met on paper: 4.78 days with two cells (3.35 at -20 °C); 2.39 with one |
| R9 | Energy neutral in winter | At 1.5 peak sun hours with street shading derating | Energy budget, field log | Met on paper: 20 W stores 14.5 Wh/day against 6.43 Wh/day; 6 W does not |
| R10 | Ingress protection | IP65 for the enclosure and the sensor head | Spray test | Not verifiable at TRL 3 |
| R11 | Mass on the pole | 6 kg or less | Weighing | At risk: 6.02 kg (TRL 2 estimate was 4.2 kg) |
| R12 | Installation | Two trained people, 60 min, no drilling, welding or pole wiring; withstands 35 m/s gusts | Timed trial, bracket calculation | Not verifiable at TRL 3: 59 min estimate; wind and fit met on paper |
| R13 | Parts cost | $150 or less per counter (budget of $275 recommended, awaiting Amish) | Priced BOM | **Not met:** $290.00 |
| R14 | Service life | 5 years outdoors with one battery change | Design review, UV-stable materials | Not verifiable at TRL 3 |
| R15 | Radio use | Within EU868 1 % duty cycle and the US915 dwell limits | Airtime calculation | At risk: 0.91 s/h at SF9; the 14-byte record exceeds the 11-byte US915 DR0 limit |

Table 2. Assumptions behind the targets.

| Assumption | Value | Source or basis |
| --- | --- | --- |
| Walking speed | 1.0 to 1.5 m/s | Typical design range (estimate) |
| Cyclist speed | up to 25 km/h | Typical urban maximum (estimate) |
| Vehicle speed in the nearest lane | up to 50 km/h | Common urban limit (estimate) |
| Peak sun hours, winter design case | 1.5 h | Mid-latitude winter (estimate) |
| Street shading and dust derating | 40 % | Estimate, to be checked on real poles |

Proposed changes awaiting Amish (see `docs/REVIEW.md`): restate R4 as "8 px/m or less at head height, below the IEC 62676-4 detection level of 25 px/m" in place of the ground pixel size; keep R11 at 6 kg and trim mass, or relax it to 6.5 kg; set the payload for R15 at 10 bytes.
