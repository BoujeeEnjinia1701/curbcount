"""CurbCount product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is: FieldNode enclosure with lid, lugs, glands, ports,
vent, antenna, internal plate, cell, boards and connector strip; both saddle plates, V-saddles and bands; the arm tube,
brackets and end cap; the sensor head with hood, wedge pad, window frame, film and array; the pole-top mount, rail plate and
panel; both cables, the notice plate, and every bolt, nut, washer and screw. Only the site is added, as context parts: a
concrete sidewalk slab and kerb on the street, the 114.3 mm steel pole set into the slab, a painted bike lane line and a 1.75 m
mannequin standing on the sidewalk for scale. Ground level is model z = 0 (the road surface); the sidewalk top is
sw_h = 150 mm above it, as in model.py, and every site part reaches below ground.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "CurbCount: privacy-safe street counter for people, bikes and vehicles"

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=42,-112", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 10, "az": -128, "args": _SITE,
     "note": "Site render from the sidewalk, front left and a little above (about 10 deg elevation): the counter on a 114 mm "
             "street pole at a curb, FieldNode enclosure at 3.85 m, sensor head on its arm reaching over the street, solar panel on "
             "the pole top; 1.75 m person on the sidewalk for scale"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 22, "az": -128,
     "note": "Studio render from the sidewalk side, front left and above (about 22 deg elevation), without the site: enclosure "
             "and saddle plate, arm and sensor head on its saddle plate, pole-top mount and panel, cables, bands and fasteners"},
    {"name": "head", "groups": ["head"], "explode": False, "el": 20, "az": -40,
     "note": "Sensor head and arm from the street side, front right and above (about 20 deg elevation): printed housing with sun "
             "hood and COUNTS ONLY plaque, window frame over the HDPE film, arm tube, angle brackets and arm saddle plate"},
]


def site():
    """Street context: sidewalk slab with kerb, pole set into it, bike-lane line, mannequin (all reach below z = 0)."""
    P = M.PARAMS
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    sw = Pos(-P["sidewalk_w"] / 2 + 700, 0, (P["sw_h"] - 100) / 2) * Box(P["sidewalk_w"] + 1400, 6000, P["sw_h"] + 100)
    ctx("Sidewalk slab and kerb", break_edges(sw, 6), "concrete")
    D = M.derived()
    ctx("Street pole 114.3 mm", Pos(P["pole_x"], 0, (P["sw_h"] + P["pole_h"] - 100) / 2) * Cylinder(D["pole_r"], P["pole_h"] + 100), "galvanised")
    ctx("Bike lane line", Pos(P["bike_w"], 0, -2) * Box(100, 6000, 6), "label")
    try:
        import context_parts
        man = Pos(-1700, -1400, P["sw_h"]) * Rot(0, 0, 35) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # scale figure only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p); q["group"] = "shell"; out.append(q)
        bb = p["shape"].bounding_box()
        if bb.min.Z > 4150 and bb.max.Z < 4750 and bb.min.X > -420 and p["kind"] != "context":   # arm, saddle plate and head region
            r = dict(p); r["group"] = "head"; out.append(r)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "head" for p in ps), "head,",
          sum(p["group"] == "context" for p in ps), "context")
