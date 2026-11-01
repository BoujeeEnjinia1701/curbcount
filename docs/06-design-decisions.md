---
doc_id: CBC-DEC-001
title: CurbCount design decisions register
project: CurbCount
doc_type: Design decisions register
version: '0.5'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-09-30'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions gathered from the review note and the decision records
- version: '0.2'
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: '0.3'
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations for all nine open decisions on 2026-10-02 (CBC-DDR-003 accepted); moved to decisions made
- version: '0.4'
  date: '2026-10-02'
  author: Amish Chadha
  change: Decisions 5 to 9 carried into model.py, the appearance model and the BOM
- version: '0.5'
  date: '2026-10-31'
  author: Amish Chadha
  change: 'Kit 1.9.1 upgrade: open decisions O1 (cold charging) and O2 (concept choice) added; C1 (radar duty cycle) and C2 (model rebuilt, no dimension changed) recorded as decided under the standing instruction'
---

# CurbCount design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, CBC-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| O1 | Cold charging: LiFePO4 may not be charged below 0 degrees C, so charging stops below about 0 degrees C air (STM S8) | (1) limit the claim to cool sites; (2) heated cell pocket in the FieldNode core; (3) low-temperature cell | Option 1 now (done in PR-010), and raise 2 and 3 with the FieldNode project | BOM line 3 and the FieldNode enclosure if 2 or 3; PR-010; CAL-001 E | CBC-DDR-004, O1; CBC-STM-001 S8 |
| O2 | Concept choice between the thermal array head (A) and the 60 GHz radar head (B); scores 121 and 110, within 10 % so no pick is made | (1) A as the build, B as the hot-climate variant; (2) B for all sites; (3) a combined head | Option 1 (already decided on 2026-09-25; nothing changes) | Nothing if 1; the whole head, panel and cells if 2 | CBC-DDR-004, O2; CBC-OPT-001 |
| O3 | Vehicle counting: a car's warm hood is in the field for 3.2 frames, not 4 (STM S5) | (1) 32 Hz subpages with 1 MHz I2C: 6.4 frames, noise up by the square root of 2, a faster pull-up; (2) accept that vehicle counts are not met and say so; (3) a vehicle sensor on option B only | Option 1: it is firmware and bus speed, but it sets the shared FieldNode sensor port speed, so FieldNode must agree | CAL-001 C, F; PR-001, PR-003; FieldNode sensor port | CBC-DDR-004, O3; CBC-STM-001 S5 |
| O4 | If option B is carried forward: FieldNode's high-load charger for the 20 W panel (5.0 A against the 1.5 A setting, STM S28) and a shield or shaded cell for hot sites (STM S26) | (1) FieldNode high-load variant plus shield; (2) leave B as a thermal-only-hot-site study | Option 1, argued in the FieldNode project | Option B's BOM, enclosure and panel; nothing in option A | CBC-DDR-004, O4; CBC-STM-001 S26, S28 |

## To confirm when parts are bought

*Table 2. Things to check against the real part before it is used.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The solar panel's frame has a flat back lip at least 12 mm wide at its short ends | The rail plate bolts through it; without it the panel cannot be fixed as drawn | CBC-DDR-003, P5 |
| 2 | The enclosure model, its boss spacing (110 x 160 mm assumed) and its lug kit | They set the internal plate holes and the lug screw holes in the saddle plate | FND-DDR-003; CBC-DDR-003, P2 |
| 3 | Band clamps that close on the loop for the site pole: about 470 mm on a 114 mm pole (330 mm on 60 mm, 545 mm on 140 mm) | A worm-drive band has a limited range; the wrong size will not tighten | CBC-DDR-003, P1 |
| 4 | The sleeve tube's bore is at least 122 mm, and the cap disc fits it closely | The sleeve must clear a 114.3 mm pole by 3 to 4 mm all round | CBC-DDR-003, P5 |
| 5 | The band torque that gives 1,000 N of preload | The twist calculation assumes that preload | CBC-CAL-001 [H3] |
| 6 | The sensor cable has five cores of about 0.25 mm², a moulded M12 A-coded plug and an open end | The open end goes through the head gland to the breakout | CBC-DDR-003, P6 |
| 7 | Prices of every BOM line | The estimate is $1.00 under the $275 value-engineering target | CBC-CAL-001 [J1] |

## Value engineering

Value-engineering target: USD 275 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 274.00 (USD 1.00 under the target). The estimate rests on indicative prices.

Main cost drivers: the FieldNode share (lines 1 to 3, 14 and part of line 13) at USD 105.00, FieldNode's own panel (line 4) at USD 14, and the parts added for construction together with FieldNode's repricing of its core, which took the total from USD 253.00 to USD 274.00. The ESP32-S3 fallback head would cost about USD 311.00, over the target.

Savings worth trying: leaving port B out of CurbCount's core (about USD 6 less, departing from the standard FieldNode core), and confirming prices when parts are bought.

## Decisions made

*Table 3. Decisions made, with the words recorded.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Batch taken through TRL 3, nothing past it | Amish: "you know the drill, nothing gets past TRL 3" | REVIEW 2026-09-25 (TRL 3) |
| 2026-09-25 | TRL 2 items D1 to D7: $275 value-engineering target, thermal array first with radar as the hot-climate variant, FieldNode high-load variant raised with FieldNode, processor study, 15-minute bins and three classes, jumper-only calibration, public notice plate | Amish: "i accept all your recommendations, go with them across all repos." | CBC-DDR-001, CBC-DDR-002 |
| 2026-09-25 | Tracking on FieldNode's STM32WL as the baseline with the ESP32-S3 head as fallback; one cell and the 6 W panel; R4 restated in px/m; R7 for temperate sites; R11 kept at 6 kg; 10-byte record | Amish, same instruction | CBC-DDR-002, items 3 to 8 |
| 2026-09-30 | Build plan format approved for all repos; outstanding decisions kept out of the build plan, in this register | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos" | This register; CBC-BLD-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CBC-DDR-003 (changes made under this instruction; accepted on 2026-10-02, below) |
| 2026-10-02 | Design for construction accepted as a whole: the changes P1 to P7 of CBC-DDR-003 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | CBC-DDR-003, A2 |
| 2026-10-02 | First co-design partner: a city transport department that already runs manual or loop counts on a street with a bike lane and poles of 60 to 140 mm, with the first trial in a season with air under 20 °C. First candidate to approach: the City of Toronto's transportation services, which publishes its traffic count data | Amish: "i approve your recommendations for all 555 open decisions." | CBC-DDR-002, O1 |
| 2026-10-02 | Sensor port: CurbCount's position to agree with FieldNode is one common pin order for both ports (supply, ground, I2C data, I2C clock, spare), each port's supply voltage set by a per-project supply module (switched 3.3 V on port A for CurbCount), and the calibration jumper sensed on FieldNode's service header | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-25 cross-repo actions; FND-DDR-001, O2 |
| 2026-10-02 | Pole top drawn 560 mm lower in the photoreal renders accepted as a render-only layout; the caption says it is drawn closer than installed | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 1 |
| 2026-10-02 | Notice plate rendered at its installed 2.6 m, not 4.15 m | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 2 |
| 2026-10-02 | Notice plate wording adopted with one fix: "No images are stored or sent; only counts leave the device" replaces "No images are taken or stored"; the rest and the repository link are kept | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 3 |
| 2026-10-02 | Status light on the sensor head dropped | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 4 |
| 2026-10-02 | "COUNTS ONLY" plaque embossed into the printed head housing (BOM line 8); the enclosure label is part of BOM line 1 | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 5 |
| 2026-10-02 | Head window bezel and head bolts of the appearance model closed as superseded by the window frame and M5 bolts of CBC-DDR-003, P4; the appearance model was updated to match on 2026-10-02 | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 6; CBC-DDR-003, P4 |
| 2026-10-31 | C1: option B's radar runs in frame bursts for about 0.2 W average, one burst in six (was 1.2 W continuous, which drew 32 Wh/day against 14.5 Wh/day stored; 0.25 W still gave only 2.6 days with cold and end of life together); two cells and a 20 W panel unchanged | Claude, under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | CBC-DDR-004, C1; STM S22, S23 |
| 2026-10-31 | C2: model.py rebuilt to the kit 1.9 interface at D3 for both options with every fixing as a part; `PARAMS` and `derived()` identical to the kit 1.7 model, so no design dimension changed | Claude, under the same instruction (modelling only) | CBC-DDR-004, C2; cad/fidelity.json |
