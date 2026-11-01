"""CurbCount STEM check calculations (CBC-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. First-order screens of every claim the design makes. Option A (thermal array) numbers come
from the calculation note (CBC-CAL-001, docs/04-calcs/sizing.py), which this script imports (about a minute: it builds the model);
option B (60 GHz radar) numbers are computed here from stated assumptions. The sizing itself stays in the calculation note.
"""
import contextlib, io, math, sys
sys.path.insert(0, ".kit")
from stem_check import Check, WITHIN, PLAUSIBLE, FIX, SIGMA  # noqa: E402,F401
sys.path.insert(0, "docs/04-calcs")
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL   # noqa: E402  CBC-CAL-001, reads cad/src/model.py

c = Check()
P = CAL.P

# ---- Option A, physics: optics and radiation
c.claim("S1", "The thermal array cannot resolve a face or a number plate from 4.3 m: under the IEC 62676-4 detection level at head height",
        "Physics", "Optics and radiation", "Pixels per metre = 1 / (range x pixel angle); IEC 62676-4 levels detect 25, recognise 125, identify 250 px/m",
        round(CAL.ppm_head, 2), 25.0, "px/m", closed_by="CBC-CAL-001 B2 (7.6 px/m, 8.5 for 2.0 m)")
c.claim("S2", "One pole covers a 3 m sidewalk, a 2 m bike lane and the nearest 3.5 m lane (110 degree axis across the street)",
        "Physics", "Optics and radiation", "Ray geometry of the 110 x 75 degree lens, tilt 7.5 degrees toward the road",
        round(CAL.P["fov"][0] / 2 - (CAL.need_back + P["tilt"]), 1), 0.0, "deg margin on the sidewalk side", rule="above", closed_by="CBC-CAL-001 A2, A3 (10.9 deg margin on the sidewalk side)")
c.cited("S3", "A person stands out from pavement by more than the single-frame detection contrast on a mild design day", "Physics", "Heat transfer",
        "Surface energy balance and the array's noise: NETD 0.1 K RMS at 1 Hz (Melexis MLX90640 datasheet) scales as the square root of the refresh rate; "
        "4 sigma on a person that fills 0.37 of a pixel behind a 0.75 transmission window",
        f"smallest contrast {CAL.dt_min:.1f} K; blind {CAL.mild[0]:.1f} h a day on sunlit pavement with single frames, {CAL.mild[2]:.1f} h with track averaging, {CAL.mild[1]:.1f} h shaded "
        f"(assumed surface temperatures, to measure)", PLAUSIBLE)
tau_hdpe = CAL.TAU
c.claim("S4", "A 0.5 mm unpigmented HDPE film passes at least 0.5 of 8 to 14 um radiation", "Physics", "Optics and radiation",
        "Two Fresnel reflections (n 1.53) and bulk absorption of 4 per cm, band-averaged (assumed; polyethylene is known to be IR transparent, thin film transmits most of the band)",
        round(tau_hdpe, 2), 0.5, "transmission", rule="above", margin=0.5, closed_by="")
H_WIN = (P["window_z"] - P["sw_h"]) / 1000.0           # m, window above the sidewalk; the road is 0.15 m lower
H_ROAD = P["window_z"] / 1000.0
frames_road = CAL.frames["car, mid lane"][0] / CAL.V_CAR * CAL.FRAME_HZ
frames_hood = frames_road * (H_ROAD - 1.0) / H_ROAD     # the warm hood is about 1.0 m up, where the field along the street is shorter
frames_hood32 = frames_hood * 2                          # 32 Hz subpages
c.cited("S5", "A car at 50 km/h stays in the field for the 4 frames the tracker needs", "Engineering and technology", "Sensing resolution",
        "Frames = field length / speed x frame rate (8 full frames a second from 16 Hz subpages). CAL-001 C1 treats the car as a point at road level (4.2 frames); "
        "the warm hood is about 1.0 m up, where the along-street field shrinks by (4.3 - 1.0) / 4.3 (independent review)",
        f"{frames_road:.1f} frames at road level, {frames_hood:.1f} at the hood, against 4: fails. Fix proposed: 32 Hz subpages (16 frames a second) give {frames_hood32:.1f}, "
        "at 1 MHz I2C (bus 24 % busy at 16 Hz, 48 % at 32 Hz, CAL-001 F1), noise up by the square root of 2 (recovered by track averaging) and a faster pull-up (644 ohm, F2); "
        "this changes the sensor port speed of the shared FieldNode core, so it goes to Amish (CBC-DEC-001 O3)", FIX)
# ---- Option A, engineering: power, link budget
c.claim("S6", "Winter solar harvest covers the daily load (6 W panel, 1.5 peak sun hours, 40 % derating)", "Physics", "Electromagnetism and circuits",
        "Stored energy = panel W x sun hours x derating x MPPT efficiency x charge efficiency", round(CAL.s6, 2), round(CAL.draw, 2), "Wh/day", rule="above",
        closed_by="CBC-CAL-001 E3 (4.4 Wh against 2.47 Wh, while the cell can charge: see S8, S25)")
c.claim("S7", "One cell carries the node for 3 days without sun", "Chemistry", "Electrochemistry and batteries",
        "Usable energy = 3.2 V x 6 Ah x 80 % depth of discharge; load 103 mW average; 70 % capacity at -20 C and 80 % at end of life (independent review: both together)",
        3.0, round(CAL.auto1 * CAL.CAP_COLD * CAL.CAP_EOL, 2), "days (-20 C, end of life)", closed_by="CBC-CAL-001 E2 (4.36 days at -20 C; 3.49 days with the end-of-life 80 % as well)")
# Cold charging: a LiFePO4 cell may not be charged below 0 C (cell makers; FieldNode's NTC lockout enforces it)
alpha, g_sun, a_sun, ua = 0.4, 300.0, 0.05, 1.2    # light grey enclosure, winter sun W/m2, sunlit area m2, UA of the box in wind W/K (assumptions)
DERATE_SHADE = 0.6                                  # street shade, the same 40 % derating as the panel (independent review)
dt_box = (alpha * g_sun * a_sun * DERATE_SHADE + 0.1) / ua
air_min = -dt_box
c.cited("S8", "The node stays energy neutral through a winter at sites where the air falls below freezing", "Chemistry", "Electrochemistry and batteries",
        "LiFePO4 cells must not be charged below 0 C (lithium plating); FieldNode's NTC lockout stops charging. First-order enclosure temperature in winter sun: "
        f"(0.4 x 300 W/m2 x 0.05 m2 x 0.6 shade + 0.1 W) / 1.2 W/K = {dt_box:.1f} K above the air (assumptions)",
        f"by this estimate the cell can charge only when the air is above about {air_min:.0f} C, and nearer 0 C allowing for the thermal lag of the cell after a cold night (independent review), so 0 C is taken as the limit; below that the node lives on the stored 4.4 days and then stops, so energy neutrality holds for "
        "cool sites, not for a Toronto January. The claim fails for cold sites; fixes (heated cell pocket, low-temperature cell) change the shared FieldNode core and the scope, "
        "so they go to Amish (CBC-DEC-001 O1)", FIX)
c.claim("S9", "The 10-byte record fits US915 DR0 and its airtime stays under the 400 ms dwell limit", "Engineering and technology", "Power and link budgets",
        "LoRa time on air (Semtech AN1200.13) for 10 + 13 bytes at SF10, 125 kHz; US915 DR0 allows 11 bytes", round(CAL.t10p * 1000, 0), 400.0, "ms",
        closed_by="CBC-CAL-001 G2 (371 ms)")
c.claim("S10", "Uplinks stay inside the EU868 1 % duty cycle", "Engineering and technology", "Power and link budgets",
        "Airtime per hour = 4 x time on air at SF9 (206 ms)", round(CAL.t9 * 4, 2), 36.0, "s/h", closed_by="CBC-CAL-001 G1 (0.82 s/h)")
c.claim("S11", "Six 12-bit counters hold a 15-minute count in the busiest lane", "Mathematics", "Orders of magnitude",
        "Nearest lane at 1,800 vehicles/h (saturation flow, assumed) is 450 per 15 min; a 12-bit counter holds 4,095", 450.0, 4095.0, "counts per bin")
c.claim("S12", "Wind load: the post carries the panel at 35 m/s gusts with a safety factor of 1.5", "Physics", "Strength of materials",
        "Drag = 0.5 rho v2 Cf A; bending of a 42.4 x 3 mm aluminium post, 6063-T6 yield 150 MPa", round(CAL.s_post, 1), round(CAL.FY_AL / 1.5, 1), "MPa",
        closed_by="CBC-CAL-001 H1 (stress 2.7 MPa class, factor 55)")
c.claim("S13", "The band saddles hold the arm against the twist of the wind on arm and head", "Physics", "Mechanics and statics",
        "Friction torque of two bands at 1,000 N preload each, mu 0.2 (assumed) against the wind torque; if the liners creep and half the preload is lost the factor falls to about 1.6 (independent review), so a re-torque interval is needed", round(CAL.T_twist, 1), round(CAL.T_cap / 1.5, 1), "N m",
        closed_by="CBC-CAL-001 H3 (factor 3.3)")
m_total = sum(CAL.M_BOUGHT.values()) + CAL.M_FND_CORE + sum(CAL.m_made.values())
c.claim("S14", "The counter weighs 6 kg or less on the pole", "Engineering and technology", "Manufacturing tolerances",
        "Sum of modelled volumes times density plus catalogue masses of bought parts", round(m_total, 2), 6.0, "kg", margin=0.05, closed_by="CBC-CAL-001 H5")
r_max = 300e-9 / (0.8473 * CAL.c_bus)
c.claim("S15", "The I2C bus runs at 400 kHz over the 2 m M12 cable", "Physics", "Electromagnetism and circuits",
        "Rise time 0.8473 R C <= 300 ns (I2C fast mode) with 220 pF of cable (100 pF/m assumed, to measure): pull-up of at most 1.6 kohm, sink current 2 mA (within the 3 mA limit)",
        1.5, round(r_max / 1e3, 2), "kohm pull-up", margin=0.15, closed_by="")
c.cited("S16", "The STM32WL runs the fixed-point tracker (about 150 cycles per pixel, 2 % of a 48 MHz core, about 40 kB of RAM)", "Engineering and technology", "Control",
        "Operation counts: 768 pixels x 150 cycles x 8 frames/s / 48 MHz; RAM tally of CBC-CAL-001 F4 (64 kB part); the vendor's floating-point conversion would not fit (50 % of the core)",
        "cycle count is an estimate until the tracker is profiled on the part (TRL 4, on hold)", PLAUSIBLE)
c.claim("S17", "Parts cost stays within the USD 275 value-engineering target", "Engineering and technology", "Standards practice",
        "Sum of the 14 BOM lines (indicative prices; thermal array USD 64.95 at SparkFun, checked 2026-10-31)", round(CAL.total, 2), 275.0, "USD", margin=0.02)
c.cited("S18", "The window film survives five years of sun", "Chemistry", "Materials and polymer chemistry",
        "Unstabilised polyethylene photo-oxidises and embrittles under UV; carbon black would stop it but also blocks the infrared, so a UV-stabilised (hindered amine) clear grade is needed",
        "no grade chosen; film to be specified and measured (TRL 4, on hold)", PLAUSIBLE)
c.cited("S19", "Aluminium saddles, plates and arm with stainless bands and bolts last five years on a steel street pole", "Chemistry", "Inorganic",
        "Aluminium is anodic to stainless steel and to a steel pole in a wet, salted street; the contacts are small and painted or coated in practice, but the joints are not specified",
        "isolating washers or coating to specify; to confirm in the build plan checks (TRL 4, on hold)", PLAUSIBLE)
c.cited("S20", "The counter records no image and no personal identifier: only six counters leave the device in normal operation", "Biology", "Human physiology and biomechanics",
        "No personal data can be recovered from 7.6 px/m thermal frames held in RAM and overwritten every 125 ms; the record identifies no one (data protection by design, GDPR Article 25). "
        "During an aim check the calibration jumper streams frames to a laptop at the pole (CBC-CAL-001 H6, PR-020), and quiet night-time bins can single out one person (independent review)",
        "S1 gives the resolution; the firmware path for the jumper stream, its limits and the small-count bins are firmware design and audit questions (TRL 4, on hold)", PLAUSIBLE)
c.cited("S25", "Option A at temperate sites: the cell stays below its 45 C charge limit", "Chemistry", "Electrochemistry and batteries",
        f"Enclosure temperature = air + {dt_box:.1f} K (S8 estimate) with the temperate design day capped at 20 C air (PR-008); LiFePO4 charging allowed 0 to 45 C (cell datasheet class)",
        f"{20 + dt_box:.0f} C <= 45 C; on a hot clear day outside this scope FieldNode's own figures give 0.8 Wh stored against 2.47 Wh drawn without a shield (CBC-CAL-001 E6)", WITHIN,
        closed_by="CBC-CAL-001 E6 (temperate scope, PR-008)")
c.cited("S29", "The window stays clear of dew, frost, insects and droppings", "Physics", "Optics and radiation",
        "A film of water or frost on the window absorbs 8 to 14 um radiation strongly (a 10 um water film is estimated to pass about 0.37 by the independent review; not recomputed here); webs, insects and droppings block pixels",
        "no heater, hydrophobic coating or wiper is in the design; contrast margin (S3) and cleaning interval to measure (TRL 4, on hold)", PLAUSIBLE)
c.cited("S30", "The 2 m sensor cable and the node survive surges and electrostatic discharge on a street pole", "Engineering and technology", "Standards practice",
        "A cable running up a pole is exposed to induced surges and static discharge; the BOM has resettable fuses (line 14) but no surge protection devices",
        "protection to specify with the FieldNode project; to assess (TRL 4, on hold)", PLAUSIBLE)
c.cited("S31", "The tracker classes people, bicycles and cars correctly and does not count dogs, umbrellas or prams as extra people", "Engineering and technology", "Control",
        "Class by blob area, speed and track length at 32 x 24 pixels; a dog or a pram is a small warm blob, an umbrella can hide a person from above (independent review)",
        "no calculation possible at TRL 3; replay of recorded frames at TRL 4 (on hold); tracked in CBC-RSK-001 F9", PLAUSIBLE)

# ---- Option B, 60 GHz radar head
EIRP_W = 1.0     # generous upper bound on radiated power, W (assumption; module datasheet figure to assess)
r_head = (P["window_z"] - P["sw_h"] - 1750.0) / 1000.0   # m, radar to the head of a person on the sidewalk (independent review: 2.40 m, not 2.55 m)
s_rf = EIRP_W / (4 * math.pi * r_head ** 2)
c.claim("S21", "Option B: RF exposure of a person under the radar is far below the ICNIRP limit", "Biology", "Toxicology",
        "Power density = EIRP / (4 pi r2) at head height, 2.40 m, with 1 W EIRP (a deliberate overestimate); ICNIRP 2020 general public limit 10 W/m2 above 6 GHz (to confirm against the guideline text)",
        round(s_rf * 1000, 2), 10000.0, "mW/m2", closed_by="")
P_RADAR = 1.2    # W, continuous average power of a radar module with its processor (assumption, to assess)
panel20 = CAL.stored(20)
P_DUTY = 0.20                                   # W average after the fix: one frame burst in six (CBC-DEC-001 C1)
for label, p_avg in (("as first drawn, continuous 1.2 W (claim failed)", P_RADAR), ("duty-cycled 0.4 W (autonomy still short)", 0.4), ("duty-cycled 0.25 W (short once cold and end of life are combined)", 0.25), (f"duty-cycled {P_DUTY} W (the fix)", P_DUTY)):
    d_b = p_avg * 24 / CAL.ETA_RAIL + CAL.CORE_WH
    print(f"[option B] {label}: {d_b:.1f} Wh/day against {panel20:.1f} Wh/day stored by the 20 W panel; autonomy {2 * CAL.e_cell * CAL.USABLE / d_b:.1f} days, {2 * CAL.e_cell * CAL.USABLE * CAL.CAP_COLD * CAL.CAP_EOL / d_b:.1f} days at -20 C and end of life")
d_duty = P_DUTY * 24 / CAL.ETA_RAIL + CAL.CORE_WH
c.cited("S22", "Option B: a 20 W panel keeps the radar head energy neutral in winter (radar frames duty-cycled to 0.2 W average; running continuously at 1.2 W it drew 32 Wh/day and failed)", "Physics", "Electromagnetism and circuits",
        "Stored energy of a 20 W panel (1.5 peak sun hours, 40 % derating) against the daily draw; fix decided under the standing instruction (CBC-DEC-001 C1): one frame burst in six. TI's reference may draw more than 1.2 W and the burst rate the tracker needs is unproven (independent review)",
        f"{d_duty:.1f} Wh/day <= {panel20:.1f} Wh/day stored on paper; the burst rate that still gives 4 frames per vehicle is to be profiled (TRL 4, on hold)", PLAUSIBLE)
c.claim("S23", "Option B: two cells carry the radar head for 3 days without sun (0.2 W duty-cycled average; at 0.25 W they gave only 2.6 days with cold and end of life together and failed)", "Chemistry", "Electrochemistry and batteries",
        "Usable energy of two 3.2 V 6 Ah cells at 80 % against the duty-cycled draw, 70 % capacity at -20 C and 80 % at end of life, together (independent review)", 3.0,
        round(2 * CAL.e_cell * CAL.USABLE / d_duty * CAL.CAP_COLD * CAL.CAP_EOL, 2), "days (-20 C, end of life)", closed_by="CBC-DEC-001 C1")
c.cited("S24", "Option B: a 60 GHz radar counts people and vehicles by range, angle and speed in rain, dark and heat", "Physics", "Optics and radiation",
        "FMCW radar resolves range from the beat frequency and speed from phase; Texas Instruments offers a people counting and tracking reference for the IWR6843 (TI, checked 2026-10-31)",
        "the principle is established; counting accuracy and false counts from wind-blown foliage are not shown (TRL 4, on hold)", PLAUSIBLE)

import json
_fid = json.load(open("cad/fidelity.json"))["options"]
m_b = m_total + (_fid["B"]["mass_kg"] - _fid["A"]["mass_kg"])
c.claim("S27", "Option B stays at 6 kg or less on the pole", "Engineering and technology", "Manufacturing tolerances",
        f"Option A's {m_total:.2f} kg plus the CAD mass difference between the two models ({_fid['B']['mass_kg'] - _fid['A']['mass_kg']:.1f} kg: second cell, larger panel, radar head); the independent review put it nearer 6.8 kg, to profile",
        round(m_b, 2), 6.0, "kg", margin=0.1, closed_by="")
i_chg20 = 20 * CAL.ETA_MPPT / CAL.V_CHG
c.cited("S28", "Option B: FieldNode's charger passes the 20 W panel's current into two cells", "Physics", "Electromagnetism and circuits",
        f"Peak charge current of a 20 W panel at 1,000 W/m2 is {i_chg20:.1f} A (CBC-CAL-001 E5) against FieldNode's standard charger setting of 1.5 A; two cells in parallel take {i_chg20 / 2:.1f} A each ({i_chg20 / 2 / CAL.AH_CELL:.2f} C)",
        "the charger setting caps the harvest unless FieldNode's high-load variant (raised in CBC-DDR-001 D3) is used; a shared-core change, so it goes to Amish with option B (CBC-DEC-001 O4)", FIX)
c.cited("S26", "Option B at hot sites: the cell can still charge when the air is near 40 C", "Chemistry", "Electrochemistry and batteries",
        "LiFePO4 charging is allowed to 45 C only (cell datasheet class); FieldNode's own figures put the cell above the limit for most sun hours on a hot clear day and store 0.8 Wh against 2.47 Wh drawn without a shield, 13.1 Wh with its proposed shield (CBC-CAL-001 E6)",
        "option B is the hot-climate variant but shares the same cell and enclosure, so it needs the shield or a cell pack in shade; a shared-core change, so it goes to Amish with option B (CBC-DEC-001 O4)", FIX)

state = c.write()
print("project.yaml stem_check:", state)
