---
doc_id: CBC-CAL-001
title: CurbCount sizing calculations
project: CurbCount
doc_type: Calculation
version: "0.3"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (coverage, pixel size and privacy, frames per crossing, merging, thermal contrast and window, energy, processor study, radio, wind and mounting, mass, installation, service life, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-30'
  author: Amish Chadha
  change: Design for construction (CBC-DDR-003); wind, arm, mass, installation and cost figures recalculated from the constructable model; no requirement changed status
---

# CurbCount sizing calculations

With the decisions Amish accepted on 2026-09-25 (CBC-DDR-002) applied, CurbCount meets eight of its fifteen requirements on paper (seven by calculation, one by design), has three at risk, cannot show four at TRL 3 and misses none. The largest change is where the tracking runs: it moves from a separate ESP32-S3 in the sensor head to FieldNode's STM32WL, in fixed point. That cuts the head load from 241 mW to 92 mW, so the counter runs on standard FieldNode power (one cell and the 6 W panel) and still counts for 6.2 days without sun; parts fall from $290.00 to $253.00 against the new $275 budget; and the mass falls from 6.02 kg to 4.44 kg. Version 0.3 recalculates the mounting, mass and cost figures for the constructable design of CBC-DDR-003 (saddles, brackets, a bolted pole-top mount and their fixings): the counter now weighs 5.26 kg and costs $274.00, and no requirement changes status. The record is packed into 10 bytes so it fits US915 DR0; R4 is restated in pixels per meter at head height, which the sensor meets at 7.6 px/m; and R7 is restated for temperate sites, where it remains at risk because sunlit sidewalks need track averaging. The three at-risk requirements are R1 (4.2 frames for a car at 50 km/h), R2 (merging) and R7. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [E2], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the mount is safe on a particular pole, that the cell is safe in a particular climate or that the device complies with data protection law where it is installed. Pole loading must be checked by the pole owner. See CBC-PRC-001, Safety.

## Scope and method

The note checks every requirement in CBC-REQ-001 v0.4 against the design in CBC-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and its camera model, so the head height, tilt, arm, enclosure, panel and footprint used here are those in the STEP files, in drawing CBC-DWG-001 and in the concept media. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is one counter on a 114 mm street pole 0.45 m behind the curb, the sensor window 4.3 m above the road, a 3 m sidewalk (0.15 m above the road), a 2.0 m bike lane and one 3.5 m traffic lane.

Changes from v0.1: the baseline processor is the STM32WL (the ESP32-S3 head is a fallback on paper); one cell and FieldNode's 6 W panel replace two cells and a 20 W panel; the payload is 10 bytes; R4, R7 and R13 are checked against their restated targets; `budget_usd` is $275.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Lens | Separable equiangular model: 110 / 32 = 3.44 degrees per pixel across, 75 / 24 = 3.13 degrees along; flat ground; the sidewalk 150 mm above the road | Simplification of the MLX90640 wide lens; real distortion to be measured |
| Sensor | 16 Hz chess-mode subpages, so 8 full frames a second; noise 0.10 K rms at 1 Hz, scaling with the square root of the rate, times 1.25 at the lens edge; 23 mA at 3.3 V | Typical MLX90640 class values, to confirm from the datasheet of the chosen part |
| Detection | Single-frame threshold 4 times the noise; a person's plan area 0.099 m² (0.45 x 0.28 m ellipse); half the signal in the brightest pixel; a track needs 4 frames for class and direction | Engineering judgment |
| Window | 0.5 mm HDPE, refractive index 1.53, band-averaged absorption 4 /cm over 8 to 14 µm | Assumption, to be measured |
| Surface temperatures | Air as a daily cosine (minimum 03:00, maximum 15:00); sunlit concrete 3 K above air at night plus up to 15 K in sun; shaded concrete 1 K above air; a person seen from above halfway between air and 34 °C, plus up to 5 K in sun | Screening model; the largest uncertainty in this note |
| Speeds and flows | Walking 1.25 m/s mean, 1.5 m/s maximum; cyclists 25 km/h; cars 50 km/h; 600 people per hour per direction | CBC-REQ-001 Table 2 |
| Electronics | STM32WL run mode 5 mA at 3.3 V for tracking (baseline); ESP32-S3 50 mA at 3.3 V (fallback only); rails 90 % efficient; FieldNode core 4.0 mWh/day | Typical values; FND-CAL-001 [A1] |
| Energy | One 3.2 V 6 Ah LiFePO4 cell, 80 % usable, 70 % at -20 °C, 80 % at end of life; FieldNode's 6 W panel; winter 1.5 peak sun hours with 40 % derating for street shade, dust and heat; charger 85 %, charging 95 % | CBC-REQ-001 R8 and R9; FieldNode efficiencies |
| Radio | 10-byte payload (six 12-bit counters and a status byte) plus 13 bytes of LoRaWAN overhead, 125 kHz, coding rate 4/5, 8-symbol preamble, 96 uplinks a day | As FND-CAL-001; payload per CBC-DDR-002 |
| Wind and mounting | 35 m/s gust, 1.225 kg/m³; force coefficients 1.2 (panel), 1.3 (boxes), 2.0 (square tube); band preload 1,000 N, friction 0.2 (as FND-CAL-001); 6063 aluminium, yield 150 MPa | Screening values, not a code check |
| Masses | FieldNode core 1.02 kg (FND-CAL-001 [F1] less its panel, bracket and mount); 6 W panel 0.55 kg (FND-CAL-001); made parts from model volumes | Typical catalog masses |

## A. Coverage (R6)

- **Orientation.** The TRL 2 concept put the 75 degree axis across the street, tilted 10 degrees. That covers the sidewalk only to 2.08 m behind the curb, 69 % of the 3 m sidewalk [A4]. The design case spans 36.6 degrees behind and 51.6 degrees ahead of the vertical, 88.2 degrees in all [A3], which only the 110 degree axis can reach.
- **Chosen layout.** With the array turned 90 degrees and the view tilted 7.5 degrees toward the road, the footprint runs from 4.45 m behind the curb to 8.34 m into the road, 12.79 m across [A2], with 10.9 degrees of margin at both edges [A3]. Along the street it covers 5.71 m at the sidewalk back to 7.28 m at mid lane [A5]. The far part of the road is masked in firmware; only the nearest lane is counted.
- **Shadow.** The pole and the enclosure hide a strip up to 0.73 m wide at the back of the sidewalk, 13 % of the field along the street there [A6]. The tracker must join tracks across it.

R6 is **met on paper**.

## B. Pixel size and privacy (R4)

- **Ground pixel.** Below the head a pixel covers 0.251 x 0.233 m; at the curb edge of the sidewalk 0.251 x 0.224 m; at the back of the sidewalk 0.376 x 0.203 m; at mid lane 0.442 x 0.259 m [B1]. The smallest is 0.224 m, along the street near the head [B1b]. This was the v0.1 measure of R4 and is no longer the requirement.
- **What the sensor can resolve.** Privacy depends on resolution at the subject, not on the ground. A 1.75 m person directly below is 2.40 m from the sensor and is imaged at 7.6 px/m; a 2.0 m person at 8.5 px/m [B2]. The IEC 62676-4 levels for video surveillance are 25 px/m to detect, 125 px/m to recognize and 250 px/m to identify a person (values quoted from the standard, not checked online). A number plate at mid lane spans 1.8 pixels [B3].

R4, restated by CBC-DDR-002 as 8 px/m or less at head height for the 1.75 m design person, is **met on paper** at 7.6 px/m. A 2.0 m person is imaged at 8.5 px/m, still a third of the detection level and about 30 times below identification.

## C. Counting (R1, R2, R3)

*Table 2. Frames per crossing at 8 frames per second [C1].*

| Road user | Field along the street | Speed | Time in view | Frames |
| --- | --- | --- | --- | --- |
| Pedestrian, sidewalk back | 5.71 m | 5 km/h | 3.80 s | 30.4 |
| Pedestrian, mid-sidewalk | 6.00 m | 5 km/h | 4.00 s | 32.0 |
| Cyclist, mid bike lane | 6.73 m | 25 km/h | 0.97 s | 7.7 |
| Car, mid lane | 7.28 m | 50 km/h | 0.52 s | 4.2 |

- **R1.** A car at 50 km/h gives 4.2 frames, just above the 4 assumed necessary; above 52 km/h it gives fewer [C2]. Turning the array halved the frames for cars. R1 is **at risk** for fast vehicles.
- **Smear.** At 50 km/h a car moves 0.87 m (3.4 pixels) during one 62.5 ms subpage [C2], which distorts its blob in the chess readout. R3 (vehicle accuracy) is **not verifiable at TRL 3**.
- **Merging (R2).** At 600 people per hour per direction, random arrivals alone put a following walker within 0.50 m of another for 6.5 % of people [C3]; each such merge loses a count. People walking side by side add to this unless the tracker splits blobs by area. R2 is **at risk** and not verifiable at TRL 3.

## D. Thermal contrast and window (R7)

- **Window.** A 0.5 mm HDPE film passes about 0.75 of the long-wave signal; 0.25 mm passes 0.83 and 1.0 mm 0.61 [D1]. The thinner film helps little and is more fragile.
- **Threshold.** With 0.50 K rms of noise per pixel at the lens edge and half the person's signal in one pixel, a single frame needs at least 5.3 K between a person and the pavement [D2, D3]. Averaging 8 frames along a track could lower this to about 1.9 K [D3], but only if the tracker can follow a target it cannot yet see in one frame.

*Table 3. Hours a day with pedestrian contrast below the threshold [D4].*

| Design day | Sunlit sidewalk, 5.3 K | Shaded sidewalk, 5.3 K | Sunlit, 1.9 K with track averaging |
| --- | --- | --- | --- |
| Hot, air 25 to 35 °C | 14.2 h | 24.0 h | 11.2 h |
| Mild, air 10 to 20 °C | 10.2 h | 0.0 h | 3.2 h |
| Cold, air -10 to 0 °C | 3.2 h | 0.0 h | 0.0 h |

On a hot day a clothed person is within a few kelvin of the pavement at night and all day in shade, so a thermal-only counter goes blind for much of the day. On sunlit pavement the contrast crosses zero as the pavement heats, and the model puts that crossing band at several hours even on mild days. The surface temperature model is crude and these hours are the least certain figures in the note, but the conclusion for hot weather holds across the assumptions tried. Under Amish's decision of 2026-09-25 (CBC-DDR-002), R7 is restated: the thermal build is for temperate sites, taken here as design days with air up to 20 °C, and hot-climate sites use the radar variant. On the mild design day a shaded sidewalk never drops below the threshold, but a sunlit one does for 10.2 h with single frames and 3.2 h if track averaging reaches 1.9 K [D5]. The restated R7 is therefore **at risk**: it depends on track averaging that can only be shown on a bench at TRL 4. The hot-day figures stand as the reason for the scope limit. The electronics temperature part of R7 inherits FieldNode's R2 and R3 (see section E).

## E. Energy (R8, R9)

- **Load.** With tracking on the STM32WL, the head carries only the array: 76 mW, plus 16.5 mW for the STM32WL running the tracker, 92 mW delivered. With 90 % rail efficiency and the FieldNode core, the counter takes 2.47 Wh/day from the cell, 103 mW on average, 92 % of FieldNode's proposed 100 mW sensor allowance [E1]. The ESP32-S3 fallback would draw 241 mW and 6.43 Wh/day, 2.1 times FieldNode's current 115 mW allowance [E1b].
- **Autonomy (R8).** One cell holds 19.2 Wh, 15.4 Wh usable: 6.22 days without sun, 4.36 days at -20 °C and 4.98 days at end of life [E2]. R8 (3 days) is **met on paper** with one cell.
- **Winter harvest (R9).** *Table 4. Panel size in the winter design case [E3].*

| Panel | Stored per day | Ratio to 2.47 Wh drawn | Refill after 3 sunless days |
| --- | --- | --- | --- |
| 6 W (FieldNode standard) | 4.4 Wh | 1.77 | 3.9 days |
| 10 W | 7.3 Wh | 2.94 | 1.5 days |
| 20 W | 14.5 Wh | 5.89 | 0.6 days |

  The smallest energy-neutral panel is 3.4 W; the fallback would need 8.8 W, which is why v0.1 used a 20 W panel [E4]. R9 is **met on paper** with FieldNode's 6 W panel.
- **Charger.** At full sun the 6 W panel pushes 1.5 A into the cell (0.25 C), FieldNode's standard setting; the 20 W panel of the fallback would push 5.0 A [E5]. The baseline needs no charger change in FieldNode.
- **Heat.** FieldNode's calculation shows that on a hot clear day its cell sits above the 45 °C charge limit for most of the sun hours. With FieldNode's 6 W figures, CurbCount would store 0.8 Wh against 2.47 Wh drawn without a sun shield and run flat after 9.2 days of such weather; with FieldNode's proposed shield it stores 13.1 Wh [E6]. The CurbCount enclosure is not under its panel, so these shares are probably optimistic; the thermal build is for temperate sites in any case (R7).

## F. Tracking on the STM32WL (baseline, CBC-DDR-002)

- **Bus.** Reading one subpage takes 37.6 ms at 400 kHz I²C (60 % of the bus at 16 Hz) or 15.0 ms at 1 MHz (24 %) [F1]. Over the 2 m M12 cable (about 220 pF) the pull-ups must be 1.6 kΩ or less at 400 kHz and 644 Ω or less at 1 MHz, sinking 2.1 and 5.1 mA [F2]. Both fit I²C limits on paper; noise pickup on a cable up a street pole is a TRL 4 question.
- **Compute.** The STM32WL's Cortex-M4 core runs at 48 MHz and is taken here as having no floating-point unit (to confirm). The reference temperature conversion, at an estimated 2,000 to 4,000 cycles a pixel in software, would take 26 to 51 % of the core at 8 frames a second; a fixed-point pipeline on the raw data, at about 150 cycles a pixel, takes 2 % [F3]. RAM is estimated at 44 kB of 64 kB, most of it the LoRaWAN stack [F4].
- **Change from v0.1.** Head load 241 to 92 mW, draw 6.43 to 2.47 Wh/day, two cells and a 20 W panel to one cell and 6 W [F5].

The STM32WL baseline is feasible on paper only if the tracker is written in fixed point. The ESP32-S3 head on the high-load power variant stays as the fallback if bench profiling (TRL 4, on hold) shows otherwise. The calibration jumper moves from the head to FieldNode's service header, so frames can still reach a laptop only through a physical link (DDR-001 D6).

## G. Radio and data (R5, R15)

- **Airtime.** A 10-byte uplink takes 61.7 ms at SF7, 205.8 ms at SF9, 370.7 ms at SF10 and 1,482.8 ms at SF12. At SF9 that is 19.8 s a day and 0.82 s an hour, against 36 s an hour for the EU868 1 % duty cycle and 30 s a day for The Things Network's fair use; at SF10 and slower the fair-use limit is exceeded [G1].
- **US915.** At SF9 an uplink takes 206 ms against the 400 ms dwell limit. At DR0 (SF10) the payload limit is 11 bytes; the 10-byte record takes 371 ms there, within both limits, where the 14-byte v0.1 record could not be sent at all [G2].
- **Data.** 96 records of 10 bytes are 0.96 kB a day; the frames, 12.3 kB/s or 1.06 GB a day, stay in RAM [G3].

R5 is **met by design** and R15 is **met on paper**.

## H. Wind, mounting and mass (R11, R12)

- **Panel.** A 35 m/s gust gives 750 Pa and 52 N normal to the 6 W panel. The panel now sits centred over the post on its rail plate (CBC-DDR-003), so the lever to the post base is 0.180 m (0.256 m in v0.2) and the moment 9 N·m, which stresses the 42.4 x 3.0 mm aluminium post to 3 MPa (factor 55 on yield) [H1]. The 100 mm sleeve bears on the pole top with about 169 N. The pole itself carries the 52 N at 5.3 m, 279 N·m at its base, which the pole owner must check [H2]. The v0.1 figures with the 20 W panel were 170 N and 933 N·m.
- **Arm.** The arm is now 498 mm long, butted to its saddle plate. Wind along the street loads the arm with 30 N and the head with 8 N, twisting the arm about the pole by 14.0 N·m against 45.7 N·m of saddle friction from two bands (factor 3.3) [H3]. The arm bends to 3.1 MPa and its tip moves 0.16 mm, 0.018 degrees of aim [H4].
- **Mass (R11).** Masses of made parts come from the volumes of the constructable model. The FieldNode core is 1.04 kg with its connector strip; made parts are the arm with its saddle plate, V-saddles and brackets 0.89 kg, the pole-top mount 1.29 kg, the enclosure saddle plate with its V-saddles 0.36 kg, the printed head with its wedge pad and window frame 0.26 kg and the notice plate 0.16 kg; bought parts add 1.26 kg, 0.55 kg of it the panel. The total is 5.26 kg (4.44 kg in v0.2, before the saddles, brackets, clips, plugs and fixings were added); the ESP32-S3 fallback would be about 6.81 kg [H5]. R11 (6 kg) is **met on paper**, kept at 6 kg as Amish decided.
- **Installation (R12).** The task list comes to 59 min for two people with a mobile platform [H6], at the 60 min limit. Wind and fit are met on paper, but the time is **not verifiable at TRL 3**. The pole-top mount fits only poles with a free top.

## I. Sealing and service life (R10, R14)

- A winter night of 16 h discharges the cell by 9 %, and five years is 1,825 such cycles [I1], well within LiFePO4 cycle life at that depth. Calendar ageing in hot enclosures (see FND-CAL-001) and ultraviolet ageing of the HDPE window are unknown. R14 is **not verifiable at TRL 3**.
- The FieldNode enclosure is IP65 by design and the head's film window is clamped to a ledge by a printed frame; R10 is **not verifiable at TRL 3**.

## J. Cost (R13)

The BOM has 14 lines, all priced; the total is $274.00 against the $275 `budget_usd`, a margin of $1.00 [J1] ($253.00 in v0.2). The rise comes from the parts added for construction (CBC-DDR-003) and from FieldNode's repricing of its core, which now includes the connector strip: the FieldNode share (lines 1 to 3, 14 and part of 13) is $105.00, and line 4 is FieldNode's own $14 panel. The ESP32-S3 fallback would cost about $311.00, over the budget [J2]. R13 is **met on paper**, with a thin margin that rests on indicative prices (CBC-DEC-001).

## Results

*Table 5. Requirement status. Values from `docs/04-calcs/results.csv`.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Classes and directions | 4.2 frames minimum (car at 50 km/h); 4 assumed needed | 3 classes x 2 directions | At risk |
| R2 | Pedestrian and cyclist accuracy | Random merges alone 6.5 % at 600/h; groups extra | Within 10 % per hour | At risk (not verifiable at TRL 3) |
| R3 | Vehicle accuracy | 4.2 frames per car; 3.4 px smear per subpage | Within 15 % per hour | Not verifiable at TRL 3 |
| R4 | Privacy | 7.6 px/m at head height for a 1.75 m person (8.5 for 2.0 m) | 8 px/m or less at head height, below 25 px/m | Met on paper |
| R5 | Output format | 10 bytes per 15 min bin | 15 min counts, open format | Met by design |
| R6 | Coverage | Footprint -4.45 to 8.34 m; 10.9 degree margins; 0.73 m shadow | 3 m sidewalk, 2 m bike lane, nearest lane | Met on paper (array turned) |
| R7 | Operating range | Mild day: 10.2 h sunlit below single-frame contrast, 3.2 h with track averaging, 0 h shaded | -20 to +50 °C; counting at temperate sites | At risk (track averaging needed) |
| R8 | Autonomy | 6.22 d; 4.36 d at -20 °C; 4.98 d at end of life | 3 days | Met on paper (one cell) |
| R9 | Winter energy | 4.4 Wh/day stored against 2.47 Wh/day | Energy neutral at 1.5 sun hours | Met on paper (6 W) |
| R10 | Ingress protection | IP65 enclosure, gasketed head | IP65 | Not verifiable at TRL 3 |
| R11 | Mass | 5.26 kg | 6 kg or less | Met on paper |
| R12 | Installation | 59 min estimate; panel post factor 55; twist factor 3.3 | Two people, 60 min, no drilling, 35 m/s | Not verifiable at TRL 3 (wind and fit met on paper) |
| R13 | Cost | $274.00 | $275 or less | Met on paper |
| R14 | Service life | 9 % nightly depth of discharge | 5 years, one battery change | Not verifiable at TRL 3 |
| R15 | Radio use | 0.82 s/h at SF9; 371 ms at US915 DR0; 10 of 11 bytes | EU868 1 % and US915 dwell | Met on paper |

Counts: 0 not met, 3 at risk, 4 not verifiable at TRL 3, 7 met on paper, 1 met by design.
