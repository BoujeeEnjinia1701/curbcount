"""CurbCount prototype build plan pictures (CBC-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything; a sheet, joint or step can also be drawn alone, for example
`sheets:101` or `steps:5`, which keeps memory low. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png          every component pulled apart, numbered in build order
    cad/drawings/CBC-DWG-101 to 116          making sketches for the made and drilled components
    docs/05-build-plan/*-holes.png           hole layouts for the two saddle plates and the enclosure base
    docs/05-build-plan/joint-NN.png          close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png           one picture per assembly step
    docs/05-build-plan/wiring.png            block-level wiring of the sensor cable (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, pole_stub, fuse, _vsaddle_local, port_world  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
REPO = "github.com/BoujeeEnjinia1701/curbcount"
D = derived(P)
C = build_components(P)
S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731
PX = P["pole_x"]
AZ = D["arm_z"]
EZ = P["enc_zc"]
CT = D["cap_top"]

COL = {"enc_plate": "#A8A29E", "vs": "#57534E", "body": "#D1D5DB", "lid": "#E5E7EB", "lugs": "#374151",
       "pens": "#1F2937", "ports": "#D4A017", "mplate": "#94A3B8", "modules": "#16A34A", "cell": "#C2410C",
       "strip": "#7C3AED", "arm_plate": "#78716C", "brk": "#1D4ED8", "tube": "#A16207", "housing": "#0F766E",
       "frame": "#475569", "film": "#FBBF24", "array": "#7C3AED", "sleeve": "#64748B", "disc": "#334155",
       "post": "#0E7490", "plugs": "#155E75", "lclip": "#1D4ED8", "uclip": "#6D28D9", "rail": "#B45309",
       "panel": "#1E3A8A", "band": "#9CA3AF", "cable": "#111827", "lead": "#991B1B", "notice": "#F59E0B",
       "bolt": "#111827", "pole": "#9CA3AF", "gland": "#1F2937"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def pole(z0, z1, name="Pole (site supplied)"):
    return part(name, pole_stub(z0, z1), COL["pole"])


def made():
    return {
        "enc_plate": part("Enclosure saddle plate", C["enc_plate"].shape, COL["enc_plate"]),
        "enc_vs": part("V-saddles, enclosure (2)", S("enc_vs_up", "enc_vs_low"), COL["vs"]),
        "body": part("FieldNode enclosure, drilled, with lugs", S("body", "lugs", "lug_screws"), COL["body"]),
        "pens": part("Glands, vent, ports, antenna", S("glands", "vent", "ports", "antenna"), COL["pens"]),
        "inside": part("Internal plate with cell, modules, strip", S("mplate", "cell", "power", "ctrl", "connectors", "mplate_screws"), COL["modules"]),
        "lid": part("Enclosure lid", C["lid"].shape, COL["lid"]),
        "arm_plate": part("Arm saddle plate", C["arm_plate"].shape, COL["arm_plate"]),
        "arm_vs": part("V-saddles, arm (2)", S("arm_vs_up", "arm_vs_low"), COL["vs"]),
        "tube": part("Arm tube with end cap", S("arm_tube", "arm_cap"), COL["tube"]),
        "brk": part("Arm brackets (2) and bolts", S("arm_brk_up", "arm_brk_low", "arm_bolts") + _win(C["arm_spacers"].shape, D["arm_x0"] - 1, D["arm_x0"] + 50, -50, 50, AZ - 50, AZ + 50), COL["brk"]),
        "housing": part("Head housing", S("housing", "head_gland"), COL["housing"]),
        "array": part("Thermal array", C["array"].shape, COL["array"]),
        "film": part("Window film", C["film"].shape, COL["film"]),
        "frame": part("Window frame", S("frame", "frame_screws"), COL["frame"]),
        "sleeve": part("Sleeve with rivet nuts", S("sleeve", "rivnuts"), COL["sleeve"]),
        "disc": part("Cap disc", S("disc", "disc_screws"), COL["disc"]),
        "post": part("Post with plugs", S("post", "plugs"), COL["post"]),
        "lclip": part("Lower post clips (2)", S("lclip_r", "lclip_l"), COL["lclip"]),
        "uclip": part("Upper post clips (2)", S("uclip_r", "uclip_l"), COL["uclip"]),
        "rail": part("Rail plate", C["rail"].shape, COL["rail"]),
        "panel": part("Solar panel", C["panel"].shape, COL["panel"]),
        "enc_bands": part("Band clamps, enclosure (2)", C["enc_bands"].shape, COL["band"]),
        "arm_bands": part("Band clamps, arm (2)", C["arm_bands"].shape, COL["band"]),
        "bands": part("Band clamps (4)", S("enc_bands", "arm_bands"), COL["band"]),
        "cable": part("Sensor cable", C["cable"].shape, COL["cable"]),
        "lead": part("Panel extension lead", C["panel_lead"].shape, COL["lead"]),
        "notice": part("Notice plate and ties", S("notice", "notice_ties"), COL["notice"]),
    }


ORDER = ["enc_plate", "enc_vs", "body", "pens", "inside", "lid", "arm_plate", "arm_vs", "tube", "brk", "housing",
         "array", "film", "frame", "sleeve", "disc", "post", "lclip", "uclip", "rail", "panel", "enc_bands", "arm_bands", "cable", "lead", "notice"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    # three groups drawn closer together than installed, then each part pulled apart within its group
    E, T, U = -600.0, 850.0, -900.0                      # enclosure group left, pole-top group right and lower
    off = {"enc_plate": (0, E, 0), "enc_vs": (170, E, 0), "body": (-170, E, 0), "pens": (-170, E, -170),
           "inside": (-330, E, 0), "lid": (-470, E, 0), "enc_bands": (330, E, 0),
           "arm_plate": (40, 0, 0), "arm_vs": (-90, 0, 0), "tube": (180, 0, 0), "brk": (110, 0, 120),
           "housing": (380, 0, -130), "array": (380, 0, -260), "film": (380, 0, -330), "frame": (380, 0, -400), "arm_bands": (-260, 0, 0),
           "sleeve": (0, T, U), "disc": (0, T, U + 150), "post": (0, T, U + 260), "lclip": (0, T + 170, U + 200),
           "uclip": (0, T + 170, U + 380), "rail": (0, T, U + 440), "panel": (0, T, U + 600),
           "cable": (0, 1400, -150), "lead": (0, 1550, -150), "notice": (0, -1050, 1150)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CurbCount prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Groups drawn closer together than installed. Seen from the road side and above",
                       elev=14, azim=-35, size=(12, 10), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="CurbCount", date=DATE)
    out = []
    pe = pole(EZ - 260, EZ + 260)
    pa = pole(AZ - 200, AZ + 200)
    pt = pole(D["pole_top"] - 300, D["pole_top"])
    H = b.Pos(P["head_x"], 0, D["head_zc"]) * b.Rot(0, -P["tilt"], 0)
    RF = b.Pos(*D["rail_P0"]) * b.Rot(0, -P["panel_tilt"], 0)

    def want(n):
        return only is None or n in only

    if want(101):
        sh = C["enc_plate"].shape
        out.append(bv.component_sheet(
            Part("Enclosure saddle plate", sh, COL["enc_plate"]), [M["enc_vs"], M["body"], M["enc_bands"], pe],
            dwg_no="CBC-DWG-101", title="CurbCount enclosure saddle plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061 class",
            view_shape=flat(sh, (D["enc_plate_x"], 0, EZ), (0, -1, 0), (0, 0, 1)), inset_view=(18, 35),
            notes=["Blank 160 x 300 mm, 3 mm aluminium. Front view is the face the box sits on.",
                   "Heights from the bottom edge; sideways from the centre line.",
                   "Window 100 x 150 mm, 6 mm corners, 75 to 225 mm up: drill the corners",
                   "  12 mm, cut between with a jigsaw, file straight. It saves weight.",
                   "Band slots 3 x 15 mm at 66 mm each side, centred 17 and 283 mm up:",
                   "  chain drill 3 mm and file square. The bands pass through these.",
                   "Lug screws 5.5 mm at 62 mm each side, 41 and 259 mm up.",
                   "V-saddle screws 4.5 mm on the centre line, 42, 62, 238 and 258 mm up;",
                   "  countersink from the front so the screw heads sit flush.",
                   "Deburr every hole and edge; round the corners to about 2 mm.",
                   "Fit: V-saddles on the back, the enclosure on the front between the",
                   "  bands; each band crosses the front above or below the box.",
                   "Check: lay the saddles and lugs on it and look through each hole."], **base))

    if want(102):
        vs = _vsaddle_local(P)
        out.append(bv.component_sheet(
            Part("V-saddle", C["enc_vs_up"].shape, COL["vs"]), [M["enc_plate"], M["body"], pe],
            dwg_no="CBC-DWG-102", title="CurbCount V-saddle (make 4): making sketch", material="Aluminium sheet 3 mm, 5052-H32 (bends cold)",
            view_shape=vs, inset_view=(55, 160),
            notes=["Make four, all the same: two for the enclosure plate, two for the arm plate.",
                   "Blank 150 x 40 mm of 3 mm sheet: a 20 mm flat in the middle and a",
                   "  65 mm wing each side. Scribe the two bend lines 10 mm each side",
                   "  of the centre line.",
                   "Bend each wing 45 degrees in a vice with soft jaws, inside radius",
                   "  about 3 mm, so the two wings meet at 90 degrees (the V).",
                   "Two holes on the centre line of the flat, 10 mm each side of the",
                   "  middle: drill 3.3 mm and tap M4. File the screw tails flush later.",
                   "Fit: the flat sits on the back of a saddle plate, the V opens toward",
                   "  the pole; two M4 countersunk screws from the plate's front.",
                   "The 114 mm pole touches both wings 43 mm out from the bends;",
                   "  60 to 140 mm poles also seat on both wings.",
                   "Check: both wings at 45 degrees to the flat, within 1 degree."], **base))

    if want(103):
        out.append(bv.component_sheet(
            Part("Enclosure body", S("body", "vent"), COL["body"]), [M["enc_plate"], M["pens"]],
            dwg_no="CBC-DWG-103", title="CurbCount FieldNode enclosure: drilling sketch", material="Bought IP65 polycarbonate box 150 x 90 x 200 mm",
            view_shape=_body_upside_down(), inset_view=(-30, 140),
            notes=["The FieldNode enclosure, drilled exactly as FieldNode's build plan says.",
                   "Drawn upside down: stand the box on its top, back face toward you.",
                   "Back row, 27 mm from the back face: gland 1 at 40 left, gland 2 at",
                   "  8 left (16.2 mm holes), vent at 24 right (12.2 mm).",
                   "Front row, 55 mm from the back face: port A at 54 left, port B at",
                   "  22 left (16.2 mm), antenna at 30 right (6.5 mm).",
                   "Left and right as seen from the front (the lid).",
                   "Tape the face, pilot drill 3 mm slowly with wood behind, open out with",
                   "  a step drill. No solvents: polycarbonate crazes.",
                   "Fit the maker's four lugs at the back corners.",
                   "In CurbCount, gland 1 takes the panel lead and port A the sensor",
                   "  cable; gland 2 is plugged and port B capped."], **base))

    if want(104):
        sh = C["arm_plate"].shape
        out.append(bv.component_sheet(
            Part("Arm saddle plate", sh, COL["arm_plate"]), [M["arm_vs"], M["tube"], M["brk"], M["arm_bands"], pa],
            dwg_no="CBC-DWG-104", title="CurbCount arm saddle plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061 class",
            view_shape=flat(sh, (D["saddle_x"], 0, AZ), (0, 1, 0), (0, 0, 1)), inset_view=(18, -40),
            notes=["Blank 160 x 250 mm, 3 mm aluminium. Front view is the face the arm",
                   "  butts against. Heights from the bottom edge; sideways from the centre.",
                   "Band slots 3 x 15 mm at 66 mm each side, centred 15 and 235 mm up:",
                   "  chain drill 3 mm and file square.",
                   "Bracket bolts 6.6 mm at 10 mm each side, 83 and 167 mm up.",
                   "V-saddle screws 4.5 mm on the centre line, 40, 60, 190 and 210 mm up;",
                   "  countersink from the front.",
                   "Deburr every hole; round the corners to about 2 mm.",
                   "Fit: V-saddles on the back; the arm tube butts the front at mid",
                   "  height, held by the two brackets; the bands cross the front above",
                   "  and below the brackets.",
                   "Check: offer the brackets up and look through the bolt holes."], **base))

    if want(105):
        sh = C["arm_brk_up"].shape
        out.append(bv.component_sheet(
            Part("Arm bracket", sh, COL["brk"]), [M["arm_plate"], M["tube"], pa],
            dwg_no="CBC-DWG-105", title="CurbCount arm bracket (make 2): making sketch", material="Aluminium equal angle 40 x 40 x 4 mm",
            view_shape=b.Pos(-D["arm_x0"], 0, -AZ) * sh, inset_view=(20, -40),
            notes=["Cut two 40 mm lengths of 40 x 40 x 4 angle; square and deburr.",
                   "Upright leg (goes on the plate): two 6.6 mm holes 10 mm each side",
                   "  of the middle, 22 mm from the heel (the outside corner).",
                   "Flat leg (goes on the tube): two 6.6 mm holes on the middle line,",
                   "  15 and 30 mm from the heel.",
                   "Both brackets are the same; one goes on top of the tube, the other",
                   "  underneath, upside down.",
                   "Fit: the upright leg on the plate's front, its heel at the tube's",
                   "  top (or bottom) face; M6 bolts through the plate, nuts behind.",
                   "Two M6 bolts go down through both brackets and the tube, each",
                   "  with a crush spacer inside the tube.",
                   "Check: the bracket sits flat on both the plate and the tube."], **base))

    if want(106):
        sh = S("arm_tube")
        out.append(bv.component_sheet(
            Part("Arm tube", sh, COL["tube"]), [M["arm_plate"], M["brk"], M["housing"], pa],
            dwg_no="CBC-DWG-106", title="CurbCount arm tube: making sketch", material="Aluminium square tube 40 x 40 x 2 mm, 6063",
            view_shape=b.Pos(-D["arm_x0"], 0, -AZ) * sh, inset_view=(20, -40),
            notes=[f"Cut {D['arm_len']:.0f} mm of 40 x 40 x 2 tube; square both ends (the pole end",
                   "  must sit flat on the plate) and deburr.",
                   "Plate end: two 6.6 mm holes straight through top and bottom walls,",
                   "  on the centre line, 15 and 30 mm from the end.",
                   "Head end: two 5.5 mm holes straight through, on the centre line,",
                   f"  {P['head_bolts_x'][0] - D['arm_x0']:.0f} and {P['head_bolts_x'][1] - D['arm_x0']:.0f} mm from the plate end.",
                   "Drill each pair square through both walls (drill press, V-block).",
                   "Cut four crush spacers 36 mm long from 10 mm aluminium tube; they",
                   "  sit inside the tube on the bolts so the walls do not crush.",
                   "Fit a plastic end cap in the head end.",
                   "Check: on a flat bench the tube does not rock; holes line up",
                   "  top to bottom (a rod passes straight through)."], **base))

    if want(107):
        sh = H.inverse() * C["housing"].shape
        out.append(bv.component_sheet(
            Part("Head housing", C["housing"].shape, COL["housing"]), [M["tube"], M["frame"], M["film"]],
            dwg_no="CBC-DWG-107", title="CurbCount head housing: making sketch", material="ASA, 3D printed, 4 perimeters, 40 % infill",
            view_shape=sh, inset_view=(15, -50),
            notes=["Print in ASA in an enclosed printer, hood down on the bed; support",
                   "  the window ledge. Housing 110 x 90 x 70 mm, walls 3 mm,",
                   "  hood 150 x 120 x 4 mm, set 10 mm toward the road side.",
                   "Ledge 8 mm wide inside the open bottom: the window clamps to it.",
                   "Four corner bosses: press in M3 heat-set inserts, 47 and 37 mm",
                   "  each side of centre, from below.",
                   "Four standoffs from the roof carry the array breakout.",
                   "Wedge pad on the hood top: it makes the 7.5 degree tilt; its top is",
                   "  level under the arm. Press in two M5 heat-set inserts, 60 apart.",
                   "End wall (pole side): 16.2 mm hole, 15 mm off centre, for the gland.",
                   "Drill a 5 mm lanyard hole in the hood's road-side overhang.",
                   "Road-side wall: a raised plaque 64 x 16 mm, 0.8 mm high, with",
                   "  COUNTS ONLY in 7 mm letters 0.4 mm higher, printed in the housing.",
                   "Check: the wedge top is flat; the ledge face is flat for the film."], **base))

    if want(108):
        sh = H.inverse() * C["frame"].shape
        out.append(bv.component_sheet(
            Part("Window frame", C["frame"].shape, COL["frame"]), [M["housing"], M["film"]],
            dwg_no="CBC-DWG-108", title="CurbCount window frame and film: making sketch", material="Frame ASA, 3D printed; film 0.5 mm HDPE",
            view_shape=sh, inset_view=(-35, -50),
            notes=["Frame: print flat in ASA, 110 x 90 x 3 mm with an 88 x 68 mm opening",
                   "  and four 3.4 mm holes, 47 and 37 mm each side of centre.",
                   "Film: cut 100 x 80 mm from 0.5 mm unpigmented HDPE with a sharp",
                   "  knife on glass; do not touch the middle with bare fingers.",
                   "Use the frame as a template: punch four 3.5 mm holes in the film.",
                   "Fit: film on the housing ledge, frame over it, four M3 screws into",
                   "  the heat-set inserts, tightened evenly until the film is flat.",
                   "The array looks through the 88 x 68 mm opening; the field of view",
                   "  needs only about 30 x 20 mm of it.",
                   "Check: the film is flat and taut with no creases in the opening."], **base))

    if want(109):
        sh = S("sleeve")
        out.append(bv.component_sheet(
            Part("Sleeve", sh, COL["sleeve"]), [M["disc"], M["post"], pt],
            dwg_no="CBC-DWG-109", title="CurbCount sleeve: making sketch", material="Aluminium round tube about 128 x 3 mm, bore 122 mm or more",
            view_shape=b.Pos(-PX, 0, 0) * sh, inset_view=(20, -60),
            notes=["Cut 100 mm of round tube; square and deburr both ends.",
                   "The bore must be 122 mm or more so it slides over a 114 mm pole.",
                   "Top: four 4.5 mm holes 4 mm down from the top edge, at 45, 135,",
                   "  225 and 315 degrees; countersink them for M4 screws.",
                   "Bottom: three 11 mm holes 25 mm up from the bottom edge, at 0, 120",
                   "  and 240 degrees; set an M8 stainless rivet nut in each.",
                   "Put the hole at 0 degrees on the road side when fitting.",
                   "Fit: the cap disc goes inside the top, flush, on the four radial",
                   "  screws; the sleeve then sits on the pole top through the disc.",
                   "Three M8 cup-point set screws in the rivet nuts centre it on the pole.",
                   "Check: it slides over a 114 mm tube with 3 to 4 mm all round."], **base))

    if want(110):
        sh = S("disc")
        out.append(bv.component_sheet(
            Part("Cap disc", sh, COL["disc"]), [M["sleeve"], M["post"], M["lclip"], pt],
            dwg_no="CBC-DWG-110", title="CurbCount cap disc: making sketch", material="Aluminium plate 8 mm, 6082 or 5083 class",
            view_shape=b.Pos(-PX, 0, 0) * sh, inset_view=(35, -60),
            notes=["Cut a disc 122 mm across from 8 mm plate (hole saw or bandsaw and",
                   "  file); it must be a close sliding fit in the sleeve bore.",
                   "Edge: four holes into the edge at 45, 135, 225 and 315 degrees,",
                   "  4 mm from the top face: drill 3.3 mm 12 deep and tap M4.",
                   "  Drill them through the sleeve's holes with the disc in place.",
                   "Face: eight 5.5 mm holes for the lower clips, 40 mm each side of the",
                   "  centre line and 9 mm either side of the cross line; countersink",
                   "  them from below so the screw heads sit flush (the pole top bears",
                   "  on the underside).",
                   "Fit: disc inside the top of the sleeve, top faces flush.",
                   "Check: underside flat; no screw head stands proud."], **base))

    if want(111):
        sh = S("post")
        out.append(bv.component_sheet(
            Part("Post", sh, COL["post"]), [M["disc"], M["lclip"], M["uclip"], M["rail"]],
            dwg_no="CBC-DWG-111", title="CurbCount post: making sketch", material="Aluminium round tube 42.4 x 3.0 mm, 6063",
            view_shape=b.Pos(-PX, 0, 0) * sh, inset_view=(20, -60),
            notes=["Cut 150 mm of 42.4 x 3.0 tube; square both ends and deburr.",
                   "Fit a plug in each end first (next sheet), then drill the post and",
                   "  plug together, straight across, 8.5 mm:",
                   "  bottom end: 12 and 28 mm up from the bottom;",
                   "  top end: 10 and 26 mm down from the top.",
                   "All four holes lie in one plane: drill in a V-block on a drill press.",
                   "Fit: the bottom end stands on the cap disc between the lower clips;",
                   "  the top end sits between the upper clips under the rail plate,",
                   "  4 mm clear of it. Two M8 bolts through each end.",
                   "Check: a rod passes straight through each hole pair."], **base))

    if want(112):
        sh = S("plugs")
        out.append(bv.component_sheet(
            Part("Post plugs", sh, COL["plugs"]), [M["post"], M["lclip"], M["uclip"]],
            dwg_no="CBC-DWG-112", title="CurbCount post plug (make 2): making sketch", material="Aluminium round bar 36 mm, 6082",
            view_shape=b.Pos(-PX, 0, -CT) * (sh & b.Pos(PX, 0, CT + 50) * b.Box(100, 100, 100)), inset_view=(20, -60),
            notes=["Cut two 40 mm lengths of 36 mm round bar; face both ends.",
                   "Turn or file to a push fit in the post's 36.4 mm bore.",
                   "Push one into each end of the post, flush with the end.",
                   "Drill through with the post (8.5 mm, as the post sheet shows).",
                   "The plugs stop the thin post wall from crushing when the M8",
                   "  cross bolts are tightened.",
                   "Check: flush with the post end; the bolts slide through freely."], **base))

    if want(113):
        sh = C["lclip_r"].shape
        out.append(bv.component_sheet(
            Part("Lower post clip", sh, COL["lclip"]), [M["disc"], M["post"], M["sleeve"]],
            dwg_no="CBC-DWG-113", title="CurbCount lower post clip (make 2): making sketch", material="Aluminium equal angle 50 x 50 x 5 mm",
            view_shape=b.Pos(-PX, 0, -CT) * sh, inset_view=(25, -60),
            notes=["Cut two 35 mm lengths of 50 x 50 x 5 angle.",
                   "Trim the flat leg to 30 mm wide (from the heel) so it fits on the disc.",
                   "Upright leg: two 8.5 mm holes at mid-length, 12 and 28 mm up",
                   "  from the bottom face of the flat leg.",
                   "Flat leg: two 5.5 mm holes 19 mm out from the upright leg's inside",
                   "  face, 9 mm either side of mid-length.",
                   "Both clips are the same; they face each other across the post.",
                   "Fit: flat leg on the disc, upright leg against the post; two M5",
                   "  countersunk screws up through the disc, nuts on top.",
                   "Check: the clips stand square on the disc, 42.4 mm apart inside."], **base))

    if want(114):
        sh = RF.inverse() * C["uclip_r"].shape
        out.append(bv.component_sheet(
            Part("Upper post clip", C["uclip_r"].shape, COL["uclip"]), [M["rail"], M["post"], M["panel"]],
            dwg_no="CBC-DWG-114", title="CurbCount upper post clip (make 2): making sketch", material="Aluminium equal angle 50 x 50 x 5 mm",
            view_shape=sh, inset_view=(-20, -70),
            notes=["Cut two 35 mm lengths of 50 x 50 x 5 angle.",
                   "Flat leg (goes under the rail plate): two 5.5 mm holes 30 mm out",
                   "  from the upright leg's inside face, 10 and 25 mm from one end.",
                   "Upright leg: two 8.5 mm holes for the post bolts. Mark them from",
                   "  the post: clamp the clip to the rail plate, set the post between",
                   "  the clips at the 35 degree tilt, and drill through the post holes.",
                   "  They fall about 12 and 21 mm from the upper end, 25 and 38 mm down.",
                   "The two clips are mirror images; drill them as a pair.",
                   "Fit: M5 screws through the rail plate, nuts under the clip.",
                   "This joint sets the panel's 35 degree tilt.",
                   "Check: the rail plate sits at 35 degrees, give or take 1."], **base))

    if want(115):
        sh = RF.inverse() * C["rail"].shape
        out.append(bv.component_sheet(
            Part("Rail plate", C["rail"].shape, COL["rail"]), [M["uclip"], M["post"], M["panel"]],
            dwg_no="CBC-DWG-115", title="CurbCount rail plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061 class",
            view_shape=sh, inset_view=(-25, -60),
            notes=["Blank 290 x 150 mm of 3 mm sheet; the long side runs up the slope.",
                   "Lip bolts: four 4.5 mm holes 6 mm in from each short end, 50 mm",
                   "  each side of the centre line (they go through the panel's lip).",
                   "Clip screws: four 5.5 mm holes, 51 mm each side of the centre line,",
                   "  15 and 30 mm below the middle (toward the low edge).",
                   "Two lightening windows 90 x 90 mm, 6 mm corners, centred 85 mm",
                   "  each side of the middle along the long side.",
                   "Lanyard hole 6 mm on the middle line, 12 mm in from one long edge.",
                   "Deburr everything.",
                   "Fit: the panel's frame lip sits on the plate's ends; M4 bolts with",
                   "  the nuts inside the frame. The upper clips go underneath.",
                   "Check: the panel lip holes line up with the plate's end holes."], **base))

    if want(116):
        sh = C["notice"].shape
        out.append(bv.component_sheet(
            Part("Notice plate", sh, COL["notice"]), [M["notice"], pole(P["notice_z"] - 200, P["notice_z"] + 200)],
            dwg_no="CBC-DWG-116", title="CurbCount public notice plate: making sketch", material="Aluminium sheet 2 mm, printed UV-stable face",
            view_shape=flat(sh, (PX - D["pole_r"] - 1, 0, P["notice_z"]), (0, -1, 0), (0, 0, 1)), inset_view=(15, 150),
            notes=["Blank 150 x 200 mm of 2 mm aluminium; round the corners 5 mm.",
                   "Four tie slots 3 x 10 mm, 60 mm each side of the centre line,",
                   "  centred 30 and 170 mm up from the bottom edge.",
                   "Print or apply a UV-stable face: what is counted, \"No images are",
                   "  stored or sent; only counts leave the device\", and the repository link.",
                   "Fit: the back lies against the pole, centred on it; two stainless",
                   "  steel cable ties pass round the pole and through the slots.",
                   "At the site it goes at eye height, about 2.6 m up, facing the",
                   "  sidewalk.",
                   "Check: the ties pull the plate flat against the pole."], **base))
    return out


def _body_upside_down():
    import build123d as b
    sh = S("body", "vent")
    return b.Rot(180, 0, 0) * b.Pos(-D["enc_xc"], 0, -EZ) * sh


# ----------------------------------------------------------------- hole layouts
def _holes(face):
    out = []
    for w in face.inner_wires():
        bb = w.bounding_box()
        edges = w.edges()
        circ = len(edges) == 1 or (all(e.geom_type == "CIRCLE" for e in edges) and len(edges) <= 2)
        out.append(("circle" if circ else "slot", bb.center(), bb.size))
    return out


def _plate_layout(shape, x_face, sign, title, sub, key, out, wv, hz, z0):
    """Hole layout of a saddle plate seen from its front. sign: +1 if 'right' is world +Y."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyBboxPatch
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    face = [f for f in shape.faces() if abs(f.center().X - x_face) < 0.01 and f.area > 1e4][0]
    H = _holes(face)
    zb = z0 - hz / 2
    fig = plt.figure(figsize=(9.5, 11), dpi=150)
    ax = fig.add_axes([0.08, 0.07, 0.62, 0.84]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-wv / 2, 0), wv, hz, fc="#F5F5F4", ec=INK, lw=1.2))
    ax.axvline(0, color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    xs, zs = set(), set()
    for kind, c, sz in H:
        x, z = sign * c.Y, c.Z - zb
        if kind == "circle":
            d = sz.Y
            ax.add_patch(plt.Circle((x, z), d / 2, fc="white", ec=INK, lw=1))
            ax.plot([x - d / 2 - 2, x + d / 2 + 2], [z, z], color=MUT, lw=0.4); ax.plot([x, x], [z - d / 2 - 2, z + d / 2 + 2], color=MUT, lw=0.4)
        else:
            r = 6 if sz.Y > 50 else 0
            ax.add_patch(FancyBboxPatch((x - sz.Y / 2 + r, z - sz.Z / 2 + r), sz.Y - 2 * r, sz.Z - 2 * r, boxstyle=f"round,pad={r}", fc="white", ec=INK, lw=1))
        if x > 0.5:
            xs.add(round(x, 1))
        if kind == "slot" and sz.Y > 50:
            zs.add(round(z - sz.Z / 2, 1)); zs.add(round(z + sz.Z / 2, 1)); xs.add(round(sz.Y / 2, 1))
        else:
            zs.add(round(z, 1))
    for i, x in enumerate(sorted(xs)):
        yl = -12 - 9 * (i % 2)
        ax.plot([x, x], [0, yl + 3], color=AC, lw=0.4, ls=":")
        ax.text(x, yl, f"{x:g}", ha="center", va="top", fontsize=7.5, color=AC)
    ax.text(0, -36, "sideways from the centre line, mm (same each side)", ha="center", fontsize=8, color=MUT)
    for i, z in enumerate(sorted(zs)):
        xl = -wv / 2 - 6 - 16 * (i % 2)
        ax.plot([xl + 2, -wv / 2], [z, z], color=AC, lw=0.4, ls=":")
        ax.text(xl, z, f"{z:g}", ha="right", va="center", fontsize=7.5, color=AC)
    ax.text(-wv / 2 - 40, hz / 2, "up from the bottom edge, mm", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.set_xlim(-wv / 2 - 46, wv / 2 + 10); ax.set_ylim(-42, hz + 10)
    fig.text(0.04, 0.975, title, fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.95, sub, fontsize=8.5, color=MUT, va="top")
    fig.text(0.72, 0.86, "What each opening is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.72, 0.83 - i * 0.022, t, fontsize=8, color=INK, va="top")
    fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def layouts():
    res = []
    st, sw, sh = P["enc_plate"]
    res.append(_plate_layout(C["enc_plate"].shape, D["enc_plate_front"], -1, "Enclosure saddle plate: hole and cut-out positions",
                             "Seen from the front (the face the enclosure sits on). Full size figures in mm, taken from the model.",
                             ["Window 100 x 150, 6 mm corners", "  (behind the enclosure, saves weight)", "Band slots 3 x 15, at 66",
                              "Lug screws 5.5, at 62", "V-saddle screws 4.5, countersunk", "  from the front, on the centre line",
                              "", "Heights 17 and 283 are the", "  two band clamps (266 apart)"],
                             OUT / "enc-plate-holes.png", sw, sh, EZ))
    st, sw, sh = P["saddle"]
    res.append(_plate_layout(C["arm_plate"].shape, D["arm_plate_front"], 1, "Arm saddle plate: hole positions",
                             "Seen from the front (the face the arm butts against). Full size figures in mm, taken from the model.",
                             ["Band slots 3 x 15, at 66", "Bracket bolts 6.6, at 10", "V-saddle screws 4.5, countersunk",
                              "  from the front, on the centre line", "", "Heights 15 and 235 are the", "  two band clamps (220 apart);",
                              "  the arm's axis is at 125"],
                             OUT / "arm-plate-holes.png", sw, sh, AZ))
    res.append(_base_layout())
    return res


def _base_layout():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    ew, ed = P["enc"][0], P["enc"][1] - P["lid_d"]
    lbl = {"gland_1": "Gland 1, panel lead", "gland_2": "Gland 2, plugged", "vent": "Vent", "port_a": "Port A, sensor cable",
           "port_b": "Port B, capped", "antenna": "Antenna"}
    fig = plt.figure(figsize=(11, 7), dpi=150)
    ax = fig.add_axes([0.05, 0.1, 0.9, 0.75]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-ew / 2, 0), ew, ed, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-ew / 2, ed), ew, P["lid_d"], fc="white", ec=MUT, lw=0.8, ls="--"))
    ax.text(0, ed + P["lid_d"] / 2, "lid (do not drill)", ha="center", va="center", fontsize=7.5, color=MUT)
    ax.text(-ew / 2 + 2, -2, "back face (goes against the saddle plate), toward you", ha="left", va="top", fontsize=8, color=MUT)
    ax.axvline(0, ymin=0.05, ymax=0.95, color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    for k, (x, row, dt, df) in P["pens"].items():
        yy = P["pen_rows"][row]
        hole = dt + (0.2 if dt >= 10 else 0.1)
        ax.add_patch(plt.Circle((x, yy), df / 2, fc="none", ec=MUT, lw=0.6, ls="--"))
        ax.add_patch(plt.Circle((x, yy), hole / 2, fc="white", ec=INK, lw=1.1))
        ax.plot([x - df / 2 - 2, x + df / 2 + 2], [yy, yy], color=MUT, lw=0.4); ax.plot([x, x], [yy - df / 2 - 2, yy + df / 2 + 2], color=MUT, lw=0.4)
        ax.text(x, yy + (-df / 2 - 1.5 if row == 0 else df / 2 + 1.5), f"{lbl[k]}\n{hole:.1f} hole, {x:+g}",
                ha="center", va="top" if row == 0 else "bottom", fontsize=7, color=INK, linespacing=1.2, zorder=3,
                bbox=dict(boxstyle="round,pad=0.15", fc="#F3F4F6", ec="none"))
    for r in P["pen_rows"]:
        ax.plot([ew / 2, ew / 2 + 14], [r, r], color=AC, lw=0.5, ls=":")
        ax.text(ew / 2 + 15, r, f"{r:g} from the back face", va="center", fontsize=8, color=AC)
    ax.set_xlim(-ew / 2 - 10, ew / 2 + 70); ax.set_ylim(-12, ed + P["lid_d"] + 4)
    fig.text(0.03, 0.97, "FieldNode enclosure bottom face: drilling layout (as FieldNode)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Box standing upside down on its top, back face toward you. Sideways positions from the centre line, + to the right as seen from the front.\n"
             "Solid circle: the hole to drill. Dashed circle: the outside flange of the part that goes in it.", fontsize=8.2, color=MUT, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    out = OUT / "base-holes.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


# ----------------------------------------------------------------- joints
def _win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def joints(only=None):
    out = []
    pr = D["pole_r"]

    def want(n):
        return only is None or n in only

    def J(n, parts, title, sub, **kw):
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    big_pole = pole(EZ - 400, EZ + 400)
    if want(1):
        z = EZ + P["enc_vs_dz"]
        bx_ = (PX - 160, PX + 70, -95, 95, z - 12, z + 8)
        J(1, [part("Pole (site supplied)", _win(big_pole.shape, *bx_), COL["pole"]),
              part("Enclosure saddle plate", _win(C["enc_plate"].shape, *bx_), COL["enc_plate"]),
              part("V-saddle, wings at 90 degrees", _win(C["enc_vs_up"].shape, *bx_), COL["vs"])],
          "V-saddle on the pole (enclosure side, upper saddle)",
          "Cut level with the saddle, seen from above. The pole bears on both wings of the V, never on the flat",
          elev=80, azim=-90, size=(8, 6))
    if want(2):
        z = EZ + P["enc_band_dz"]
        bx_ = (PX - 160, PX + 70, -95, 95, z - 10, z + 4)
        J(2, [part("Pole (site supplied)", _win(big_pole.shape, *bx_[:4], z - 10, z - 7), COL["pole"]),
              part("Enclosure saddle plate (band slots)", _win(C["enc_plate"].shape, *bx_), COL["enc_plate"]),
              part("Band clamp", _win(C["enc_bands"].shape, *bx_), COL["band"]),
              part("Sensor cable and panel lead, over the band", _win(S("cable", "panel_lead"), *bx_), COL["cable"])],
          "band clamp through the plate slots (enclosure, upper band)",
          "Cut level with the band, seen from above. The band runs round the pole, through both slots and across the plate front",
          elev=80, azim=-90, size=(8, 6))
    if want(3):
        xf = D["enc_plate_front"]
        bx_ = (xf - 40, xf + 12, -95, -30, D["enc_top"] - 15, D["enc_top"] + 30)
        J(3, [part("Enclosure saddle plate", _win(C["enc_plate"].shape, *bx_), COL["enc_plate"]),
              part("Enclosure body", _win(C["body"].shape, *bx_), COL["body"]),
              part("Lug (maker's kit)", _win(C["lugs"].shape, *bx_), COL["lugs"]),
              part("M5 screw from behind, nyloc nut in front", _win(C["lug_screws"].shape, *bx_), COL["bolt"])],
          "enclosure lug on the saddle plate (top, road-side corner)",
          "The box back sits flat on the plate; each lug is held by one M5 screw", elev=35, azim=-150, size=(8, 6))
    if want(4):
        eb = D["enc_bot"]
        bx_ = (D["enc_plate_front"] - 95, PX + 80, -60, 100, eb - 110, eb + 3.5)
        J(4, [part("Enclosure bottom", _win(C["body"].shape, *bx_), COL["body"]),
              part("Glands and vent (back row)", _win(S("glands", "vent"), *bx_), COL["pens"]),
              part("Sensor ports (front row)", _win(C["ports"].shape, *bx_), COL["ports"]),
              part("Antenna bulkhead", _win(C["antenna"].shape, *bx_), COL["gland"]),
              part("Sensor cable with M12 plug, into port A", _win(C["cable"].shape, *bx_), COL["cable"]),
              part("Panel lead, into gland 1", _win(C["panel_lead"].shape, *bx_), COL["lead"])],
          "the enclosure's bottom face, with both cables",
          "Seen from below; pole and plate left out. The cables leave toward the pole at different heights and turn up its side",
          elev=-40, azim=-120, size=(9, 6.5))
    if want(5):
        x0 = D["arm_x0"]
        bx_ = (D["arm_plate_back"] - 12, x0 + 55, -0.01, 90, AZ - 70, AZ + 70)
        J(5, [part("Arm saddle plate", _win(C["arm_plate"].shape, *bx_), COL["arm_plate"]),
              part("Arm tube", _win(C["arm_tube"].shape, *bx_), COL["tube"]),
              part("Brackets, top and bottom", _win(S("arm_brk_up", "arm_brk_low"), *bx_), COL["brk"]),
              part("M6 bolts and crush spacers", _win(S("arm_bolts", "arm_spacers"), *bx_), COL["bolt"])],
          "arm tube on the arm saddle plate (cut on the arm's centre line)",
          "Seen from the side. Two brackets, four bolts through the plate and two down through the tube on crush spacers",
          elev=8, azim=-70, size=(8, 6))
    if want(6):
        bx_ = (20, 135, -0.01, 70, D["head_zc"] - 45, AZ + 30)
        J(6, [part("Arm tube", _win(S("arm_tube", "arm_cap"), *bx_), COL["tube"]),
              part("Head housing with wedge pad (cut)", _win(C["housing"].shape, *bx_), COL["housing"]),
              part("M5 bolts into heat-set inserts, crush spacers", _win(S("head_bolts", "arm_spacers"), *bx_), COL["bolt"]),
              part("Thermal array on its standoffs", _win(C["array"].shape, *bx_), COL["array"]),
              part("Window film and frame", _win(S("film", "frame"), *bx_), COL["film"])],
          "head on the arm, and the array inside (cut on the centre line)",
          "The wedge pad makes the 7.5 degree tilt; the array looks down through the film, which the frame clamps to the ledge",
          elev=6, azim=-75, size=(8, 6))
    if want(7):
        import build123d as b
        H = b.Pos(P["head_x"], 0, D["head_zc"]) * b.Rot(0, -P["tilt"], 0)
        cut = H * b.Pos(40, 48.5, -28) * b.Box(36, 23, 26)
        J(7, [part("Housing ledge and corner boss", C["housing"].shape & cut, COL["housing"]),
              part("Window film, 0.5 mm", C["film"].shape & cut, COL["film"]),
              part("Window frame", C["frame"].shape & cut, COL["frame"]),
              part("M3 screw into a heat-set insert", C["frame_screws"].shape & cut, COL["bolt"])],
          "window corner (cut through a frame screw)",
          "Cut through the screw, seen from inside: the film is clamped between the ledge and the frame",
          elev=8, azim=-90, size=(8, 6))
    if want(8):
        bx_ = (PX - 75, PX + 75, -75, 75, D["pole_top"] - 80, CT + 60)
        J(8, [part("Pole top (site)", _win(pole(D["pole_top"] - 200, D["pole_top"]).shape, *bx_), COL["pole"]),
              part("Sleeve", _win(C["sleeve"].shape, *bx_), COL["sleeve"]),
              part("Cap disc on the pole top", _win(C["disc"].shape, *bx_), COL["disc"]),
              part("Rivet nut and set screw", _win(C["rivnuts"].shape, *bx_), COL["bolt"]),
              part("M4 radial screw", _win(C["disc_screws"].shape, *bx_), COL["bolt"]),
              part("Lower clips and post", _win(S("lclip_r", "lclip_l", "post", "plugs"), *bx_), COL["lclip"])],
          "sleeve and cap disc on the pole top (cut away at the front)",
          "The disc carries the load onto the pole top; three set screws centre the sleeve with 4 mm all round",
          cut="+Y", elev=8, azim=-90, size=(8, 6))
    if want(9):
        bx_ = (PX - 60, PX + 60, -60, 60, CT - 10, CT + 60)
        J(9, [part("Cap disc", _win(C["disc"].shape, *bx_), COL["disc"]),
              part("Lower post clips", _win(S("lclip_r", "lclip_l"), *bx_), COL["lclip"]),
              part("Post", _win(C["post"].shape, *bx_), COL["post"]),
              part("Plug inside the post", _win(C["plugs"].shape, *bx_), COL["plugs"]),
              part("M8 cross bolts, M5 screws", _win(S("post_bolts", "clip_screws"), *bx_), COL["bolt"])],
          "post foot on the lower clips",
          "Two M8 bolts through clip, post, plug, post and clip; each clip held to the disc by two countersunk M5 screws",
          elev=20, azim=-35, size=(8, 6))
    if want(10):
        pt_ = D["post_top"]
        bx_ = (PX - 70, PX + 70, -80, 80, pt_ - 60, pt_ + 45)
        J(10, [part("Rail plate (35 degrees)", _win(C["rail"].shape, *bx_), COL["rail"]),
               part("Upper post clips", _win(S("uclip_r", "uclip_l"), *bx_), COL["uclip"]),
               part("Post", _win(C["post"].shape, *bx_), COL["post"]),
               part("Plug inside the post", _win(C["plugs"].shape, *bx_), COL["plugs"]),
               part("M8 cross bolts, M5 screws", _win(S("post_bolts", "clip_screws"), *bx_), COL["bolt"])],
           "post head under the rail plate",
           "Seen from below on the sidewalk side. Two M8 bolts fix the tilt; the post top stays 4 mm clear of the plate",
           elev=-20, azim=-130, size=(8, 6))
    if want(11):
        import build123d as b
        RF = b.Pos(*D["rail_P0"]) * b.Rot(0, -P["panel_tilt"], 0)
        cut = RF * b.Pos(128, 62.5, 7) * b.Box(44, 25, 36)
        whole = RF * b.Pos(128, 50, 7) * b.Box(44, 20, 36)
        J(11, [part("Solar panel frame (lip at the end)", C["panel"].shape & cut, COL["panel"]),
               part("Rail plate", C["rail"].shape & cut, COL["rail"]),
               part("M4 bolt through the lip, nut inside the frame", C["clip_screws"].shape & whole, COL["bolt"])],
           "panel frame lip on the rail plate (high end)",
           "Cut through a lip bolt (panel drawn as a solid block): the lip sits on the rail plate's end; two M4 bolts at each end, never through the glass",
           elev=0, azim=-90, size=(8, 6))
    if want(12):
        ap = D["arm_plate_front"]
        bx_ = (PX - 70, ap + 70, -10, 100, AZ - 130, AZ + 30)
        J(12, [part("Pole", _win(pole(AZ - 300, AZ + 200).shape, *bx_), COL["pole"]),
               part("Arm saddle plate", _win(C["arm_plate"].shape, *bx_), COL["arm_plate"]),
               part("Arm tube and lower bracket", _win(S("arm_tube", "arm_brk_low"), *bx_), COL["tube"]),
               part("Arm band (lower)", _win(C["arm_bands"].shape, *bx_), COL["band"]),
               part("Sensor cable", _win(C["cable"].shape, *bx_), COL["cable"]),
               part("Panel lead (continues down)", _win(C["panel_lead"].shape, *bx_), COL["lead"])],
           "the sensor cable leaves the pole for the arm",
           "Both cables are tied to the pole side by side and pass over the bands; the sensor cable turns round the plate edge",
           elev=25, azim=60, size=(8, 6))
    if want(13):
        nz = P["notice_z"]
        bx_ = (PX - 75, PX + 75, -90, 90, nz + 50, nz + 90)
        J(13, [part("Pole", _win(pole(nz - 150, nz + 150).shape, *bx_), COL["pole"]),
               part("Notice plate", _win(C["notice"].shape, *bx_), COL["notice"]),
               part("Stainless cable tie through the slots", _win(C["notice_ties"].shape, *bx_), COL["band"])],
           "notice plate tie (upper)",
           "The plate lies against the pole; the tie runs round the pole and through both slots", elev=55, azim=-150, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def want(n):
        return only is None or n in only

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    ep = M["enc_plate"]
    st(1, [ep], [mv(part("V-saddle (upper)", C["enc_vs_up"].shape, COL["vs"]), (90, 0, 0)),
                 mv(part("V-saddle (lower)", C["enc_vs_low"].shape, COL["vs"]), (90, 0, 0))],
       "V-saddles onto the enclosure saddle plate",
       "Two M4 countersunk screws each, from the plate's front, threadlocker; V opening away from the plate. Seen from the pole side",
       elev=20, azim=30, label_done=False)
    st(2, [part("Enclosure body, drilled", S("body", "lugs"), COL["body"])],
       [mv(part("Glands and vent (back row)", S("glands", "vent"), COL["pens"]), (0, 0, -100)),
        mv(part("Sensor ports (front row)", C["ports"].shape, COL["ports"]), (0, 0, -60)),
        mv(part("Antenna bulkhead and whip", C["antenna"].shape, COL["gland"]), (0, 0, -150)),
        mv(part("Internal plate, wired (as FieldNode)", S("mplate", "cell", "power", "ctrl", "connectors"), COL["modules"]), (-170, 0, 0))],
       "build the FieldNode core",
       "Penetrations from below, nuts inside; internal plate on the bosses. As FieldNode's build plan, steps 2, 4 and 5",
       elev=-15, azim=-150, label_done=False)
    vs = M["enc_vs"]
    core = part("FieldNode core, lid closed", S("body", "lugs", "glands", "vent", "ports", "antenna", "lid"), COL["body"])
    st(3, [ep, vs], [mv(core, (-120, 0, 0)), mv(part("M5 screws, lugs (4)", C["lug_screws"].shape, COL["bolt"]), (60, 0, 0))],
       "enclosure onto the saddle plate",
       "Lid closed. Box back flat on the plate, between the band slots; four M5 screws from behind, nyloc nuts in front",
       elev=18, azim=-150, label_done=False)
    apl = M["arm_plate"]
    st(4, [apl], [mv(part("V-saddle (upper)", C["arm_vs_up"].shape, COL["vs"]), (-90, 0, 0)),
                  mv(part("V-saddle (lower)", C["arm_vs_low"].shape, COL["vs"]), (-90, 0, 0))],
       "V-saddles onto the arm saddle plate",
       "As step 1: two M4 countersunk screws each, from the plate's front. Seen from the pole side",
       elev=20, azim=150, label_done=False)
    st(5, [apl, M["arm_vs"]],
       [mv(part("Arm tube with end cap", S("arm_tube", "arm_cap"), COL["tube"]), (160, 0, 0)),
        mv(part("Upper bracket", C["arm_brk_up"].shape, COL["brk"]), (0, 0, 80)),
        mv(part("Lower bracket", C["arm_brk_low"].shape, COL["brk"]), (0, 0, -80))],
       "arm tube and brackets onto the arm plate",
       "Tube end square on the plate; M6 bolts through bracket and plate (nuts behind), two M6 down through the tube on crush spacers",
       elev=18, azim=-60)
    import build123d as b
    Hm = b.Pos(P["head_x"], 0, D["head_zc"]) * b.Rot(0, -P["tilt"], 0)
    up_ = (Hm * b.Pos(0, 0, 60)).position - (Hm * b.Pos(0, 0, 0)).position
    dn = tuple(-v for v in (up_.X, up_.Y, up_.Z))
    hs = part("Head housing", C["housing"].shape, COL["housing"])
    st(6, [hs], [mv(part("Thermal array breakout", C["array"].shape, COL["array"]), dn),
                 mv(part("M16 gland (end wall)", C["head_gland"].shape, COL["gland"]), (-60, 0, 0))],
       "array and gland into the head",
       "Breakout on its four standoffs, M2.5 screws; gland in the end wall, nut inside. Seen from below, through the open bottom",
       elev=-35, azim=-60, label_done=False)
    hsa = part("Head with array and gland", S("housing", "array", "head_gland"), COL["housing"])
    st(7, [hsa], [mv(part("Window film", C["film"].shape, COL["film"]), tuple(1.0 * v for v in dn)),
                  mv(part("Window frame and four M3 screws", S("frame", "frame_screws"), COL["frame"]), tuple(2.0 * v for v in dn))],
       "window film and frame onto the head",
       "Film on the ledge, frame over it, four M3 screws into the inserts, tightened evenly. Seen from below",
       elev=-40, azim=-60, label_done=False)
    arm_done = [apl, M["arm_vs"], M["tube"], M["brk"]]
    head_full = part("Sensor head, complete", S("housing", "array", "head_gland", "film", "frame", "frame_screws"), COL["housing"])
    st(8, arm_done, [mv(head_full, (0, 0, -90)), mv(part("M5 bolts (2)", C["head_bolts"].shape, COL["bolt"]), (0, 0, 70))],
       "head onto the arm",
       "Wedge pad up against the arm's underside; two M5 bolts down through the arm and its crush spacers into the inserts",
       elev=12, azim=-60, label_done=False)
    st(9, [M["sleeve"]], [mv(M["disc"], (0, 0, 130)), mv(part("M4 radial screws (4)", C["disc_screws"].shape, COL["bolt"]), (0, 0, 130))],
       "cap disc into the sleeve",
       "Rivet nuts already set. Disc into the top of the sleeve, flush; four M4 countersunk screws through the sleeve into its edge",
       elev=20, azim=-60, label_done=False)
    sd = [M["sleeve"], M["disc"]]
    st(10, sd, [mv(M["lclip"], (0, 0, 70)), mv(M["post"], (0, 0, 200)),
                mv(part("M8 bolts and M5 screws, lower", C["post_bolts"].shape & _box_below(CT + 60), COL["bolt"]), (0, 120, 0))],
       "lower clips and post onto the disc",
       "Clips on two countersunk M5 screws each from below; post between them on two M8 bolts through the plug",
       elev=18, azim=-55, label_done=False)
    import model as _m
    nrm = D["rail_n"]
    lift = tuple(120 * v for v in nrm)
    lowb = part("Lower M8 bolts", C["post_bolts"].shape & _box_below(CT + 60), COL["bolt"])
    st(11, sd + [M["lclip"], M["post"], lowb],
       [mv(part("Rail plate with the upper clips", S("rail", "uclip_r", "uclip_l"), COL["rail"]), lift),
        mv(part("M8 bolts, upper", C["post_bolts"].shape & _box_above(D["post_top"] - 60), COL["bolt"]), (0, 140, 0))],
       "rail plate onto the post",
       "Upper clips screwed under the rail plate first (M5); then the clips over the post head, two M8 bolts. Tilt 35 degrees",
       elev=15, azim=-55, label_done=False)
    st(12, sd + [M["lclip"], M["post"], lowb, M["uclip"], M["rail"],
                 part("Upper M8 bolts", C["post_bolts"].shape & _box_above(D["post_top"] - 60), COL["bolt"])],
       [mv(M["panel"], tuple(110 * v for v in nrm))],
       "panel onto the rail plate",
       "Frame lip on the plate ends; four M4 bolts with the nuts inside the frame. Panel lead taped along the post",
       elev=15, azim=-55, label_done=False)
    del _m
    # on the pole stub
    enc_asm = part("Enclosure on its saddle plate", S("enc_plate", "enc_vs_up", "enc_vs_low", "body", "lugs", "lid", "glands",
                                                    "vent", "ports", "antenna", "lug_screws"), COL["body"])
    st(13, [], [mv(enc_asm, (-160, 0, 0)), mv(part("Band clamps (2)", C["enc_bands"].shape, COL["band"]), (160, 0, 0))],
       "enclosure assembly onto the pole",
       "Saddles against the pole; each band round the pole, through its two slots and across the plate front, above or below the box",
       context=[pole(EZ - 350, EZ + 350)], elev=20, azim=-145, label_done=False)
    arm_asm = part("Arm and head", S("arm_plate", "arm_vs_up", "arm_vs_low", "arm_tube", "arm_cap", "arm_brk_up", "arm_brk_low",
                                     "arm_bolts", "housing", "array", "head_gland", "film", "frame"), COL["tube"])
    st(14, [], [mv(arm_asm, (160, 0, 0)), mv(part("Band clamps (2)", C["arm_bands"].shape, COL["band"]), (-160, 0, 0))],
       "arm assembly onto the pole",
       "Arm square to the street and level within 1 degree; bands through the slots and across the plate front",
       context=[pole(AZ - 300, AZ + 300)], elev=20, azim=-40, label_done=False)
    top_asm = part("Pole-top mount with panel", S("sleeve", "rivnuts", "disc", "disc_screws", "post", "plugs", "lclip_r", "lclip_l",
                                                  "uclip_r", "uclip_l", "rail", "panel", "post_bolts", "clip_screws"), COL["sleeve"])
    st(15, [], [mv(top_asm, (0, 0, 220))],
       "pole-top mount onto the pole top",
       "Down until the disc sits on the pole top; panel turned toward the equator; three set screws; panel lanyard",
       context=[pole(D["pole_top"] - 400, D["pole_top"])], elev=15, azim=-55, label_done=False)
    done = [part("Enclosure assembly", S("enc_plate", "enc_vs_up", "enc_vs_low", "body", "lugs", "lid", "glands", "vent", "ports",
                                         "antenna", "enc_bands"), COL["body"]),
            part("Arm and head", S("arm_plate", "arm_vs_up", "arm_vs_low", "arm_tube", "arm_cap", "arm_brk_up", "arm_brk_low",
                                   "housing", "film", "frame", "head_gland", "arm_bands"), COL["tube"])]
    st(16, done, [mv(part("Sensor cable: port A, up the pole, beside the arm, into the head", C["cable"].shape, COL["cable"]), (0, 140, 0)),
                  mv(part("Panel lead: from the sleeve, down the pole, into gland 1", C["panel_lead"].shape & _box_below(AZ + 300), COL["lead"]), (0, 260, 0))],
       "sensor cable and panel lead",
       "Both tied to the pole side by side every 150 mm with UV-stable ties, over the bands, never under them. Seen from the side they run on",
       context=[pole(EZ - 300, AZ + 300)], elev=12, azim=100, label_done=False, size=(8, 7))
    nz = P["notice_z"]
    st(17, [], [mv(part("Notice plate", C["notice"].shape, COL["notice"]), (-90, 0, 0)),
                mv(part("Stainless cable ties (2)", C["notice_ties"].shape, COL["band"]), (90, 0, 0))],
       "public notice plate",
       "Plate back against the pole, facing the sidewalk; ties through the slots, pulled tight, tails cut flush",
       context=[pole(nz - 250, nz + 250)], elev=15, azim=-150, label_done=False)
    return out


def _box_below(z):
    import build123d as b
    return b.Pos(PX, 0, z - 2000) * b.Box(4000, 4000, 4000)


def _box_above(z):
    import build123d as b
    return b.Pos(PX, 0, z + 2000) * b.Box(4000, 4000, 4000)


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 6.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 66); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 64, "CurbCount prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 60.6, "The FieldNode core is wired exactly as FieldNode's build plan shows. CurbCount adds only the sensor cable and the panel extension lead.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.4, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.35)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, t, color, ha="left"):
        ax.text(x, y, t, fontsize=7.2, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(3, 38, 16, 14, "Solar panel", "6 W, 9 V class,\nits own 1 m lead", "#1E3A8A")
    blk(26, 38, 16, 14, "Inline connector", "sealed, 2-pin,\ntaped to the pole", "#991B1B")
    ax.add_patch(FancyBboxPatch((50, 10), 38, 46, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(51.5, 54.6, "FieldNode core (wired as FieldNode)", fontsize=8, color=MUT, va="top")
    blk(53, 38, 32, 12, "Connector strip", "panel input; port A supply and\nsignals; gland 2 and port B unused", "#7C3AED")
    blk(53, 14, 32, 18, "Charger, cell, controller", "STM32WL reads the array over I2C\nand runs the tracker; switches the\nport A 3.3 V rail; 0.5 A rail fuse", "#16A34A")
    blk(97, 30, 19, 22, "Thermal array", "breakout in the head:\n3.3 V, GND,\nSDA, SCL", "#7C3AED")
    wire([(19, 45), (26, 45)], RED); lab(22.5, 47.3, "panel lead", RED, "center")
    wire([(42, 45), (53, 45)], RED); lab(43, 47.3, "extension, 0.75 mm²,\nin through gland 1", RED)
    wire([(69, 38), (69, 32)], GRY, 1.4)
    wire([(85, 44), (97, 44)], BLU); wire([(85, 41), (97, 41)], RED)
    ax.text(86, 36.2, "Sensor cable:\nM12 plug on port A,\nopen end through\nthe head gland", fontsize=7.2, color=INK, va="top", linespacing=1.3)
    lab(91, 38.4, "4 of 5 cores, 0.25 mm²", MUT, "center")
    ax.text(97, 27.5, "Solder each core to the breakout's\npins; heat-shrink every joint;\nleave the fifth core cut back.", fontsize=7.2, color=MUT, va="top")
    ax.text(3, 30, "Pins: port A's pin numbers follow the FieldNode\nsensor port pinout once it is agreed; check the\nbreakout's labels, not wire colours.",
            fontsize=7.4, color=INK, va="top")
    ax.text(3, 19, "Red: power. Blue: signal (I2C).", fontsize=7.4, color=MUT, va="top")
    ax.text(3, 15, "All circuits extra-low voltage: 3.6 V cell,\n3.3 V sensor rail, under 15 V from the panel.", fontsize=7.4, color=MUT, va="top")
    ax.text(3, 7.5, "Safety: cell out and fuse out until the stop points in section 6 of the plan are passed.", fontsize=7.6, color="#B45309", fontweight="bold")
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    OUT.mkdir(parents=True, exist_ok=True)
    for w in what:
        name, _, sel = w.partition(":")
        if sel:
            r = fns[name]({int(v) for v in sel.split(",")})
        else:
            r = fns[name]()
        print(w, "->", r)
