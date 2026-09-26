---
doc_id: CBC-REQ-001
title: CurbCount requirements
project: CurbCount
doc_type: Requirements
version: "0.2"
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
---

# CurbCount requirements

These requirements are proposed targets for concept review, awaiting Amish, and must be revised with a co-design partner before the design is frozen. Status is judged against the first-order estimates in CBC-PRC-001; "met" means met on paper only. Three requirements are **not met** by the current concept (R6 for wide sidewalks, R13 cost, and R8 and R9 if the standard FieldNode power parts are used), and two are at risk (R2, R7).

Design case: one counter on a pole 0.45 m behind the curb, sensor window 4.3 m above the road, a 3 m sidewalk, a 1.8 m bike lane and one 3.5 m traffic lane.

Table 1. Requirements.

| ID | Requirement | Target | Verification | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Count pedestrians, cyclists (including micromobility) and motor vehicles in the nearest lane, by direction along the street | 3 classes x 2 directions | Test against manual counts | Plausible (7 to 14 frames per crossing) |
| R2 | Count accuracy for pedestrians and cyclists | Within ±10 % of manual counts per hour at flows up to 600 per hour per direction | Field comparison with manual counts | At risk: groups merge into one blob |
| R3 | Count accuracy for motor vehicles in the nearest lane | Within ±15 % of manual counts per hour | Field comparison | Unverified |
| R4 | Privacy: no image, audio or identifier leaves the device; frames held only in RAM; sensor unable to resolve faces or plates | Ground pixel size 0.25 m or larger at the design height | Design review, firmware audit, geometry | Met by design (about 0.3 to 0.4 m) |
| R5 | Output format | 15-minute counts per class and direction in an open, documented format over LoRaWAN | Design review | Met by design (14 bytes per bin) |
| R6 | Coverage from one pole | Full width of a 3 m sidewalk, a 2 m bike lane and the nearest lane | Geometry, field check | **Not met:** about 2.1 m behind the curb covered |
| R7 | Operating range | -20 °C to +50 °C; counting works with air up to 35 °C | Thermal chamber, hot-season field test | At risk: little thermal contrast near body temperature |
| R8 | Autonomy without sun | 3 days of continuous counting | Energy budget, bench test | Met with two cells (about 4.3 days); **not met** with one (about 2.1 days) |
| R9 | Energy neutral in winter | At 1.5 peak sun hours with street shading derating | Energy budget, field log | Met with 20 W panel (about 16 Wh/day for 7.2 Wh/day); **not met** with 6 W |
| R10 | Ingress protection | IP65 for the enclosure and the sensor head | Spray test | By design, unverified |
| R11 | Mass on the pole | 6 kg or less | Weighing | Met (about 4.2 kg) |
| R12 | Installation | Two trained people, 60 min, no drilling, welding or pole wiring; withstands 35 m/s gusts | Timed trial, bracket calculation | By design; wind load about 170 N to check |
| R13 | Parts cost | $150 or less per counter | Priced BOM | **Not met:** about $271 |
| R14 | Service life | 5 years outdoors with one battery change | Design review, UV-stable materials | Unverified |
| R15 | Radio use | Within EU868 1 % duty cycle and the US915 dwell limits | Airtime calculation | Met (about 0.8 s/h against 36 s/h) |

Table 2. Assumptions behind the targets.

| Assumption | Value | Source or basis |
| --- | --- | --- |
| Walking speed | 1.0 to 1.5 m/s | Typical design range (estimate) |
| Cyclist speed | up to 25 km/h | Typical urban maximum (estimate) |
| Vehicle speed in the nearest lane | up to 50 km/h | Common urban limit (estimate) |
| Peak sun hours, winter design case | 1.5 h | Mid-latitude winter (estimate) |
| Street shading and dust derating | 40 % | Estimate, to be checked on real poles |
