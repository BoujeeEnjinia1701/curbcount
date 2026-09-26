"""CurbCount parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    curbcount-assembly.step / .stl    the whole counter on a 114 mm street pole (pole included as context)
    sensor-head.step / .stl           sensor arm, saddle, head housing, hood, window and array
    power-core.step / .stl            FieldNode core (enclosure, board, cells) with its saddle plate, clamps and panel mount

Axes (mm): road surface at Z = 0, curb face at X = 0, sidewalk at X < 0 with its top at Z = sw_h,
the street runs along Y. The pole stands in the sidewalk behind the curb. The sensor head hangs
from a short arm over the curb and looks down across the sidewalk, bike lane and nearest lane,
tilted toward the road. The FieldNode enclosure sits on the back of the pole, the standard 6 W
FieldNode panel on a pole-top mount. Tracking runs on the FieldNode STM32WL (CBC-DDR-002), so the
head carries the array only and the core uses standard FieldNode power (one cell). Main dimensions and interfaces only: not fabrication detail, not for fabrication.

The same PARAMS and the camera model below feed docs/04-calcs/sizing.py (CBC-CAL-001), the
drawing CBC-DWG-001 (cad/src/sheets.py) and the concept media (cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # street design case (CBC-REQ-001): 3 m sidewalk, 2 m bike lane, one 3.5 m traffic lane
    "sw_h": 150.0, "sidewalk_w": 3000.0, "bike_w": 2000.0, "lane_w": 3500.0,
    # site pole (context, not in the BOM): 114.3 mm (4.5 in) steel pole, 5 m above the sidewalk
    "pole_x": -450.0, "pole_od": 114.3, "pole_h": 5000.0,
    # 10 thermal array: MLX90640 class, 32 x 24 px, 110 x 75 deg lens, 110 deg axis ACROSS the street (CBC-CAL-001 B)
    "px": (32, 24), "fov": (110.0, 75.0),
    # 8 to 10 sensor head: window height above the road, head center X, tilt of the view toward the road
    "window_z": 4300.0, "head_x": 80.0, "tilt": 7.5,
    "head": (110.0, 90.0, 70.0), "head_wall": 3.0, "hood": (150.0, 120.0, 4.0),
    "window": (100.0, 80.0, 0.5),                  # 9 HDPE film, 0.5 mm
    # 7 sensor arm: 40 x 40 x 2 aluminium tube on a saddle plate with two band clamps
    "arm": (40.0, 2.0), "saddle": (6.0, 90.0, 160.0), "arm_band_dz": 55.0,
    # 1 to 3 FieldNode core (FND-PRC-001 v0.3): enclosure 150 W x 90 D x 200 H, center height
    "enc": (150.0, 90.0, 200.0), "enc_wall": 3.0, "enc_zc": 3850.0,
    "enc_plate": (3.0, 140.0, 260.0),              # 6 aluminium enclosure saddle plate (FieldNode's V-blocks fit 40 to 60 mm poles only)
    "board": (10.0, 60.0, 80.0), "ctrl": (8.0, 45.0, 70.0),
    "cell": (32.0, 70.0), "n_cells": 1,          # standard FieldNode: one cell (CBC-DDR-002)
    "whip": (10.0, 190.0), "m12_d": 16.0,
    # 4, 5 solar panel 6 W (FieldNode standard, 9 V class) on an aluminium pole-top mount: sleeve, post and hinge plate
    "panel": (290.0, 200.0, 17.0), "panel_tilt": 35.0,
    "sleeve": (120.0, 4.0, 4.0),                   # length, wall, radial clearance
    "post": (42.4, 3.0, 150.0),                    # OD, wall, height above the sleeve cap
    "hinge": (140.0, 160.0, 5.0),                  # hinge plate under the panel frame
    # 6 band clamps: 12 mm stainless bands
    "band_w": 12.0,
    # 11 sensor cable
    "cable_d": 6.0,
    # 12 public notice plate on the pole, facing the sidewalk
    "notice": (1.5, 150.0, 200.0), "notice_z": 2600.0,
    # scene extents for context (road beyond the nearest lane, street length)
    "scene_y": 5000.0, "road_w": 6000.0,
}

BOM = {  # key: (BOM line in bom/bom.csv, name)
    "enclosure": (1, "FieldNode enclosure, ports, antenna"),
    "board": (2, "FieldNode power and radio board"),
    "cells": (3, "LiFePO4 cell, 6 Ah"),
    "panel": (4, "Solar panel, 6 W"),
    "mount": (5, "Panel pole-top mount"),
    "clamps": (6, "Band clamps (4), enclosure saddle"),
    "arm": (7, "Sensor arm with saddle"),
    "housing": (8, "Sensor head housing and hood"),
    "window": (9, "LWIR window, 0.5 mm HDPE"),
    "array": (10, "Thermal array, 32 x 24 px"),
    "cable": (11, "Sensor cable, M12"),
    "notice": (12, "Public notice plate"),
}


# ------------------------------------------------------------------ camera model (pure math)
def _unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def camera(p=PARAMS):
    """Sensor origin and axes. The optical axis points down, tilted toward +X (road) by p['tilt'].
    u (the 110 deg, 32 px axis) runs across the street, v (75 deg, 24 px) along it."""
    t = math.radians(p["tilt"])
    origin = (p["head_x"], 0.0, p["window_z"])
    axis = (math.sin(t), 0.0, -math.cos(t))
    e_u = (math.cos(t), 0.0, math.sin(t))
    e_v = (0.0, 1.0, 0.0)
    return origin, axis, e_u, e_v


def ray(au_deg, av_deg, p=PARAMS):
    """Ray for image angles (au across, av along), separable equiangular lens model (assumption)."""
    _, a, eu, ev = camera(p)
    tu, tv = math.tan(math.radians(au_deg)), math.tan(math.radians(av_deg))
    return _unit(tuple(a[i] + tu * eu[i] + tv * ev[i] for i in range(3)))


def ground_hit(d, p=PARAMS):
    """Where a ray meets the street surface: sidewalk top (X < 0) or road (X >= 0). None if it misses."""
    o = camera(p)[0]
    if d[2] >= -1e-9:
        return None
    for zg in (0.0, p["sw_h"]):
        s = (zg - o[2]) / d[2]
        x = o[0] + s * d[0]
        if (zg == 0.0 and x >= 0.0) or (zg > 0.0 and x < 0.0):
            return (x, o[1] + s * d[1], zg)
    s = (0.0 - o[2]) / d[2]                       # ray lands on the curb face; take the road point
    return (o[0] + s * d[0], o[1] + s * d[1], 0.0)


def pixel_edges(p=PARAMS):
    fu, fv = p["fov"]
    nu, nv = p["px"]
    return ([-fu / 2 + i * fu / nu for i in range(nu + 1)], [-fv / 2 + j * fv / nv for j in range(nv + 1)])


def footprint_outline(p=PARAMS, n=24):
    """Ground outline of the field of view (list of (x, y)), walking the image border."""
    fu, fv = p["fov"][0] / 2, p["fov"][1] / 2
    pts = []
    for k in range(n):
        pts.append((-fu + 2 * fu * k / n, -fv))
    for k in range(n):
        pts.append((fu, -fv + 2 * fv * k / n))
    for k in range(n):
        pts.append((fu - 2 * fu * k / n, fv))
    for k in range(n):
        pts.append((-fu, fv - 2 * fv * k / n))
    return [ground_hit(ray(au, av, p), p)[:2] for au, av in pts]


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    pr = p["pole_od"] / 2
    hx, hy, hz = p["head"]
    head_zc = p["window_z"] + hz / 2
    arm_z = head_zc + hz / 2 + p["hood"][2] + p["arm"][0] / 2
    pole_face = p["pole_x"] + pr                  # road-side face of the pole
    saddle_x = pole_face + p["saddle"][0] / 2
    arm_x0 = pole_face + p["saddle"][0]
    arm_x1 = p["head_x"] + hx / 2 - 10
    ex, ey, ez = p["enc"][1], p["enc"][0], p["enc"][2]
    enc_plate_x = p["pole_x"] - pr - p["enc_plate"][0] / 2
    enc_xc = p["pole_x"] - pr - p["enc_plate"][0] - ex / 2
    pole_top = p["sw_h"] + p["pole_h"]
    sl_len, sl_wall, sl_clr = p["sleeve"]
    sleeve_r_in = pr + sl_clr
    cap_top = pole_top + sl_wall + 6.0
    post_top = cap_top + p["post"][2]
    t = math.radians(p["panel_tilt"])
    pw, pl, pt = p["panel"]
    panel_c = (p["pole_x"] - 40.0, 0.0, post_top + 20.0 + pw / 2 * math.sin(t))
    panel_top = panel_c[2] + pw / 2 * math.sin(t) + pt / 2 * math.cos(t)
    fp = footprint_outline(p)
    xs = [q[0] for q in fp]
    edges_u, edges_v = pixel_edges(p)
    return {
        "pole_r": pr, "pole_face": pole_face, "pole_top": pole_top,
        "head_zc": head_zc, "arm_z": arm_z, "saddle_x": saddle_x, "arm_x0": arm_x0, "arm_x1": arm_x1,
        "arm_len": arm_x1 - arm_x0, "reach": p["head_x"] - p["pole_x"],
        "enc_xc": enc_xc, "enc_plate_x": enc_plate_x, "enc_dims_xyz": (ex, ey, ez),
        "enc_top": p["enc_zc"] + ez / 2, "enc_bot": p["enc_zc"] - ez / 2,
        "sleeve_r_in": sleeve_r_in, "sleeve_r_out": sleeve_r_in + sl_wall, "sleeve_bot": cap_top - sl_len,
        "cap_top": cap_top, "post_top": post_top, "panel_c": panel_c, "panel_top": panel_top,
        "panel_area_m2": pw * pl / 1e6,
        "fp_x_min": min(xs), "fp_x_max": max(xs),
        "clear_over_road": p["window_z"],
        "edges_u": edges_u, "edges_v": edges_v,
    }


# ------------------------------------------------------------------ geometry
def _tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _band(x, z, r_in, w):
    from build123d import Cylinder, Pos
    return Pos(x, 0, z) * (Cylinder(r_in + 1.5, w) - Cylinder(r_in, w + 2))


def build_parts(p=PARAMS):
    """Return {key: solid} for BOM lines 1 to 12 (line 13, hardware, has no geometry)."""
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(p)
    pr = D["pole_r"]
    out = {}

    # 1 FieldNode enclosure (hollow box, lid line, two M12 ports and an antenna on the bottom face)
    ex, ey, ez = D["enc_dims_xyz"]
    w = p["enc_wall"]
    ec = (D["enc_xc"], 0, p["enc_zc"])
    body = Pos(*ec) * (Box(ex, ey, ez) - Box(ex - 2 * w, ey - 2 * w, ez - 2 * w))
    lid = Pos(ec[0] - ex / 2 - 6, 0, ec[2]) * Box(12, ey, ez)
    ports = (Pos(ec[0], -40, D["enc_bot"] - 12) * Cylinder(p["m12_d"] / 2, 24)
             + Pos(ec[0], -10, D["enc_bot"] - 12) * Cylinder(p["m12_d"] / 2, 24))
    whip = Pos(ec[0], 50, D["enc_bot"] - p["whip"][1] / 2) * Cylinder(p["whip"][0] / 2, p["whip"][1])
    out["enclosure"] = body + lid + ports + whip

    # 2 power and radio board, controller (on the internal plate, against the pole-side wall)
    bx, by, bz = p["board"]
    out["board"] = (Pos(ec[0] + ex / 2 - w - 12, -20, ec[2] + 30) * Box(bx, by, bz)
                    + Pos(ec[0] + ex / 2 - w - 26, 35, ec[2] + 30) * Box(*p["ctrl"]))

    # 3 LiFePO4 cells, lying in the enclosure base along Y
    cd, cl = p["cell"]
    cells = None
    for i in range(p["n_cells"]):
        c = Pos(ec[0] - 18 + i * (cd + 4), 0, D["enc_bot"] + w + cd / 2 + 4) * Rot(90, 0, 0) * Cylinder(cd / 2, cl)
        cells = c if cells is None else cells + c
    out["cells"] = cells

    # 4 solar panel on the pole-top mount, tilted, facing -X (turned toward the equator on site)
    pw, pl, pt = p["panel"]
    out["panel"] = Pos(*D["panel_c"]) * Rot(0, -p["panel_tilt"], 0) * Box(pw, pl, pt)

    # 5 pole-top mount: sleeve with cap over the pole top, post, hinge plate
    sl_len = p["sleeve"][0]
    sl_wall = p["sleeve"][1]
    sleeve = Pos(p["pole_x"], 0, D["sleeve_bot"] + sl_len / 2) * (
        Cylinder(D["sleeve_r_out"], sl_len) - Pos(0, 0, -sl_wall) * Cylinder(D["sleeve_r_in"], sl_len))
    po, pwall, ph = p["post"]
    post = Pos(p["pole_x"], 0, D["cap_top"] + ph / 2) * (Cylinder(po / 2, ph) - Cylinder(po / 2 - pwall, ph + 2))
    hinge = Pos(p["pole_x"] - 20, 0, D["post_top"] + 8) * Rot(0, -p["panel_tilt"], 0) * Box(*p["hinge"])
    out["mount"] = sleeve + post + hinge

    # 6 four band clamps (two on the enclosure saddle, two on the arm saddle) and the enclosure saddle plate
    bw = p["band_w"]
    tx, ty, tz = p["enc_plate"]
    plate = Pos(D["enc_plate_x"], 0, p["enc_zc"]) * Box(tx, ty, tz)
    bands = (_band(p["pole_x"], p["enc_zc"] - tz / 2 + 40, pr, bw) + _band(p["pole_x"], p["enc_zc"] + tz / 2 - 40, pr, bw)
             + _band(p["pole_x"], D["arm_z"] - p["arm_band_dz"], pr, bw) + _band(p["pole_x"], D["arm_z"] + p["arm_band_dz"], pr, bw))
    out["clamps"] = plate + bands

    # 7 sensor arm: saddle plate on the road side of the pole and a square tube to the head
    a, at = p["arm"]
    sx, sy, sz = p["saddle"]
    saddle = Pos(D["saddle_x"], 0, D["arm_z"]) * Box(sx, sy, sz)
    L = D["arm_len"]
    tube = Pos(D["arm_x0"] + L / 2, 0, D["arm_z"]) * (Box(L, a, a) - Box(L + 2, a - 2 * at, a - 2 * at))
    out["arm"] = saddle + tube

    # 8 to 10 sensor head: housing open underneath for the window, sun hood, array; tilted toward the road
    hx, hy, hz = p["head"]
    hw = p["head_wall"]
    H = Pos(p["head_x"], 0, D["head_zc"]) * Rot(0, -p["tilt"], 0)
    shell = Box(hx, hy, hz) - Pos(0, 0, -hw) * Box(hx - 2 * hw, hy - 2 * hw, hz)
    hood = Pos(10, 0, hz / 2 + p["hood"][2] / 2) * Box(*p["hood"])
    out["housing"] = H * (shell + hood)
    wx, wy, wt = p["window"]
    out["window"] = H * Pos(0, 0, -hz / 2 + 2) * Box(wx, wy, max(wt, 1.0))
    out["array"] = H * (Pos(0, 0, -hz / 2 + 14) * Cylinder(4.7, 12) + Pos(0, 0, -hz / 2 + 21) * Box(32, 26, 2))

    # 11 sensor cable: M12 port under the enclosure, round to the pole, up the pole, along the arm, into the head
    r = p["cable_d"] / 2
    cy = -pr - 8
    z0 = D["enc_bot"] - 30
    pts = [(ec[0], -40, D["enc_bot"] - 24), (ec[0], -40, z0), (p["pole_x"] - pr + 10, cy, z0),
           (p["pole_x"], cy, z0), (p["pole_x"], cy, D["arm_z"] - 30),
           (D["pole_face"] + 20, -30, D["arm_z"] - 30), (p["head_x"] - 20, -30, D["arm_z"] - 30),
           (p["head_x"] - 20, -30, D["head_zc"] + hz / 2 - 5)]
    cable = None
    for a_, b_ in zip(pts[:-1], pts[1:]):
        seg = _tube(a_, b_, r)
        cable = seg if cable is None else cable + seg
    out["cable"] = cable

    # 12 public notice plate, banded to the sidewalk side of the pole at eye height
    nx, ny, nz = p["notice"]
    out["notice"] = Pos(p["pole_x"] - pr - nx / 2, 0, p["notice_z"]) * Box(nx, ny, nz)
    return out


def context_parts(p=PARAMS):
    """Grey context (not in the BOM): pole, sidewalk and road with lane lines, sensing footprint."""
    from build123d import Box, Cylinder, Pos, Polyline, make_face, extrude
    D = derived(p)
    L = p["scene_y"]
    sw = Pos(-p["sidewalk_w"] / 2, 0, p["sw_h"] / 2) * Box(p["sidewalk_w"], L, p["sw_h"])
    road = Pos(p["road_w"] / 2, 0, -30) * Box(p["road_w"], L, 60)
    lines = (Pos(p["bike_w"], 0, 1) * Box(100, L, 2)
             + Pos(p["bike_w"] + p["lane_w"], 0, 1) * Box(100, L, 2))
    pole = Pos(p["pole_x"], 0, p["sw_h"] + p["pole_h"] / 2) * Cylinder(D["pole_r"], p["pole_h"])
    # footprint: outline on the ground, clipped to the scene, split at the curb so it sits on each surface
    pts = [(min(max(x, -p["sidewalk_w"] + 5), p["road_w"] - 5), min(max(y, -L / 2 + 5), L / 2 - 5))
           for x, y in footprint_outline(p)]
    pts = [q for i, q in enumerate(pts) if math.dist(q, pts[i - 1]) > 1.0]      # drop points merged by the clipping
    face = make_face(Polyline(*[(x, y, 0) for x, y in pts], close=True))
    slab = extrude(face, 3)
    fp = (Pos(0, 0, p["sw_h"] + 1) * (slab & Pos(-5000, 0, 0) * Box(10000, 2 * L, 20))
          + Pos(0, 0, 1) * (slab & Pos(5000, 0, 0) * Box(10000, 2 * L, 20)))
    return {"pole": pole, "street": sw + road + lines, "footprint": fp}


def assembly(p=PARAMS, with_context=True):
    from build123d import Compound
    kids = list(build_parts(p).values())
    if with_context:
        c = context_parts(p)
        kids += [c["pole"]]
    return Compound(children=kids)


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    C = context_parts()
    groups = {
        "curbcount-assembly": list(P.values()) + [C["pole"]],
        "sensor-head": [P[k] for k in ("arm", "housing", "window", "array")],
        "power-core": [P[k] for k in ("enclosure", "board", "cells", "panel", "mount", "clamps")],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"arm {D['arm_len']:.0f} mm, head reach from pole axis {D['reach']:.0f} mm, arm axis at {D['arm_z']:.0f} mm; "
          f"panel top {D['panel_top']:.0f} mm above the road; footprint across {D['fp_x_min']:.0f} to {D['fp_x_max']:.0f} mm")
