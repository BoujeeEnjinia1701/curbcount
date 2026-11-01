---
doc_id: CBC-FEA-001
title: CurbCount feasibility assessment
project: CurbCount
doc_type: Feasibility assessment
version: '0.1'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-10-31'
  author: Amish Chadha
  change: Opened in the kit 1.9.1 upgrade
---

# CurbCount feasibility assessment

The thermal array counter is feasible to build and mount on paper at the 275 USD target (274.00 USD), and its main weakness is counting accuracy, not construction; the radar option is feasible in principle but not shown to fit the cost or the rules. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | The thermal array design is constructable on paper: 127 parts modelled at D3 with real stock, fasteners and clearances, interference-free; wind, twist, coverage, energy and radio close in CAL-001 | High | The tracker's frame-count margin for cars is 4.2 against 4 needed (PR-001); sunlit pavement hides people for part of a warm day (PR-008) | STM S1 to S7, CAL-001, cad/fidelity.json |
| Materials | Aluminium sections and sheet, printed ASA, a polycarbonate FieldNode enclosure, stainless fasteners and bands: all stock | Medium | HDPE window film grade for UV is unchosen (S18); aluminium against stainless and a steel pole needs a coating or isolating washers (S19) | STM S18, S19; BOM |
| Manufacturing and assembly | Garage-buildable: cut and drill aluminium, print one housing, assemble with hand tools; 14 BOM lines; install by two people in about 59 minutes | High | Many holes are drilled to a template; the build plan (BLD-001) gives the order and the jigs | BLD-001, CAL-001 H6 |
| Power and controls | One LiFePO4 cell and a 6 W panel give 6.22 days of autonomy and 4.4 Wh/day against 2.47; the tracker takes about 2 % of the processor | Medium | Charging stops below about 0 degrees C air (S8, open decision O1); cycle count of the tracker is an estimate until profiled (S16) | STM S6 to S8, S16; CAL-001 E, F |
| Supply of parts | Every line is a catalogue part or a stock section; the array breakout is the one costly line (65.00 USD, SparkFun class) | Medium | The BOM total sits 1.00 USD under the 275 USD target on indicative prices; the sensor price was checked on 2026-10-31 (64.95 USD) and the rest is unchecked | BOM, MKT |
| Sensing and data (the risk the design rests on) | The principle holds (S1, S2) but accuracy is not shown until counts are compared with manual counts | Low | PR-001, PR-002 and PR-008 are at risk on paper; a field comparison is TRL 4 work and on hold | CAL-001 C, D; PRS |
| Option B (radar head) | Modelled at D3 (128 parts); energy closes only with a duty-cycled radar, a 20 W panel and two cells | Low | Module price and 60 GHz rules unknown (G9); tracker burst rate to be profiled; 60 GHz hardware is harder to build in a garage | STM S21 to S24; OPT |

Ratings: High, Medium, Low.
