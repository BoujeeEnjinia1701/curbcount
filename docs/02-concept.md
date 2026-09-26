---
doc_id: CBC-PRC-001
title: CurbCount design precis
project: CurbCount
doc_type: Design precis
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update from CBC-CAL-001 and CBC-DDR-001 (array turned 90 degrees, aluminium panel mount, FieldNode TRL 3 enclosure, notice plate, numbers replaced by calculated values, design choices adopted for TRL 3)
---

# CurbCount design precis

CurbCount is a clamp-on street pole counter. A 32 x 24 pixel thermal array looks down from 4.3 m over the sidewalk, bike lane and nearest traffic lane; an edge processor turns the heat blobs into counts of people, cyclists and vehicles by direction; and a FieldNode core sends only 15-minute counts over LoRaWAN. The sensor images a person's head at no more than 8.5 px/m, far below what is needed to recognize anyone, so privacy does not depend on the firmware. The calculations in CBC-CAL-001 show that it can count for 4.8 days without sun and stay energy neutral in winter with a 20 W panel, but the parts cost of $290.00 is well over the $150 budget, and a thermal-only counter goes blind for much of a hot day.

![Figure 1. CurbCount on a street pole with a 1.75 m person for scale; the teal area is the calculated sensing footprint](../media/hero.png)

## How it works

1. **Sense.** The thermal array reads 32 x 24 temperatures in two chess-pattern subpages, 16 a second, giving 8 full frames a second. Its 110 degree axis spans the street. People, cyclists and engines stand out from the pavement as warm (or, on hot pavement, cool) blobs.
2. **Track.** The edge processor keeps a slowly updated background, subtracts it, finds blobs and follows each blob across frames. Frames live only in RAM and are overwritten every 125 ms.
3. **Classify.** Each finished track is classed as pedestrian, cyclist (including e-scooters and other micromobility) or motor vehicle from its size, speed and zone (sidewalk, bike lane or nearest lane), and given a direction along the street. The far part of the road is masked.
4. **Count.** Tracks increment six counters (three classes by two directions); the track data is then deleted. Every 15 minutes the counters close as one 14-byte record.
5. **Send.** The FieldNode core sends each record over LoRaWAN to the lab's TwinKit gateway, a city server or The Things Network, with a daily health message (battery, temperature, frame errors).

![Figure 2. Data and energy flow (estimates from CBC-CAL-001)](../media/flow.png)

## Main components

Table 1. Main components. Numbers match the exploded view (Figure 3), `bom/bom.csv` and `cad/src/model.py`.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | FieldNode enclosure with ports and antenna | IP65 polycarbonate, 150 x 90 x 200 mm, two M12 5-pin ports and the whip on the bottom face | From FieldNode (FND-PRC-001 v0.3), unchanged |
| 2 | FieldNode power and radio board | MPPT charger with cold-charge lockout, STM32WL-class LoRaWAN module, switched sensor rails | From FieldNode; charger current must suit a 20 W panel |
| 3 | LiFePO4 cells | Two 3.2 V 6 Ah cells in parallel (FieldNode's one plus one added) | High-load variant (DDR-001 D3) |
| 4 | Solar panel | 20 W, 540 x 350 mm, 12 V class, in place of FieldNode's 6 W | High-load variant (DDR-001 D3) |
| 5 | Panel pole-top mount | Aluminium sleeve over the pole top, 42.4 mm post, hinge plate at 35 degrees | Changed from steel at TRL 3 for mass |
| 6 | Band clamps and enclosure saddle | Four 12 mm stainless bands for 60 to 140 mm poles, aluminium saddle plate | No drilling; FieldNode's V-blocks fit only 40 to 60 mm poles |
| 7 | Sensor arm | 40 x 40 x 2 mm aluminium tube, 512 mm, on a saddle plate; head 530 mm from the pole axis | Keeps the head clear of the pole |
| 8 | Sensor head housing | 3D-printed ASA, 110 x 90 x 70 mm, with a sun hood | View tilted 7.5 degrees toward the road |
| 9 | Window | 0.5 mm HDPE film, about 0.75 transmission at 8 to 14 µm (estimate) | Far cheaper than germanium; to be measured |
| 10 | Thermal array | MLX90640 class, 32 x 24 px, 110 x 75 degree lens, 110 degree axis across the street | DDR-001 D2; radar kept as a hot-climate variant |
| 11 | Edge processor | ESP32-S3 class module, radio disabled; calibration jumper | DDR-001 D4 and D6; STM32WL-only variant studied |
| 12 | Sensor cable | M12 5-pin, about 2 m, to a FieldNode sensor port | FieldNode pinout (open in FieldNode) |
| 13 | Public notice plate | 150 x 200 mm aluminium plate at 2.6 m | DDR-001 D7 |

![Figure 3. Exploded view with BOM numbers](../media/exploded.png)

![Figure 4. Cutaway: sensor head with processor, array and window (top right); FieldNode enclosure with cells and board (bottom left)](../media/cutaway.png)

The parametric model is `cad/src/model.py` (STEP and STL in `cad/step/` and `cad/stl/`), and the general arrangement is drawing [CBC-DWG-001](../cad/drawings/CBC-DWG-001.pdf).

## Key numbers

Table 2. Key numbers from CBC-CAL-001. Tags refer to lines of `docs/04-calcs/sizing.py` output.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Footprint across the street | 4.45 m behind the curb to 8.34 m into the road [A2] | R6 met on paper |
| Footprint along the street | 5.71 to 7.28 m [A5] | |
| Smallest ground pixel | 0.224 m along the street near the head [B1b] | R4 not met as written |
| Resolution at head height | 7.6 to 8.5 px/m [B2] | R4 privacy aim met |
| Frames per crossing | 30 for pedestrians, 7.7 for cyclists at 25 km/h, 4.2 for cars at 50 km/h [C1] | R1 at risk |
| Hours below detection contrast, hot day | 14.2 h sunlit, 24 h shaded [D4] | R7 not met on paper |
| Load from the cells | 268 mW average, 6.43 Wh/day [E1] | 2.1 times FieldNode's 115 mW allowance |
| Autonomy | 4.78 days; 3.35 days at -20 °C [E2] | R8 met on paper |
| Winter harvest, 20 W | 14.5 Wh/day, 2.26 times the draw [E3] | R9 met on paper |
| Uplink | 14 bytes per 15 min; 226 ms at SF9, 0.91 s/h [G1] | R5 met; R15 at risk (US915 DR0) |
| Wind on panel | 170 N at 35 m/s; post factor 9 [H1] | R12 |
| Mass on the pole | 6.02 kg [H5] | R11 at risk |
| Parts cost | $290.00 [J1] | R13 not met |

Counts will still run low where parked vans, trees and awnings hide the footprint, and where people walk side by side.

## Key design choices

All choices below are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (CBC-DDR-001), unless marked otherwise.

- **Thermal array rather than a camera.** At 32 x 24 pixels the sensor cannot capture an identifiable image at the mounting height used here, so privacy does not depend on trusting the firmware.
- **Thermal array first, 60 GHz radar as a hot-climate variant.** CBC-CAL-001 makes the radar variant more than an option: without it the counter does not work in hot weather (R7).
- **Array turned so its wide axis spans the street.** A CBC-CAL-001 change: it covers the full design case (R6) at the cost of fewer frames per fast vehicle (R1).
- **Frames never leave RAM.** The firmware has no code path that writes or sends a frame. A calibration mode shows frames on a laptop only through a physical jumper in the head, never over the radio.
- **FieldNode core with a larger panel and a second cell.** The counter draws 2.1 times FieldNode's current sensor allowance. The high-load variant is to be raised with the FieldNode project, not made to FieldNode here.
- **Separate processor in the head.** Only counts cross the M12 cable. CBC-CAL-001 finds that tracking on FieldNode's STM32WL alone is feasible on paper in fixed point and would remove the high-load power variant; that switch is proposed, awaiting Amish.
- **15-minute bins, three classes by two directions.**
- **Public notice plate on every pole.**

## Safety

> **Safety:** Installing on a street pole is work at height next to traffic. Install only with the pole owner's permission, by trained crews, with fall protection and traffic management as local rules require. Keep clear of overhead power lines and street-light wiring, and never open a pole's electrical hatch. The pole owner must check that the pole can carry the extra 170 N wind load at 5.5 m.

> **Safety:** The node contains two LiFePO4 cells, about 38 Wh. Fuse each cell, charge only within the cell maker's temperature limits (FieldNode's cold- and hot-charge lockout applies), size the charger for the 5 A a 20 W panel can deliver, and do not install a node with a swollen or damaged cell.

> **Safety:** A falling part from 4 to 5.7 m can injure people below. Use a secondary safety lanyard on the panel and the sensor head, torque the sleeve set screws and bands, and check clamps after the first storm.

**Privacy.** No images, audio recordings or personal identifiers leave the device; only aggregate counts are stored or sent. Any change to a higher-resolution sensor needs a fresh privacy review. Check local data protection law before any deployment, and fit the notice plate saying what is counted and where the design is documented.

## Open questions

- Measure HDPE window transmission at 8 to 14 µm and the MLX90640 noise at 16 Hz.
- Settle the sensor for hot climates: radar variant, or a hybrid, given the R7 result.
- Define the tracker for merged blobs (groups, parents with strollers) and the target accuracy per class.
- Decide whether tracking moves to the STM32WL (proposed, awaiting Amish).
- Agree the M12 pinout and the high-load charger current with the FieldNode project.
- Find a side-arm panel mount for poles whose top carries a lantern.
- Choose the first co-design partner and street (awaiting Amish).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
