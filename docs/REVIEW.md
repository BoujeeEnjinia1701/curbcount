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

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` to $275; (b) keep $150 and cost the FieldNode core (about $95 of the $271) under FieldNode, leaving about $176 for CurbCount parts, still over; (c) cut cost with an 8 x 8 thermal array and no separate processor, which weakens R1 and R2. Recommendation: (a). `project.yaml` is unchanged.
2. **Sensor.** Option A: 32 x 24 thermal array (cheap, low power, privacy by physics). Option B: 60 GHz mmWave radar (works in heat and darkness, costs and draws more). Recommendation: A for the first build, B studied as a hot-climate variant.
3. **Power.** The counter needs a FieldNode "high-load" variant (20 W panel, second cell). Recommendation: raise this with the FieldNode project rather than changing FieldNode here.
4. **Processor.** ESP32-S3 in the sensor head, or tracking on FieldNode's STM32WL alone. Recommendation: ESP32-S3 first; STM32WL-only as a TRL 3 study.
5. **Count interval** of 15 minutes, and three classes (pedestrian, cyclist or micromobility, motor vehicle). Recommendation: adopt both.
6. **Calibration mode** that shows frames on a laptop through a physical jumper only. Recommendation: allow it, never over the radio.
7. **Public notice** on each pole linking to this repository. Recommendation: yes.
8. **First partner and street** for co-design.

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
