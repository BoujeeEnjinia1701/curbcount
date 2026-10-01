"""CurbCount parametric model (build123d), TRL 3, constructable design (CBC-DDR-003).

Run from the repo root:  python cad/src/model.py          exports and prints the checks
                         python cad/src/model.py --check  prints the constructability checks only
Exports STEP and STL into cad/step and cad/stl:
    curbcount-assembly.step / .stl    the whole counter on its 114.3 mm street pole (pole as context)
    sensor-head.step / .stl           arm saddle plate, arm, sensor head, window and array
    power-core.step / .stl            FieldNode core on its saddle plate, bands, panel and pole-top mount

Axes (mm): road surface at Z = 0, curb face at X = 0, sidewalk at X < 0 with its top at Z = sw_h,
the street runs along Y. The pole stands in the sidewalk 450 mm behind the curb. The sensor head
hangs under an arm on the road side of the pole and looks down across the sidewalk, bike lane and
nearest lane, tilted toward the road. The FieldNode enclosure sits on a saddle plate on the
sidewalk side of the pole; the standard 6 W FieldNode panel sits on a pole-top mount. Tracking
runs on the FieldNode STM32WL (CBC-DDR-002), so the head carries the array only.

Revised 2026-09-30 under Amish's instruction to make the design physically buildable
(CBC-DDR-003, "Design for construction"). Every component is now a shape that can be cut,
drilled, bent, printed or bought, and every joint has a fixing:
    saddle plates seat on the pole through bent 90 deg V-saddles and are held by band clamps
    that pass through slots in the plate (60 to 140 mm poles);
    the FieldNode core is FieldNode's constructable core (FND-DDR-003): lugs on the plate,
    two rows of penetrations, internal plate on bosses, plug-in connector strip;
    the arm butts the arm saddle plate and is held by two angle brackets and through-bolts;
    the head hangs from the arm on a printed wedge pad with heat-set inserts, has a printed
    window frame that clamps the film to an inner ledge, standoffs for the array, a cable gland;
    the pole-top mount is all bolted: sleeve with rivet-nut set screws, cap disc on radial
    screws, post on angle clips and plugs, panel on a tilted rail plate through its frame lip;
    the cables are tied to the pole, pass over the bands and run beside the arm;
    the notice plate is tied to the pole through slots.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (CBC-CAL-001), the drawing CBC-DWG-001 (cad/src/sheets.py), the concept
media (cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # street design case (CBC-REQ-001): 3 m sidewalk, 2 m bike lane, one 3.5 m traffic lane
    "sw_h": 150.0, "sidewalk_w": 3000.0, "bike_w": 2000.0, "lane_w": 3500.0,
    # site pole (context, not in the BOM): 114.3 mm (4.5 in) steel pole, 5 m above the sidewalk
    "pole_x": -450.0, "pole_od": 114.3, "pole_h": 5000.0, "pole_range": (60.0, 140.0),
    # 10 thermal array: MLX90640 class, 32 x 24 px, 110 x 75 deg lens, 110 deg axis ACROSS the street (CBC-CAL-001 B)
    "px": (32, 24), "fov": (110.0, 75.0),
    # 8 to 10 sensor head: underside of the housing above the road, head center X, tilt toward the road
    "window_z": 4300.0, "head_x": 80.0, "tilt": 7.5,
    "head": (110.0, 90.0, 70.0), "head_wall": 3.0, "hood": (150.0, 120.0, 4.0), "hood_dx": 10.0,
    "ledge": 8.0,                                  # inner ledge at the housing bottom that the film is clamped to
    "frame_t": 3.0,                                # printed window frame
    "window": (100.0, 80.0, 0.5),                  # 9 HDPE film, 0.5 mm
    "head_screws": (47.0, 37.0),                   # M3 frame screws into heat-set inserts in four corner bosses
    "wedge_x": (30.0, 120.0), "wedge_min": 3.0,    # printed wedge pad under the arm (world x span), thinnest point
    "head_bolts_x": (45.0, 105.0),                 # M5 bolts through the arm into the wedge pad (world x)
    # 7 sensor arm: 40 x 40 x 2 aluminium tube, butted to its saddle plate and held by two angle brackets
    "arm": (40.0, 2.0), "saddle": (3.0, 160.0, 250.0), "arm_band_dz": 110.0, "arm_vs_dz": 75.0,
    "arm_bracket": (40.0, 4.0, 40.0),              # angle leg, thickness, width
    # 1 to 3 FieldNode core (FND-PRC-001 v0.5, FND-DDR-003): enclosure 150 W x 90 D x 200 H, center height
    "enc": (150.0, 90.0, 200.0), "enc_wall": 3.0, "lid_d": 12.0, "enc_zc": 3850.0,
    "lug": (62.0, 16.0, 4.0, 16.0),                # lug x of centre, width, thickness, reach beyond the box
    "mplate": (130.0, 180.0, 3.0), "boss": (55.0, 80.0, 6.0),
    "board": (80.0, 60.0, 10.0), "ctrl": (70.0, 45.0, 8.0), "strip": (70.0, 12.0, 14.0),
    "cell": (32.0, 70.0), "n_cells": 1,            # standard FieldNode: one cell (CBC-DDR-002)
    "pen_rows": (27.0, 55.0),
    "pens": {"gland_1": (-40.0, 0, 16.0, 24.0), "gland_2": (-8.0, 0, 16.0, 24.0), "vent": (24.0, 0, 12.0, 18.0),
             "port_a": (-54.0, 1, 16.0, 22.0), "port_b": (-22.0, 1, 16.0, 22.0), "antenna": (30.0, 1, 6.4, 18.0)},
    "whip": (10.0, 190.0), "m12_d": 16.0,
    # 6 enclosure saddle plate (thickness, width along the street, height) and its bands and V-saddles
    "enc_plate": (3.0, 160.0, 300.0), "enc_band_dz": 133.0, "enc_vs_dz": 98.0,
    "enc_window": (100.0, 150.0, 6.0),             # lightening window behind the enclosure (W x H, corner radius)
    # V-saddle: bent 3 mm aluminium, flat width, wing length, height, 90 deg included angle
    "vsaddle": (3.0, 20.0, 65.0, 40.0),
    # 6 band clamps: 12 mm stainless, 0.8 mm thick; slot centre from the plate centre line
    "band_w": 12.0, "band_t": 0.8, "slot_y": 66.0, "slot": (3.0, 15.0),
    # 4, 5 solar panel 6 W (FieldNode standard, 9 V class) on an aluminium pole-top mount
    "panel": (290.0, 200.0, 17.0), "panel_tilt": 35.0,
    "sleeve": (100.0, 3.0, 3.85),                  # length, wall, radial clearance (122 mm bore on a 114.3 mm pole)
    "cap_t": 8.0,                                  # cap disc inside the sleeve top, sits on the pole top
    "post": (42.4, 3.0, 150.0),                    # OD, wall, height above the cap disc
    "plug": (40.0,),                               # solid plugs in each end of the post
    "pclip": (50.0, 5.0, 35.0),                    # post clips: angle leg, thickness, length
    "hinge": (290.0, 150.0, 3.0),                  # tilted rail plate under the panel (slope x width x t)
    "rail_gap": 20.0,                              # rail plate underside above the post top, at the post axis
    "upper_clip_s": (-40.0, -5.0),                 # upper post clips along the slope (from the post axis)
    # 11 sensor cable and the panel extension lead
    "cable_d": 6.0, "cable_r": 62.2,               # cables tied to the pole, passing over the bands
    "cable_theta": (87.0, 93.0),                  # sensor cable, panel lead (deg, from +X toward +Y)
    # 12 public notice plate on the pole, facing the sidewalk, tied through slots
    "notice": (2.0, 150.0, 200.0), "notice_z": 2600.0, "notice_tie": (8.0, 0.5, 60.0, 70.0),
    # scene extents for context (road beyond the nearest lane, street length)
    "scene_y": 5000.0, "road_w": 6000.0,
}

BOM = {  # group key: (BOM line in bom/bom.csv, name)
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
    "connectors": (14, "Plug-in connector strip, fuses"),
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought" or "fixing"
    group: str | None  # key in BOM (build_parts groups components by it)


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


# ------------------------------------------------------------------ derived dimensions
def vsaddle_offset(r, p=PARAMS):
    """Distance from the saddle plate's back face to the pole axis for a pole of radius r.
    The V's faces meet (virtually) f behind the flat's pole-side face, f = half the flat width."""
    t, flat, _, _ = p["vsaddle"]
    return t - flat / 2 + r * math.sqrt(2)


def head_frame_point(xl, yl, zl, p=PARAMS):
    """World point of a point given in the head frame (housing centre, tilted toward the road)."""
    t = math.radians(p["tilt"])
    hz = p["head"][2]
    zc = p["window_z"] + hz / 2
    return (p["head_x"] + xl * math.cos(t) - zl * math.sin(t), yl, zc + xl * math.sin(t) + zl * math.cos(t))


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    pr = p["pole_od"] / 2
    hx, hy, hz = p["head"]
    head_zc = p["window_z"] + hz / 2
    # arm underside: the highest point of the tilted hood top under the wedge span, plus the thinnest pad
    hood_top = hz / 2 + p["hood"][2]
    t = math.radians(p["tilt"])
    xl_max = (p["wedge_x"][1] - p["head_x"]) / math.cos(t) + 5
    arm_bot = head_zc + xl_max * math.sin(t) + hood_top * math.cos(t) + p["wedge_min"]
    arm_z = arm_bot + p["arm"][0] / 2
    off = vsaddle_offset(pr, p)                   # pole axis to the back face of either saddle plate
    st = p["enc_plate"][0]
    enc_plate_back = p["pole_x"] - off
    enc_plate_front = enc_plate_back - st
    arm_plate_back = p["pole_x"] + off
    arm_plate_front = arm_plate_back + p["saddle"][0]
    arm_x0 = arm_plate_front
    arm_x1 = p["head_x"] + hx / 2 - 10
    ew, ed, eh = p["enc"]
    enc_xc = enc_plate_front - ed / 2
    pole_top = p["sw_h"] + p["pole_h"]
    sl_len, sl_wall, sl_clr = p["sleeve"]
    sleeve_r_in = pr + sl_clr
    cap_top = pole_top + p["cap_t"]
    post_top = cap_top + p["post"][2]
    tp = math.radians(p["panel_tilt"])
    n = (-math.sin(tp), 0.0, math.cos(tp))
    u = (math.cos(tp), 0.0, math.sin(tp))
    P0 = (p["pole_x"], 0.0, post_top + p["rail_gap"])      # rail plate underside on the post axis
    pw, pl, pt = p["panel"]
    rt = p["hinge"][2]
    panel_c = tuple(P0[i] + n[i] * (rt + pt / 2) for i in range(3))
    panel_top = panel_c[2] + pw / 2 * math.sin(tp) + pt / 2 * math.cos(tp)
    panel_low = panel_c[2] - pw / 2 * math.sin(tp) - pt / 2 * math.cos(tp)
    fp = footprint_outline(p)
    xs = [q[0] for q in fp]
    edges_u, edges_v = pixel_edges(p)
    return {
        "pole_r": pr, "pole_face": p["pole_x"] + pr, "pole_top": pole_top,
        "head_zc": head_zc, "arm_z": arm_z, "arm_bot": arm_bot,
        "saddle_x": arm_plate_back + p["saddle"][0] / 2, "arm_plate_back": arm_plate_back, "arm_plate_front": arm_plate_front,
        "arm_x0": arm_x0, "arm_x1": arm_x1, "arm_len": arm_x1 - arm_x0, "reach": p["head_x"] - p["pole_x"],
        "vs_offset": off, "enc_plate_back": enc_plate_back, "enc_plate_front": enc_plate_front,
        "enc_plate_x": enc_plate_back - st / 2,
        "enc_xc": enc_xc, "enc_dims_xyz": (ed, ew, eh),
        "enc_top": p["enc_zc"] + eh / 2, "enc_bot": p["enc_zc"] - eh / 2,
        "sleeve_r_in": sleeve_r_in, "sleeve_r_out": sleeve_r_in + sl_wall, "sleeve_bot": cap_top - sl_len,
        "cap_top": cap_top, "post_top": post_top, "rail_P0": P0, "rail_u": u, "rail_n": n,
        "panel_c": panel_c, "panel_top": panel_top, "panel_low": panel_low,
        "panel_area_m2": pw * pl / 1e6,
        "fp_x_min": min(xs), "fp_x_max": max(xs),
        "clear_over_road": p["window_z"],
        "edges_u": edges_u, "edges_v": edges_v,
    }


# ------------------------------------------------------------------ geometry helpers
def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def ycyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def xcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


def hexprism(axis, x, y, z, af, h):
    """Hexagon (across flats af) of length h along axis 'x', 'y' or 'z', centred on (x, y, z)."""
    b = _b3d()
    s = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h / 2, both=True)
    rot = {"z": b.Rot(0, 0, 0), "y": b.Rot(90, 0, 0), "x": b.Rot(0, 90, 0)}[axis]
    return b.Pos(x, y, z) * rot * s


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _tube(a, c, r):
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def _route(pts, r):
    """A cable along a polyline, with a ball at each bend so the run is continuous."""
    b = _b3d()
    segs = [_tube(a, c, r) for a, c in zip(pts[:-1], pts[1:])]
    balls = [b.Solid.make_sphere(r).moved(b.Location(q)) for q in pts[1:-1]]
    return segs[0].fuse(*(segs[1:] + balls)).clean()


def route_length(pts):
    return sum(math.dist(a, c) for a, c in zip(pts[:-1], pts[1:]))


def _bolt_x(xa, xb, y, z, d=6.0, head=10.0):
    """Hex bolt and nut along X clamping the stack between xa and xb (xa < xb)."""
    hl, nl = 0.6 * d, 0.9 * d
    return (hexprism("x", xa - hl / 2, y, z, head, hl) + xcyl((xa + xb) / 2, y, z, d / 2, xb - xa)
            + hexprism("x", xb + nl / 2, y, z, head, nl) + xcyl(xb + nl + 1, y, z, d / 2, 2))


def _bolt_y(ya, yb, x, z, d=8.0, head=13.0):
    """Hex bolt and nut along Y clamping the stack between ya and yb (ya < yb)."""
    hl, nl = 0.6 * d, 0.9 * d
    return (hexprism("y", x, ya - hl / 2, z, head, hl) + ycyl(x, (ya + yb) / 2, z, d / 2, yb - ya)
            + hexprism("y", x, yb + nl / 2, z, head, nl) + ycyl(x, yb + nl + 1, z, d / 2, 2))


def _bolt_z(za, zb, x, y, d=6.0, head=10.0):
    """Hex bolt and nut along Z clamping the stack between za and zb (za < zb), head on top."""
    hl, nl = 0.6 * d, 0.9 * d
    return (hexprism("z", x, y, zb + hl / 2, head, hl) + zcyl(x, y, (za + zb) / 2, d / 2, zb - za)
            + hexprism("z", x, y, za - nl / 2, head, nl) + zcyl(x, y, za - nl - 1, d / 2, 2))


# ------------------------------------------------------------------ saddle plates, V-saddles and bands
def _vsaddle_local(p=PARAMS):
    """Bent V-saddle in plate coordinates: u from the plate's back face toward the pole, v across,
    extruded along Z (height), centred on z = 0."""
    b = _b3d()
    t, flat, wing, h = p["vsaddle"]
    f = flat / 2
    s = wing / math.sqrt(2)
    k = t / math.sqrt(2)
    # outer face of the wing: offset of the inner face by t, meeting the plate face u = 0
    v0 = f + k - (t - k)            # where the outer wing face crosses u = 0
    half = [(0, 0), (0, v0), (t + s - k, f + s + k), (t + s, f + s), (t, f), (t, 0)]
    pts = half + [(u, -v) for u, v in reversed(half)][1:-1]
    face = b.make_face(b.Polyline(*[(u, v, 0) for u, v in pts], close=True))
    sad = b.extrude(face, h / 2, both=True)
    return sad


def _band_local(d, r, sy, st, w, th):
    """Band round a pole of radius r whose axis is d in front of the plate's back face (u = d),
    through slots at v = +-sy and across the plate's front face (u = -st). Plate coordinates."""
    b = _b3d()
    L = math.hypot(d, sy)
    phi = math.atan2(sy, -d)
    a = math.acos(r / L)
    tp = (d + r * math.cos(phi - a), r * math.sin(phi - a))
    tm = (tp[0], -tp[1])
    inner = b.make_face(b.Wire([b.Line((-st, -sy), (-st, sy)), b.Line((-st, sy), (0, sy)), b.Line((0, sy), tp),
                                 b.ThreePointArc(tp, (d + r, 0), tm), b.Line(tm, (0, -sy)), b.Line((0, -sy), (-st, -sy))]))
    outer = b.offset(inner, th, kind=b.Kind.ARC)
    ring = outer - inner
    return b.extrude(ring, w / 2, both=True)


def _plate_local(st, wv, hz, holes=(), slots=()):
    """Flat plate: u from -st (front) to 0 (back), v across, z up, centred on z = 0.
    holes: (v, z, r); slots: (v, z, wv, hz)."""
    pl = bx(-st, 0, -wv / 2, wv / 2, -hz / 2, hz / 2)
    for v, z, r in holes:
        pl -= xcyl(-st / 2, v, z, r, st + 2)
    for v, z, sv, sz in slots:
        pl -= box(-st / 2, v, z, st + 2, sv, sz)
    return pl


def _to_world(shape, side, x_back, z0):
    """Plate coordinates to world. side = +1: plate on the sidewalk side, u toward +X;
    side = -1: plate on the road side, u toward -X. x_back is the world x of the plate's back face."""
    b = _b3d()
    if side > 0:
        return b.Pos(x_back, 0, z0) * shape
    return b.Pos(x_back, 0, z0) * shape.mirror(b.Plane.YZ)


# ------------------------------------------------------------------ the FieldNode core (local frame)
def _core_local(p=PARAMS):
    """FieldNode's constructable core (FND-DDR-003) in its own frame: box back face at y = 0, lid
    toward -Y, bottom at z = 0, x to the right seen from the front. Returns {key: (name, shape, bom, kind, group)}."""
    b = _b3d()
    ew, ed, eh = p["enc"]
    w, ld = p["enc_wall"], p["lid_d"]
    z0, zc = 0.0, eh / 2
    yb = 0.0
    out = {}
    pen_xy = {k: (x, yb - p["pen_rows"][row]) for k, (x, row, _, _) in p["pens"].items()}
    bd = ed - ld
    ybody = yb - bd / 2
    body = box(0, ybody, zc, ew, bd, eh) - box(0, ybody - w, zc, ew - 2 * w, bd, eh - 2 * w)
    bxo, bzo, bh = p["boss"]
    for sx in (-1, 1):
        for sz in (-1, 1):
            body += ycyl(sx * bxo, yb - w - bh / 2, zc + sz * bzo, 4.0, bh)
            body -= ycyl(sx * bxo, yb - w - bh + 4, zc + sz * bzo, 1.6, 8.1)
    for k, (x, row, dt, df) in p["pens"].items():
        hole = dt / 2 + (0.1 if dt >= 10 else 0.05)
        body -= zcyl(x, pen_xy[k][1], z0 + w / 2, hole, w + 2)
    out["body"] = ("Enclosure body", body, 1, "bought", "enclosure")
    ylid = yb - ed + ld / 2
    out["lid"] = ("Enclosure lid", box(0, ylid, zc, ew, ld, eh) - box(0, ylid + w, zc, ew - 2 * w, ld, eh - 2 * w), 1, "bought", "enclosure")
    lx, lw, lt, lr = p["lug"]
    lugs, lug_fix = [], []
    st = p["enc_plate"][0]
    for sx in (-1, 1):
        for zlo, zhi in ((eh, eh + lr), (z0 - lr, z0)):
            lug = bx(sx * lx - lw / 2, sx * lx + lw / 2, yb - lt, yb, zlo, zhi)
            zh = (zlo + zhi) / 2 + (1 if zlo > z0 else -1)
            lug -= ycyl(sx * lx, yb - lt / 2, zh, 2.75, lt + 2)
            lugs.append(lug)
            hl, nl = 2.75, 4.5
            lug_fix.append(ycyl(sx * lx, yb + st + hl / 2, zh, 4.75, hl) + ycyl(sx * lx, yb + st / 2 - lt / 2, zh, 2.75, st + lt)
                           + hexprism("y", sx * lx, yb - lt - nl / 2, zh, 8.0, nl) + ycyl(sx * lx, yb - lt - nl - 1, zh, 2.5, 2))
    out["lugs"] = ("Enclosure lugs (4)", fuse(lugs), 1, "bought", "enclosure")
    out["lug_screws"] = ("M5 screws and nuts, lugs (4)", fuse(lug_fix), 13, "fixing", None)

    def pen(k):
        x, y = pen_xy[k]
        _, _, dt, df = p["pens"][k]
        return x, y, dt, df, zcyl(x, y, z0 - 1.5, df / 2, 3.0), zcyl(x, y, z0 + w / 2, dt / 2, w)
    glands = []
    for k in ("gland_1", "gland_2"):
        x, y, dt, df, fl, thr = pen(k)
        glands.append(fl + zcyl(x, y, z0 - 10, 10.0, 14.0) + thr + hexprism("z", x, y, z0 + w + 2.5, 22.0, 5.0)
                      + zcyl(x, y, z0 + w + 6, dt / 2, 2))
    out["glands"] = ("Cable glands, 2 x M16", fuse(glands), 1, "bought", "enclosure")
    ports = []
    for k in ("port_a", "port_b"):
        x, y, dt, df, fl, thr = pen(k)
        ports.append(fl + zcyl(x, y, z0 - 12.5, 8.0, 19.0) + thr + hexprism("z", x, y, z0 + w + 2.5, 22.0, 5.0)
                     + zcyl(x, y, z0 + w + 9, 7.0, 8))
    out["ports"] = ("Sensor ports, 2 x M12", fuse(ports), 1, "bought", "enclosure")
    x, y, dt, df, fl, thr = pen("vent")
    out["vent"] = ("Membrane vent", zcyl(x, y, z0 - 4, df / 2, 8.0) + thr + hexprism("z", x, y, z0 + w + 1.5, 17.0, 3.0),
                   1, "bought", "enclosure")
    x, y, dt, df, fl, thr = pen("antenna")
    wd, wl = p["whip"]
    out["antenna"] = ("Antenna, bulkhead and whip", hexprism("z", x, y, z0 - 2, 16.0, 4.0) + thr + hexprism("z", x, y, z0 + w + 1.5, 8.0, 3.0)
                      + zcyl(x, y, z0 - 12, 7.0, 16.0) + zcyl(x, y, z0 - 20 - wl / 2, wd / 2, wl), 1, "bought", "enclosure")
    mw, mh, mt = p["mplate"]
    yp1 = yb - w - bh
    mf = yp1 - mt
    mp = bx(-mw / 2, mw / 2, mf, yp1, zc - mh / 2, zc + mh / 2)
    for sx in (-1, 1):
        for sz in (-1, 1):
            mp -= ycyl(sx * bxo, yp1 - mt / 2, zc + sz * bzo, 2.25, mt + 2)
    finger = b.Pos(0, yp1 - mt / 2, zc + mh / 2 - 12) * b.Box(40, mt + 2, 10)
    mp -= b.fillet(finger.edges().filter_by(b.Axis.Y), 4.9)
    out["mplate"] = ("Internal plate", mp, 1, "made", "enclosure")
    out["mplate_screws"] = ("M4 screws, internal plate (4)",
                            fuse(ycyl(sx * bxo, mf - 1.4, zc + sz * bzo, 3.5, 2.8) for sx in (-1, 1) for sz in (-1, 1)), 13, "fixing", None)
    cd, cl = p["cell"]
    out["cell"] = ("LiFePO4 cell in fused holder", zcyl(-38, mf - cd / 2 - 4, z0 + 75, cd / 2, cl) + box(-38, mf - 5, z0 + 75, cd + 6, 10, cl + 10),
                   3, "bought", "cells")
    pw_, ph_, pt_ = p["board"]
    out["power"] = ("Power modules", box(22, mf - pt_ / 2, z0 + 70, pw_, pt_, ph_)
                    + box(30, mf - pt_ - 6, z0 + 62, 22, 12, 18) + box(5, mf - pt_ - 4, z0 + 82, 14, 8, 10), 2, "bought", "board")
    cw, ch, ct = p["ctrl"]
    out["ctrl"] = ("Controller and LoRa module", box(10, mf - ct / 2, z0 + 150, cw, ct, ch) + box(0, mf - ct - 3, z0 + 150, 24, 6, 20),
                   2, "bought", "board")
    sw, sd, sh = p["strip"]
    zs = zc - mh / 2 + 4 + sh / 2
    out["connectors"] = ("Plug-in connector strip", box(0, mf - sd / 2, zs, sw, sd, sh) + box(0, mf - sd - 4, zs, sw - 6, 8, sh - 4),
                         14, "bought", "connectors")
    return out


def core_to_world(shape, p=PARAMS):
    """FieldNode local frame (back face y = 0, lid toward -Y, bottom z = 0) to world: lid toward -X
    (the sidewalk), back face on the enclosure saddle plate. Local +x becomes world -y."""
    b = _b3d()
    D = derived(p)
    return b.Pos(D["enc_plate_front"], 0, D["enc_bot"]) * b.Rot(0, 0, -90) * shape


def port_world(key, p=PARAMS):
    """World (x, y) of a bottom-face penetration."""
    D = derived(p)
    x, row, _, _ = p["pens"][key]
    yl = -p["pen_rows"][row]
    return (D["enc_plate_front"] + yl, -x)


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component as a Comp, keyed by a short name."""
    b = _b3d()
    D = derived(p)
    pr = D["pole_r"]
    px = p["pole_x"]
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    # ---- 1 to 3, 14: the FieldNode core, in world position
    for k, (name, shape, bom, kind, group) in _core_local(p).items():
        add(k, name, core_to_world(shape, p), bom, kind, group)

    # ---- 6 enclosure saddle plate, V-saddles, bands
    st, sw, sh = p["enc_plate"]
    off = D["vs_offset"]
    lx, lw_, lt, lr = p["lug"]
    eh = p["enc"][2]
    lug_z = [eh / 2 + lr / 2 + 1, -(eh / 2 + lr / 2 + 1)]
    sy = p["slot_y"]
    sv, sz_ = p["slot"]
    vsh = p["vsaddle"][3]
    vs_screw = [(0.0, dz + s * 10) for dz in (p["enc_vs_dz"], -p["enc_vs_dz"]) for s in (-1, 1)]
    holes = [(v, z, 2.75) for v in (-lx, lx) for z in lug_z] + [(v, z, 2.25) for v, z in vs_screw]
    slots = [(v, z, sv, sz_) for v in (-sy, sy) for z in (p["enc_band_dz"], -p["enc_band_dz"])]
    plate = _plate_local(st, sw, sh, holes, slots)
    ww, wh, wr = p["enc_window"]
    win = b.Pos(-st / 2, 0, 0) * b.Rot(0, 90, 0) * b.extrude(b.RectangleRounded(wh, ww, wr), st / 2 + 1, both=True)
    plate -= win
    zc = p["enc_zc"]
    add("enc_plate", "Enclosure saddle plate", _to_world(plate, 1, D["enc_plate_back"], zc), 6, "made", "clamps")
    sad = _vsaddle_local(p)
    for nm, dz in (("up", p["enc_vs_dz"]), ("low", -p["enc_vs_dz"])):
        s_ = b.Pos(0, 0, dz) * sad
        for s in (-1, 1):
            s_ -= xcyl(1.5, 0, dz + s * 10, 2.0, 3.2)
        add(f"enc_vs_{nm}", f"V-saddle, enclosure {'upper' if nm == 'up' else 'lower'}", _to_world(s_, 1, D["enc_plate_back"], zc), 6, "made", "clamps")
    scr = fuse(xcyl(-st + (st + 3) / 2, v, z, 2.0, st + 3) for v, z in vs_screw)
    add("enc_vs_screws", "M4 countersunk screws, V-saddles (4)", _to_world(scr, 1, D["enc_plate_back"], zc), 13, "fixing", None)
    bw, bt = p["band_w"], p["band_t"]
    bands = fuse(b.Pos(0, 0, dz) * _band_local(off, pr, sy, st, bw, bt) for dz in (p["enc_band_dz"], -p["enc_band_dz"]))
    add("enc_bands", "Band clamps, enclosure (2)", _to_world(bands, 1, D["enc_plate_back"], zc), 6, "bought", "clamps")

    # ---- 7 arm saddle plate, V-saddles, bands, tube, brackets
    ast, asw, ash = p["saddle"]
    az = D["arm_z"]
    al, at_, aw = p["arm_bracket"]
    bb_bolts = [(v, s * 42.0) for v in (-10.0, 10.0) for s in (-1, 1)]
    vs2 = [(0.0, dz + s * 10) for dz in (p["arm_vs_dz"], -p["arm_vs_dz"]) for s in (-1, 1)]
    aholes = [(v, z, 3.3) for v, z in bb_bolts] + [(v, z, 2.25) for v, z in vs2]
    aslots = [(v, z, sv, sz_) for v in (-sy, sy) for z in (p["arm_band_dz"], -p["arm_band_dz"])]
    aplate = _plate_local(ast, asw, ash, aholes, aslots)
    add("arm_plate", "Arm saddle plate", _to_world(aplate, -1, D["arm_plate_back"], az), 7, "made", "arm")
    for nm, dz in (("up", p["arm_vs_dz"]), ("low", -p["arm_vs_dz"])):
        s_ = b.Pos(0, 0, dz) * sad
        for s in (-1, 1):
            s_ -= xcyl(1.5, 0, dz + s * 10, 2.0, 3.2)
        add(f"arm_vs_{nm}", f"V-saddle, arm {'upper' if nm == 'up' else 'lower'}", _to_world(s_, -1, D["arm_plate_back"], az), 7, "made", "arm")
    scr = fuse(xcyl(-ast + (ast + 3) / 2, v, z, 2.0, ast + 3) for v, z in vs2)
    add("arm_vs_screws", "M4 countersunk screws, V-saddles (4)", _to_world(scr, -1, D["arm_plate_back"], az), 13, "fixing", None)
    bands = fuse(b.Pos(0, 0, dz) * _band_local(off, pr, sy, ast, bw, bt) for dz in (p["arm_band_dz"], -p["arm_band_dz"]))
    add("arm_bands", "Band clamps, arm (2)", _to_world(bands, -1, D["arm_plate_back"], az), 6, "bought", "clamps")
    a, wt = p["arm"]
    x0, x1 = D["arm_x0"], D["arm_x1"]
    tube = bx(x0, x1, -a / 2, a / 2, az - a / 2, az + a / 2) - bx(x0 - 1, x1 + 1, -a / 2 + wt, a / 2 - wt, az - a / 2 + wt, az + a / 2 - wt)
    tb_x = [x0 + 15.0, x0 + 30.0]
    hb_x = list(p["head_bolts_x"])
    for xx in tb_x:
        tube -= zcyl(xx, 0, az, 3.3, a + 2)
    for xx in hb_x:
        tube -= zcyl(xx, 0, az, 2.75, a + 2)
    add("arm_tube", "Arm tube", tube, 7, "made", "arm")
    add("arm_cap", "Arm end cap", bx(x1, x1 + 3, -a / 2, a / 2, az - a / 2, az + a / 2) + bx(x1 - 8, x1, -a / 2 + wt, a / 2 - wt, az - a / 2 + wt, az + a / 2 - wt),
        7, "bought", "arm")
    brk = []
    for s in (1, -1):
        zf = az + s * a / 2                        # tube face the leg sits on
        leg_v = bx(x0, x0 + at_, -aw / 2, aw / 2, zf, zf + s * al) if s > 0 else bx(x0, x0 + at_, -aw / 2, aw / 2, zf - al, zf)
        leg_h = bx(x0, x0 + al, -aw / 2, aw / 2, zf, zf + s * at_) if s > 0 else bx(x0, x0 + al, -aw / 2, aw / 2, zf - at_, zf)
        br = leg_v + leg_h
        for v, z in bb_bolts:
            if z * s > 0:
                br -= xcyl(x0 + at_ / 2, v, az + z, 3.3, at_ + 2)
        for xx in tb_x:
            br -= zcyl(xx, 0, zf + s * at_ / 2, 3.3, at_ + 2)
        brk.append(br)
    add("arm_brk_up", "Arm bracket, upper", brk[0], 7, "made", "arm")
    add("arm_brk_low", "Arm bracket, lower", brk[1], 7, "made", "arm")
    # the nut goes behind the plate (pole side): build head at the bracket, nut behind
    fx = [hexprism("x", x0 + at_ + 1.8, v, az + z, 10.0, 3.6) + xcyl((D["arm_plate_back"] + x0 + at_) / 2, v, az + z, 3.0, x0 + at_ - D["arm_plate_back"])
          + hexprism("x", D["arm_plate_back"] - 2.7, v, az + z, 10.0, 5.4) + xcyl(D["arm_plate_back"] - 6.4, v, az + z, 3.0, 2)
          for v, z in bb_bolts]
    spacers = []
    for xx in tb_x:
        fx.append(_bolt_z(az - a / 2 - at_, az + a / 2 + at_, xx, 0, 6.0, 10.0))
        spacers.append(zcyl(xx, 0, az, 5.0, a - 2 * wt) - zcyl(xx, 0, az, 3.0, a))
    add("arm_bolts", "M6 bolts, arm brackets (6)", fuse(fx), 13, "fixing", None)
    add("arm_spacers", "Crush spacers in the arm (4)", fuse(spacers + [zcyl(xx, 0, az, 5.0, a - 2 * wt) - zcyl(xx, 0, az, 2.75, a) for xx in hb_x]),
        13, "fixing", None)

    # ---- 8 to 10 sensor head (head frame, then tilted into place)
    hx, hy, hz = p["head"]
    hw = p["head_wall"]
    H = b.Pos(p["head_x"], 0, D["head_zc"]) * b.Rot(0, -p["tilt"], 0)
    shell = box(0, 0, 0, hx, hy, hz) - box(0, 0, -hw, hx - 2 * hw, hy - 2 * hw, hz)
    hood = box(p["hood_dx"], 0, hz / 2 + p["hood"][2] / 2, *p["hood"])
    lg = p["ledge"]
    iw, ih = hx - 2 * hw, hy - 2 * hw
    ledge = box(0, 0, -hz / 2 + 1.5, iw, ih, 3) - box(0, 0, -hz / 2 + 1.5, iw - 2 * lg, ih - 2 * lg, 5)
    sx_, sy_ = p["head_screws"]
    bosses = fuse(box(s1 * (iw / 2 - 5), s2 * (ih / 2 - 5), -hz / 2 + 3 + 6, 10, 10, 12) for s1 in (-1, 1) for s2 in (-1, 1))
    stand = fuse(zcyl(s1 * 12, s2 * 9, (-13 + hz / 2 - hw) / 2, 3.0, hz / 2 - hw + 13) for s1 in (-1, 1) for s2 in (-1, 1))
    housing = shell + hood + ledge + bosses + stand
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            housing -= zcyl(s1 * sx_, s2 * sy_, -hz / 2 + 6, 1.5, 12.2)
    gy = 15.0
    housing -= xcyl(-hx / 2 + hw / 2, gy, 0, 8.0, hw + 2)
    housing = H * housing
    # wedge pad: from the tilted hood top up to the arm underside, under the arm
    wx0, wx1 = p["wedge_x"]
    slab = bx(wx0, wx1, -a / 2, a / 2, D["arm_bot"] - 30, D["arm_bot"])
    below = H * box(0, 0, hz / 2 + p["hood"][2] - 500, 2000, 2000, 1000)
    wedge = slab - below
    for xx in hb_x:
        wedge -= zcyl(xx, 0, D["arm_bot"] - 5, 2.5, 10.01)
    add("housing", "Head housing with hood and wedge pad", housing + wedge, 8, "made", "housing")
    fw = p["frame_t"]
    film_t = p["window"][2]
    fr = box(0, 0, -hz / 2 - film_t - fw / 2, hx, hy, fw) - box(0, 0, -hz / 2 - film_t - fw / 2, iw - 2 * lg, ih - 2 * lg, fw + 2)
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            fr -= zcyl(s1 * sx_, s2 * sy_, -hz / 2 - film_t - fw / 2, 1.7, fw + 2)
    add("frame", "Window frame", H * fr, 8, "made", "housing")
    wx_, wy_, _ = p["window"]
    film = box(0, 0, -hz / 2 - film_t / 2, wx_, wy_, film_t)
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            film -= zcyl(s1 * sx_, s2 * sy_, -hz / 2 - film_t / 2, 1.75, 2)
    add("film", "Window film", H * film, 9, "bought", "window")
    add("frame_screws", "M3 screws, window frame (4)",
        H * fuse(zcyl(s1 * sx_, s2 * sy_, -hz / 2 - film_t - fw + 6, 1.5, 12) + zcyl(s1 * sx_, s2 * sy_, -hz / 2 - film_t - fw - 1, 2.75, 2)
                 for s1 in (-1, 1) for s2 in (-1, 1)), 13, "fixing", None)
    add("array", "Thermal array on its breakout", H * (zcyl(0, 0, -hz / 2 + 14, 4.7, 12) + box(0, 0, -hz / 2 + 21, 32, 26, 2)), 10, "bought", "array")
    add("head_bolts", "M5 bolts, head to arm (2)",
        fuse(hexprism("z", xx, 0, az + a / 2 + 1.75, 8.0, 3.5) + zcyl(xx, 0, (az + a / 2 + D["arm_bot"] - 10) / 2, 2.5, az + a / 2 - D["arm_bot"] + 10)
             for xx in hb_x), 13, "fixing", None)
    gl = (xcyl(-hx / 2 - 1.5, gy, 0, 10.0, 3.0) + xcyl(-hx / 2 - 3 - 7, gy, 0, 7.0, 14.0)
          + xcyl(-hx / 2 + hw / 2, gy, 0, 8.0, hw) + hexprism("x", -hx / 2 + hw + 2.5, gy, 0, 18.0, 5.0))
    add("head_gland", "Cable gland on the head, M16", H * gl, 13, "bought", None)

    # ---- 5 pole-top mount
    pt = D["pole_top"]
    ri, ro = D["sleeve_r_in"], D["sleeve_r_out"]
    slen = p["sleeve"][0]
    ct = D["cap_top"]
    sleeve = zcyl(px, 0, ct - slen / 2, ro, slen) - zcyl(px, 0, ct - slen / 2, ri, slen + 2)
    disc = zcyl(px, 0, pt + p["cap_t"] / 2, ri, p["cap_t"])
    zd = pt + p["cap_t"] / 2
    rad = [b.Pos(px + ((ri - 12) + ro) / 2 * math.cos(math.radians(45 + 90 * k)), ((ri - 12) + ro) / 2 * math.sin(math.radians(45 + 90 * k)), zd)
           * b.Rot(0, 0, 45 + 90 * k) * b.Rot(0, 90, 0) * b.Cylinder(2.0, ro - ri + 12) for k in range(4)]
    for s_ in rad:
        sleeve -= s_
        disc -= s_
    zs_ = D["sleeve_bot"] + 25
    riv, sets = [], []
    for k in range(3):
        R = b.Rot(0, 0, 120 * k)
        body = b.Pos(px, 0, zs_) * R * (b.Pos((ri + ro) / 2, 0, 0) * b.Rot(0, 90, 0) * (b.Cylinder(5.5, ro - ri) - b.Cylinder(4.0, ro - ri + 1))
                                        + b.Pos(ro + 0.75, 0, 0) * b.Rot(0, 90, 0) * (b.Cylinder(7.5, 1.5) - b.Cylinder(4.0, 2)))
        sleeve -= b.Pos(px, 0, zs_) * R * b.Pos((ri + ro) / 2, 0, 0) * b.Rot(0, 90, 0) * b.Cylinder(5.5, ro - ri + 1)
        riv.append(body)
        sets.append(b.Pos(px, 0, zs_) * R * (b.Pos((pr + ro + 1.5 + 8) / 2, 0, 0) * b.Rot(0, 90, 0) * b.Cylinder(4.0, ro + 1.5 + 8 - pr)))
    add("sleeve", "Sleeve", sleeve, 5, "made", "mount")
    add("disc", "Cap disc", disc, 5, "made", "mount")
    add("disc_screws", "M4 countersunk screws, cap disc (4)", fuse(rad), 13, "fixing", None)
    add("rivnuts", "M8 rivet nuts and set screws (3)", fuse(riv) + fuse(sets), 5, "bought", "mount")
    po, pw2, ph = p["post"]
    post = zcyl(px, 0, ct + ph / 2, po / 2, ph) - zcyl(px, 0, ct + ph / 2, po / 2 - pw2, ph + 2)
    pl_ = p["plug"][0]
    pz_low = [ct + 12.0, ct + 28.0]
    ptop = D["post_top"]
    pz_up = [ptop - 10.0, ptop - 26.0]
    plugs = zcyl(px, 0, ct + pl_ / 2, po / 2 - pw2, pl_) + zcyl(px, 0, ptop - pl_ / 2, po / 2 - pw2, pl_)
    for zz in pz_low + pz_up:
        post -= ycyl(px, 0, zz, 4.25, po + 2)
        plugs -= ycyl(px, 0, zz, 4.25, po + 2)
    add("post", "Post", post, 5, "made", "mount")
    add("plugs", "Post plugs (2)", plugs, 5, "made", "mount")
    cl_, ctk, clen = p["pclip"]
    rpo = po / 2
    low = []
    lowfix = []
    for s in (1, -1):
        y0, y1 = s * rpo, s * (rpo + ctk)
        leg_v = bx(px - clen / 2, px + clen / 2, min(y0, y1), max(y0, y1), ct, ct + cl_)
        yh = s * (rpo + 30)
        leg_h = bx(px - clen / 2, px + clen / 2, min(y0, yh), max(y0, yh), ct, ct + ctk)
        cl = leg_v + leg_h
        for zz in pz_low:
            cl -= ycyl(px, (y0 + y1) / 2, zz, 4.25, ctk + 2)
        for dx in (-9, 9):
            cl -= zcyl(px + dx, s * (rpo + 19), ct + ctk / 2, 2.75, ctk + 2)
            lowfix.append(zcyl(px + dx, s * (rpo + 19), ct - p["cap_t"] / 2 + ctk / 2, 2.75, p["cap_t"] + ctk)
                          + hexprism("z", px + dx, s * (rpo + 19), ct + ctk + 2.25, 8.0, 4.5))
        low.append(cl)
    add("lclip_r", "Lower post clip (right)", low[1], 5, "made", "mount")
    add("lclip_l", "Lower post clip (left)", low[0], 5, "made", "mount")
    # disc holes for the lower clip screws
    dd = C["disc"].shape
    for dx in (-9, 9):
        for s in (1, -1):
            dd -= zcyl(px + dx, s * (rpo + 19), pt + p["cap_t"] / 2, 2.75, p["cap_t"] + 2)
    C["disc"].shape = dd
    # upper clips and rail plate, built in the rail frame: s along the slope, y across, m along the plate normal
    P0, u, n = D["rail_P0"], D["rail_u"], D["rail_n"]
    tp = p["panel_tilt"]
    RF = b.Pos(*P0) * b.Rot(0, -tp, 0)        # local x = s, local z = m
    s0, s1 = p["upper_clip_s"]
    up = []
    upfix = []
    for s in (1, -1):
        y0, y1 = s * rpo, s * (rpo + ctk)
        leg_v = bx(s0, s1, min(y0, y1), max(y0, y1), -cl_, 0)
        yh = s * (rpo + cl_)
        leg_h = bx(s0, s1, min(y0, yh), max(y0, yh), -ctk, 0)
        cl = RF * (leg_v + leg_h)
        for zz in pz_up:
            cl -= ycyl(px, (y0 + y1) / 2, zz, 4.25, ctk + 2)
        for ss in (-30.0, -15.0):
            cl -= RF * zcyl(ss, s * (rpo + 30), -ctk / 2, 2.75, ctk + 2)
        up.append(cl)
    add("uclip_r", "Upper post clip (right)", up[1], 5, "made", "mount")
    add("uclip_l", "Upper post clip (left)", up[0], 5, "made", "mount")
    rl, rw, rt = p["hinge"]
    rail = bx(-rl / 2, rl / 2, -rw / 2, rw / 2, 0, rt)
    for s in (1, -1):
        for ss in (-30.0, -15.0):
            rail -= zcyl(ss, s * (rpo + 30), rt / 2, 2.75, rt + 2)
            upfix.append(zcyl(ss, s * (rpo + 30), (rt - ctk) / 2, 2.5, rt + ctk) + zcyl(ss, s * (rpo + 30), rt + 1.4, 4.5, 2.8)
                         + hexprism("z", ss, s * (rpo + 30), -ctk - 2.0, 8.0, 4.0))
    pw, pln, pth = p["panel"]
    lip = 12.0
    for sl in (-1, 1):
        for yy in (-50.0, 50.0):
            rail -= zcyl(sl * (pw / 2 - lip / 2), yy, rt / 2, 2.25, rt + 2)
            upfix.append(zcyl(sl * (pw / 2 - lip / 2), yy, (rt + 4) / 2 - 0.5, 2.0, rt + 5) + hexprism("z", sl * (pw / 2 - lip / 2), yy, -1.4, 7.0, 2.8))
    rail -= zcyl(0, rw / 2 - 12, rt / 2, 3.0, rt + 2)       # lanyard hole
    for sl in (-1, 1):                                       # lightening windows between the clips and the lip bolts
        rail -= b.Pos(sl * 85.0, 0, rt / 2) * b.extrude(b.RectangleRounded(90, 90, 6), rt / 2 + 1, both=True)
    add("rail", "Rail plate", RF * rail, 5, "made", "mount")
    add("panel", "Solar panel, 6 W", RF * box(0, 0, rt + pth / 2, pw, pln, pth), 4, "bought", "panel")
    cbolts = [_bolt_y(-(rpo + ctk), rpo + ctk, px, zz, 8.0, 13.0) for zz in pz_low + pz_up]
    add("post_bolts", "M8 bolts, post clips (4)", fuse(cbolts), 13, "fixing", None)
    add("clip_screws", "M5 screws, clips to disc and rail plate (8); M4 bolts, panel lip (4)",
        fuse(lowfix) + RF * fuse(upfix), 13, "fixing", None)

    # ---- 11 sensor cable and panel lead, tied to the pole on its +Y side, over the bands
    cr = p["cable_d"] / 2
    R = p["cable_r"]
    th_s, th_p = (math.radians(t_) for t_ in p["cable_theta"])
    cs = (px + R * math.cos(th_s), R * math.sin(th_s))
    cpl = (px + R * math.cos(th_p), R * math.sin(th_p))
    pa = port_world("port_a", p)
    g1 = port_world("gland_1", p)
    eb = D["enc_bot"]
    zc1, zc2 = eb - 65.0, eb - 90.0
    gx, gyw, gzw = head_frame_point(-hx / 2 - 17, gy, 0, p)
    gx2, _, gzw2 = head_frame_point(-hx / 2 - 37, gy, 0, p)
    ap = D["arm_plate_front"]
    zarm = az - 30.0
    sensor = [(pa[0], pa[1], eb - 70), (pa[0], pa[1], zc2), (cs[0] - 25, cs[1], zc2), (cs[0], cs[1], zc2),
              (cs[0], cs[1], zarm), (px + 40, 88.0, zarm), (ap + cr, 88.0, zarm), (ap + cr, a / 2 + cr, zarm),
              (ap + cr + 10, a / 2 + cr, az), (gx - 40, a / 2 + cr, az), (gx - 40, a / 2 + cr, az - 35), (gx2, gy, gzw2), (gx, gy, gzw)]
    plug = zcyl(pa[0], pa[1], eb - 22 - 24, 8.0, 48)
    add("cable", "Sensor cable with M12 plug", _route(sensor, cr) + plug, 11, "bought", "cable")
    lead = [(cpl[0], cpl[1], D["sleeve_bot"] - 20), (cpl[0], cpl[1], zc1), (g1[0] + 15, g1[1], zc1), (g1[0], g1[1], zc1),
            (g1[0], g1[1], eb - 17)]
    add("panel_lead", "Panel extension lead", _route(lead, cr), 13, "bought", None)

    # ---- 12 notice plate, tied through slots
    nt, nw, nh = p["notice"]
    tw, tt, ty, tz = p["notice_tie"]
    nplate = _plate_local(nt, nw, nh, (), [(v, z, 3.0, tw + 2) for v in (-ty, ty) for z in (-tz, tz)])
    nz = p["notice_z"]
    add("notice", "Public notice plate", _to_world(nplate, 1, px - pr, nz), 12, "made", "notice")
    ties = fuse(b.Pos(0, 0, z) * _band_local(pr, pr, ty, nt, tw, tt) for z in (-tz, tz))
    add("notice_ties", "Stainless cable ties, notice plate (2)", _to_world(ties, 1, px - pr, nz), 12, "bought", "notice")
    return C


def cable_routes(p=PARAMS):
    """Lengths of the two cable runs (mm), from the same points as the model."""
    C = build_components(p)
    return {k: C[k].shape.volume / (math.pi * (p["cable_d"] / 2) ** 2) for k in ("cable", "panel_lead")}


def build_parts(p=PARAMS):
    """Return {BOM group key: solid} for the BOM lines with geometry. Fixings are left out."""
    C = build_components(p)
    out = {}
    for c in C.values():
        if c.group:
            out[c.group] = c.shape if c.group not in out else out[c.group] + c.shape
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
    pts = [(min(max(x, -p["sidewalk_w"] + 5), p["road_w"] - 5), min(max(y, -L / 2 + 5), L / 2 - 5))
           for x, y in footprint_outline(p)]
    pts = [q for i, q in enumerate(pts) if math.dist(q, pts[i - 1]) > 1.0]
    face = make_face(Polyline(*[(x, y, 0) for x, y in pts], close=True))
    slab = extrude(face, 3)
    fp = (Pos(0, 0, p["sw_h"] + 1) * (slab & Pos(-5000, 0, 0) * Box(10000, 2 * L, 20))
          + Pos(0, 0, 1) * (slab & Pos(5000, 0, 0) * Box(10000, 2 * L, 20)))
    return {"pole": pole, "street": sw + road + lines, "footprint": fp}


def pole_stub(z0, z1, p=PARAMS):
    D = derived(p)
    return zcyl(p["pole_x"], 0, (z0 + z1) / 2, D["pole_r"], z1 - z0)


def assembly(p=PARAMS, with_context=True):
    from build123d import Compound
    kids = [c.shape for c in build_components(p).values()]
    if with_context:
        kids += [context_parts(p)["pole"]]
    return Compound(children=kids)


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch or stay apart. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    D = derived(p)
    pole = context_parts(p)["pole"]
    S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # enclosure saddle
    for k in ("enc_vs_up", "enc_vs_low"):
        chk(f"{C[k].name} on the enclosure plate", S(k), S("enc_plate"), "touch")
        chk(f"{C[k].name} on the pole (V faces)", S(k), pole, "touch")
        chk(f"{C[k].name} clear of the bands", S(k), S("enc_bands"), 3.0)
    chk("Enclosure bands on the pole", S("enc_bands"), pole, "touch")
    chk("Enclosure bands through the slots and across the plate front", S("enc_bands"), S("enc_plate"), "touch")
    chk("Enclosure plate clear of the pole", S("enc_plate"), pole, 5.0)
    chk("Enclosure body on the plate", S("body"), S("enc_plate"), "touch")
    chk("Lugs on the plate", S("lugs"), S("enc_plate"), "touch")
    chk("Lugs against the enclosure", S("lugs"), S("body"), "touch")
    chk("Lug screws clear of the bands", S("lug_screws"), S("enc_bands"), 5.0)
    chk("Lug screws clear of the pole", S("lug_screws"), pole, 5.0)
    chk("Enclosure clear of the bands", S("body", "lid", "lugs"), S("enc_bands"), 5.0)
    chk("Lid on the body", S("lid"), S("body"), "touch")
    chk("Internal plate on the bosses", S("mplate"), S("body"), "touch")
    for k in ("cell", "power", "ctrl", "connectors"):
        chk(f"{C[k].name} on the internal plate", S(k), S("mplate"), "touch")
        chk(f"{C[k].name} clear of the lid", S(k), S("lid"), 1.0)
    for k in ("glands", "ports", "vent", "antenna"):
        chk(f"{C[k].name} in the bottom face", S(k), S("body"), "touch")
        chk(f"{C[k].name} clear of the internal plate and strip", S(k), S("mplate", "connectors"), 1.0)
    names = ("glands", "ports", "vent", "antenna")
    for i, a_ in enumerate(names):
        for b2 in names[i + 1:]:
            chk(f"{C[a_].name} apart from {C[b2].name}", S(a_), S(b2), 4.0)
    # arm saddle, arm and brackets
    for k in ("arm_vs_up", "arm_vs_low"):
        chk(f"{C[k].name} on the arm plate", S(k), S("arm_plate"), "touch")
        chk(f"{C[k].name} on the pole (V faces)", S(k), pole, "touch")
        chk(f"{C[k].name} clear of the bands", S(k), S("arm_bands"), 3.0)
        chk(f"{C[k].name} clear of the bracket bolts", S(k), S("arm_bolts"), 2.0)
    chk("Arm bands on the pole", S("arm_bands"), pole, "touch")
    chk("Arm bands through the slots and across the plate front", S("arm_bands"), S("arm_plate"), "touch")
    chk("Arm bands clear of the brackets", S("arm_bands"), S("arm_brk_up", "arm_brk_low"), 5.0)
    chk("Arm plate clear of the pole", S("arm_plate"), pole, 5.0)
    chk("Arm tube butts the plate", S("arm_tube"), S("arm_plate"), "touch")
    for k in ("arm_brk_up", "arm_brk_low"):
        chk(f"{C[k].name} on the plate", S(k), S("arm_plate"), "touch")
        chk(f"{C[k].name} on the tube", S(k), S("arm_tube"), "touch")
    chk("Bracket bolt nuts clear of the pole", S("arm_bolts"), pole, 2.0)
    chk("Crush spacers inside the tube", S("arm_spacers"), S("arm_tube"), "touch")
    chk("End cap on the tube", S("arm_cap"), S("arm_tube"), "touch")
    # head
    chk("Head wedge pad under the arm", S("housing"), S("arm_tube"), "touch")
    chk("Head housing clear of the arm cap", S("housing"), S("arm_cap"), 0.0)
    chk("Film on the housing ledge", S("film"), S("housing"), "touch")
    chk("Window frame on the film", S("frame"), S("film"), "touch")
    chk("Window frame clear of the housing (film between)", S("frame"), S("housing"), 0.4)
    chk("Array on its standoffs", S("array"), S("housing"), "touch")
    chk("Array lens clear of the film", S("array"), S("film"), 3.0)
    chk("Head gland in the end wall", S("head_gland"), S("housing"), "touch")
    chk("Head bolts in the arm and pad", S("head_bolts"), S("arm_tube"), "touch")
    chk("Head clear of the pole", S("housing", "frame"), pole, 300.0)
    # pole-top mount
    chk("Cap disc on the pole top", S("disc"), pole, "touch")
    chk("Cap disc inside the sleeve", S("disc"), S("sleeve"), "touch")
    chk("Sleeve clear of the pole (set screws centre it)", S("sleeve"), pole, 3.0)
    chk("Set screws on the pole", S("rivnuts"), pole, "touch")
    chk("Post on the cap disc", S("post"), S("disc"), "touch")
    chk("Plugs inside the post", S("plugs"), S("post"), "touch")
    for k in ("lclip_r", "lclip_l"):
        chk(f"{C[k].name} on the disc", S(k), S("disc"), "touch")
        chk(f"{C[k].name} against the post", S(k), S("post"), "touch")
    for k in ("uclip_r", "uclip_l"):
        chk(f"{C[k].name} under the rail plate", S(k), S("rail"), "touch")
        chk(f"{C[k].name} against the post", S(k), S("post"), "touch")
    chk("Rail plate clear of the post top", S("rail"), S("post", "plugs"), 3.0)
    chk("Panel on the rail plate", S("panel"), S("rail"), "touch")
    chk("Panel clear of the sleeve", S("panel"), S("sleeve"), 50.0)
    chk("Panel clear of the post", S("panel"), S("post", "plugs"), 5.0)
    chk("Post bolts clear of the panel", S("post_bolts"), S("panel"), 5.0)
    # cables
    chk("Sensor cable clear of the bands", S("cable"), S("enc_bands", "arm_bands"), 0.2)
    chk("Sensor cable clear of the V-saddles", S("cable"), S("enc_vs_up", "enc_vs_low", "arm_vs_up", "arm_vs_low"), 5.0)
    chk("Sensor cable clear of the enclosure plate", S("cable"), S("enc_plate"), 5.0)
    chk("Sensor cable along the arm plate and bracket", S("cable"), S("arm_plate", "arm_brk_low"), "touch")
    chk("Sensor cable along the arm", S("cable"), S("arm_tube"), "touch")
    chk("Sensor cable into the head gland", S("cable"), S("head_gland"), "touch")
    chk("Sensor cable clear of the antenna whip", S("cable"), S("antenna"), 10.0)
    chk("Sensor cable clear of the hood", S("cable"), S("housing"), 3.0)
    chk("Sensor cable clear of the panel lead", S("cable"), S("panel_lead"), 0.3)
    chk("Panel lead clear of the bands", S("panel_lead"), S("enc_bands", "arm_bands"), 0.2)
    chk("Panel lead clear of the V-saddles", S("panel_lead"), S("enc_vs_up", "enc_vs_low", "arm_vs_up", "arm_vs_low"), 5.0)
    chk("Panel lead clear of the plates", S("panel_lead"), S("enc_plate", "arm_plate"), 5.0)
    chk("Panel lead into gland 1", S("panel_lead"), S("glands"), "touch")
    chk("Panel lead clear of the set screws", S("panel_lead"), S("rivnuts", "sleeve"), 2.0)
    chk("Sensor cable plug on port A", S("cable"), S("ports"), "touch")
    # notice
    chk("Notice plate on the pole", S("notice"), pole, "touch")
    chk("Notice ties on the pole", S("notice_ties"), pole, "touch")
    chk("Notice ties through the plate", S("notice_ties"), S("notice"), "touch")
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    pole = context_parts()["pole"]
    head = [k for k, c in C.items() if c.bom in (7, 8, 9, 10) or k in ("arm_bolts", "arm_spacers", "arm_vs_screws", "head_bolts",
                                                                         "frame_screws", "head_gland")]
    core = [k for k in C if k not in head and k not in ("cable", "notice", "notice_ties")]
    groups = {
        "curbcount-assembly": [c.shape for c in C.values()] + [pole],
        "sensor-head": [C[k].shape for k in head],
        "power-core": [C[k].shape for k in core],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"arm {D['arm_len']:.0f} mm, head reach from pole axis {D['reach']:.0f} mm, arm axis at {D['arm_z']:.0f} mm; "
          f"panel top {D['panel_top']:.0f} mm above the road; footprint across {D['fp_x_min']:.0f} to {D['fp_x_max']:.0f} mm; "
          f"pole axis to saddle plate back {D['vs_offset']:.1f} mm")
    print_checks()
