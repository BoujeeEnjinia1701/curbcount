---
doc_id: CBC-PRS-001
title: CurbCount product requirements and specifications
project: CurbCount
doc_type: Product requirements and specifications
version: '0.7'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: '0.2'
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (numbered, measurable requirements with targets and concept status)
- version: '0.3'
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from CBC-CAL-001; design case bike lane 2.0 m to match R6; decisions from CBC-DDR-001 reflected; proposed restatements of R4 and R11 noted
- version: '0.4'
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: '0.5'
  date: '2026-09-30'
  author: Amish Chadha
  change: Status figures from CBC-CAL-001 v0.3 after the design for construction (CBC-DDR-003); no status changed
- version: '0.6'
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: '0.7'
  date: '2026-10-31'
  author: Amish Chadha
  change: 'Kit 1.9.1 upgrade: restated as product requirements PR-001 to PR-021, each traced to a user requirement in CBC-URS-001; old R numbers kept in the Was column; document type PRS (was REQ, CBC-REQ-001); R9 now at risk below about -5 C air (STEM check S8); R7 and R12 split; mass 5.24 kg from CBC-CAL-001 sizing.py'
---

# CurbCount product requirements and specifications

What the counter must do, each requirement traced to a user need in CBC-URS-001. Targets are proposals for review with a co-design partner. Method: STANDARDS section 22. Status comes from the calculation note CBC-CAL-001 (v0.4 and `sizing.py`) and the STEM check CBC-STM-001; "met on paper" means met by calculation only. **No requirement is not met.** Five are at risk (PR-001, PR-002, PR-008, PR-010 and PR-016) and five cannot be shown at TRL 3 and are marked to verify at TRL 4 (PR-003, PR-007, PR-011, PR-013 and PR-017).

The design choices behind these requirements (thermal array, tracking on FieldNode's STM32WL with standard FieldNode power, 15-minute bins and three classes in a 10-byte record, jumper-only calibration, public notice) were decided by Amish on 2026-09-25 (CBC-DDR-001 and CBC-DDR-002). Version 0.7 restates the fifteen requirements R1 to R15 of CBC-REQ-001 v0.6 as product requirements PR-001 to PR-021 (the Was column keeps the old numbers) and traces each to a user requirement.

Design case: one counter on a 114 mm pole 0.45 m behind the curb, sensor window 4.3 m above the road, a 3 m sidewalk, a 2.0 m bike lane and one 3.5 m traffic lane.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-003 | Performance | Count three classes in two directions | The counter shall count pedestrians, cyclists (including micromobility) and motor vehicles in the nearest lane, by direction along the street | 6 | min | counters (3 classes x 2 directions) | Analysis (CAL-001 C), TRL 3; test against manual counts, TRL 4 | At risk: 4.2 frames for a point at road level, 3.2 for a warm hood 1.0 m up (STM S5), against 4 assumed needed; fix proposed to Amish (CBC-DEC-001 O3) | R1 |
| PR-002 | UR-004 | Performance | Pedestrian and cyclist accuracy | The hourly count of pedestrians and cyclists shall be within 10 % of a manual count at flows up to 600 per hour per direction | 10 | max error | % | Analysis (CAL-001 C), TRL 3; field comparison with manual counts, TRL 4 | At risk: random merging alone loses 6.5 %; groups add more | R2 |
| PR-003 | UR-004 | Performance | Motor vehicle accuracy | The hourly count of motor vehicles in the nearest lane shall be within 15 % of a manual count | 15 | max error | % | Analysis (CAL-001 C), TRL 3; field comparison, TRL 4 | To verify at TRL 4: 4.2 frames per car, 3.4 px smear | R3 |
| PR-004 | UR-006 | Safety | Sensor cannot resolve a face or a plate | No image, audio or identifier shall leave the device and frames shall be held only in RAM; the sensor shall give at most 8 px/m at head height for a 1.75 m person, below the IEC 62676-4 detection level of 25 px/m | 8 | max | px/m | Analysis (CAL-001 B), TRL 3; design review and firmware audit, TRL 4 | Met on paper: 7.6 px/m (8.5 for a 2.0 m person) for passers-by; an installer within 0.5 m is above the detection level | R4 |
| PR-005 | UR-007 | Software | Open 10-byte count record | The counter shall send 15-minute counts per class and direction in an open, documented record of six 12-bit counters and a status byte over LoRaWAN | 10 | max | bytes | Inspection (design review, CAL-001 G), TRL 3 | Met by design | R5 |
| PR-006 | UR-005 | Performance | Coverage from one pole | One counter shall cover the full width of a 3 m sidewalk, a 2 m bike lane and the nearest 3.5 m traffic lane | 8.5 | min | m across the street | Analysis (CAL-001 A), TRL 3; field check, TRL 4 | Met on paper with the array turned 90 degrees: -4.45 to 8.34 m across | R6 |
| PR-007 | UR-009 | Materials | Survive -20 to +50 degrees C | The counter shall survive air temperatures from -20 degrees C to +50 degrees C | 70 | span | K | Inspection (part ratings, STM S7, S8), TRL 3; thermal chamber, TRL 4 | To verify at TRL 4: cell discharge rating and window film not yet measured | R7 |
| PR-008 | UR-009 | Performance | Count in sun and shade at temperate sites | The counter shall count at temperate sites, on design days with air up to 20 degrees C; hot-climate sites use the radar variant (CBC-DDR-002) | 20 | max air | degrees C | Analysis (CAL-001 D, STM S3), TRL 3; seasonal field test, TRL 4 | At risk: on the mild design day sunlit pavement hides pedestrians for 10.2 h with single frames, 3.2 h with track averaging; shaded 0 h. Summer days above 20 degrees C are outside the claim (the independent review put a 15 to 28 degrees C day at about 12 h blind on shaded pavement; not recomputed here) | R7 |
| PR-009 | UR-010 | Electrical | Three days without sun | The counter shall keep counting for 3 days without sun | 3 | min | days | Analysis (CAL-001 E2), TRL 3; bench test, TRL 4 | Met on paper: 6.22 days on one cell (4.36 at -20 degrees C, 3.49 with the end-of-life 80 % as well) | R8 |
| PR-010 | UR-010 | Electrical | Energy neutral in winter | The panel shall store more energy per day than the counter uses at 1.5 peak sun hours with a 40 % street derating, while the cell is allowed to charge (air above about 0 degrees C, STM S8) | 1.5 | min | peak sun hours | Analysis (CAL-001 E3, STM S6 and S8), TRL 3; field log, TRL 4 | At risk below about 0 degrees C air (cell may not charge below 0 degrees C; CBC-DEC-001 O1). Met on paper above it: 4.4 Wh/day stored against 2.47 Wh/day | R9 |
| PR-011 | UR-011 | Physical architecture | IP65 enclosure and head | The enclosure and the sensor head shall meet IP65 | 65 | min | IP rating | Inspection (design review, CAL-001 I), TRL 3; spray test, TRL 4 | To verify at TRL 4 | R10 |
| PR-012 | UR-002 | Physical architecture | Mass on the pole | The counter shall have a total mass of 6 kg or less | 6 | max | kg | Analysis (CAL-001 H5, cad/fidelity.json), TRL 3; weighing, TRL 4 | Met on paper: 5.24 kg with bought parts (CAD model 4.8 kg) | R11 |
| PR-013 | UR-001 | Usability | Install in 60 minutes by two people | Two trained people shall install the counter in 60 minutes or less | 60 | max | min | Analysis (CAL-001 H6, BLD-001), TRL 3; timed trial, TRL 4 | To verify at TRL 4: 59 min estimate for the task list in CAL-001 H6; it leaves out platform set-up, traffic control and teardown, which the independent review put at 75 to 90 min in all | R12 |
| PR-014 | UR-001 | Physical architecture | No drilling, welding or pole wiring | The counter shall fit with band clamps and a pole-top sleeve, with no drilling, welding or connection to the pole's wiring | 0 | max | pole modifications | Inspection (BLD-001, BOM lines 5 to 7), TRL 3 | Met by design | R12 |
| PR-015 | UR-015 | Physical architecture | Withstand 35 m/s gusts | The mounting shall withstand 35 m/s gusts with a safety factor of at least 1.5 on the pole top, arm and head | 35 | min | m/s | Analysis (CAL-001 H1, H3), TRL 3; bracket calculation, TRL 4 | Met on paper: panel 52 N, post factor 55, twist factor 3.3 | R12 |
| PR-016 | UR-013 | Packaging and transport | Parts cost within the value-engineering target | The priced BOM shall total 275 USD or less (a value-engineering target, not a limit) | 275 | max | USD | Analysis (BOM, CAL-001 J1), TRL 3 | At risk: 274.00 USD is 1.00 USD (0.4 %) under the target, less than the uncertainty in indicative prices | R13 |
| PR-017 | UR-011, UR-012 | Materials | Five years outdoors, one cell change | The counter shall last 5 years outdoors with one battery change, using UV-stable materials | 5 | min | years | Design review (CAL-001 I, STM S18 and S19), TRL 3; ageing and field trial, TRL 4 | To verify at TRL 4: window film grade and joint coatings not yet specified | R14 |
| PR-018 | UR-014 | Electrical | Radio within licence-free limits | Uplinks shall stay within the EU868 1 % duty cycle and the US915 400 ms dwell limit | 1 | max | % duty | Analysis (CAL-001 G), TRL 3 | Met on paper: 0.82 s/h at SF9 (limit 36 s/h); 371 ms at US915 DR0 | R15 |
| PR-019 | UR-016 | Usability | Public notice plate | A notice plate on the pole shall state what is counted, that no image is stored or sent, and the repository link | 1 | min | plate | Inspection (BOM line 12, BLD-001), TRL 3 | Met by design (CBC-DDR-001 D7) | R4 |
| PR-020 | UR-008 | Usability | Aim check on site | A crew shall be able to check the aim and confirm an uplink with a laptop or phone, using the calibration jumper and no special software | 10 | max | min | Analysis (CAL-001 H6), TRL 3; demonstration, TRL 4 | Met by design: 8 min estimate | R12 |
| PR-021 | UR-015 | Safety | Panel and head retained by lanyards | The panel mount and the sensor head shall each be held by a lanyard so that a failed fixing does not drop a part onto the street | 2 | min | lanyards | Inspection (BLD-001, BOM line 13), TRL 3 | Met by design | R12 |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Changes from CBC-REQ-001 v0.6

- R7 is split into PR-007 (survive -20 to +50 degrees C) and PR-008 (count at temperate sites). R12 is split into PR-013 (install time), PR-014 (no drilling), PR-015 (wind), PR-020 (aim check) and PR-021 (lanyards).
- PR-010 (was R9) is now at risk for sites where the air stays below about 0 degrees C: a LiFePO4 cell must not be charged below 0 degrees C and FieldNode's lockout stops charging (STM S8). The fix changes the shared FieldNode core, so it is an open decision for Amish (CBC-DEC-001 O1).
- PR-019 records the public notice plate decided on 2026-09-25 as its own requirement.
- PR-012 reads 5.24 kg, the figure `sizing.py` now prints for the model with fixings as individual parts; CBC-REQ-001 v0.6 said 5.26 kg.

## Assumptions

Table 2. Assumptions behind the targets.

| Assumption | Value | Source or basis |
| --- | --- | --- |
| Walking speed | 1.0 to 1.5 m/s | Typical design range (estimate) |
| Cyclist speed | up to 25 km/h | Typical urban maximum (estimate) |
| Vehicle speed in the nearest lane | up to 50 km/h | Common urban limit (estimate) |
| Peak sun hours, winter design case | 1.5 h | Mid-latitude winter (estimate) |
| Street shading and dust derating | 40 % | Estimate, to be checked on real poles |
| Temperate design day | Air 10 to 20 degrees C | CBC-CAL-001 section D |
