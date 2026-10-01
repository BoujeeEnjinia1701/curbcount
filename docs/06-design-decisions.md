---
doc_id: CBC-DEC-001
title: CurbCount design decisions register
project: CurbCount
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions gathered from the review note and the decision records
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# CurbCount design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, CBC-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Decisions still to be made.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction (saddles, bands through slots, FieldNode constructable core, bolted arm, head fixing and window frame, bolted pole-top mount, cable routes, notice ties) | Accept; or change individual items | Accept | The whole build plan | CBC-DDR-003, A2 |
| 2 | First co-design partner and street | City transport department, residents' group or university | None made | Pole size and band size; climate (a hot city brings the radar variant forward) | CBC-DDR-002, O1 |
| 3 | Sensor port pinout, port A's supply voltage and the calibration jumper, agreed with FieldNode | I2C and a switched 3.3 V rail on port A's five pins (the build plan fits a 3.3 V load switch in place of FieldNode's port A boost converter); a jumper-sense pin on FieldNode's service header | Agree with the FieldNode project | Which cores of the sensor cable go to which breakout pin; the port A supply module (build plan section 3.3) | REVIEW 2026-09-25 cross-repo actions; FND-DDR-001, O2 |
| 4 | Pole top drawn 560 mm lower in the photoreal renders | Accept as render-only layout; or render at the installed height | Accept as render-only | None (renders only) | REVIEW 2026-09-26, item 1 |
| 5 | Notice plate drawn at 4.15 m in the renders (installed at 2.6 m) | Accept as render-only; or render at 2.6 m | Accept as render-only | None (renders only) | REVIEW 2026-09-26, item 2 |
| 6 | Notice plate wording | Adopt the proposed wording ("PRIVACY-SAFE COUNTER", what is counted, no images taken or stored, only counts sent, repository link); or reword | Adopt. The fixing is now set by the design for construction (two ties through slots) | The printed face of the notice plate | REVIEW 2026-09-26, item 3 |
| 7 | Status light on the sensor head | Drop it; or keep it as a public "counting" cue at about 1 mW | Drop it | None in the build plan (no light is fitted) | REVIEW 2026-09-26, item 4 |
| 8 | "COUNTS ONLY" plaque on the head and the enclosure label | Print or emboss the plaque in the housing and treat the label as part of BOM line 1; or separate parts | Print and treat as BOM line 1 | Head housing print (an optional embossed plaque) | REVIEW 2026-09-26, item 5 |
| 9 | Head window bezel and head bolts shown in the appearance model | Superseded by the window frame and M5 bolts of the design for construction; update the appearance model to match | Close as superseded once item 1 is accepted | None beyond item 1 | REVIEW 2026-09-26, item 6; CBC-DDR-003, P4 |

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
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CBC-DDR-003 (changes made under this instruction, open for review: open decision 1) |
