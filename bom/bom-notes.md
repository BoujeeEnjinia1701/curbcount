# BOM notes

Costs are indicative (September 2026 estimates) until suppliers are selected. Line numbers match the callouts in `media/exploded.png` and the part keys in `cad/src/model.py`; line 13 has no callout.

- Total parts cost is $274.00 (checked by `docs/04-calcs/sizing.py`, CBC-CAL-001 [J1]), against a `budget_usd` of $275 in `project.yaml`, set by Amish's decision of 2026-09-25 (CBC-DDR-002). The margin is $1.00, which rests on indicative prices (CBC-DEC-001).
- Baseline since CBC-DDR-002: tracking runs on FieldNode's STM32WL, so the separate ESP32-S3 edge processor (TRL 3 line 11, $12) is gone, and the counter runs on standard FieldNode power: one cell and FieldNode's 6 W panel ($14) in place of the second cell ($9) and the 20 W panel ($30). The saving is $37.00 against the $290.00 TRL 3 BOM.
- Lines 1, 2, 3, 14 and $6 of line 13 are the FieldNode core, $105.00, priced from the FieldNode constructable BOM (FND-DDR-003). Line 4 is FieldNode's own 6 W panel, mounted on CurbCount's pole-top mount (line 5).
- ESP32-S3 fallback (kept on paper only, CBC-DDR-002): add the processor ($12), a second cell ($9) and a 20 W panel ($30 in place of $14), about $311.00 in all, above the budget.
- Line 5 is aluminium and all bolted (CBC-DDR-003): sleeve with rivet-nut set screws, cap disc, post on angle clips with plugs, and a 290 x 150 x 3 mm rail plate that the panel bolts to through its frame lip.
- Line 13 includes the calibration jumper link: frames can be shown on a laptop only with the link fitted on the FieldNode service header, never over the radio (DDR-001 D6).
- The street pole is not part of the BOM.

- Design for construction (CBC-DDR-003, 2026-09-30): lines 1, 5, 6, 7, 8, 9, 11, 12 and 13 respecified for the constructable design; line 14 (plug-in connector strip and rail fuses, $5, FieldNode BOM line 15) added; line 1 repriced to FieldNode's $49 core. The total rose from $253.00 to $274.00.
