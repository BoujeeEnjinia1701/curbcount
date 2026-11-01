"""CurbCount repo-specific parts helpers (small screws and placement) on top of .kit/cad_parts.py.

All fasteners are drawn along +Z with the head's bearing face at z = 0 and the shank down -Z, like cad_parts.
`put()` places such a part with its head on a point, pointing out along a direction.
"""
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[1] / ".kit")]
from build123d import Cylinder, Plane, Pos, Rot, extrude, Circle, Sketch, Solid, Vector  # noqa: E402
import cad_parts as cp  # noqa: E402

# sizes the parts library does not list: (s across flats, k head height, m nut height, washer d2, washer h, pitch)
cp.ISO.setdefault(4, (7, 2.8, 3.2, 9, 0.8, 0.7))
cp.ISO.setdefault(3, (5.5, 2.0, 2.4, 7, 0.5, 0.5))


def pan_screw(d, length):
    """Pan head machine screw (ISO 7045 class): head dia 2d, height 0.6d, shank down from z = 0."""
    head = Pos(0, 0, 0.3 * d) * Cylinder(d, 0.6 * d)
    head = cp.break_edges(head, 0.2 * d)
    return head + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def csk_screw(d, length):
    """Countersunk screw (ISO 7046 class, 90 degree head): flat top at z = 0, head dia 2d and depth d/2, shank to z = -length."""
    cone = Solid.make_cone(d / 2, d, d / 2, Plane.XY.offset(-d / 2))
    return cone + Pos(0, 0, -(d / 2 + length) / 2) * Cylinder(d / 2, length - d / 2)


def set_screw(d, length):
    """Cup-point socket set screw along +Z, top at z = 0, tip at z = -length."""
    s = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    return cp.break_edges(s, 0.4)


def spacer(od, idia, length):
    """Crush spacer tube from z = 0 to z = length."""
    return extrude(Sketch() + Circle(od / 2) - Circle(idia / 2), length)


def put(shape, origin, zdir):
    """Place a part drawn along +Z with its z = 0 plane at origin and +Z pointing along zdir."""
    zd = Vector(*zdir).normalized()
    xd = Vector(1, 0, 0) if abs(zd.X) < 0.9 else Vector(0, 1, 0)
    xd = (xd - zd * xd.dot(zd)).normalized()
    return Plane(origin=origin, x_dir=xd, z_dir=zd).location * shape
