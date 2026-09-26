---
doc_id: CBC-CAL-001
title: CurbCount sizing calculations
project: CurbCount
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (coverage, pixel size and privacy, frames per crossing, merging, thermal contrast and window, energy, processor study, radio, wind and mounting, mass, installation, service life, cost)
---

# CurbCount sizing calculations

On paper, CurbCount meets four of its fifteen requirements (three by calculation, one by design), has four at risk, cannot show four at TRL 3 and misses three. The misses are cost (R13: $290.00 against the $150 budget and against the recommended $275), counting in hot weather (R7: on a hot design day a pedestrian's contrast with the pavement stays below the detection threshold for 14 h on a sunlit sidewalk and all day on a shaded one), and R4 as written (the smallest ground pixel is 0.22 m, not 0.25 m, although the privacy aim is met with a wide margin at 8.5 px/m at head height). The calculations changed three things in the TRL 2 concept: the thermal array is turned 90 degrees so that its 110 degree axis spans the street, which fixes coverage (R6); the pole-top panel mount is aluminium instead of steel; and the FieldNode enclosure takes its TRL 3 size with a CurbCount saddle plate. Several TRL 2 figures were optimistic: the ground pixel (0.22 m, not 0.3 to 0.4 m) and the mass (6.02 kg, not 4.2 kg). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [E2], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the mount is safe on a particular pole, that the cells are safe in a particular climate or that the device complies with data protection law where it is installed. Pole loading must be checked by the pole owner. See CBC-PRC-001, Safety.

## Scope and method

The note checks every requirement in CBC-REQ-001 v0.3 against the design in CBC-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and its camera model, so the head height, tilt, arm, enclosure, panel and footprint used here are those in the STEP files, in drawing CBC-DWG-001 and in the concept media. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is one counter on a 114 mm street pole 0.45 m behind the curb, the sensor window 4.3 m above the road, a 3 m sidewalk (0.15 m above the road), a 2.0 m bike lane and one 3.5 m traffic lane.

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
| Electronics | ESP32-S3 50 mA at 3.3 V (240 MHz, radio off), 25 mA at 80 MHz; STM32WL run mode 5 mA; rails 90 % efficient; FieldNode core 4.0 mWh/day | TRL 2 figure kept as conservative; FND-CAL-001 [A1] |
| Energy | Two 3.2 V 6 Ah LiFePO4 cells, 80 % usable, 70 % at -20 °C, 80 % at end of life; winter 1.5 peak sun hours with 40 % derating for street shade, dust and heat; charger 85 %, charging 95 % | CBC-REQ-001 R8 and R9; FieldNode efficiencies |
| Radio | 14-byte payload plus 13 bytes of LoRaWAN overhead, 125 kHz, coding rate 4/5, 8-symbol preamble, 96 uplinks a day | As FND-CAL-001 |
| Wind and mounting | 35 m/s gust, 1.225 kg/m³; force coefficients 1.2 (panel), 1.3 (boxes), 2.0 (square tube); band preload 1,000 N, friction 0.2 (as FND-CAL-001); 6063 aluminium, yield 150 MPa | Screening values, not a code check |
| Masses | FieldNode core 1.02 kg (FND-CAL-001 [F1] less its panel, bracket and mount); 20 W framed panel 1.90 kg; made parts from model volumes | Typical catalog masses |

## A. Coverage (R6)

- **Orientation.** The TRL 2 concept put the 75 degree axis across the street, tilted 10 degrees. That covers the sidewalk only to 2.08 m behind the curb, 69 % of the 3 m sidewalk [A4]. The design case spans 36.6 degrees behind and 51.6 degrees ahead of the vertical, 88.2 degrees in all [A3], which only the 110 degree axis can reach.
- **Chosen layout.** With the array turned 90 degrees and the view tilted 7.5 degrees toward the road, the footprint runs from 4.45 m behind the curb to 8.34 m into the road, 12.79 m across [A2], with 10.9 degrees of margin at both edges [A3]. Along the street it covers 5.71 m at the sidewalk back to 7.28 m at mid lane [A5]. The far part of the road is masked in firmware; only the nearest lane is counted.
- **Shadow.** The pole and the enclosure hide a strip up to 0.73 m wide at the back of the sidewalk, 13 % of the field along the street there [A6]. The tracker must join tracks across it.

R6 is **met on paper**.

## B. Pixel size and privacy (R4)

- **Ground pixel.** Below the head a pixel covers 0.251 x 0.233 m; at the curb edge of the sidewalk 0.251 x 0.224 m; at the back of the sidewalk 0.376 x 0.203 m; at mid lane 0.442 x 0.259 m [B1]. The smallest is 0.224 m, along the street near the head. TRL 2 quoted 0.3 to 0.4 m, which was an average, not the minimum [B1b].
- **What the sensor can resolve.** Privacy depends on resolution at the subject, not on the ground. A 1.75 m person directly below is 2.40 m from the sensor and is imaged at 7.6 px/m; a 2.0 m person at 8.5 px/m [B2]. The IEC 62676-4 levels for video surveillance are 25 px/m to detect, 125 px/m to recognize and 250 px/m to identify a person (values quoted from the standard, not checked online in this session). The sensor stays below even the detection level for a face. A number plate at mid lane spans 1.8 pixels [B3].

R4 is **not met as written** (0.22 m against 0.25 m), but its privacy aim is met with a margin of about 30 times against identification. A restatement of R4 in px/m is proposed in `docs/REVIEW.md`.

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

On a hot day a clothed person is within a few kelvin of the pavement at night and all day in shade, so a thermal-only counter goes blind for much of the day. On sunlit pavement the contrast crosses zero as the pavement heats, and the model puts that crossing band at several hours even on mild days. The surface temperature model is crude and these hours are the least certain figures in the note, but the conclusion for hot weather holds across the assumptions tried. R7 is **not met on paper** for counting with air up to 35 °C. The radar variant kept under DDR-001 D2 is the route for hot climates; the electronics temperature part of R7 inherits FieldNode's R2 and R3 (see section E).

## E. Energy (R8, R9)

- **Load.** The array draws 76 mW and the processor 165 mW, 241 mW at the head. With 90 % rail efficiency and the FieldNode core, the counter takes 6.43 Wh/day from the cells, 268 mW on average [E1]. TRL 2 quoted 0.30 W and 7.2 Wh/day. At 80 MHz the processor would bring this to 4.23 Wh/day [E1b]. Either way the counter needs 2.1 times FieldNode's current 115 mW sensor allowance and 2.4 times the proposed 100 mW [E1b].
- **Autonomy (R8).** Two cells hold 38.4 Wh, 30.7 Wh usable: 4.78 days without sun, 3.35 days at -20 °C and 3.82 days at end of life. One cell gives 2.39 days [E2]. R8 (3 days) is **met on paper** with two cells.
- **Winter harvest (R9).** *Table 4. Panel size in the winter design case [E3].*

| Panel | Stored per day | Ratio to 6.43 Wh drawn | Refill after 3 sunless days |
| --- | --- | --- | --- |
| 6 W (FieldNode standard) | 4.4 Wh | 0.68 | Not energy neutral |
| 10 W | 7.3 Wh | 1.13 | 23.0 days |
| 15 W | 10.9 Wh | 1.70 | 4.3 days |
| 20 W | 14.5 Wh | 2.26 | 2.4 days |

  The smallest energy-neutral panel is 8.8 W [E4]. R9 is **met on paper** with the 20 W panel; a 15 W panel would also meet it with slower recovery.
- **Charger.** At full sun the 20 W panel pushes 5.0 A into the cells (0.42 C for two), against about 1.5 A from FieldNode's 6 W panel, and each cell holder carries a 5 A fuse [E5]. The high-load variant needs a charger set for at least 5 A or a limit on panel power; this is an interface point for FieldNode. The 12 V class panel's open-circuit voltage reaches about 25.0 V at -20 °C, and its maximum power voltage falls to about 14.8 V at 75 °C [E5b], both inside the input range of a bq24650 class charger (to confirm for the chosen part).
- **Heat.** FieldNode's calculation shows that on a hot clear day its cell sits above the 45 °C charge limit for most of the sun hours. Borrowing FieldNode's charge-window share, CurbCount would store 2.7 Wh against 6.43 Wh drawn without a sun shield and run flat after 8.2 days of such weather; with FieldNode's proposed shield it stores 43.7 Wh [E6]. The CurbCount enclosure is not under its panel, so the borrowed share is probably optimistic.

## F. Processor study: tracking on the STM32WL alone (DDR-001 D4)

- **Bus.** Reading one subpage takes 37.6 ms at 400 kHz I²C (60 % of the bus at 16 Hz) or 15.0 ms at 1 MHz (24 %) [F1]. Over the 2 m M12 cable (about 220 pF) the pull-ups must be 1.6 kΩ or less at 400 kHz and 644 Ω or less at 1 MHz, sinking 2.1 and 5.1 mA [F2]. Both fit I²C limits on paper; noise pickup on a cable up a street pole is a TRL 4 question.
- **Compute.** The STM32WL's Cortex-M4 core runs at 48 MHz and is taken here as having no floating-point unit (to confirm). The reference temperature conversion, at an estimated 2,000 to 4,000 cycles a pixel in software, would take 26 to 51 % of the core at 8 frames a second; a fixed-point pipeline on the raw data, at about 150 cycles a pixel, takes 2 % [F3]. RAM is estimated at 44 kB of 64 kB, most of it the LoRaWAN stack [F4].
- **Energy.** Without the ESP32-S3 the head load falls to 92 mW, inside FieldNode's allowance, and the counter draws 2.47 Wh/day. On standard FieldNode power (one cell, 6 W panel) that gives 6.22 days without sun (4.36 at -20 °C) and 1.77 times the draw in winter [F5], meeting R8 and R9 without the high-load variant. Parts would fall to about $253.00 [J2].

The STM32WL-only design is feasible on paper if the tracker is written in fixed point; it removes the high-load power variant and $37 of parts but still misses the budget. It is proposed as the preferred path in `docs/REVIEW.md`, awaiting Amish; bench profiling is TRL 4 work.

## G. Radio and data (R5, R15)

- **Airtime.** A 14-byte uplink takes 66.8 ms at SF7, 226.3 ms at SF9, 411.6 ms at SF10 and 1,646.6 ms at SF12. At SF9 that is 21.7 s a day and 0.91 s an hour, against 36 s an hour for the EU868 1 % duty cycle and 30 s a day for The Things Network's fair use; at SF10 and slower the fair-use limit is exceeded [G1].
- **US915.** At SF9 an uplink takes 226 ms against the 400 ms dwell limit. At DR0 (SF10) the payload limit is 11 bytes, so the 14-byte record cannot be sent at all; packing six 12-bit counters and a status byte into 10 bytes would fit and take 371 ms [G2].
- **Data.** 96 records of 14 bytes are 1.34 kB a day; the frames, 12.3 kB/s or 1.06 GB a day, stay in RAM [G3].

R5 is **met by design**. R15 is **at risk** until the payload packing is settled for US915.

## H. Wind, mounting and mass (R11, R12)

- **Panel.** A 35 m/s gust gives 750 Pa and 170 N normal to the panel. With a 0.327 m lever to the post base the moment is 56 N·m, which stresses the 42.4 x 3.0 mm aluminium post to 16 MPa (factor 9 on yield) [H1]. The 120 mm sleeve bears on the pole top with about 750 N. The pole itself carries the 170 N at 5.5 m, 933 N·m at its base, which the pole owner must check [H2].
- **Arm.** Wind along the street loads the arm with 31 N and the head with 8 N, twisting the arm about the pole by 14.1 N·m against 45.7 N·m of saddle friction from two bands (factor 3.2) [H3]. The arm bends to 3.3 MPa and its tip moves 0.17 mm, 0.019 degrees of aim [H4].
- **Mass (R11).** The FieldNode core is 1.02 kg; made parts are the arm and saddle 0.65 kg, the pole-top mount 1.13 kg, the enclosure saddle plate 0.29 kg, the head 0.19 kg and the notice plate 0.12 kg; bought parts add 2.61 kg, 1.90 kg of it the panel. The total is 6.02 kg [H5], at the 6 kg limit and within the uncertainty of the assumed masses. A steel mount, as at TRL 2, would have weighed 5.7 kg on its own. R11 is **at risk**; the STM32WL-only variant with a 6 W panel would take about 1.5 kg off.
- **Installation (R12).** The task list comes to 59 min for two people with a mobile platform [H6], at the 60 min limit. Wind and fit are met on paper, but the time is **not verifiable at TRL 3**. The pole-top mount fits only poles with a free top; a street light with its lantern on top needs a side-arm panel mount instead.

## I. Sealing and service life (R10, R14)

- A winter night of 16 h discharges the two cells by 11 %, and five years is 1,825 such cycles [I1], well within LiFePO4 cycle life at that depth. Calendar ageing in hot enclosures (see FND-CAL-001) and ultraviolet ageing of the HDPE window are unknown. R14 is **not verifiable at TRL 3**.
- The FieldNode enclosure is IP65 by design and the head is gasketed around the film window; R10 is **not verifiable at TRL 3**.

## J. Cost (R13)

The BOM has 14 lines, all priced; the total is $290.00, $140.00 over `budget_usd` ($150) and $15.00 over the recommended $275 [J1]. The FieldNode share (lines 1, 2, one cell of 3, and part of 14) is $98.00, consistent with FieldNode's $126.00 core less its 6 W panel, bracket and mount kit. The STM32WL-only variant on standard FieldNode power would cost about $253.00 [J2]. R13 is **not met**.

## Results

*Table 5. Requirement status. Values from `docs/04-calcs/results.csv`.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Classes and directions | 4.2 frames minimum (car at 50 km/h); 4 assumed needed | 3 classes x 2 directions | At risk |
| R2 | Pedestrian and cyclist accuracy | Random merges alone 6.5 % at 600/h; groups extra | Within 10 % per hour | At risk (not verifiable at TRL 3) |
| R3 | Vehicle accuracy | 4.2 frames per car; 3.4 px smear per subpage | Within 15 % per hour | Not verifiable at TRL 3 |
| R4 | Privacy | Smallest ground pixel 0.22 m; 8.5 px/m at head height (identify needs 250) | Ground pixel 0.25 m or larger | **Not met** as written; privacy aim met |
| R5 | Output format | 14 bytes per 15 min bin | 15 min counts, open format | Met by design |
| R6 | Coverage | Footprint -4.45 to 8.34 m; 10.9 degree margins; 0.73 m shadow | 3 m sidewalk, 2 m bike lane, nearest lane | Met on paper (array turned) |
| R7 | Operating range | Hot day: below detection contrast 14.2 h sunlit, 24.0 h shaded | -20 to +50 °C; counting with air to 35 °C | **Not met** on paper (hot weather) |
| R8 | Autonomy | 4.78 d; 3.35 d at -20 °C; 2.39 d with one cell | 3 days | Met on paper (two cells) |
| R9 | Winter energy | 14.5 Wh/day stored against 6.43 Wh/day | Energy neutral at 1.5 sun hours | Met on paper (20 W) |
| R10 | Ingress protection | IP65 enclosure, gasketed head | IP65 | Not verifiable at TRL 3 |
| R11 | Mass | 6.02 kg | 6 kg or less | At risk |
| R12 | Installation | 59 min estimate; panel post factor 9; twist factor 3.2 | Two people, 60 min, no drilling, 35 m/s | Not verifiable at TRL 3 (wind and fit met on paper) |
| R13 | Cost | $290.00 | $150 (recommended $275) | **Not met** |
| R14 | Service life | 11 % nightly depth of discharge | 5 years, one battery change | Not verifiable at TRL 3 |
| R15 | Radio use | 0.91 s/h at SF9; 226 ms dwell; 14 bytes exceed US915 DR0 | EU868 1 % and US915 dwell | At risk (US915 DR0 payload) |

Counts: 3 not met, 4 at risk, 4 not verifiable at TRL 3, 3 met on paper, 1 met by design.
