"""CurbCount product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the privacy-safe street counter: a filleted
sensor head with its sun hood, a dark window bezel with a parting step, the HDPE window and the
thermal array visible behind it, a teal "counts only" plaque and a lit status light; a rounded
aluminium arm with an end cap on its saddle plate; stainless band clamps with worm-drive
housings; the FieldNode enclosure with its lid, lid screws, label, status light, knurled M12
ports, cable gland, vent and whip antenna; the power board, controller and LiFePO4 cell inside;
the 6 W panel with cell grid, glass and junction box on its pole-top mount; the sensor cable with
rounded bends; and the public notice plate with raised text stating that counting happens on the
device and no images are taken or stored. Context is a short section of the 114 mm street pole.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build_parts() in model.py.
Axes as model.py: road at Z = 0, curb face at X = 0, sidewalk toward -X, street along Y.
The sensor head, arm, saddles, clamps, enclosure and cable are at their model.py positions.
For a compact product render two things are shown closer than installed (see docs/REVIEW.md,
session 2026-09-26): the pole top with its mount and panel is drawn TOP_DROP lower, and the
public notice plate is drawn just above the enclosure (NOTICE_Z) instead of at eye height.
All sizes are unchanged.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build123d import (Align, Axis, Box, Cylinder, Plane, Pos, RectangleRounded, Rot, Solid, Sphere,
                       Text, Vector, extrude, fillet)
from model import PARAMS, derived, build_parts

TITLE = "CurbCount: privacy-safe street counter for people, bikes and vehicles"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 20, "az": -128,
     "note": "Product render from the sidewalk side, front left and above (about 20 deg elevation); notice plate "
             "and FieldNode enclosure on the pole, sensor head on its arm reaching over the street. Pole top and "
             "notice are drawn closer than installed"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -128,
     "note": "Exploded view from the sidewalk side, front left and above (about 28 deg elevation): sensor head "
             "housing, hood, window, bezel and thermal array; arm and clamps; enclosure, lid, power board, "
             "controller and cell; solar panel and pole-top mount; notice plate"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 14, "az": -40,
     "note": "Detail from the street side, front right and slightly above (about 14 deg elevation), without the "
             "pole: sensor head tilted toward the road in front, arm, clamps and enclosure behind"},
]

# Render layout (not the installed layout); see the module docstring.
TOP_DROP = 560.0          # pole top, sleeve, post, hinge plate and panel drawn this much lower
NOTICE_Z = 4150.0         # notice plate centre, drawn between the enclosure saddle and the arm clamps
POLE_Z0 = 3500.0          # bottom of the context pole section

# Colours (restrained product palette; kit accent)
C_HEAD = "#EEF0F2"
C_HOOD = "#D5D9DE"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_WHITE = "#F7F7F5"
C_ALU = "#C4C9CF"
C_STEEL = "#B8BEC6"
C_ENC = "#DADDE1"
C_LID = "#E6E8EB"
C_WINDOW = "#E4ECF0"
C_PCB = "#166534"
C_PCB_DARK = "#1A1D21"
C_CHIP = "#111827"
C_CELL = "#1E3A8A"
C_PV = "#1C2B4A"
C_GLASS = "#DCEBF5"
C_TEXT = "#1F2937"
C_LED = "#22C55E"
C_POLE = "#8C9197"
C_BRASS = "#C9A227"
FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")


# ------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _rbox(lx, ly, lz, r_z=0.0, r_top=0.0, r_bot=0.0, axis=Axis.Z):
    """Box centred at the origin; fillet the edges parallel to `axis` (r_z), then the +axis face
    edges (r_top) and the -axis face edges (r_bot), each with smaller fallbacks."""
    b = Box(lx, ly, lz)
    if r_z:
        b = _fillet_try(b, b.edges().filter_by(axis), [r_z, r_z * 0.6, r_z * 0.3])
    faces = b.faces().sort_by(axis)
    if r_top:
        b = _fillet_try(b, faces[-1].edges(), [r_top, r_top * 0.6, r_top * 0.3])
    faces = b.faces().sort_by(axis)
    if r_bot:
        b = _fillet_try(b, faces[0].edges(), [r_bot, r_bot * 0.6, r_bot * 0.3])
    return b


def _tube(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _text(txt, size, plane, h=0.4, font=FONT):
    """Raised text on `plane` (x_dir reads left to right, z_dir out of the surface)."""
    t = Text(txt, font_size=size, font_path=font, align=(Align.CENTER, Align.CENTER))
    return extrude(plane * t, amount=h)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _band(x, z, r_in, w, ang_deg=-135.0):
    """Stainless band clamp: ring round the pole with a worm-drive housing and screw."""
    ring = Pos(x, 0, z) * (Cylinder(r_in + 1.2, w) - Cylinder(r_in, w + 2))
    a = math.radians(ang_deg)
    rr = r_in + 1.2
    hx, hy = x + (rr + 2.5) * math.cos(a), (rr + 2.5) * math.sin(a)
    rot = Rot(0, 0, ang_deg + 90.0)
    housing = Pos(hx, hy, z) * rot * _rbox(18.0, 5.0, w + 2.0, r_z=0.0, r_top=0.0)
    housing = _fillet_try(housing, housing.edges().filter_by(Axis.Z), [1.2, 0.6])
    sx, sy = x + (rr + 6.5) * math.cos(a), (rr + 6.5) * math.sin(a)
    screw = Pos(sx, sy, z) * rot * Rot(0, 90, 0) * Cylinder(3.2, 22.0)
    head = Pos(sx, sy, z) * rot * Pos(12.5, 0, 0) * Rot(0, 90, 0) * Cylinder(4.2, 3.0)
    return ring + housing + screw + head


# ------------------------------------------------------------------ parts
def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    pr = D["pole_r"]
    px = P["pole_x"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ============ sensor head (BOM 8, 9, 10), in the head frame of model.py
    hx, hy, hz = P["head"]
    hw = P["head_wall"]
    HF = Pos(P["head_x"], 0, D["head_zc"]) * Rot(0, -P["tilt"], 0)
    bez_h = 6.0
    E_HEAD = (0, 0, 0)

    shell = _rbox(hx, hy, hz, r_z=12.0, r_top=4.0)
    shell -= Pos(0, 0, -hw) * _rbox(hx - 2 * hw, hy - 2 * hw, hz, r_z=9.0)
    shell &= Pos(0, 0, bez_h / 2 + 0.3) * Box(hx + 2, hy + 2, hz - bez_h + 0.6)   # stops above the bezel
    add("Sensor head housing (ASA)", HF * shell, C_HEAD, "plastic", 8, "shell", E_HEAD)

    hood = Pos(10, 0, hz / 2 + P["hood"][2] / 2) * _rbox(*P["hood"], r_z=14.0, r_top=1.5, r_bot=0.8)
    add("Sun hood", HF * hood, C_HOOD, "plastic", 8, "shell", (0, 0, 110))

    # bezel frame: slightly inset for a visible parting step, window slot, open aperture
    wx, wy, _ = P["window"]
    bez = Pos(0, 0, -hz / 2 + bez_h / 2) * _rbox(hx - 1.0, hy - 1.0, bez_h, r_z=11.5, r_bot=1.5)
    bez -= Pos(0, 0, -hz / 2) * _rbox(wx - 8, wy - 8, 2 * bez_h + 2, r_z=5.0)
    bez -= Pos(0, 0, -hz / 2 + 2) * Box(wx + 0.4, wy + 0.4, 1.2)
    bez -= Pos(0, 0, -hz / 2 + bez_h) * _rbox(wx + 0.4, wy + 0.4, 5.0, r_z=5.0)
    add("Window bezel and gasket", HF * bez, C_DARK, "rubber", 8, "shell", (0, 0, -150))
    win = Pos(0, 0, -hz / 2 + 2) * _rbox(wx, wy, 1.0, r_z=4.0)
    add("LWIR window, HDPE", HF * win, C_WINDOW, "clear", 9, "shell", (0, 0, -110))

    # thermal array: breakout board, sensor can and lens, as model.py
    brd = Pos(0, 0, -hz / 2 + 21) * _rbox(32, 26, 1.6, r_z=1.5)
    brd += Pos(0, 11.0, -hz / 2 + 22.6) * Box(10.0, 3.0, 1.6)                          # I2C header
    add("Thermal array breakout", HF * brd, C_PCB_DARK, "plastic", 10, "internal", (0, 0, -70))
    can = Pos(0, 0, -hz / 2 + 14) * Cylinder(4.7, 12)
    can = _fillet_try(can, can.faces().sort_by(Axis.Z)[0].edges(), [0.8, 0.4])
    add("Thermal array can", HF * can, C_STEEL, "metal", 10, "internal", (0, 0, -70))
    lens = Pos(0, 0, -hz / 2 + 8.2) * Sphere(2.2) & Pos(0, 0, -hz / 2 + 7.0) * Box(6, 6, 2.6)
    add("Thermal array lens", HF * lens, C_BLACK, "screen", 10, "internal", (0, 0, -70))

    # teal "counts only" plaque on the -Y face and status light
    fy = -hy / 2
    plq = Pos(0, fy - 0.3, 6.0) * _rbox(64.0, 0.6, 16.0, r_z=0.0)
    plq = _fillet_try(plq, plq.edges().filter_by(Axis.Y), [3.0, 1.5])
    add("Head plaque", HF * plq, C_ACCENT, "plastic", 8, "shell", E_HEAD)
    pl = Plane(origin=(0, fy - 0.6, 6.0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    add("Head plaque text", HF * _text("COUNTS ONLY", 7.0, pl, 0.3), C_WHITE, "plastic", 8, "shell", E_HEAD)
    led = Pos(-40.0, fy, 22.0) * (Sphere(2.2) & Pos(0, -2, 0) * Box(5, 4, 5))
    add("Head status light", HF * led, C_LED, "emissive", 8, "shell", E_HEAD)

    # ============ arm (BOM 7): rounded 40 x 40 tube, end cap, saddle plate and bolts
    a, at = P["arm"]
    az_ = D["arm_z"]
    L = D["arm_len"]
    prof = Plane.YZ * (RectangleRounded(a, a, 3.0) - RectangleRounded(a - 2 * at, a - 2 * at, 1.2))
    tube = Pos(D["arm_x0"], 0, az_) * extrude(prof, amount=L - 3.0)
    add("Aluminium sensor arm", tube, C_ALU, "metal", 7, "shell", (0, 0, 0))
    cap = Pos(D["arm_x1"] - 1.5, 0, az_) * _rbox(3.0, a, a, r_z=0.0)
    cap = _fillet_try(cap, cap.edges().filter_by(Axis.X), [3.0, 1.5])
    cap = _fillet_try(cap, cap.faces().sort_by(Axis.X)[-1].edges(), [1.2, 0.6])
    add("Arm end cap", cap, C_BLACK, "plastic", 7, "shell", (60, 0, 0))
    sx, sy, sz = P["saddle"]
    sad = Pos(D["saddle_x"], 0, az_) * _rbox(sx, sy, sz, r_z=10.0, axis=Axis.X)
    sad = _fillet_try(sad, sad.faces().sort_by(Axis.X)[-1].edges(), [1.0, 0.5])
    add("Arm saddle plate", sad, C_ALU, "metal", 7, "shell", (0, 0, 0))
    # two bolts through the arm into the hood mounting boss
    bolts = []
    for bx in (P["head_x"] - 25.0, P["head_x"] + 25.0):
        h = Pos(bx, 0, az_ + a / 2 + 1.5) * Cylinder(6.5, 3.0)
        h = _fillet_try(h, h.faces().sort_by(Axis.Z)[-1].edges(), [0.8, 0.4])
        bolts.append(h)
    add("Head mounting bolts", _union(bolts), C_STEEL, "metal", 13, "shell", (0, 0, 60))

    # ============ band clamps (BOM 6): four bands, enclosure saddle plate
    bw = P["band_w"]
    for i, z in enumerate((P["enc_zc"] - P["enc_plate"][2] / 2 + 40, P["enc_zc"] + P["enc_plate"][2] / 2 - 40)):
        add(f"Enclosure band clamp {i + 1}", _band(px, z, pr, bw), C_STEEL, "metal", 6, "shell", (0, 0, 0))
    for i, z in enumerate((az_ - P["arm_band_dz"], az_ + P["arm_band_dz"])):
        band = _band(px, z, pr, bw)
        band += Pos(D["arm_x0"] + 0.6, 0, z) * Box(1.2, sy + 2.0, bw)                    # over the saddle face
        add(f"Arm band clamp {i + 1}", band, C_STEEL, "metal", 6, "shell", (0, 0, 0))
    tx, ty, tz = P["enc_plate"]
    eplate = Pos(D["enc_plate_x"], 0, P["enc_zc"]) * _rbox(tx, ty, tz, r_z=10.0, axis=Axis.X)
    add("Enclosure saddle plate", eplate, C_ALU, "metal", 6, "shell", (-60, 0, 0))

    # ============ FieldNode enclosure (BOM 1): body, lid, screws, label, light, ports, gland, vent, whip
    ex, ey, ez = D["enc_dims_xyz"]
    w = P["enc_wall"]
    ecx, ecz = D["enc_xc"], P["enc_zc"]
    x_back = ecx + ex / 2                   # pole side
    x_front = ecx - ex / 2                  # lid side (sidewalk)
    lid_t = 12.0
    E_ENC = (-130, 0, 0)
    E_LID = (-330, 0, 0)

    body = Pos(ecx, 0, ecz) * _rbox(ex, ey, ez, r_z=8.0, r_top=0.0, axis=Axis.X)
    body = _fillet_try(body, body.faces().sort_by(Axis.X)[-1].edges(), [2.0, 1.0])
    body -= Pos(ecx - w, 0, ecz) * _rbox(ex, ey - 2 * w, ez - 2 * w, r_z=5.5, axis=Axis.X)
    # lid seat step (parting line)
    body -= Pos(x_front + 1.0, 0, ecz) * (Box(2.0, ey + 2, ez + 2) - _rbox(4.0, ey - 1.6, ez - 1.6, r_z=7.2, axis=Axis.X))
    add("FieldNode enclosure body", body, C_ENC, "plastic", 1, "shell", E_ENC)

    lid = Pos(x_front - lid_t / 2, 0, ecz) * _rbox(lid_t, ey, ez, r_z=8.0, axis=Axis.X)
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.X)[0].edges(), [3.0, 2.0, 1.0])
    lid -= Pos(x_front - lid_t, 0, ecz) * _rbox(1.2, ey - 30, ez - 30, r_z=6.0, axis=Axis.X)   # shallow panel
    xl = x_front - lid_t
    for (yy, zz) in ((-ey / 2 + 9, ecz - ez / 2 + 9), (ey / 2 - 9, ecz - ez / 2 + 9),
                     (-ey / 2 + 9, ecz + ez / 2 - 9), (ey / 2 - 9, ecz + ez / 2 - 9)):
        lid -= Pos(xl + 0.8, yy, zz) * Rot(0, 90, 0) * Cylinder(3.6, 2.0)                # screw counterbores
    add("FieldNode enclosure lid", lid, C_LID, "plastic", 1, "shell", E_LID)
    screws = []
    for (yy, zz) in ((-ey / 2 + 9, ecz - ez / 2 + 9), (ey / 2 - 9, ecz - ez / 2 + 9),
                     (-ey / 2 + 9, ecz + ez / 2 - 9), (ey / 2 - 9, ecz + ez / 2 - 9)):
        s = Pos(xl + 0.4, yy, zz) * Rot(0, 90, 0) * Cylinder(2.9, 1.2)
        s -= Pos(xl - 0.1, yy, zz) * Box(0.6, 3.6, 0.8)
        s -= Pos(xl - 0.1, yy, zz) * Box(0.6, 0.8, 3.6)
        screws.append(s)
    add("Lid screws", _union(screws), C_STEEL, "metal", 13, "shell", E_LID)
    xf = xl + 1.2                                              # floor of the shallow lid panel
    lab = Pos(xf - 0.2, 0, ecz + 38) * _rbox(0.4, 96.0, 44.0, r_z=3.0, axis=Axis.X)
    add("Enclosure label", lab, C_WHITE, "paper", 1, "shell", E_LID)
    lp = Plane(origin=(xf - 0.4, 0, ecz + 46), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))
    lp2 = Plane(origin=(xf - 0.4, 0, ecz + 30), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))
    ltxt = _text("CurbCount", 11.0, lp, 0.3) + _text("FieldNode core", 6.5, lp2, 0.3)
    add("Enclosure label text", ltxt, C_ACCENT, "plastic", 1, "shell", E_LID)
    ring = Pos(xf - 0.6, 0, ecz - 40) * Rot(0, 90, 0) * (Cylinder(5.0, 1.2) - Cylinder(3.0, 2.0))
    add("Status light bezel", ring, C_DARK, "plastic", 1, "shell", E_LID)
    sled = Pos(xf, 0, ecz - 40) * (Sphere(3.0) & Pos(-2, 0, 0) * Box(4, 8, 8))
    add("Enclosure status light", sled, C_LED, "emissive", 1, "shell", E_LID)

    zb = D["enc_bot"]
    # M12 ports: knurled nickel nuts (the -40 port takes the sensor cable, the -10 port is capped)
    for i, yy in enumerate((-40.0, -10.0)):
        nut = Pos(ecx, yy, zb - 12) * Cylinder(P["m12_d"] / 2, 24)
        for k in range(18):
            ang = 360.0 * k / 18
            nut -= Pos(ecx, yy, zb - 14) * Rot(0, 0, ang) * Pos(P["m12_d"] / 2, 0, 0) * Box(1.0, 1.0, 16.0)
        nut = _fillet_try(nut, nut.faces().sort_by(Axis.Z)[0].edges(), [0.8, 0.4])
        add(f"M12 port {i + 1}", nut, C_STEEL, "metal", 1, "shell", E_ENC)
    bcap = Pos(ecx, -10.0, zb - 27) * Cylinder(7.5, 6.0)
    bcap = _fillet_try(bcap, bcap.faces().sort_by(Axis.Z)[0].edges(), [2.0, 1.0])
    add("M12 blanking cap", bcap, C_BLACK, "rubber", 13, "shell", E_ENC)
    gland = Pos(ecx, 18.0, zb - 3.5) * Cylinder(10.0, 7.0)
    gland += Pos(ecx, 18.0, zb - 11) * Cylinder(8.0, 8.0)
    gland = _fillet_try(gland, gland.faces().sort_by(Axis.Z)[0].edges(), [2.5, 1.2])
    add("Cable gland M16", gland, C_DARK, "plastic", 1, "shell", E_ENC)
    vent = Pos(ecx + 22.0, -62.0, zb - 2.5) * Cylinder(6.0, 5.0)
    vent = _fillet_try(vent, vent.faces().sort_by(Axis.Z)[0].edges(), [1.5, 0.8])
    add("ePTFE vent", vent, C_DARK, "plastic", 1, "shell", E_ENC)
    wr, wl = P["whip"][0] / 2, P["whip"][1]
    wbase = Pos(ecx, 50.0, zb - 12) * Cylinder(wr + 2.5, 24)
    add("Antenna base", wbase, C_STEEL, "metal", 1, "shell", E_ENC)
    whip = Pos(ecx, 50.0, zb - 24 - (wl - 24 - wr) / 2) * Cylinder(wr, wl - 24 - wr)
    whip += Pos(ecx, 50.0, zb - wl + wr) * Sphere(wr)
    add("Whip antenna", whip, C_BLACK, "rubber", 1, "shell", E_ENC)

    # ============ internals (BOM 2, 3)
    E_INT = (-230, 0, 0)
    bx_, by_, bz_ = P["board"]
    bcx, bcy, bcz = ecx + ex / 2 - w - 12, -20.0, ecz + 30
    pcb = Pos(bcx + bx_ / 2 - 0.8, bcy, bcz) * _rbox(1.6, by_, bz_, r_z=2.0, axis=Axis.X)
    add("Power and radio board", pcb, C_PCB, "plastic", 2, "internal", E_INT)
    xc = bcx + bx_ / 2 - 1.6                                    # component side faces the lid
    comp = [Pos(xc - 2.5, bcy - 12, bcz + 20) * Box(5.0, 12.0, 12.0),             # inductor
            Pos(xc - 1.0, bcy + 10, bcz + 22) * Box(2.0, 9.0, 9.0),               # charger IC
            Pos(xc - 0.8, bcy + 12, bcz - 6) * Box(1.6, 7.0, 7.0),                # fuel gauge
            Pos(xc - 4.0, bcy, bcz - 32) * Box(8.0, 40.0, 8.0)]                   # terminal block
    add("Power board components", _union(comp[1:3]), C_CHIP, "plastic", 2, "internal", E_INT)
    add("Power board inductor", comp[0], "#3A3F47", "plastic", 2, "internal", E_INT)
    add("Power board terminals", comp[3], "#2E7D5B", "plastic", 2, "internal", E_INT)
    caps = [Pos(xc - 4.0, bcy + dy, bcz + 5) * Rot(0, 90, 0) * Cylinder(3.2, 8.0) for dy in (-18, -8)]
    add("Power board capacitors", _union(caps), C_STEEL, "metal", 2, "internal", E_INT)
    cx_, cy_, cz_ = P["ctrl"]
    ccx, ccy = ecx + ex / 2 - w - 26, 35.0
    cpcb = Pos(ccx + cx_ / 2 - 0.6, ccy, bcz) * _rbox(1.2, cy_, cz_, r_z=1.5, axis=Axis.X)
    add("Controller board", cpcb, C_PCB_DARK, "plastic", 2, "internal", E_INT)
    shield = Pos(ccx + cx_ / 2 - 1.2 - 1.2, ccy, bcz + 10) * _rbox(2.4, 26.0, 30.0, r_z=1.0, axis=Axis.X)
    add("STM32WL module shield", shield, C_STEEL, "metal", 2, "internal", E_INT)
    ufl = Pos(ccx + cx_ / 2 - 2.0, ccy + 14, bcz - 20) * Rot(0, 90, 0) * Cylinder(1.5, 2.0)
    add("Controller antenna connector", ufl, C_BRASS, "metal", 2, "internal", E_INT)

    cd, cl = P["cell"]
    ccx0, ccz0 = ecx - 18, zb + w + cd / 2 + 4
    endc = 1.0
    wrap = Pos(ccx0, 0, ccz0) * Rot(90, 0, 0) * Cylinder(cd / 2, cl - 2 * endc)
    wrap = _fillet_try(wrap, wrap.edges(), [0.8, 0.4])
    add("LiFePO4 cell wrap", wrap, C_CELL, "painted", 3, "internal", (-230, 0, -40))
    ends = _union([Pos(ccx0, s * (cl / 2 - endc / 2), ccz0) * Rot(90, 0, 0) * Cylinder(cd / 2 - 1.0, endc)
                   for s in (-1, 1)])
    add("LiFePO4 cell end caps", ends, C_STEEL, "metal", 3, "internal", (-230, 0, -40))
    hold = Pos(ccx0, 0, zb + w + 4 + 5) * Box(cd + 6, cl + 10, 10.0)
    hold -= Pos(ccx0, 0, ccz0) * Rot(90, 0, 0) * Cylinder(cd / 2 + 0.3, cl + 20)
    hold -= Pos(ccx0, 0, ccz0) * Rot(90, 0, 0) * Cylinder(cd / 2 - 3, cl + 20)
    hold = _fillet_try(hold, hold.edges().filter_by(Axis.Z), [1.5, 0.8])
    add("Fused cell holder", hold, "#3A3F47", "plastic", 3, "internal", (-230, 0, -40))

    # ============ solar panel (BOM 4) and pole-top mount (BOM 5), drawn TOP_DROP lower
    drop = Pos(0, 0, -TOP_DROP)
    E_TOP = (0, 0, 180)
    E_PANEL = (0, 0, 360)
    pw, pl, pt = P["panel"]
    PF = drop * Pos(*D["panel_c"]) * Rot(0, -P["panel_tilt"], 0)
    frame = _rbox(pw, pl, pt, r_z=3.0)
    frame -= Pos(0, 0, pt / 2) * _rbox(pw - 12, pl - 12, 16.0, r_z=1.5)
    frame -= Pos(0, 0, -pt / 2) * _rbox(pw - 8, pl - 8, 16.0, r_z=1.5)     # open back channel
    add("Solar panel frame (aluminium)", PF * frame, C_ALU, "metal", 4, "shell", E_PANEL)
    back = Pos(0, 0, pt / 2 - 6.5) * Box(pw - 11, pl - 11, 1.0)
    add("Solar panel backsheet", PF * back, "#E5E7EB", "plastic", 4, "shell", E_PANEL)
    cells = Pos(0, 0, pt / 2 - 5.25) * Box(pw - 12, pl - 12, 1.5)
    nc_x, nc_y = 6, 4
    gx, gy = (pw - 12) / nc_x, (pl - 12) / nc_y
    for i in range(1, nc_x):
        cells -= Pos(-(pw - 12) / 2 + i * gx, 0, pt / 2 - 4.5) * Box(1.6, pl, 0.6)
    for j in range(1, nc_y):
        cells -= Pos(0, -(pl - 12) / 2 + j * gy, pt / 2 - 4.5) * Box(pw, 1.6, 0.6)
    add("Solar cells", PF * cells, C_PV, "screen", 4, "shell", E_PANEL)
    glass = Pos(0, 0, pt / 2 - 3.25) * Box(pw - 12.2, pl - 12.2, 2.5)
    add("Solar panel glass", PF * glass, C_GLASS, "clear", 4, "shell", E_PANEL)
    jb = Pos(55, 0, -6.5) * _rbox(60, 40, 12, r_z=4.0, r_bot=1.5)
    add("Panel junction box", PF * jb, C_BLACK, "plastic", 4, "shell", E_PANEL)

    sl_len, sl_wall, _ = P["sleeve"]
    sleeve = Pos(px, 0, D["sleeve_bot"] + sl_len / 2) * (
        Cylinder(D["sleeve_r_out"], sl_len) - Pos(0, 0, -sl_wall) * Cylinder(D["sleeve_r_in"], sl_len))
    sleeve = _fillet_try(sleeve, sleeve.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
    sleeve = _fillet_try(sleeve, [e for e in sleeve.faces().sort_by(Axis.Z)[0].edges()
                                  if e.radius > D["sleeve_r_in"] + 1], [1.0, 0.5])
    add("Pole-top sleeve", drop * sleeve, C_ALU, "metal", 5, "shell", E_TOP)
    setsc = []
    for k in range(3):
        ang = math.radians(-150 + 120 * k)
        r0 = D["sleeve_r_out"]
        zz = D["sleeve_bot"] + 30
        c = Pos(px + (r0 + 3.5) * math.cos(ang), (r0 + 3.5) * math.sin(ang), zz) * Rot(0, 0, math.degrees(ang)) * \
            Rot(0, 90, 0) * Cylinder(8.5, 7.0)
        c = _fillet_try(c, c.edges(), [0.6, 0.3])
        setsc.append(c)
    add("Set screws M10", drop * _union(setsc), C_STEEL, "metal", 5, "shell", E_TOP)
    po, pwall, ph = P["post"]
    post = Pos(px, 0, D["cap_top"] + ph / 2) * (Cylinder(po / 2, ph) - Cylinder(po / 2 - pwall, ph + 2))
    add("Panel post", drop * post, C_ALU, "metal", 5, "shell", E_TOP)
    hinge = Pos(px - 20, 0, D["post_top"] + 8) * Rot(0, -P["panel_tilt"], 0) * _rbox(*P["hinge"], r_z=10.0)
    add("Hinge plate", drop * hinge, C_ALU, "metal", 5, "shell", E_TOP)

    # ============ sensor cable (BOM 11): model.py route, rounded bends, M12 plug at the head
    r = P["cable_d"] / 2
    cy = -pr - 8
    z0 = D["enc_bot"] - 30
    ec = (ecx, 0, P["enc_zc"])
    pts = [(ec[0], -40, D["enc_bot"] - 24), (ec[0], -40, z0), (px - pr + 10, cy, z0),
           (px, cy, z0), (px, cy, az_ - 30),
           (D["pole_face"] + 20, -30, az_ - 30), (P["head_x"] - 20, -30, az_ - 30),
           (P["head_x"] - 20, -30, D["head_zc"] + hz / 2 - 5)]
    segs = [_tube(p0, p1, r) for p0, p1 in zip(pts[:-1], pts[1:])]
    segs += [Pos(*q) * Sphere(r) for q in pts[1:-1]]
    add("Sensor cable, M12", _union(segs), C_BLACK, "rubber", 11, "shell", (0, -60, 0))

    # ============ public notice plate (BOM 12), drawn at NOTICE_Z
    nx, ny, nz = P["notice"]
    xn = px - pr - nx / 2
    xfn = xn - nx / 2                                          # front face, toward the sidewalk
    E_NOT = (-120, 0, 0)
    plate = Pos(xn, 0, NOTICE_Z) * _rbox(nx, ny, nz, r_z=8.0, axis=Axis.X)
    add("Public notice plate", plate, C_WHITE, "painted", 12, "shell", E_NOT)
    band = Pos(xfn - 0.15, 0, NOTICE_Z + nz / 2 - 22) * Box(0.3, ny, 44)
    band &= Pos(xfn - 0.15, 0, NOTICE_Z) * _rbox(2.0, ny, nz, r_z=8.0, axis=Axis.X)
    add("Notice header band", band, C_ACCENT, "painted", 12, "shell", E_NOT)

    def tp(z, x0=xfn - 0.3):
        return Plane(origin=(x0, 0, NOTICE_Z + z), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))

    head_t = _text("PRIVACY-SAFE COUNTER", 10.5, tp(nz / 2 - 22), 0.3)
    add("Notice header text", head_t, C_WHITE, "painted", 12, "shell", E_NOT)
    lines = [("Counts people, bikes and", 9.0, 44), ("vehicles on the device.", 9.0, 30),
             ("No images are taken", 9.5, 4), ("or stored.", 9.5, -10),
             ("Only counts are sent.", 9.0, -36), ("github.com/BoujeeEnjinia1701/curbcount", 5.2, -70)]
    body_t = _union([_text(s, sz_, tp(z, xfn), 0.4) for s, sz_, z in lines])
    add("Notice text", body_t, C_TEXT, "painted", 12, "shell", E_NOT)
    rivets = [Pos(xfn - 0.6, yy, NOTICE_Z + zz) * (Sphere(3.0) & Pos(-2, 0, 0) * Box(4, 8, 8))
              for yy in (-ny / 2 + 10, ny / 2 - 10) for zz in (-nz / 2 + 10, nz / 2 - 10)]
    add("Notice rivets", _union(rivets), C_STEEL, "metal", 13, "shell", E_NOT)

    # ============ context: short section of the 114 mm street pole
    ptop = D["pole_top"] - TOP_DROP
    pole = Pos(px, 0, (POLE_Z0 + ptop) / 2) * Cylinder(pr, ptop - POLE_Z0)
    add("Street pole section, 114 mm", pole, C_POLE, "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:34s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
