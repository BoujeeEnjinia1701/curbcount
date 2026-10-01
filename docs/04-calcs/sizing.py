"""CurbCount sizing calculations, CBC-CAL-001 v0.3 (TRL 3, CBC-DDR-002 and the design for construction CBC-DDR-003 applied).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that docs/04-calcs/01-sizing.md quotes, tagged [A1], [B2] and so on, and
writes docs/04-calcs/results.csv (requirement status table). Geometry comes from the parametric
model cad/src/model.py (PARAMS, derived() and the camera model); costs from bom/bom.csv; the
budget from project.yaml. First-principles estimates for a paper proof of concept only.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, ray, ground_hit, footprint_outline, pixel_edges, build_components  # noqa: E402

D = derived(P)
RESULTS = []


def out(tag, text):
    print(f"[{tag}] {text}")


def res(rid, value, target, status):
    RESULTS.append((rid, value, target, status))


# =============================================================== assumptions
# Street design case (CBC-REQ-001 v0.4)
X_SW_BACK = -P["sidewalk_w"]                     # mm, back of the sidewalk
X_BIKE_OUT = P["bike_w"]                         # mm, outer edge of the bike lane
X_LANE_OUT = P["bike_w"] + P["lane_w"]           # mm, outer edge of the nearest traffic lane
# Speeds (CBC-REQ-001 Table 2)
V_PED, V_BIKE, V_CAR = 1.5, 25 / 3.6, 50 / 3.6   # m/s, design maxima
V_PED_MEAN = 1.25
# Sensor (MLX90640 class, typical datasheet class values, to confirm)
SUBPAGE_HZ = 16.0                                # chess-mode subpages per second
FRAME_HZ = SUBPAGE_HZ / 2                        # full frames per second used by the tracker
NETD_1HZ = 0.10                                  # K rms at 1 Hz refresh
EDGE_NOISE = 1.25                                # noise factor at the edge of the wide lens (assumption)
K_SIGMA = 4.0                                    # single-frame detection threshold in noise units (assumption)
MIN_FRAMES = 4                                   # frames a track needs for class and direction (assumption)
I_ARRAY, V_HEAD = 23e-3, 3.3                     # A, V
I_ESP, I_ESP_LOW = 50e-3, 25e-3                  # A: ESP32-S3 at 240 MHz radio off (fallback, as TRL 2); at 80 MHz
I_STM_RUN = 5e-3                                 # A: STM32WL run mode at 48 MHz with I2C and DMA (baseline, CBC-DDR-002)
# Window: 0.5 mm HDPE film
N_HDPE, ALPHA_HDPE = 1.53, 4.0                   # refractive index; band-averaged absorption 8 to 14 um, 1/cm (assumption)
# People and privacy
A_PERSON = math.pi / 4 * 0.45 * 0.28             # m2, plan area of head and shoulders
STRADDLE = 0.5                                   # average share of a blob's signal in its brightest pixel
H_PERSON, H_TALL = 1.75, 2.0                     # m
DORI = {"monitor": 12.5, "detect": 25.0, "observe": 62.5, "recognize": 125.0, "identify": 250.0}   # px/m, IEC 62676-4
PLATE_W = 0.52                                   # m, EU plate width
Q_PED = 600.0                                    # people per hour per direction (R2)
BODY_DEPTH = 0.30                                # m, along the walking direction
# Energy (FieldNode values from FND-CAL-001 where shared)
ETA_RAIL, ETA_MPPT, ETA_CHG = 0.90, 0.85, 0.95
CORE_WH = 0.0040                                 # Wh/day, FieldNode core at 15 min (FND-CAL-001 [A1])
V_CELL, AH_CELL = 3.2, 6.0
USABLE, CAP_COLD, CAP_EOL = 0.80, 0.70, 0.80
PSH_WINTER, DERATE = 1.5, 0.60                   # h; street shade, dust and heat (CBC-REQ-001 R9)
V_CHG = 3.4                                      # V, cell voltage while charging
FND_ALLOW = (0.100, 0.115)                       # W, FieldNode sensor allowance (proposed, current)
# FieldNode hot clear day, 6 W panel (FND-CAL-001 [C3]): stored Wh without and with the proposed shield, of 25.5 possible
FND_HOT = {"no shield": 0.8, "shield": 13.1}
FND_HOT_POSSIBLE, FND_PANEL_W = 25.5, 6.0
# Radio (as FND-CAL-001)
PAYLOAD, OVERHEAD, BW, CR, NPRE = 10, 13, 125e3, 1, 8   # 10-byte record: six 12-bit counters and a status byte (CBC-DDR-002)
PAYLOAD_OLD = 14                                 # bytes, TRL 3 v0.1 record
EU_DC, TTN_S, US_DWELL = 0.01, 30.0, 0.400
US915_DR0_MAX = 11                               # bytes of application payload at US915 DR0 (SF10, 125 kHz)
# Wind and structure
RHO_AIR, V_GUST = 1.225, 35.0
CF_PANEL, CF_BOX, CF_SQUARE = 1.2, 1.3, 2.0
T_BAND, MU = 1000.0, 0.20                        # N preload per band (as FND-CAL-001), friction with rubber liner
FY_AL, E_AL = 150.0, 69e3                        # MPa, 6063-T6 class
RHO = {"al": 2.70e-6, "steel": 7.85e-6, "asa": 1.07e-6, "hdpe": 0.95e-6}   # kg/mm3
# Bought-part masses, kg (FieldNode core from FND-CAL-001 [F1] less its panel, bracket and mount)
M_FND_CORE = 0.43 + 0.08 + 0.15 + 0.03 + 0.05 + 0.02 + 0.06 + 0.06 + 0.03 + 0.01 + 0.10 + 0.02   # + connector strip (FND-DDR-003)
M_BOUGHT = {"6 W panel (FieldNode, 0.55 kg per FND-CAL-001)": 0.55, "four bands": 0.20,
            "thermal array breakout": 0.01, "M12 cable": 0.12, "hardware, lanyards": 0.25,
            "panel extension lead": 0.06, "rivet nuts, set screws, gland, ties, end cap": 0.07}
M_FALLBACK = 0.18 + 1.90 - 0.55 + 0.02           # kg added by the ESP32-S3 fallback: second cell, 20 W panel, processor board
PED_LIMIT = 8.0                                  # px/m at head height, restated R4 target (CBC-DDR-002)


# =============================================================== A. Geometry and coverage (R6)
def x_of(au):
    return ground_hit(ray(au, 0.0))[0]


def au_for_x(x_target):
    lo, hi = -P["fov"][0] / 2, P["fov"][0] / 2
    for _ in range(60):
        mid = (lo + hi) / 2
        if x_of(mid) < x_target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


x0, x1 = D["fp_x_min"], D["fp_x_max"]
out("A1", f"sensor window {P['window_z']:.0f} mm above the road at X = {P['head_x']:.0f} mm, view tilted {P['tilt']} deg toward the road; "
          f"array turned so its {P['fov'][0]:.0f} deg axis spans the street")
out("A2", f"footprint across the street {x0 / 1000:.2f} m to {x1 / 1000:.2f} m (width {(x1 - x0) / 1000:.2f} m); "
          f"design case needs {X_SW_BACK / 1000:.2f} m to {X_LANE_OUT / 1000:.2f} m")
need_back = math.degrees(math.atan((P["head_x"] - X_SW_BACK) / (P["window_z"] - P["sw_h"])))
need_front = math.degrees(math.atan((X_LANE_OUT - P["head_x"]) / P["window_z"]))
out("A3", f"design case spans {need_back:.1f} deg behind and {need_front:.1f} deg ahead of the vertical ({need_back + need_front:.1f} deg); "
          f"margins at the tilt used: {P['fov'][0] / 2 - (need_back + P['tilt']):.1f} deg (sidewalk) and "
          f"{P['fov'][0] / 2 - (need_front - P['tilt']):.1f} deg (lane)")
# TRL 2 orientation for comparison: 75 deg across, tilt 10 deg
Q = dict(P, fov=(75.0, 110.0), tilt=10.0, px=(24, 32))
fp_old = footprint_outline(Q)
x_old = min(q[0] for q in fp_old)
out("A4", f"TRL 2 orientation (75 deg across, 10 deg tilt): sidewalk covered to {x_old / 1000:.2f} m behind the curb, "
          f"{-x_old / -X_SW_BACK * 100:.0f} % of the 3 m sidewalk")


def along_length(x_mm):
    au = au_for_x(x_mm)
    a = ground_hit(ray(au, -P["fov"][1] / 2))
    b = ground_hit(ray(au, P["fov"][1] / 2))
    return (b[1] - a[1]) / 1000.0


L_SW_BACK, L_SW_MID, L_BIKE, L_LANE, L_NADIR = (along_length(X_SW_BACK + 50), along_length(X_SW_BACK / 2),
                                                 along_length(X_BIKE_OUT / 2), along_length(P["bike_w"] + P["lane_w"] / 2),
                                                 along_length(P["head_x"] + 1))
out("A5", f"footprint along the street: {L_NADIR:.2f} m below the head, {L_SW_MID:.2f} m at mid-sidewalk, {L_SW_BACK:.2f} m at the sidewalk back, "
          f"{L_BIKE:.2f} m at mid bike lane, {L_LANE:.2f} m at mid lane")
# Occlusion by the pole and the enclosure behind it
d_pole = (P["head_x"] - P["pole_x"]) / 1000
d_enc = (P["head_x"] - (D["enc_xc"])) / 1000
dist_back = (P["head_x"] - X_SW_BACK) / 1000
w_pole = P["pole_od"] / 1000 * dist_back / d_pole
w_enc = P["enc"][0] / 1000 * dist_back / d_enc
out("A6", f"shadow behind the pole at the sidewalk back: pole {w_pole:.2f} m wide, enclosure {w_enc:.2f} m wide, "
          f"{max(w_pole, w_enc) / L_SW_BACK * 100:.0f} % of the along-street field there; tracks must bridge it")
res("R6", f"Footprint {x0 / 1000:.2f} to {x1 / 1000:.2f} m across; margins {P['fov'][0] / 2 - (need_back + P['tilt']):.1f} deg; "
          f"shadow {max(w_pole, w_enc):.2f} m wide behind the pole",
    "3 m sidewalk, 2 m bike lane and nearest lane from one pole", "Met on paper (array turned 90 deg)")

# =============================================================== B. Pixel size and privacy (R4)
eu, ev = pixel_edges(P)


def pixel_size_at(x_mm, z_surface):
    au = au_for_x(x_mm)
    i = min(range(len(eu) - 1), key=lambda k: abs((eu[k] + eu[k + 1]) / 2 - au))
    a = ground_hit(ray(eu[i], 0.0)); b = ground_hit(ray(eu[i + 1], 0.0))
    j = len(ev) // 2
    c = ground_hit(ray(au, ev[j - 1])); d = ground_hit(ray(au, ev[j]))
    return abs(b[0] - a[0]) / 1000, abs(d[1] - c[1]) / 1000


px_nadir = pixel_size_at(P["head_x"] + 1, 0)
px_sw_near = pixel_size_at(-60, P["sw_h"])
px_sw_back = pixel_size_at(X_SW_BACK + 50, P["sw_h"])
px_lane = pixel_size_at(P["bike_w"] + P["lane_w"] / 2, 0)
out("B1", f"ground pixel (across x along): {px_nadir[0]:.3f} x {px_nadir[1]:.3f} m below the head; "
          f"{px_sw_near[0]:.3f} x {px_sw_near[1]:.3f} m at the curb edge of the sidewalk; "
          f"{px_sw_back[0]:.3f} x {px_sw_back[1]:.3f} m at the sidewalk back; {px_lane[0]:.3f} x {px_lane[1]:.3f} m at mid lane")
px_min = min(px_nadir + px_sw_near)
out("B1b", f"smallest ground pixel {px_min:.3f} m (along the street, near the head); TRL 2 quoted about 0.3 to 0.4 m")
dtheta_min = math.radians(min(P["fov"][0] / P["px"][0], P["fov"][1] / P["px"][1]))
r_head = (P["window_z"] - P["sw_h"]) / 1000 - H_PERSON
r_tall = (P["window_z"] - P["sw_h"]) / 1000 - H_TALL
ppm_head, ppm_tall = 1 / (r_head * dtheta_min), 1 / (r_tall * dtheta_min)
out("B2", f"resolution at head height: {ppm_head:.1f} px/m for a 1.75 m person directly below (range {r_head:.2f} m); "
          f"{ppm_tall:.1f} px/m for a 2.0 m person (range {r_tall:.2f} m); IEC 62676-4 levels: detect {DORI['detect']:.0f}, "
          f"recognize {DORI['recognize']:.0f}, identify {DORI['identify']:.0f} px/m")
r_plate = math.hypot((P["bike_w"] + P["lane_w"] / 2 - P["head_x"]) / 1000, P["window_z"] / 1000 - 0.5)
out("B3", f"number plate at mid lane, 0.5 m high: range {r_plate:.2f} m, {PLATE_W / (r_plate * dtheta_min):.1f} px across the plate")
res("R4", f"{ppm_head:.1f} px/m at head height for a 1.75 m person ({ppm_tall:.1f} for 2.0 m); detect needs {DORI['detect']:.0f}, identify {DORI['identify']:.0f}",
    f"{PED_LIMIT:.0f} px/m or less at head height (1.75 m person), below the IEC 62676-4 detection level of {DORI['detect']:.0f} px/m",
    "Met on paper" if ppm_head <= PED_LIMIT else "Not met")

# =============================================================== C. Detection and counting (R1, R2, R3)
frames = {"pedestrian, sidewalk back": (L_SW_BACK, V_PED), "pedestrian, mid-sidewalk": (L_SW_MID, V_PED),
          "cyclist, mid bike lane": (L_BIKE, V_BIKE), "car, mid lane": (L_LANE, V_CAR)}
fmin = 1e9
for k, (L, v) in frames.items():
    n = L / v * FRAME_HZ
    fmin = min(fmin, n)
    out("C1", f"{k}: {L:.2f} m of field at {v * 3.6:.0f} km/h = {L / v:.2f} s, {n:.1f} frames at {FRAME_HZ:.0f} Hz")
v_car_max = L_LANE * FRAME_HZ / MIN_FRAMES * 3.6
out("C2", f"fastest vehicle with {MIN_FRAMES} frames at mid lane: {v_car_max:.0f} km/h; smear in one {1 / SUBPAGE_HZ * 1000:.1f} ms subpage "
          f"at 50 km/h: {V_CAR / SUBPAGE_HZ:.2f} m ({V_CAR / SUBPAGE_HZ / px_lane[1]:.1f} px)")
res("R1", f"{fmin:.1f} frames minimum (car at 50 km/h); at least {MIN_FRAMES} assumed needed",
    "3 classes x 2 directions", "Met on paper" if fmin >= 1.5 * MIN_FRAMES else "At risk")
lam = Q_PED / 3600
d_merge = BODY_DEPTH + px_sw_back[1]
p_merge = 1 - math.exp(-lam * d_merge / V_PED_MEAN)
out("C3", f"random merging at {Q_PED:.0f} per hour per direction: a following walker within {d_merge:.2f} m ({BODY_DEPTH} m body plus one pixel) "
          f"for {p_merge * 100:.1f} % of people; side-by-side pairs merge unless the tracker splits blobs by area")
res("R2", f"Random merges alone {p_merge * 100:.1f} % undercount at 600/h; groups extra",
    "Within 10 % of manual counts per hour", "At risk (not verifiable at TRL 3)")
res("R3", f"{frames['car, mid lane'][0] / V_CAR * FRAME_HZ:.1f} frames per car; {V_CAR / SUBPAGE_HZ / px_lane[1]:.1f} px smear per subpage",
    "Within 15 % of manual counts per hour", "Not verifiable at TRL 3")

# =============================================================== D. Thermal contrast and window (R7)
R = ((N_HDPE - 1) / (N_HDPE + 1)) ** 2


def tau(d_mm):
    a = math.exp(-ALPHA_HDPE * d_mm / 10)
    return (1 - R) ** 2 * a / (1 - R ** 2 * a ** 2)


TAU = tau(P["window"][2])
out("D1", f"HDPE window transmission 8 to 14 um: {tau(0.25):.2f} (0.25 mm), {TAU:.2f} (0.5 mm), {tau(1.0):.2f} (1.0 mm); "
          f"surface reflection {R * 100:.1f} % per face")
netd = NETD_1HZ * math.sqrt(SUBPAGE_HZ) * EDGE_NOISE
a_px_back = px_sw_back[0] * px_sw_back[1]
f_back = min(1.0, A_PERSON / a_px_back) * STRADDLE
f_near = min(1.0, A_PERSON / (px_sw_near[0] * px_sw_near[1])) * STRADDLE
dt_min = K_SIGMA * netd / (f_back * TAU)
out("D2", f"noise {netd:.2f} K rms per pixel at {SUBPAGE_HZ:.0f} Hz subpages (edge of lens); person plan area {A_PERSON:.3f} m2; "
          f"pixel fill {f_back:.2f} at the sidewalk back, {f_near:.2f} near the pole")
out("D3", f"smallest person-to-pavement contrast for single-frame detection: {dt_min:.1f} K ({K_SIGMA:.0f} sigma); "
          f"{K_SIGMA * netd / (f_back * tau(0.25)):.1f} K with a 0.25 mm window; averaging 8 frames along a track could lower it to about "
          f"{dt_min / math.sqrt(8):.1f} K")


def air(h, tmin, tmax):
    return (tmin + tmax) / 2 + (tmax - tmin) / 2 * math.cos(2 * math.pi * (h - 15) / 24)


def sun(h):
    return max(0.0, math.sin(math.pi * (h - 6) / 13)) if 6 <= h <= 19 else 0.0


def blind_hours(tmin, tmax, sunlit=True, thr=dt_min):
    hrs = []
    for k in range(24 * 4):
        h = k / 4
        ta = air(h, tmin, tmax)
        pave = ta + (3 + 15 * sun(h) if sunlit else 1.0)
        person = ta + 0.5 * (34 - ta) + (5 * sun(h) if sunlit else 0.0)
        if abs(person - pave) < thr:
            hrs.append(h)
    return len(hrs) / 4, hrs


DAYS = {"hot (air 25 to 35 C)": (25, 35), "mild (air 10 to 20 C)": (10, 20), "cold (air -10 to 0 C)": (-10, 0)}
blind = {}
for name, (lo, hi) in DAYS.items():
    b_sun, hrs = blind_hours(lo, hi, True)
    b_sh, _ = blind_hours(lo, hi, False)
    b_avg, _ = blind_hours(lo, hi, True, dt_min / math.sqrt(8))
    blind[name] = (b_sun, b_sh, b_avg)
    out("D4", f"{name}: contrast below {dt_min:.1f} K for {b_sun:.1f} h on a sunlit sidewalk, {b_sh:.1f} h on a shaded one; "
              f"{b_avg:.1f} h (sunlit) if track averaging reaches {dt_min / math.sqrt(8):.1f} K")
hot = blind["hot (air 25 to 35 C)"]
mild = blind["mild (air 10 to 20 C)"]
out("D5", f"restated R7 (temperate sites, CBC-DDR-002): mild design day below contrast {mild[0]:.1f} h sunlit single-frame, "
          f"{mild[2]:.1f} h with track averaging, {mild[1]:.1f} h shaded; hot design day {hot[0]:.1f} h sunlit, {hot[1]:.1f} h shaded (hot sites use the radar variant)")
res("R7", f"Mild design day: {mild[0]:.1f} h sunlit below single-frame contrast, {mild[2]:.1f} h with track averaging, {mild[1]:.1f} h shaded",
    "-20 to +50 C survival; counting at temperate sites (air up to 20 C); hot sites use the radar variant",
    "At risk (sunlit sidewalks need track averaging)" if mild[2] > 0 else "Met on paper")

# =============================================================== E. Energy (R8, R9): baseline, tracking on the STM32WL (CBC-DDR-002)
p_array = I_ARRAY * V_HEAD
p_stm = I_STM_RUN * V_HEAD
p_head = p_array + p_stm                         # delivered on FieldNode's switched sensor rail and core
draw = p_head * 24 / ETA_RAIL + CORE_WH
out("E1", f"baseline load: array {p_array * 1000:.0f} mW, STM32WL tracking {p_stm * 1000:.1f} mW, total {p_head * 1000:.0f} mW delivered; "
          f"{draw:.2f} Wh/day drawn from the cell ({draw / 24 * 1000:.0f} mW average) with {ETA_RAIL * 100:.0f} % rail efficiency and a "
          f"{CORE_WH * 1000:.1f} mWh/day core; FieldNode sensor allowance {FND_ALLOW[1] * 1000:.0f} mW current, {FND_ALLOW[0] * 1000:.0f} mW proposed "
          f"({p_head / FND_ALLOW[0] * 100:.0f} % of the proposed)")
p_esp = I_ESP * V_HEAD
p_head_esp = p_array + p_esp
draw_esp = p_head_esp * 24 / ETA_RAIL + CORE_WH
out("E1b", f"ESP32-S3 fallback: {p_head_esp * 1000:.0f} mW delivered, {draw_esp:.2f} Wh/day ({draw_esp / 24 * 1000:.0f} mW average), "
           f"{p_head_esp / FND_ALLOW[1]:.1f} times FieldNode's 115 mW allowance")
e_cell = V_CELL * AH_CELL
usable1, usable2 = e_cell * USABLE, 2 * e_cell * USABLE
auto1 = usable1 / draw
out("E2", f"one cell {e_cell:.1f} Wh, {usable1:.1f} Wh usable: {auto1:.2f} days without sun; {auto1 * CAP_COLD:.2f} days at -20 C; "
          f"{auto1 * CAP_EOL:.2f} days at end of life (fallback on two cells: {usable2 / draw_esp:.2f} days)")
res("R8", f"{auto1:.2f} d (one cell); {auto1 * CAP_COLD:.2f} d at -20 C; {auto1 * CAP_EOL:.2f} d at end of life",
    "3 days of continuous counting", "Met on paper (one cell)")


def stored(panel_w, psh=PSH_WINTER, derate=DERATE):
    return panel_w * psh * derate * ETA_MPPT * ETA_CHG


for w in (6, 10, 20):
    s_ = stored(w)
    surplus = s_ - draw
    refill = (3 * draw) / surplus if surplus > 0 else float("inf")
    out("E3", f"{w:>2} W panel, winter: {s_:.1f} Wh/day stored against {draw:.2f} drawn ({s_ / draw:.2f} times); "
              + (f"refill after 3 sunless days {refill:.1f} days" if surplus > 0 else "not energy neutral"))
w_min = draw / (PSH_WINTER * DERATE * ETA_MPPT * ETA_CHG)
s6 = stored(6)
out("E4", f"smallest energy-neutral panel {w_min:.1f} W; 6 W gives {s6:.1f} Wh/day, {s6 / draw:.2f} times the draw; "
          f"fallback needs {draw_esp / (PSH_WINTER * DERATE * ETA_MPPT * ETA_CHG):.1f} W (20 W panel)")
res("R9", f"{s6:.1f} Wh/day stored against {draw:.2f} Wh/day (6 W)",
    "Energy neutral at 1.5 peak sun hours, 40 % derating", "Met on paper (6 W)")
i_chg = 6 * ETA_MPPT / V_CHG
out("E5", f"peak charge current at 1,000 W/m2 with the 6 W panel: {i_chg:.1f} A ({i_chg / AH_CELL:.2f} C for one cell), FieldNode's standard "
          f"charger setting; the fallback's 20 W panel would push {20 * ETA_MPPT / V_CHG:.1f} A")
for k, v in FND_HOT.items():
    frac = v / FND_HOT_POSSIBLE
    net = v - draw
    txt = f"net {net:+.1f} Wh/day" + (f"; from full the cell lasts {usable1 / -net:.1f} days" if net < 0 else "")
    out("E6", f"hot clear day, {k} (FieldNode 6 W figures, FND-CAL-001 [C3], charge-window share {frac * 100:.0f} %): "
              f"{v:.1f} Wh stored against {draw:.2f} drawn, {txt}")

# =============================================================== F. Tracking on the STM32WL (baseline, CBC-DDR-002)
bits_per_subpage = 832 * 2 * 9 + 60
for f_i2c in (400e3, 1e6):
    t = bits_per_subpage / f_i2c
    out("F1", f"I2C at {f_i2c / 1e3:.0f} kHz: {t * 1000:.1f} ms per subpage, bus busy {t * SUBPAGE_HZ * 100:.0f} % at {SUBPAGE_HZ:.0f} Hz")
c_bus = 2.0 * 100e-12 + 20e-12                   # 2 m M12 cable (BOM line 11) at 100 pF/m, plus devices
for f_i2c, tr in ((400e3, 300e-9), (1e6, 120e-9)):
    r_max = tr / (0.8473 * c_bus)
    out("F2", f"bus over the 2 m M12 cable, {c_bus * 1e12:.0f} pF: pull-up up to {r_max:.0f} ohm at {f_i2c / 1e3:.0f} kHz, "
              f"{V_HEAD / r_max * 1000:.1f} mA sink current")
for cyc, label in ((2000, "reference floating-point conversion, low"), (4000, "reference floating-point conversion, high"),
                   (150, "fixed-point pipeline on raw data")):
    share = 768 * cyc * FRAME_HZ / 48e6
    out("F3", f"{label}: {cyc} cycles per pixel, {share * 100:.0f} % of a 48 MHz core without FPU at {FRAME_HZ:.0f} frames/s")
ram = {"calibration parameters": 768 * 12, "two frame buffers": 2 * 1664, "background (int16)": 768 * 2,
       "labels and tracks": 768 + 1024, "LoRaWAN stack and FieldNode firmware (estimate)": 28 * 1024}
out("F4", f"RAM estimate {sum(ram.values()) / 1024:.0f} kB of 64 kB (" + ", ".join(f"{k} {v / 1024:.1f} kB" for k, v in ram.items()) + ")")
out("F5", f"change from CBC-CAL-001 v0.1 (ESP32-S3 baseline): {p_head_esp * 1000:.0f} to {p_head * 1000:.0f} mW at the head, "
          f"{draw_esp:.2f} to {draw:.2f} Wh/day; two cells and 20 W to one cell and 6 W")

# =============================================================== G. Radio (R5, R15)


def toa(sf, pl, bw=BW):
    de = 1 if (sf >= 11 and bw == 125e3) else 0
    ts = 2 ** sf / bw
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (CR + 4), 0)
    return (NPRE + 4.25) * ts + n * ts


ups = 96
for sf in (7, 9, 10, 12):
    t = toa(sf, PAYLOAD + OVERHEAD)
    out("G1", f"SF{sf}: {t * 1000:.1f} ms per {PAYLOAD}-byte uplink, {t * ups:.1f} s/day, {t * 4:.2f} s/h (EU868 limit {EU_DC * 3600:.0f} s/h; "
              f"TTN {TTN_S:.0f} s/day)")
t9 = toa(9, PAYLOAD + OVERHEAD)
t10p = toa(10, PAYLOAD + OVERHEAD)
fits = PAYLOAD <= US915_DR0_MAX and t10p <= US_DWELL
out("G2", f"US915: SF9 uplink {t9 * 1000:.0f} ms against the {US_DWELL * 1000:.0f} ms dwell limit; at DR0 (SF10) the payload limit is "
          f"{US915_DR0_MAX} bytes; the {PAYLOAD}-byte record (six 12-bit counters plus a status byte) takes {t10p * 1000:.0f} ms at SF10, "
          f"{'within' if fits else 'outside'} both limits (the {PAYLOAD_OLD}-byte v0.1 record did not fit)")
out("G3", f"data: {PAYLOAD} bytes x {ups} = {PAYLOAD * ups / 1000:.2f} kB/day; frames {768 * 2 * FRAME_HZ / 1000:.1f} kB/s "
          f"({768 * 2 * FRAME_HZ * 86400 / 1e9:.2f} GB/day) stay in RAM")
res("R5", f"{PAYLOAD} bytes per 15 min bin, six 12-bit counters and a status byte", "15-minute counts per class and direction, open format", "Met by design")
res("R15", f"{t9 * 4:.2f} s/h at SF9 (limit {EU_DC * 3600:.0f} s/h); {t10p * 1000:.0f} ms at US915 DR0 against 400 ms dwell; {PAYLOAD} of {US915_DR0_MAX} bytes",
    "EU868 1 % duty cycle and US915 dwell limits", "Met on paper" if fits else "At risk (US915 DR0 payload)")

# =============================================================== H. Wind, mounting and mass (R11, R12)
q = 0.5 * RHO_AIR * V_GUST ** 2
F_panel = q * CF_PANEL * D["panel_area_m2"]
pc = D["panel_c"]
lever = math.hypot(pc[2] - D["cap_top"], pc[0] - P["pole_x"]) / 1000
M_post = F_panel * lever
po, pw_, _ = P["post"]
Z_post = math.pi * (po ** 4 - (po - 2 * pw_) ** 4) / (32 * po)
s_post = M_post * 1000 / Z_post
out("H1", f"gust pressure {q:.0f} Pa; panel {D['panel_area_m2']:.3f} m2, {F_panel:.0f} N normal to the panel; lever to the post base {lever:.3f} m, "
          f"moment {M_post:.0f} N m; post {po} x {pw_} aluminium stress {s_post:.0f} MPa against {FY_AL:.0f} (factor {FY_AL / s_post:.0f})")
sl = P["sleeve"][0]
F_bear = M_post / (0.8 * sl / 1000) + F_panel
out("H2", f"sleeve over the pole top, {sl:.0f} mm long: bearing couple about {F_bear:.0f} N on the pole top; the pole itself carries "
          f"{F_panel:.0f} N at {pc[2] / 1000:.1f} m, {F_panel * pc[2] / 1000:.0f} N m at its base, for the pole owner to check")
a_arm = P["arm"][0] / 1000 * D["arm_len"] / 1000
F_arm = q * CF_SQUARE * a_arm
a_head = (P["head"][0] * P["head"][2] + P["hood"][0] * P["hood"][2]) / 1e6
F_head = q * CF_BOX * a_head
r_arm = (D["arm_x0"] + D["arm_len"] / 2 - P["pole_x"]) / 1000
r_head_ = D["reach"] / 1000
T_twist = F_arm * r_arm + F_head * r_head_
T_cap = MU * 2 * (2 * T_BAND) * D["pole_r"] / 1000
out("H3", f"wind along the street: arm {F_arm:.0f} N, head {F_head:.0f} N; twist about the pole {T_twist:.1f} N m against saddle friction "
          f"{T_cap:.1f} N m from two bands (factor {T_cap / T_twist:.1f})")
a_, t_ = P["arm"]
I_arm = (a_ ** 4 - (a_ - 2 * t_) ** 4) / 12
M_arm = F_arm * D["arm_len"] / 2000 + F_head * D["arm_len"] / 1000
s_arm = M_arm * 1000 / (I_arm / (a_ / 2))
defl = F_head * D["arm_len"] ** 3 / (3 * E_AL * I_arm) + F_arm * D["arm_len"] ** 3 / (8 * E_AL * I_arm)
out("H4", f"arm 40 x 40 x 2: bending {s_arm:.1f} MPa against {FY_AL:.0f}; tip deflection {defl:.2f} mm, "
          f"{math.degrees(defl / D['arm_len']):.3f} deg of aim")
COMP = build_components(P)
vol = lambda *ks: sum(COMP[k].shape.volume for k in ks)  # noqa: E731
m_made = {"sensor arm, saddle plate, V-saddles, brackets (Al)": vol("arm_tube", "arm_plate", "arm_vs_up", "arm_vs_low", "arm_brk_up", "arm_brk_low") * RHO["al"],
          "pole-top mount (Al)": vol("sleeve", "disc", "post", "plugs", "lclip_r", "lclip_l", "uclip_r", "uclip_l", "rail") * RHO["al"],
          "enclosure saddle plate and V-saddles (Al)": vol("enc_plate", "enc_vs_up", "enc_vs_low") * RHO["al"],
          "head housing, hood, wedge pad and window frame (ASA)": vol("housing", "frame") * RHO["asa"], "notice plate (Al)": vol("notice") * RHO["al"]}
m_total = M_FND_CORE + sum(M_BOUGHT.values()) + sum(m_made.values())
out("H5", f"mass: FieldNode core {M_FND_CORE:.2f} kg; " + ", ".join(f"{k} {v:.2f}" for k, v in m_made.items())
          + "; bought " + ", ".join(f"{k} {v:.2f}" for k, v in M_BOUGHT.items()) + f"; total {m_total:.2f} kg (ESP32-S3 fallback about {m_total + M_FALLBACK:.2f} kg)")
res("R11", f"{m_total:.2f} kg", "6 kg or less", "Met on paper" if m_total <= 5.4 else ("At risk (within the 5 % uncertainty of the assumed masses)" if m_total <= 6.3 else "Not met"))
tasks = [("Fit panel to the pole-top mount on the ground", 5), ("Raise, fit sleeve on the pole top, set screws, lanyard", 12),
         ("Band the enclosure saddle plate, FieldNode core already on it", 8), ("Band the arm saddle plate, head already on the arm, level the arm", 8),
         ("Head lanyard, route and tie the sensor cable and panel lead", 10), ("Aim check on a laptop through the calibration jumper", 8),
         ("Close up, confirm an uplink on a phone", 5), ("Fit the public notice plate", 3)]
t_inst = sum(t for _, t in tasks)
out("H6", "install (two people, mobile platform): " + "; ".join(f"{k} {t} min" for k, t in tasks) + f"; total {t_inst} min")
res("R12", f"Install estimate {t_inst} min; panel {F_panel:.0f} N, post factor {FY_AL / s_post:.0f}, twist factor {T_cap / T_twist:.1f}",
    "Two people, 60 min, no drilling; 35 m/s gusts", "Not verifiable at TRL 3 (wind and fit met on paper)")

# =============================================================== I. Service life, sealing (R10, R14)
night_h = 16
dod = draw / 24 * night_h / e_cell
cycles = 5 * 365
out("I1", f"winter night of {night_h} h: depth of discharge {dod * 100:.0f} % of one cell; {cycles} cycles in 5 years")
res("R10", "IP65 enclosure (FieldNode), gasketed head with film window", "IP65", "Not verifiable at TRL 3")
res("R14", f"Nightly depth of discharge {dod * 100:.0f} %; window UV and cell heat unknown", "5 years, one battery change", "Not verifiable at TRL 3")

# =============================================================== J. Cost (R13)
import yaml  # noqa: E402
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
priced = all(r["unit_cost_usd"].strip() for r in rows)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
out("J1", f"BOM {len(rows)} lines, all priced: {priced}; total ${total:.2f} against budget_usd ${budget:.0f} "
          + (f"(margin ${budget - total:.2f})" if total <= budget else f"(over by ${total - budget:.2f})"))
fallback_add = 12.0 + 9.0 + (30.0 - 14.0)
out("J2", f"ESP32-S3 fallback (processor $12, second cell $9, 20 W panel $30 in place of $14): about ${total + fallback_add:.2f}")
res("R13", f"${total:.2f}", f"${budget:.0f} or less (budget_usd)", "Met on paper" if total <= budget else "Not met")

# =============================================================== L. Requirement status table
order = [f"R{i}" for i in range(1, 16)]
RESULTS.sort(key=lambda r: order.index(r[0]))
print("\n[L] Requirement status")
counts = {}
for rid, val, tgt, st in RESULTS:
    print(f"  {rid:<4} | {st:<45} | {val}")
    key = st.split(" (")[0]
    counts[key] = counts.get(key, 0) + 1
print("  counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(RESULTS)
