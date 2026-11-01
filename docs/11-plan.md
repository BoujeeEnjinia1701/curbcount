---
doc_id: CBC-PLN-001
title: CurbCount project plan
project: CurbCount
doc_type: Project plan
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

# CurbCount project plan

CurbCount is at stage P3 (TRL 3, paper): the design is constructable and fully documented, and the next gate (P4, TRL 4) is on hold under the portfolio cap. The decisions requested from Amish are the concept choice (O2) and the cold-site question (O1) in CBC-DEC-001. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Design lead | CBC-PRB-001, CBC-URS-001 | Done (v0.8; URS v0.1) |
| STEM check | Design lead | CBC-STM-001, `stem_check.py` | Done; S8 open for Amish |
| Concept options | Design lead | CBC-OPT-001, CBC-DDR-004 | Done; choice awaits Amish |
| Requirements and traceability | Design lead | CBC-PRS-001, CBC-RTM-001 | Done; 4 PRs at risk |
| Calculations | Design lead | CBC-CAL-001, `sizing.py` | Done (v0.4) |
| CAD at D3, every option | Design lead | `cad/src/model.py`, `cad/fidelity.json`, STEP, STL, drawings | Done; D3 pass |
| Build plan | Design lead | CBC-BLD-001 | Done (paper only) |
| Regulatory, feasibility, risk, market | Design lead; regulatory consultant | CBC-REG-001, FEA-001, RSK-001, MKT-001 | Done; many rows to assess |
| Renders and storefront images | Coordinator | `media/render-*.png`, `media/options.png`, cards | Rendered on Amish's Mac; options picture pending |
| Partner and co-design | Amish | A partner city with manual counts | Not started |
| Hardware build and tests | (on hold) | TRL 4 and later | On hold by the portfolio cap |

## Resources needed

Table 2. Resources. Effort is for the work after TRL 3 and is listed only as planned work.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Partner city transport staff | Manual counts for comparison, site and pole access | to assess with the partner | to assess |
| Regulatory consultant | Rows marked to assess in CBC-REG-001 | to assess | to assess |
| Design lead | Decisions O1 and O2, partner talks | a few days | none for the design |
| Parts for a first unit (TRL 4, on hold) | BOM lines 1 to 14 | not started | 274.00 (indicative prices) |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN exist | Passed |
| P1 Definition | URS, PRS, RSK, MKT exist; REG complete | Passed (REG rows marked to assess need a consultant) |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR; STM and FEA closed | Reached except that STM has one open item (S8) and eight plausible rows, and the concept choice awaits Amish |
| P3 Design outputs | Model, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability complete | Reached; stage recorded in the kit 1.9.1 upgrade of 2026-10-31 |
| P4 Verification | Test plans and lab test reports | On hold |
| P5 Validation | Field trials with a partner, certification status | On hold |
| P6 Commercialization | Launch plan, instructions for use, standard cost | On hold; the release gate needs `stem_check: pass`

## Next steps and decision requested

1. Amish decides O2, the concept choice (A and B are within 10 %; A is the lean, with B as the hot-climate variant already agreed on 2026-09-25).
2. Amish decides O1: how to handle charging below -5 degrees C (limit the claim to cool sites now; ask FieldNode for a heated pocket or low-temperature cell).
3. The coordinator renders the product views and `media/options.png` on the Mac.
4. Close the plausible STEM rows (S3 to S5, S16 to S19, S24) by the tests that settle them once TRL 4 is allowed.

## References

- CBC-PRB-001 v0.8, CBC-STM-001 v0.1, CBC-OPT-001 v0.1, CBC-URS-001 v0.1, CBC-PRS-001 v0.7, CBC-RTM-001, CBC-CAL-001 v0.4, CBC-BLD-001, CBC-REG-001, CBC-FEA-001, CBC-RSK-001, CBC-MKT-001, CBC-DEC-001, CBC-DDR-001 to 004 (this repo).
- Melexis MLX90640 datasheet, https://media.melexis.com/-/media/files/documents/datasheets/MLX90640-datasheet-melexis.pdf, accessed 2026-10-31.
- SparkFun IR Array Sensor 110 degree FOV MLX90640, https://www.sparkfun.com/ir-array-sensor-110-degree-fov-mlx90640.html, accessed 2026-10-31.
- Texas Instruments IWR6843, https://www.ti.com/product/IWR6843, and IWR6843ISK-ODS, https://www.ti.com/tool/IWR6843ISK-ODS, accessed 2026-10-31.
- NZ Transport Agency, cycle counting summary, https://nzta2.cwp.govt.nz/resources/sustainable-transport/cycle-counting-in-nz/summary, accessed 2026-10-31.
- Regulation (EU) 2016/679, https://eur-lex.europa.eu/eli/reg/2016/679/oj; Regulation (EU) 2024/1689, https://eur-lex.europa.eu/eli/reg/2024/1689/oj.
- Department for Transport (England), Walking and cycling statistics 2023, https://www.gov.uk/government/statistics/walking-and-cycling-statistics-england-2023.
- World Health Organization, road safety news release of 13 December 2023, https://www.who.int/news/item/13-12-2023-despite-notable-progress-road-safety-remains-urgent-global-issue.
