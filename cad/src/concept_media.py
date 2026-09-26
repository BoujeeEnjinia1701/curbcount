"""CurbCount concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the counter's parts from cad/src/model.py (PARAMS) and renders the media set with
.kit/concept.py. Every colored part carries the BOM line number used in bom/bom.csv; grey parts
(street pole, sidewalk and road, sensing footprint, person) are context with no BOM number.
Figures on the sheet and in the flow diagram come from docs/04-calcs/sizing.py (CBC-CAL-001).
CONCEPT, NOT FOR FABRICATION.

Coordinates in mm as in model.py: road at Z = 0, curb face at X = 0, sidewalk at X < 0, street along Y.
"""
import math
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
from model import PARAMS as P, BOM, build_parts, context_parts, derived  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

D = derived(P)
m = build_parts(P)
c = context_parts(P)

# Exploded offsets in screen terms for the kit's default isometric camera (elevation 24 deg, azimuth -58 deg):
# sx to the right, sy up, t toward the viewer (mm). The camera looks from the road side.
_e, _a = math.radians(24), math.radians(-58)
CAM = (math.cos(_e) * math.cos(_a), math.cos(_e) * math.sin(_a), math.sin(_e))
_r = math.hypot(CAM[0], CAM[1])
RIGHT = (-CAM[1] / _r, CAM[0] / _r, 0.0)
UP = (-RIGHT[1] * CAM[2], RIGHT[0] * CAM[2], RIGHT[1] * CAM[0] - RIGHT[0] * CAM[1])


def scr(sx, sy, t=0.0, dz=0.0):
    return tuple(sx * RIGHT[i] + sy * UP[i] + t * CAM[i] + (dz if i == 2 else 0.0) for i in range(3))


STYLE = {  # key: (color, exploded offset in world mm)
    "enclosure": ("#E5E7EB", scr(-380, 0, 250)),
    "board": ("#16A34A", scr(-700, 120, 350)),
    "cells": ("#C2410C", scr(-700, -200, 350)),
    "panel": ("#1E3A8A", scr(-150, -250, 0, dz=0)),
    "mount": ("#6B7280", scr(0, -80, 0)),
    "clamps": ("#94A3B8", scr(-120, 0, 500)),
    "arm": ("#A16207", scr(120, 80, 0)),
    "housing": ("#0F766E", scr(420, 260, 0)),
    "window": ("#FDE68A", scr(420, -280, 0)),
    "array": ("#7C3AED", scr(650, -150, 0)),
    "cable": ("#111827", scr(200, -350, 250)),
    "notice": ("#F59E0B", scr(-620, -60, 0, dz=1000)),
}
parts = []
for key, (num, name) in BOM.items():
    color, off = STYLE[key]
    parts.append(Part(name, m[key], color, num, off))

person = human_figure(1750.0, x=-1700.0, y=-1500.0, z=P["sw_h"])
person.name = "Person, 1.75 m"
context = [
    Part("Street pole, 114 mm, 5 m", c["pole"], "#9CA3AF"),
    Part("Sidewalk, bike lane and road", c["street"], "#B8BDC4"),
    Part("Sensing footprint (CBC-CAL-001)", c["footprint"], "#99D5CC"),
    person,
]

# Shift everything so the counter sits near the origin (the kit's cutaway cutter is sized from the parts
# and centered on Z = 0, so a counter left at 4 m would not be cut).
SHIFT = Pos(-P["pole_x"], 0, -P["enc_zc"])
for _p in parts + context:
    _p.shape = SHIFT * _p.shape


def data_and_energy_flow(out):
    """Two-row flow: data (what leaves the device) and winter daily energy (CBC-CAL-001, estimates)."""
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
    row(0.2, [("Thermal array", "32 x 24 px, 8 frames/s\nabout 12 kB/s in RAM"),
              ("Tracker on the STM32WL", "blobs, tracks, class\nand direction"),
              ("15 min count bins", "3 classes x 2 directions\n10 bytes per bin"),
              ("LoRaWAN uplink", "96 uplinks/day, 0.96 kB/day\n0.21 s each at SF9"),
              ("TwinKit or city server", "counts and device\nhealth only")],
        [7, 4, 1.5, 1.5])
    branch(0, 0.2, "Frames overwritten in RAM\nabout 1 GB/day, never stored or sent")
    branch(1, 0.2, "Track data deleted\nafter each count")

    ax.text(0.15, -2.55, "Winter energy per day (estimates, CBC-CAL-001; 0.10 W average from the cell)", fontsize=9.5,
            fontweight="bold", color=INK)
    row(-3.6, [("6 W panel (FieldNode)", "9 Wh/day nominal\nat 1.5 sun hours"),
               ("MPPT charger", "5.4 Wh/day in\n4.6 Wh/day out"),
               ("LiFePO4 cell, 6 Ah", "4.4 Wh/day stored\n15.4 Wh usable, 6.2 days"),
               ("Counter load", "2.5 Wh/day\narray 82 %, tracking 18 %")],
        [7, 4.5, 3])
    branch(0, -3.6, "Street shade, dust, heat\n40 % derating, 3.6 Wh")
    branch(1, -3.6, "Charger 15 %, 0.8 Wh\ncharging 5 %, 0.2 Wh")
    branch(2, -3.6, "Winter surplus 1.9 Wh/day\n(refills 3 dark days in 3.9 days)")

    fig.text(0.01, 0.97, "CurbCount: data and energy flow", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.93, "CONCEPT, NOT FOR FABRICATION. Values are estimates from CBC-CAL-001.",
             fontsize=6.5, color="#B45309", va="top")
    fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    concept.ROOT = ROOT
    render_all(
        parts, project="CurbCount", title="Privacy-safe street counter concept", dwg_no="CBC-DWG-010", rev="P3",
        key_figures=["Thermal array 32 x 24 px, 110 deg across the street",
                     f"Footprint {D['fp_x_min'] / 1000:.1f} to {D['fp_x_max'] / 1000:.1f} m across, 6 to 7 m along",
                     "Counts people, bikes, vehicles; 15 min bins",
                     "No images leave the device; 7.6 px/m at head height",
                     "0.10 W from the cell; 6.2 days without sun",
                     "Parts $253 vs $275 budget (indicative)"],
        date="2026-09-25",
        scale_figure=False, context=context,
        cut_exclude=["Solar panel, 6 W", "Panel pole-top mount", "Band clamps (4), enclosure saddle",
                     "Sensor cable, M12", "Public notice plate"],
    )
    data_and_energy_flow(ROOT / "media" / "flow.png")
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
