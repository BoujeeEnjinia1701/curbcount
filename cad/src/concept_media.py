"""CurbCount concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Road surface at Z = 0, curb face at X = 0, sidewalk at X < 0 (top at Z = 150),
street running along Y. The street pole stands 450 mm behind the curb. The counter is a FieldNode
core on the back of the pole, a 20 W panel on top, and a thermal sensor head on a short arm that
looks down over the sidewalk, bike lane and nearest traffic lane.
Street, pole, person and sensing footprint are grey context shown only in the hero and blueprint
isometric; they carry no BOM number.
"""
import math
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
import concept
from concept import Part, render_all, human_figure

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------- street context ----------------
SW = 150.0            # sidewalk top above road
POLE_X, POLE_R = -450.0, 57.0   # 114 mm (4.5 in) steel street pole
POLE_TOP = SW + 5000.0
HEAD_Z = 4300.0       # sensor window height above the road (about 4.15 m above the sidewalk)
ARM_Z = HEAD_Z + 95.0
ENC_Z = 3900.0        # FieldNode enclosure center height


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def band(z, r_in=POLE_R + 1, w=30.0):
    return Pos(POLE_X, 0, z) * (Cylinder(r_in + 4, w) - Cylinder(r_in, w + 2))


sidewalk = Pos(-1500, 0, SW / 2) * Box(3000, 5000, SW)
road = Pos(2750, 0, -30) * Box(5500, 5000, 60)
stripe = Pos(1800, 0, 1) * Box(100, 5000, 2)              # bike lane line
pole = Pos(POLE_X, 0, SW + 2500) * Cylinder(POLE_R, 5000)
street = sidewalk + road + stripe

# Sensing footprint on the ground (estimate): 75 deg across the street, 110 deg along it,
# window at 4.3 m, tilted 10 deg toward the road. Along-street extent clipped to the scene.
FP_X0, FP_X1 = -2060.0, 4800.0
footprint = (Pos((FP_X0 + 0) / 2, 0, SW + 1) * Box(0 - FP_X0, 4400, 2)
             + Pos(FP_X1 / 2, 0, 1.5) * Box(FP_X1, 4400, 3))

person = human_figure(1750.0, x=-1700.0, y=-1500.0, z=SW)
person.name = "Person, 1.75 m"

# ---------------- CurbCount parts ----------------
# 1 FieldNode enclosure (IP65 polycarbonate, about 180 x 130 x 250 mm), on the back of the pole
ENC_W, ENC_D, ENC_H, WALL = 180.0, 130.0, 250.0, 4.0
enc_x = POLE_X - POLE_R - 12 - ENC_D / 2
enclosure = (Pos(enc_x, 0, ENC_Z) * (Box(ENC_D, ENC_W, ENC_H) - Box(ENC_D - 2 * WALL, ENC_W - 2 * WALL, ENC_H - 2 * WALL))
             + Pos(enc_x + ENC_D / 2 + 6, 0, ENC_Z) * Box(12, 60, ENC_H - 40))          # mounting rail to the clamps

# 2 FieldNode power and radio board (MPPT charger, STM32WL LoRaWAN), on the enclosure back plate
board = Pos(enc_x + ENC_D / 2 - WALL - 8, 0, ENC_Z + 30) * Box(10, 150, 150)
radio_ant = Pos(enc_x, 0, ENC_Z + ENC_H / 2 + 60) * Cylinder(8, 120)

# 3 Two LiFePO4 cells, 6 Ah (32700 size, 32 mm x 70 mm), lying in the enclosure base
cells = (Pos(enc_x - 15, -25, ENC_Z - 80) * Rot(90, 0, 0) * Cylinder(16, 70)
         + Pos(enc_x - 15 + 36, -25, ENC_Z - 80) * Rot(90, 0, 0) * Cylinder(16, 70))

# 4 Solar panel, 20 W, about 540 x 350 x 25 mm, on top of the pole, tilted 35 deg facing away from the road
PANEL_Z = POLE_TOP + 180
panel = Pos(POLE_X - 90, 0, PANEL_Z) * Rot(0, -35, 0) * Box(350, 540, 25)

# 5 Panel tilt bracket: pole-top cap, post and hinge plate
bracket = (Pos(POLE_X, 0, POLE_TOP + 10) * Cylinder(POLE_R + 6, 20)
           + Pos(POLE_X, 0, POLE_TOP + 70) * Cylinder(20, 110)
           + Pos(POLE_X - 20, 0, PANEL_Z - 45) * Rot(0, -35, 0) * Box(160, 200, 10))

# 6 Stainless band clamps (4): two for the enclosure, one for the arm, one for the bracket
clamps = band(ENC_Z - 80) + band(ENC_Z + 80) + band(ARM_Z) + band(POLE_TOP - 40)

# 7 Sensor arm: 40 x 40 mm aluminium tube from the pole toward the road, with a saddle plate
ARM_X1 = 60.0
arm = (Pos((POLE_X + POLE_R + ARM_X1) / 2, 0, ARM_Z) * Box(ARM_X1 - POLE_X - POLE_R, 40, 40)
       + Pos(POLE_X + POLE_R + 4, 0, ARM_Z) * Box(8, 90, 120))

# 8 to 11 Sensor head under the arm end, tilted 10 deg toward the road
HEAD = Pos(ARM_X1 + 20, 0, HEAD_Z) * Rot(0, 10, 0)
head_shell = HEAD * (Box(110, 90, 70) - Pos(0, 0, -4) * Box(102, 82, 70))       # open underneath for the window
hood = HEAD * Pos(10, 0, 40) * Box(150, 120, 6)
housing = head_shell + hood
window = HEAD * Pos(0, 0, -33) * Box(100, 80, 1.5)
sensor = HEAD * (Pos(0, 0, -18) * Cylinder(4.7, 12) + Pos(0, 0, -8) * Box(26, 26, 2))   # TO39 can on a small board
esp = HEAD * Pos(0, 0, 14) * Box(70, 50, 8)

# 12 Sensor cable: enclosure gland, up the pole, along the arm, into the head
cy = -POLE_R - 8
cable = (tube3((enc_x + 20, -40, ENC_Z + ENC_H / 2 - 20), (POLE_X, cy, ENC_Z + ENC_H / 2 + 30), 4)
         + tube3((POLE_X, cy, ENC_Z + ENC_H / 2 + 30), (POLE_X, cy, ARM_Z - 30), 4)
         + tube3((POLE_X, cy, ARM_Z - 30), (POLE_X + POLE_R + 20, -28, ARM_Z - 30), 4)
         + tube3((POLE_X + POLE_R + 20, -28, ARM_Z - 30), (ARM_X1 - 20, -28, ARM_Z - 30), 4))

parts = [
    Part("FieldNode enclosure, IP65", enclosure, "#E5E7EB", 1, (-260, 0, 0)),
    Part("FieldNode power and radio board", board + radio_ant, "#16A34A", 2, (-560, 0, 120)),
    Part("LiFePO4 cells, 2 x 6 Ah", cells, "#C2410C", 3, (-420, 0, -220)),
    Part("Solar panel, 20 W", panel, "#1E3A8A", 4, (-250, 0, 320)),
    Part("Panel tilt bracket", bracket, "#6B7280", 5, (0, 0, 120)),
    Part("Stainless band clamps (4)", clamps, "#94A3B8", 6, (0, -330, 0)),
    Part("Sensor arm, aluminium", arm, "#A16207", 7, (0, 0, 60)),
    Part("Sensor head housing and sun hood", housing, "#0F766E", 8, (260, 0, 150)),
    Part("LWIR window, 0.5 mm HDPE", window, "#FDE68A", 9, (260, 0, -300)),
    Part("Thermal array, 32 x 24 px", sensor, "#7C3AED", 10, (560, 0, -120)),
    Part("Edge processor, ESP32-S3", esp, "#2563EB", 11, (400, 0, 60)),
    Part("Sensor cable, M12", cable, "#111827", 12, (0, -300, -120)),
]

context = [
    Part("Street pole, 5 m", pole, "#9CA3AF"),
    Part("Sidewalk and road", street, "#B8BDC4"),
    Part("Sensing footprint (estimate)", footprint, "#99D5CC"),
    person,
]

# Shift everything so the counter sits near the origin (the kit's cutaway cutter is centered on Z = 0).
SHIFT = Pos(-POLE_X, 0, -ENC_Z)
for _p in parts + context:
    _p.shape = SHIFT * _p.shape


def data_and_energy_flow(out):
    """Two-row flow: data (what leaves the device) and daily energy (estimates)."""
    INK, ACCENT, LOSS = "#111827", "#0F766E", "#C2410C"
    fig, ax = plt.subplots(figsize=(15, 6.2), dpi=160)
    ax.set_xlim(0, 15); ax.set_ylim(-6.3, 1.6); ax.set_axis_off()

    def row(y, stages, lw):
        for i, (name, val) in enumerate(stages):
            x = i * 3 + 0.3
            ax.add_patch(FancyBboxPatch((x - 0.15, y - 0.55), 2.4, 1.3, boxstyle="round,pad=0.02,rounding_size=0.12",
                                        fc="#F0FDFA", ec=ACCENT, lw=1.4))
            ax.text(x + 1.05, y + 0.35, name, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK)
            ax.text(x + 1.05, y - 0.15, val, ha="center", va="center", fontsize=8, color=ACCENT, linespacing=1.3)
            if i < len(stages) - 1:
                ax.add_patch(FancyArrowPatch((x + 2.3, y + 0.1), (x + 2.8, y + 0.1), arrowstyle="-|>",
                                             mutation_scale=14, lw=lw[i], color=ACCENT, alpha=0.6))

    def branch(i, y, text):
        x = i * 3 + 0.3 + 1.05
        ax.add_patch(FancyArrowPatch((x, y - 0.6), (x, y - 1.35), arrowstyle="-|>", mutation_scale=12,
                                     lw=2.5, color=LOSS, alpha=0.6))
        ax.text(x, y - 1.7, text, ha="center", va="center", fontsize=8, color=LOSS, linespacing=1.3)

    ax.text(0.15, 1.25, "Data: counts leave the device, images never do", fontsize=9.5, fontweight="bold", color=INK)
    row(0.2, [("Thermal array", "32 x 24 px at 8 Hz\nabout 12 kB/s in RAM"),
              ("Edge tracker", "blobs, tracks, class\nand direction"),
              ("15 min count bins", "3 classes x 2 directions\n14 bytes per bin"),
              ("LoRaWAN uplink", "96 uplinks/day\nabout 1.3 kB/day"),
              ("TwinKit or city server", "counts and device\nhealth only")],
        [7, 4, 1.5, 1.5])
    branch(0, 0.2, "Frames overwritten in RAM\nabout 1 GB/day, never stored or sent")
    branch(1, 0.2, "Track data deleted\nafter each count")

    ax.text(0.15, -2.55, "Energy per day (estimates, 0.30 W continuous load)", fontsize=9.5, fontweight="bold", color=INK)
    row(-3.6, [("20 W panel", "about 30 Wh/day nominal\nat 1.5 sun hours (winter)"),
               ("MPPT charger", "about 18 Wh/day in\nabout 16 Wh/day out"),
               ("LiFePO4 cells", "38 Wh, about 31 Wh usable\nabout 4 days in the dark"),
               ("Node load", "about 7.2 Wh/day\nprocessor 55 %, array 25 %")],
        [7, 4.5, 3])
    branch(0, -3.6, "Heat, dust, street shade\nabout 40 % derating")
    branch(1, -3.6, "Charger loss\nabout 10 %")
    branch(2, -3.6, "Winter surplus about 9 Wh/day\n(cells full, charger throttles)")

    fig.text(0.01, 0.97, "CurbCount: data and energy flow", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.93, "CONCEPT, NOT FOR FABRICATION. Values are estimates to be checked at TRL 3.",
             fontsize=6.5, color="#B45309", va="top")
    fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    concept.ROOT = ROOT
    render_all(
        parts, project="CurbCount", title="Privacy-safe street counter concept", dwg_no="CBC-DWG-010",
        key_figures=["Thermal array 32 x 24 px, 110 x 75 deg, at 4.3 m",
                     "Footprint about 12 m along x 7 m across (estimate)",
                     "Counts people, bikes, vehicles; 15 min bins",
                     "No images leave the device; counts only",
                     "About 0.30 W; about 4 days without sun (est.)",
                     "Parts about $271 vs $150 budget (indicative)"],
        date="2026-09-25",
        scale_figure=False, context=context,
        cut_exclude=["Solar panel, 20 W", "Panel tilt bracket", "Stainless band clamps (4)", "Sensor cable, M12"],
    )
    data_and_energy_flow(ROOT / "media" / "flow.png")
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
