---
doc_id: CBC-DDR-003
title: CurbCount design for construction
project: CurbCount
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** proposed. Every change below was made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are "Proposed, awaiting Amish".

## Context

On 2026-09-30 Amish approved the illustrated build plan format for the portfolio and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." He also asked that outstanding decisions go in a separate design decisions register, not in the build plan.

The TRL 3 model of CurbCount (CBC-DDR-002) showed what the counter does and where its parts sit, but as a massing model: flat plates against a round pole, band clamps drawn as rings that held nothing, a head that floated under its arm, a pole-top mount that could only be made by welding, and parts with no fixing at all. Checking the model with build123d found seven problems (P1 to P7 below).

The changes keep what the counter does: the same thermal array, window height (4.3 m), tilt (7.5 degrees), reach (530 mm from the pole axis) and sensing footprint; the same FieldNode core, cell, 6 W panel at 35 degrees on the pole top; the same four band clamps, no drilling of the pole, the same public notice plate. Nothing here changes the pitch, the privacy case or the safety case. Every change is in `cad/src/model.py`, which now runs 106 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart are apart by at least the stated clearance. All 106 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The enclosure saddle plate was a flat plate against a round 114 mm pole (a line contact that can rock), and the bands were rings round the pole with no path to the plate, so nothing held the plate. The model's plate (140 x 260 x 3 mm) did not match the BOM (160 x 300 x 4 mm). | Plate 160 x 300 x 3 mm with a 100 x 150 mm lightening window behind the box. Two V-saddles bent from 3 mm sheet (20 mm flat, two 65 mm wings at 90 degrees, 40 mm tall) on its back, each on two M4 countersunk screws from the front. Each band passes round the pole, through two 3 x 15 mm slots 66 mm each side of the centre line, and across the plate front above or below the box. | The pole now seats on the faces of a true 90 degree V; 60 to 140 mm poles all seat on both wings. The saddles sit 35 mm inboard of the bands so the band path is clear of the wings on any pole in the range. A bent saddle is lighter and easier to make than a machined block for a pole this large. |
| P2 | The FieldNode enclosure had no fixing to the plate; the board, controller and cell floated inside; the ports and antenna were drawn without glands, vent or nuts. | The FieldNode constructable core of FND-DDR-003: the maker's four lugs at the box's back corners, one M5 screw each through the plate; the internal plate on the four moulded bosses; the six penetrations in two rows on the bottom face; a plug-in connector strip and rail fuses (new BOM line 14). Port A takes the sensor cable, gland 1 the panel lead; port B and gland 2 are capped. Port A's supply is 3.3 V for the array: a load switch from the 3.3 V converter replaces FieldNode's port A boost converter. | CurbCount uses FieldNode's core unchanged, so it takes FieldNode's constructable version rather than inventing its own. |
| P3 | The arm saddle plate (6 x 90 x 160 mm) was too narrow for band slots and sat flat on the pole; the bands were rings; the arm tube butted the plate with no fixing ("welded or bolted"). | Arm saddle plate 160 x 250 x 3 mm with two V-saddles and four band slots, as P1. The tube butts the plate's front and is held by two angle brackets (40 x 40 x 4 mm, 40 mm long), one on top and one underneath: four M6 bolts through the plate (nuts behind it) and two M6 bolts down through both brackets and the tube on crush spacers. The arm is 498 mm long (was 512 mm); the reach is unchanged. | Every joint is face to face and bolted; no welding. The crush spacers stop the 2 mm tube walls from collapsing under the bolts. The brackets carry the head's weight as tension and compression in their legs. |
| P4 | The head floated under the arm (the 7.5 degree tilt left a wedge-shaped gap and overlap) with no fixing; the window film floated inside an opening larger than the film; the array floated; the cable had no way in. | A printed wedge pad on the hood top fills the tilt; two M5 bolts pass down through the arm (on crush spacers) into heat-set inserts in the pad. The housing has an 8 mm ledge inside its open bottom; the film is clamped to it by a printed window frame and four M3 screws into heat-set inserts in four corner bosses. The array breakout sits on four standoffs from the roof. An M16 gland in the pole-side end wall, under the hood, takes the cable. The arm axis rises 8.5 mm to sit on the pad. | The window height, tilt and field of view are unchanged; the frame's 88 x 68 mm opening is far larger than the 30 x 20 mm the lens needs. The gland under the hood is sheltered from rain. |
| P5 | The pole-top mount could only be made by welding (a cap on the sleeve, a post standing on the cap); the hinge plate floated above the post; the panel floated above the hinge plate, which was smaller than the panel and could not reach the frame's lip; three M10 set screws in a 4 mm wall would have under three threads each. | All bolted, no welding. Sleeve 128 x 3 mm tube, 100 mm long, with three M8 rivet nuts and cup-point set screws. An 8 mm cap disc inside the sleeve top on four radial M4 screws; the disc bears on the pole top. The post stands on the disc between two lower clips (50 x 50 x 5 mm angle) on two M8 cross bolts, with a round bar plug in each end of the post. A rail plate 290 x 150 x 3 mm at 35 degrees sits on two upper clips over the post head, on two M8 cross bolts that fix the tilt. The panel is bolted through its frame's back lip to the rail plate's ends. The panel is now centred over the post (it was 40 mm toward the sidewalk); its top is 5.43 m above the road (was about 5.50 m). | Bolted joints a home workshop can make. Rivet nuts give the set screws full thread in a thin wall. The lip is the only part of a framed panel that can carry a bolt. Centring the panel shortens the wind lever. |
| P6 | The sensor cable floated 5 mm off the pole and, where it met the bands, would have been crushed under them; it had no way into the head. There was no panel lead: the panel's 1 m lead cannot reach the enclosure 1.4 m below. | Both cables run up the pole's side, tied every 150 mm, passing over the bands, never under them. The sensor cable leaves port A, runs up the pole, round the arm plate's edge and along the side of the arm, and into the head gland: 1.48 m modelled. It is single-ended (M12 plug at the port, open end into the head). A 1.5 m panel extension lead with a sealed inline connector runs from the panel's own lead down to gland 1 (BOM line 13). | Nothing clamps a cable. The route keeps both cables clear of the V-saddles and bands; the model checks every clearance. |
| P7 | The notice plate had no fixing, and the model's plate (1.5 mm) did not match the BOM (2 mm). | 2 mm plate with four 3 x 10 mm slots; two stainless steel cable ties round the pole and through the slots. | The usual way to fix a small sign to a pole; nothing is drilled. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 5.26 kg on the pole (was 4.44 kg) [H5]; R11 (6 kg) still met on paper. | Saddles, brackets, clips, plugs, rail plate, fixings and the extension lead. Lightening windows in the enclosure plate and rail plate, 3 mm plates, a 100 mm sleeve and an 8 mm disc keep the rise to 0.8 kg. |
| Cost | $274.00 (was $253.00) against the unchanged $275 `budget_usd` [J1]; margin $1.00. BOM lines 1, 5, 6, 7, 8, 12 and 13 respecified, 1, 5, 7, 8, 12 and 13 repriced, line 14 added. | Parts added for construction and FieldNode's own repricing of its core ($47 to $49, plus the $5 connector strip). |
| Wind and structure | Post factor 55 (was 38) and 169 N on the pole top (was 192 N) [H1, H2]; pole base moment 279 N·m (was 283 N·m); twist factor 3.3 (was 3.2) [H3]. | The panel now sits over the post and slightly lower. |
| Drawings | CBC-DWG-001 Rev P4; making sketches CBC-DWG-101 to 116 added. | Follows the model. |
| Documents | CBC-CAL-001 v0.3, CBC-PRC-001 v0.5, CBC-REQ-001 v0.5: mass, cost, wind and arm figures updated. No requirement changed status. | Follows the model. |
| Sensing | Unchanged: the window, tilt and camera model are the same, so the footprint (-4.45 to 8.34 m) and resolution (7.6 px/m) stand. | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The cost margin is now $1.00 on indicative prices. | (a) accept and confirm prices when parts are bought; (b) raise `budget_usd` to $290 for contingency; (c) leave port B out of CurbCount's core (about $6 less), departing from the standard FieldNode core. | (a). |
| A2 | Accept the design for construction as a whole (this record). | Accept; or change individual items. | Accept. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CBC-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open decisions are in the design decisions register CBC-DEC-001.
- Requirement status is unchanged: none not met, 3 at risk (R1, R2, R7), 7 met on paper, 1 met by design, 4 not verifiable at TRL 3 (CBC-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept saddles, arm joint, head fixing and pole-top mount; they need updating on Amish's Mac, where Blender is.
- The enclosure part, its boss spacing and lug kit, the panel's frame lip, the band size for the site pole and the sleeve tube's bore are to be confirmed when parts are bought (CBC-DEC-001).
