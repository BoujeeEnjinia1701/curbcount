# Review note: CurbCount

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CBC-PRB-001 v0.2): problem, users, operating context, constraints, prior work with cited sources, out of scope, open questions; co-design checklist kept.
- `docs/02-concept.md` (CBC-PRC-001 v0.2): how it works, 12 numbered components, first-order numbers with assumptions, key design choices, safety and privacy, open questions.
- `docs/03-requirements.md` (CBC-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, verification and concept status, plus a design case and assumptions.
- `cad/src/concept_media.py`: massing model of the counter (FieldNode enclosure, board, cells, 20 W panel and bracket, clamps, arm, sensor head, window, thermal array, processor, cable), each part with a BOM number; street pole, sidewalk, road, sensing footprint and a 1.75 m person as grey context. Also draws a custom two-row data and energy flow diagram, because the kit's flow function takes only numeric losses.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` (callouts 1 to 12 match the BOM), `cutaway.png` (enclosure and sensor head sectioned), `flow.png` (estimates labeled). Temporary `media/_views*` folders removed.
- `bom/bom.csv`: 13 lines with indicative USD prices; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line, then the required sections (Concept rationale, Burning platform, Where it could be used with industry and country tables, What sparked the idea) expanded with cited figures; Concept, Key components and Safety updated to match.
- `project.yaml`: unchanged (pitch and problem remain correct).

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Sensing footprint | about 12 m along x 6.9 m across (2.1 m behind curb to 4.8 m into the road) | R6 not met for a 3 m sidewalk |
| Ground pixel size | about 0.3 to 0.4 m | R4 met by design |
| Continuous load | about 0.30 W, 7.2 Wh/day | 2.4 times FieldNode's sensor budget |
| Autonomy | about 4.3 days (two cells); 2.1 days (one cell) | R8 met only with two cells |
| Winter harvest, 20 W panel | about 16 Wh/day | R9 met; not met with 6 W (about 4.9 Wh/day) |
| Uplink | 14 bytes per 15 min, about 0.8 s/h airtime | R5, R15 met |
| Mass on pole | about 4.2 kg | R11 met |
| Parts cost | about $271 | R13 not met ($150 budget) |

Requirements not met or at risk:

- **R13 (cost) not met:** about $271 against $150.
- **R6 (coverage) not met** for sidewalks wider than about 2 m from a pole at the curb.
- **R8 and R9 not met** with the standard FieldNode power parts (one cell, 6 W panel); met only with the proposed upgrade.
- **R2 (accuracy) at risk:** people walking side by side merge into one blob.
- **R7 (hot weather) at risk:** little thermal contrast when pavement and air are near body temperature.

### Proposed, awaiting Amish (items 1 to 7 now Decided by Amish, 2026-09-25: go with recommendation; item 8 still awaiting Amish; see CBC-DDR-002)

1. **Budget.** Options: (a) raise `budget_usd` to $275; (b) keep $150 and cost the FieldNode core (about $95 of the $271) under FieldNode, leaving about $176 for CurbCount parts, still over; (c) cut cost with an 8 x 8 thermal array and no separate processor, which weakens R1 and R2. Recommendation: (a). Decided by Amish, 2026-09-25: go with recommendation (`budget_usd` now $275, see the TRL 3 session item 2).
2. **Sensor.** Option A: 32 x 24 thermal array (cheap, low power, privacy by physics). Option B: 60 GHz mmWave radar (works in heat and darkness, costs and draws more). Recommendation: A for the first build, B studied as a hot-climate variant. Decided by Amish, 2026-09-25: go with recommendation.
3. **Power.** The counter needs a FieldNode "high-load" variant (20 W panel, second cell). Recommendation: raise this with the FieldNode project rather than changing FieldNode here. Decided by Amish, 2026-09-25: go with recommendation.
4. **Processor.** ESP32-S3 in the sensor head, or tracking on FieldNode's STM32WL alone. Recommendation: ESP32-S3 first; STM32WL-only as a TRL 3 study. Decided by Amish, 2026-09-25: go with recommendation.
5. **Count interval** of 15 minutes, and three classes (pedestrian, cyclist or micromobility, motor vehicle). Recommendation: adopt both. Decided by Amish, 2026-09-25: go with recommendation.
6. **Calibration mode** that shows frames on a laptop through a physical jumper only. Recommendation: allow it, never over the radio. Decided by Amish, 2026-09-25: go with recommendation.
7. **Public notice** on each pole linking to this repository. Recommendation: yes. Decided by Amish, 2026-09-25: go with recommendation.
8. **First partner and street** for co-design. No recommendation; Proposed, awaiting Amish.

### Safety concerns

- Work at height beside traffic when installing; pole owner's permission, trained crews, traffic management.
- Falling parts from 4 to 5 m: safety lanyards on panel and head; about 170 N wind load on the panel to check.
- Two LiFePO4 cells (about 38 Wh): fusing and cold-charge lockout.
- Privacy: the design must stay unable to capture identifiable images; any future sensor change (for example to a higher-resolution array) needs a fresh privacy review.

### Notes and gaps

- The kit's `flow_diagram` accepts only numeric losses, so `flow.png` is drawn by a small function in `concept_media.py` in the kit's style.
- In the exploded view the tiny parts (thermal array, cells) are partly hidden by their callout circles at this scale, and callout 6 sits between the four clamps.
- The split of FieldNode's about $126 cost across BOM lines 1, 2, 3 and 5 is an estimate; the FieldNode BOM is the reference.
- Some candidate sources (Telraam, Eco-Counter product pages, FHWA Traffic Monitoring Guide) could not be fetched and were left out.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check footprint, thermal contrast, window transmission, power and wind load by calculation, and to produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CBC-DDR-001 v0.1, status proposed): seven items adopted as recommended for TRL 3, open for Amish's review (D1 to D7), and two left open (O1, O2).
- `docs/04-calcs/01-sizing.md` (CBC-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: coverage and occlusion, pixel size and privacy, frames per crossing, merging, window transmission and thermal contrast on three design days, energy and panel sizing, charger current, heat, a processor study (STM32WL alone), radio airtime and US915 limits, wind and mounting, mass, installation time, service life and cost, with a status for every requirement. The script imports the model's parameters and camera model, reads the BOM and `project.yaml`, prints every number the note quotes and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model (FieldNode enclosure with ports and antenna, board, two cells, 20 W panel, aluminium pole-top mount, bands and saddle plates, sensor arm, head with hood, window, array and processor, M12 cable, notice plate) with the sensor's camera model. Exports `cad/step/` and `cad/stl/` for `curbcount-assembly`, `sensor-head` and `power-core`.
- `cad/src/sheets.py` and `cad/drawings/CBC-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:20, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". CBC-DWG-001 was free because the concept blueprint is CBC-DWG-010. The sheet shows a pole stub only; heights above the road are labeled.
- `bom/bom.csv` (14 lines, all priced with a supplier or supplier type, $290.00) and `bom/bom-notes.md`. FieldNode lines are repriced to FieldNode's TRL 3 BOM; the public notice plate is new (line 13).
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered (blueprint now Rev P2) and every image checked; temporary `_views` folders deleted.
- CBC-PRB-001, CBC-PRC-001 and CBC-REQ-001 revised to v0.3; `README.md` (TRL badge and line, links, Concept rationale figure, Concept numbers, key components) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

### Requirement status (CBC-CAL-001, Table 5)

3 not met, 4 at risk, 4 not verifiable at TRL 3, 3 met on paper, 1 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R13 Cost | **Not met** | $290.00 against $150, and $15 over the recommended $275 |
| R7 Hot weather | **Not met** on paper | Hot design day: pedestrian contrast below the 5.3 K threshold for 14.2 h (sunlit) and 24 h (shaded); 11.2 h even with track averaging |
| R4 Privacy as written | **Not met** as written | Smallest ground pixel 0.22 m against 0.25 m; privacy aim met at 8.5 px/m at head height against 250 px/m to identify |
| R1 Classes and directions | At risk | 4.2 frames for a car at 50 km/h (4 assumed needed) |
| R2 Pedestrian accuracy | At risk | Random merging alone loses 6.5 % at 600/h |
| R11 Mass | At risk | 6.02 kg against 6 kg (TRL 2 said 4.2 kg) |
| R15 Radio | At risk | 0.91 s/h at SF9 is fine; the 14-byte record does not fit US915 DR0 (11 bytes) |
| R3, R10, R12, R14 | Not verifiable at TRL 3 | R12: 59 min install estimate; panel 170 N, post factor 9, twist factor 3.2 |
| R6, R8, R9 | Met on paper | Footprint -4.45 to 8.34 m; 4.78 days without sun; 14.5 Wh/day stored against 6.43 Wh/day |
| R5 | Met by design | 14 bytes per 15 min bin |

Key numbers: 268 mW average from the cells (2.1 times FieldNode's 115 mW allowance); 5.0 A peak charge current from the 20 W panel; HDPE window transmission about 0.75 (estimate).

Design changes made from the calculations, open for Amish's review with the rest (now Decided by Amish, 2026-09-25: go with recommendation, CBC-DDR-002): the array is turned 90 degrees (110 degree axis across the street, 7.5 degree tilt), which moves R6 from not met to met on paper; the pole-top mount is aluminium (the steel one weighed 5.7 kg); the FieldNode enclosure takes its TRL 3 size (150 x 90 x 200 mm) on a CurbCount saddle plate.

### Decisions recorded (CBC-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (now all Decided by Amish, 2026-09-25: go with recommendation, CBC-DDR-002): D1 budget option (a), $275, recorded only, `budget_usd` unchanged at $150; D2 thermal array first, radar as a hot-climate variant; D3 FieldNode high-load variant, raised with FieldNode rather than changed there; D4 ESP32-S3 first, STM32WL-only studied (done, CBC-CAL-001 section F); D5 15-minute bins and three classes; D6 jumper-only calibration mode; D7 public notice plate. No reworded pitch or problem was recommended, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish (items 2 to 8 now Decided by Amish, 2026-09-25: go with recommendation, CBC-DDR-002; item 1 still awaiting Amish)

1. **O1, first co-design partner and street.** No recommendation was made.
2. **O2, budget.** `budget_usd` stays $150. The recommended $275 is itself $15 short of the $290.00 BOM. Options: (a) $300; (b) $275 with the STM32WL-only variant (about $253); (c) keep $150 and accept R13 not met. Recommendation: (b), if item 3 is accepted; otherwise (a). Decided by Amish, 2026-09-25: go with recommendation: (b).
3. **New, move tracking to the STM32WL.** CBC-CAL-001 section F finds it feasible on paper with a fixed-point tracker (2 % of the core, 44 kB of 64 kB RAM) and it brings the head to 92 mW, inside FieldNode's allowance, so standard FieldNode power (one cell, 6 W) meets R8 and R9 and about 1.5 kg and $37 come off. Risks: I²C over the 2 m cable and the reference driver's floating-point cost. Recommendation: adopt as the baseline for the first build, keep the ESP32-S3 head as the fallback. Decided by Amish, 2026-09-25: go with recommendation.
4. **New, R7 and the sensor for hot climates.** A thermal-only counter goes blind for much of a hot day. Options: (a) restrict the thermal build to temperate sites and state it; (b) bring the radar variant forward as the hot-climate build; (c) a hybrid head. Recommendation: (a) now and (b) for any hot partner city. Decided by Amish, 2026-09-25: go with recommendation.
5. **New, restate R4.** Replace "ground pixel 0.25 m or larger" with "8 px/m or less at head height, below the IEC 62676-4 detection level of 25 px/m", which matches the privacy aim. Recommendation: adopt. Decided by Amish, 2026-09-25: go with recommendation.
6. **New, R11 mass.** 6.02 kg against 6 kg. Recommendation: keep 6 kg and meet it through item 3 (about 4.5 kg). Decided by Amish, 2026-09-25: go with recommendation.
7. **New, payload.** Pack the record into 10 bytes (six 12-bit counters and a status byte) so it fits US915 DR0 (R15). Recommendation: adopt. Decided by Amish, 2026-09-25: go with recommendation.
8. **New, raise with FieldNode (not edited here):** the high-load variant needs a charger set for 5 A and a second fused cell; CurbCount needs a 60 to 140 mm pole saddle; the sensor port pinout needs I²C or UART plus a 3.3 V rail. Decided by Amish, 2026-09-25: go with recommendation; listed under cross-repo actions in the 2026-09-25 recommendations-accepted session.

Suggestion only, not in the repo: a side-arm panel mount for poles whose top carries a lantern.

### Cross-repo consistency

- FieldNode (FND REVIEW, TRL 3): enclosure 150 x 90 x 200 mm, STM32WL-class module, two M12 5-pin ports with one switched rail each, 6 Ah LiFePO4 cell charging 0 to 45 °C, core cost $126.00, 15 min default interval, TwinKit first. CurbCount now uses all of these. Conflicts noted, FieldNode not edited: (1) FieldNode's mount kit seats 40 to 60 mm poles, street poles are about 114 mm, so CurbCount adds its own saddle; (2) FieldNode's charger is sized for a 6 W panel, CurbCount's 20 W panel needs 5 A; (3) FieldNode's proposed 100 mW sensor allowance leaves CurbCount's ESP32-S3 head (241 mW) far out and the STM32WL variant (92 mW) just inside; (4) FieldNode quoted CurbCount's core share as about $95, now $98.00 from FieldNode's own BOM.
- TwinKit: LoRaWAN concentrator and 15 min reporting; a 14-byte uplink at SF9 (226 ms) is within its sizing. No conflict.
- No other shared component (CellGuard, MotionCore, ThermaCart, CalRig) is used.

### Safety concerns

- Work at height next to traffic, as at TRL 2. The counter adds 170 N of wind load at 5.5 m (933 N·m at the pole base) that the pole owner must check; the sleeve bears on the pole top with about 750 N.
- Two LiFePO4 cells, about 38 Wh, and a charge current of up to 5 A: fuse each cell, keep the 0 to 45 °C charge lockout, and never defeat the heat lockout to recover energy in a heatwave (the cells run flat after about 8 hot clear days without a shield).
- Falling parts: lanyards on panel and head; set-screw and band torque to be specified at TRL 4.
- Privacy: 8.5 px/m at head height is the design's privacy guarantee. Any change to a higher-resolution array, or a lower mounting height, needs a fresh privacy review.

### Gaps and notes

- Citations: the TRL 2 note listed no unchecked citations in the docs (the Telraam, Eco-Counter and FHWA pages had been left out). This session quotes the IEC 62676-4 detection and identification levels from the standard; WebFetch could not reach a source (one domain cache-only, one approval timed out), so those figures are flagged here as not checked online. MLX90640, ESP32-S3 and STM32WL figures, the HDPE absorption and all surface temperatures are typical values or assumptions, not checked against datasheets.
- The thermal contrast model (section D) is the weakest part of the note; the hot-weather conclusion holds across the assumptions tried, the mild-day hours do not.
- The kit's cutaway still cuts near the origin, so `concept_media.py` shifts the scene down by the enclosure height (as at TRL 2). The exploded view's callouts 10 and 11 cover their small parts.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build or firmware material exists or was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on items 1 to 7 above and the design changes listed under the requirement table; item 8 should go to the FieldNode project. For the record only, TRL 4 would need: a bench build of the sensor head on a FieldNode core; a lab test report (TST, `environment: lab`) covering window transmission, array noise at 16 Hz, tracker CPU and RAM on the STM32WL, I²C over the cable, current draw and charge current; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item in this note and in CBC-DDR-001 that carried a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (CBC-DDR-002 v0.1). The repo stays at `trl: 3`, `trl_target: 3`.

### Decisions applied and what changed

| Decision | Before | After |
| --- | --- | --- |
| Budget, option (b) (O2, TRL 3 item 2) | `budget_usd` $150; R13 target $150 | `budget_usd` $275; R13 target $275 |
| Tracking on the STM32WL as baseline, ESP32-S3 as fallback (TRL 3 item 3) | ESP32-S3 head, two cells, 20 W panel; head 241 mW; 6.43 Wh/day | No head processor, one cell, FieldNode's 6 W panel; head 92 mW; 2.47 Wh/day |
| Parts cost (follows the two above) | $290.00, 14 BOM lines | $253.00, 13 lines (line 11 removed, 12 to 14 renumbered 11 to 13) |
| Mass, keep R11 at 6 kg (TRL 3 item 6) | 6.02 kg, at risk | 4.44 kg, met on paper |
| Autonomy and winter harvest (R8, R9) | 4.78 days on two cells; 14.5 Wh/day from 20 W | 6.22 days on one cell; 4.4 Wh/day from 6 W (1.77 times the draw) |
| Payload of 10 bytes (TRL 3 item 7) | 14 bytes; does not fit US915 DR0; SF9 226 ms | 10 bytes; 371 ms at US915 DR0; SF9 206 ms |
| Restate R4 (TRL 3 item 5) | Ground pixel 0.25 m or larger; 0.22 m, not met | 8 px/m or less at head height; 7.6 px/m, met on paper |
| R7 restricted to temperate sites; radar for any hot partner city (TRL 3 item 4) | Counting with air to 35 °C; not met | Count at temperate sites (air to 20 °C); at risk (10.2 h sunlit single-frame, 3.2 h with track averaging on the mild day) |
| Wind on the panel (follows the 6 W panel) | 170 N; 933 N·m at the pole base | 52 N; 283 N·m |
| TRL 2 items D1 to D7 and the three TRL 3 design changes | Adopted for TRL 3, open for review | Decided; no further repo change |

Files changed: `project.yaml` (`budget_usd`, evidence list), `README.md` (budget line, rationale figures, "What sparked the idea" rewritten, Concept, Key components, Safety), `docs/01-problem.md` (CBC-PRB-001 v0.4), `docs/02-concept.md` (CBC-PRC-001 v0.4), `docs/03-requirements.md` (CBC-REQ-001 v0.4), `docs/04-calcs/01-sizing.md` (CBC-CAL-001 v0.2) and `sizing.py` with `results.csv`, `docs/decisions/0001-trl2-review-decisions.md` (CBC-DDR-001 v0.2), the new CBC-DDR-002, `bom/bom.csv` and `bom-notes.md`, `cad/src/model.py` with STEP and STL, `cad/src/sheets.py` and CBC-DWG-001 at Rev P2, `cad/src/concept_media.py` and all of `media/` (blueprint Rev P3). All PDFs were rebuilt; the footers now read designmolecule.com.

### Requirement status (CBC-CAL-001 v0.2)

0 not met, 3 at risk, 4 not verifiable at TRL 3, 7 met on paper, 1 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R1 Classes and directions | At risk | 4.2 frames for a car at 50 km/h (4 assumed needed) |
| R2 Pedestrian accuracy | At risk | Random merging alone loses 6.5 % at 600/h |
| R7 Operating range (temperate) | At risk | Mild day, sunlit: 10.2 h below single-frame contrast, 3.2 h with track averaging |
| R3, R10, R12, R14 | Not verifiable at TRL 3 | R12: 59 min install; post factor 38, twist factor 3.2 |
| R4, R6, R8, R9, R11, R13, R15 | Met on paper | 7.6 px/m; footprint -4.45 to 8.34 m; 6.22 days; 4.4 Wh/day; 4.44 kg; $253.00; 371 ms at DR0 |
| R5 | Met by design | 10 bytes per 15 min bin |

### Still awaiting Amish

1. **O1, first co-design partner and street.** No recommendation was made. A hot partner city would bring the radar variant forward (decided in principle, no design work until a partner is chosen).

### Cross-repo actions (FieldNode not edited here)

- FieldNode: CurbCount's baseline now fits FieldNode's standard power (one cell, 6 W panel, 1.5 A charger) and the proposed 100 mW sensor allowance (92 mW). The high-load variant (20 W panel, 5 A charger, second fused cell) is needed only by the ESP32-S3 fallback.
- FieldNode: the sensor port pinout needs I²C plus a 3.3 V switched rail, and the STM32WL firmware must host a fixed-point tracker (about 2 % of the core, 44 kB of 64 kB RAM estimated).
- FieldNode: a jumper-sense pin on the service header for CurbCount's calibration mode (frames to a laptop over the wired service port only).
- FieldNode: its mount kit seats 40 to 60 mm poles; CurbCount keeps its own 60 to 140 mm saddle. FieldNode may want a street-pole saddle option.

### Other changes

- README "What sparked the idea" rewritten: the new starting point is Ann Cavoukian's October 2018 resignation from the Sidewalk Labs Quayside project in Toronto over data not de-identified at source (cited to Engadget and Global News). The earlier text about a portfolio review was removed. No such text was found in `docs/01-problem.md`.
- Superseded PDFs in `docs/pdf` that still showed the old footer were deleted.

### Safety

- Lower loads on the pole: 52 N of panel wind load at 5.4 m instead of 170 N; the pole owner must still check it.
- One LiFePO4 cell (about 19 Wh) at FieldNode's standard 1.5 A charge; the ESP32-S3 fallback would reintroduce two cells and 5 A and needs its own fusing and charger setting.
- Privacy: 7.6 px/m at head height (8.5 px/m for a 2.0 m person) is the design's privacy guarantee. Any higher-resolution array or lower mounting height needs a fresh privacy review.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided but on hold: profiling the fixed-point tracker on the STM32WL, I²C over the 2 m cable on a street pole, window transmission and array noise measurements, and any radar build or test. Nothing past TRL 3 was created.
