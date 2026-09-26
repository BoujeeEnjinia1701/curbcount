# BOM notes

Costs are indicative (September 2026 estimates) until suppliers are selected. Line numbers match the callouts in `media/exploded.png` and the part keys in `cad/src/model.py`; line 14 has no callout.

- Total parts cost is $290.00 (checked by `docs/04-calcs/sizing.py`, CBC-CAL-001 [J1]), against a `budget_usd` of $150 in `project.yaml` and against the $275 recommended in CBC-DDR-001 D1. The budget is unchanged; the new figure awaits Amish.
- Lines 1, 2, one cell of line 3 and $6 of line 14 are the FieldNode core, $98.00. They are priced from the FieldNode TRL 3 BOM ($126.00 core, less its $14 panel, $6 bracket and $8 mount kit, which CurbCount replaces with lines 4 to 6).
- The high-load power variant is the second cell ($9) and the 20 W panel ($30) in place of FieldNode's 6 W panel ($14), a net $25.
- The STM32WL-only variant studied in CBC-CAL-001 section F would drop line 11, the second cell and the 20 W panel, about $253.00 in all.
- Changes from TRL 2: the FieldNode lines are repriced to match FieldNode ($47 + $36 + 2 x $9, was $22 + $45 + 2 x $18); the panel mount is aluminium; line 6 now includes the enclosure saddle plate; the cable is 2 m; line 13 (public notice plate) is new and hardware moves to line 14.
- The street pole is not part of the BOM.
