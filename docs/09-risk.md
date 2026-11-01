---
doc_id: CBC-RSK-001
title: CurbCount risk register and hazard analysis
project: CurbCount
doc_type: Risk register and hazard analysis
version: '0.1'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-10-31'
  author: Amish Chadha
  change: 'Opened in the kit 1.9.1 upgrade: project risks, preliminary hazard analysis and first-pass design FMEA'
---

# CurbCount risk register and hazard analysis

The top risks are that the counts will not meet the accuracy targets on warm days (K1, F8: the highest RPN, 64), that charging stops at cold sites (K2) and that a part falls from a pole (H1, mitigated by bands, spacers and lanyards). Method: STANDARDS section 23. Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high). Nothing here has been tested; every control is a design intent checked on paper.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K1 | Counts miss the accuracy targets | Cars cross the field in 4.2 frames, random merging loses 6.5 %, sunlit pavement hides people (CAL-001 C, D) | The counter fails PR-001, PR-002 or PR-008 in the field | 3 | 4 | Design lead | Track averaging in the tracker; compare with manual counts at the first partner street (TRL 4, on hold); radar variant for hot sites |
| K2 | Node stops at cold sites | LiFePO4 may not be charged below 0 degrees C; charging stops at about 0 degrees C air or below (STM S8) | Counters at cold sites run dry after about 4 days of cold | 3 | 3 | Amish; FieldNode project | Decision O1 in CBC-DEC-001: heated cell pocket, low-temperature cell, or limit the claim to cool sites (recommended now) |
| K3 | Parts cost passes the target | BOM is 1.00 USD under 275 USD on indicative prices | The target is missed by the first real quote | 4 | 2 | Design lead | Check prices when parts are bought; the target is a control figure, not a limit; savings listed in CBC-DEC-001 |
| K4 | No partner street with manual counts | No partner agreed; Toronto is only a candidate (CBC-DDR-002 O1) | Accuracy cannot be checked | 3 | 3 | Amish | Approach the first candidate; keep TRL 4 on hold until agreed |
| K5 | FieldNode core changes under CurbCount | Pin order, port supply and jumper sensing are agreed with FieldNode but not final | The sensor port and BOM lines 1, 2, 11 and 14 change | 3 | 3 | Design lead; FieldNode project | Keep the agreement items in CBC-DEC-001; re-run the trace and the BOM when FieldNode freezes |
| K6 | Residents distrust a thermal counter | A thermal camera is still a camera to many people | The pilot is refused or the device removed | 2 | 4 | Amish; partner city | Public notice plate with an accurate sentence (CBC-DDR-001 D7), open firmware, 7.6 px/m published, no frame leaves the device |
| K7 | Window film fails in sun | Film grade unchosen; unstabilised polyethylene embrittles (STM S18) | The array loses transmission or the head leaks | 3 | 3 | Design lead | Specify a UV-stabilised clear grade; replaceable by design (clamped frame) |
| K8 | Radar option cannot be shown to fit | Module price unknown, 60 GHz rules to assess (REG G9) | Option B drops out as the hot-climate variant | 3 | 3 | Amish | Research module price and rules before choosing B for any site |
| K9 | Kit or render pipeline gaps delay the media | Renders are made on Amish's Mac, not here; media/options.png is not in this commit | Documents and renders are out of step | 3 | 2 | Coordinator | Render and compose the options picture after this commit |

## Preliminary hazard analysis

Table 2. Hazards. The counter has no mains connection and no moving parts; its hazards come from working at height, a falling part, a lithium cell and the privacy promise.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Panel or head falls onto the street | Band slips, bolt or set screw loosens, 35 m/s gust | A person below is hit | 5 | 2 | Four stainless band clamps at 1,000 N preload give twist factor 3.3 (CAL-001 H3); crush spacers; nyloc nuts; panel mount and head each on a lanyard (PR-021) | Low |
| H2 | Fitter falls or drops a tool at height | Work at 4 to 5 m on a mobile platform | Injury to the fitter or a passer-by | 4 | 2 | Two people; panel fitted on the ground first; head already on the arm; work-at-height rules of the owner (REG G8, G11) | Medium until a partner's procedure is known |
| H3 | Contact with pole or street-light wiring | Fitter opens or touches pole electrics | Electric shock | 5 | 1 | No drilling, no pole wiring, clamp-on only (PR-014); the counter has no mains connection; the pole owner isolates if asked | Low |
| H4 | Lithium cell fault | Short circuit, over-temperature, charging below 0 degrees C | Heat, venting, fire in the enclosure | 4 | 2 | Fused holder 5 A, NTC lockout and protection on the FieldNode board (BOM lines 2 and 3); cell kept in the IP65 enclosure | Low |
| H5 | Cut metal edges | Sawn and drilled aluminium and stainless | Cuts to the builder | 2 | 3 | Edge break and deburr on every cut edge (modelled with `break_edges` in CAD); gloves in BLD-001 | Low |
| H6 | Wind loads the pole | Panel and head act as sails | Pole or fixing overloaded | 4 | 1 | Panel 52 N and head 8 N in a 35 m/s gust; post factor 55 (CAL-001 H1) | Low |
| H7 | Counter turned into a camera | Someone changes the firmware to store or send frames | Loss of the privacy promise | 4 | 2 | Open firmware and hardware, no code path that writes or sends a frame (STM S20), frames only on a service jumper, notice plate; a hardware change is visible | Medium; audit at TRL 4 |
| H8 | Head struck by a high vehicle | Head 4.3 m above the road | Head torn off and dropped | 3 | 2 | Head on a lanyard (PR-021) | Low to medium |
| H9 | RF exposure under the radar (option B) | 60 GHz transmitter 2.55 m above a person's head | Exposure above the guideline | 2 | 1 | 12 mW/m2 on a 1 W overestimate against 10 W/m2 (STM S21) | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection (maximum 125). Actions are required at an RPN of 36 or more and are proposals for the design review.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Band clamps | Hold the saddle plates to the pole | Loosen or slip | Arm twists, aim lost, parts fall | Preload lost by vibration or creep | 5 | 2 | 3 | 30 | Fit to the band torque that gives 1,000 N preload (to confirm, CBC-DEC-001 item 5); V-saddle grip; lanyards; inspect on each visit |
| F2 | Pole-top sleeve and set screws | Hold the panel | Set screw loosens | Panel rotates or lifts | Vibration | 4 | 2 | 3 | 24 | Thread-locking compound; lanyard |
| F3 | Arm bracket bolts and crush spacers | Carry the head on the arm | Bolt loosens or spacer crushes | Arm sags, aim drifts | Torque too high or too low | 4 | 2 | 2 | 16 | Spacers stop over-tightening (modelled); nyloc nuts |
| F4 | Printed ASA head housing | Hold the array and keep out water | UV or heat cracking | Water in, array lost | Wrong print settings, long sun | 3 | 2 | 4 | 24 | Print in ASA, a UV-stable class (BOM line 8); inspect after the first summer |
| F5 | HDPE window film | Pass 8 to 14 um radiation and seal the head | Embrittles, scratches or tears | Transmission falls, ingress | UV, grit, wrong grade (STM S18) | 3 | 4 | 3 | 36 | Specify a UV-stabilised clear grade; clamped frame so it can be replaced |
| F6 | Window frame gasket | Seal the head to IP65 | Gasket under-compressed | Water enters | Screws too loose, ledge uneven | 4 | 2 | 3 | 24 | Tighten the frame screws evenly (BLD-001); check by spray test at TRL 4 |
| F7 | M12 cable and M16 gland | Carry I2C and supply 2 m to the head | Gland leaks or cable chafes | Moisture, bus errors | Gland not tightened, sharp edge | 3 | 2 | 2 | 12 | Moulded plug, 6 mm cable in a rated gland; lanyard and ties |
| F8 | Thermal array and window | Sense people against pavement | Contrast too low on sunlit pavement | Pedestrians missed for hours | Warm surfaces in sun (STM S3) | 4 | 4 | 4 | 64 | Track averaging; measure contrast at TRL 4; radar variant for hot sites |
| F9 | Tracker on the STM32WL | Turn blobs into counts | Merges, splits or loses tracks | Wrong counts | Groups, occlusion, 4.2 frames per car | 4 | 3 | 4 | 48 | Tracker profile and replay on recorded frames at TRL 4; ESP32-S3 fallback head costs about 311 USD |
| F10 | LiFePO4 cell and charger | Store energy | Cell cannot charge in cold | Node stops after the stored days | Air below about 0 degrees C (STM S8) | 3 | 3 | 2 | 18 | Decision O1; fuel gauge reports state of charge |
| F11 | Solar panel | Harvest energy | Shading or dirt | Low harvest, flat cell | Trees, dust, bird droppings (40 % derating assumed) | 2 | 3 | 3 | 18 | Derating in CAL-001 E; panel tilt and site check |
| F12 | Enclosure lugs and saddle plate | Clamp the FieldNode enclosure to the pole | Lug screw loosens | Enclosure slips or tips | Vibration | 5 | 2 | 3 | 30 | Nyloc nuts on M5 lug bolts; bands carry the load, not the lugs |
| F13 | Aluminium against stainless and a steel pole | Carry the load for five years | Galvanic corrosion at joints | Joint weakens or seizes | Wet, salted street (STM S19) | 3 | 3 | 4 | 36 | Coat or isolate contact faces; stainless against aluminium kept to small areas |
| F14 | Calibration jumper and frame stream | Allow an aim check on site | Left connected | Frames stay viewable on the service port | Fitter forgets | 4 | 2 | 3 | 24 | Firmware sketch streams only while the jumper is present; close-up step in BLD-001 |
| F15 | Public notice plate | Tell the public what is counted | Ties fail or print fades | Plate lost or unreadable | UV, weather | 2 | 3 | 2 | 12 | Two stainless ties; UV-stable print |
| F16 | LoRa antenna and uplink | Send the 10-byte record | Detuned by metal near the antenna | Lost packets | Pole and enclosure placement | 2 | 3 | 3 | 18 | Antenna on the enclosure top, clear of the arm; link test on site |
| F17 | Option B radar bursts | Give the tracker 4 frames per vehicle at 0.2 W | Burst rate too low | Missed vehicles | Energy fix (CBC-DEC-001 C1) cuts frames | 3 | 3 | 3 | 27 | Profile the burst rate with the tracker (TRL 4) |

Highest RPN: F8 (64), F9 (48), F5 (36). Detection scores assume no field testing yet (TRL 4 is on hold), so they are conservative.
