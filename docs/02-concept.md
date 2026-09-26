---
doc_id: CBC-PRC-001
title: CurbCount design precis
project: CurbCount
doc_type: Design precis
version: "0.2"
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
---

# CurbCount design precis

CurbCount is a clamp-on street pole counter. A 32 x 24 pixel thermal array looks down from about 4.3 m over the sidewalk, bike lane and nearest traffic lane; an edge processor turns the heat blobs into counts of people, cyclists and vehicles by direction; and a FieldNode core sends only 15-minute counts over LoRaWAN. Each pixel covers about 0.3 m of ground, so the sensor cannot show a face or a number plate. First-order numbers suggest it can count continuously for about 4 days without sun, but the parts cost of about $271 is well over the $150 budget.

![Figure 1. CurbCount on a street pole with a 1.75 m person for scale; the teal area is the estimated sensing footprint](../media/hero.png)

## How it works

1. **Sense.** The thermal array reads 32 x 24 temperatures eight times a second. People, cyclists and engines stand out from the pavement as warm (or, on hot pavement, cool) blobs.
2. **Track.** The edge processor keeps a slowly updated background, subtracts it, finds blobs, and follows each blob across frames. Frames live only in RAM and are overwritten about every 125 ms.
3. **Classify.** Each finished track is classed as pedestrian, cyclist (including e-scooters and other micromobility) or motor vehicle from its size, speed and position (sidewalk, bike lane or traffic lane), and given a direction along the street.
4. **Count.** Tracks increment six counters (three classes by two directions); the track data is then deleted. Every 15 minutes the counters close as one 14-byte record.
5. **Send.** The FieldNode core sends each record over LoRaWAN to the lab's TwinKit gateway, a city server or The Things Network, with a daily health message (battery, temperature, frame errors).

![Figure 2. Data and energy flow (estimates)](../media/flow.png)

## Main components

Table 1. Main components. Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | FieldNode enclosure | IP65 polycarbonate box, about 180 x 130 x 250 mm, vent and gland | From FieldNode, unchanged |
| 2 | FieldNode power and radio board | MPPT charger with cold-charge lockout, STM32WL-class LoRaWAN module, switched sensor rail | From FieldNode, unchanged |
| 3 | LiFePO4 cells | Two 3.2 V 6 Ah cells (FieldNode's one plus one added) | Added cell proposed, awaiting Amish |
| 4 | Solar panel | 20 W, about 540 x 350 mm, in place of FieldNode's 6 W | Proposed, awaiting Amish |
| 5 | Panel tilt bracket | Pole-top cap and hinge, about 35° tilt | Adapted from FieldNode |
| 6 | Band clamps | Four stainless band clamps with rubber liners | No drilling |
| 7 | Sensor arm | 40 x 40 mm aluminum tube, about 450 mm reach toward the road | Keeps the head clear of the pole shadow |
| 8 | Sensor head housing | 3D-printed ASA, about 110 x 90 x 70 mm, with a sun hood | Tilted 10° toward the road |
| 9 | Window | 0.5 mm HDPE film, which passes long-wave infrared | Far cheaper than germanium; transmission to be checked |
| 10 | Thermal array | MLX90640 class, 32 x 24 px, 110 x 75° lens | Proposed, awaiting Amish (see radar option) |
| 11 | Edge processor | ESP32-S3 class module, radio disabled in firmware | Proposed, awaiting Amish |
| 12 | Sensor cable | M12 sealed cable to a FieldNode sensor port | FieldNode standard pinout |

![Figure 3. Exploded view with BOM numbers](../media/exploded.png)

![Figure 4. Cutaway: FieldNode enclosure with cells and board (left), sensor head with processor, array and window (right)](../media/cutaway.png)

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

Table 2. First-order numbers.

| Quantity | Estimate | Basis and assumptions | Requirement |
| --- | --- | --- | --- |
| Footprint across the street | about 6.9 m, from 2.1 m behind the curb to 4.8 m into the road | 75° field across, window 4.3 m above the road, tilted 10° toward the road | R6 met for sidewalks to 2 m; **not met** for 3 m |
| Footprint along the street | about 12 m | 110° field along, at 4.3 m | |
| Ground size of one pixel | about 0.3 to 0.4 m | 6.9 m / 24 px across; 12.3 m / 32 px along, at nadir | R4 met (no face or plate can be resolved) |
| Frames per crossing | about 14 for a cyclist at 25 km/h; about 7 for a car at 50 km/h | 12 m footprint, 8 Hz frame rate | R1 plausible |
| Raw frame data | about 12 kB/s, about 1 GB/day, held only in RAM | 768 px x 2 bytes x 8 Hz | R4 |
| Uplink data | 14 bytes per 15 min, 96 uplinks/day, about 1.3 kB/day | 3 classes x 2 directions x 2 bytes, plus status | R5 met |
| Radio airtime | about 0.2 s per uplink, about 0.8 s/h | SF9 at 125 kHz, about 27 bytes with LoRaWAN overhead; EU868 sub-band limit 1 % (36 s/h) | R15 met |
| Thermal array power | about 0.07 W | About 20 mA at 3.3 V (typical class value, to be confirmed) | |
| Edge processor power | about 0.17 W | About 50 mA at 3.3 V with its own radio off | |
| Conversion and base load | about 0.06 W | Regulator losses about 15 %; FieldNode base about 0.02 W | |
| Total continuous load | about 0.30 W, about 7.2 Wh/day | Counting 24 h a day | |
| Share of FieldNode sensor budget | about 2.4 times | FieldNode README allows about 115 mW average for sensors | **Standard FieldNode not sufficient** |
| Battery autonomy | about 4.3 days with two cells; about 2.1 days with one | 2 x 19.2 Wh, 80 % usable | R8 met with two cells only |
| Winter solar harvest | about 16 Wh/day into the cells | 20 W x 1.5 peak sun hours x 0.6 derating x 0.9 charger | R9 met (about 2.2 times the load) |
| Same with FieldNode's 6 W panel | about 4.9 Wh/day | Same assumptions | R9 **not met** |
| Mass on the pole | about 4.2 kg | FieldNode about 1.7 kg, larger panel +1.0 kg, cell +0.2 kg, head 0.35 kg, arm 0.6 kg, clamps 0.3 kg | R11 met |
| Wind load on panel | about 170 N | 0.19 m², 35 m/s gust, force coefficient 1.2 | R12, to check bracket |
| Parts cost | about $271 | Indicative prices, see `bom/bom.csv` | R13 **not met** |

The footprint and pixel size come from simple geometry over flat ground. Real streets have parked cars, trees and awnings that hide parts of the footprint, and people walking side by side will merge into one blob, so counts will run low in dense flows until the tracker handles merged blobs.

## Key design choices

- **Thermal array rather than a camera.** At 32 x 24 pixels the sensor cannot capture an identifiable image at any mounting height used here, so privacy does not depend on trusting the firmware. Proposed, awaiting Amish.
- **Thermal array rather than 60 GHz radar.** A thermal array is cheaper, simpler and lower power, and a radar is better in heat, fog and darkness and at separating people from bicycles by motion. Proposed: thermal for the first build, radar kept as a variant, awaiting Amish.
- **Frames never leave RAM.** The firmware has no code path that writes or sends a frame. A calibration mode that shows frames on a laptop through a physical jumper is proposed for setup only, awaiting Amish.
- **FieldNode core with a larger panel and a second cell.** The counter draws about 2.4 times FieldNode's sensor budget. Proposed, awaiting Amish; the change should be raised with the FieldNode project as a "high-load" variant, not made to FieldNode here.
- **Separate processor in the head.** Keeping tracking next to the sensor means only counts cross the M12 cable. Running the tracker on FieldNode's own STM32WL instead would save about $12 and most of the 0.17 W, but may be too slow for tracking at 8 Hz. Proposed: ESP32-S3 first, STM32WL-only as a TRL 3 study, awaiting Amish.
- **15-minute bins.** This matches common count practice and keeps radio airtime tiny. Proposed, awaiting Amish.

## Safety

> **Safety:** Installing on a street pole is work at height next to traffic. Install only with the pole owner's permission, by trained crews, with fall protection and traffic management as local rules require. Keep clear of overhead power lines and street-light wiring, and never open a pole's electrical hatch.

> **Safety:** The node contains two LiFePO4 cells. Fuse the pack, charge only within the cell maker's temperature limits (FieldNode's cold-charge lockout applies), and do not install a node with a swollen or damaged cell.

> **Safety:** A falling part from 4 to 5 m can injure people below. Use a secondary safety lanyard on the panel and the sensor head, and check clamps after the first storm.

**Privacy.** No images, audio recordings or personal identifiers leave the device; only aggregate counts are stored or sent. Check local data protection law before any deployment, and publish a notice on the pole saying what is counted and where the design is documented.

## Open questions for TRL 3

- Measure HDPE window transmission at 8 to 14 µm and the resulting loss of contrast.
- Test detection when pavement and air are near body temperature (about 30 to 35 °C); decide whether the radar variant is needed for hot climates.
- Define the tracker for merged blobs (groups, parents with strollers) and the target accuracy per class.
- Confirm the MLX90640 and ESP32-S3 currents at 8 Hz and whether the STM32WL alone can run the tracker.
- Check street shading of the panel on real poles, which may cut harvest more than the 40 % derating assumed.
- Choose the first co-design partner and street.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
