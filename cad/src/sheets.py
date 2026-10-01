"""CurbCount general arrangement sheet CBC-DWG-001, Rev P2 (TRL 3, CBC-DDR-002 applied).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CBC-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py. Dimensions come from PARAMS and derived(), so they follow any parameter
change. The concept blueprint in media/ is CBC-DWG-010. PRELIMINARY, NOT FOR FABRICATION.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound, Pos, Cylinder  # noqa: E402
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build_parts, derived  # noqa: E402

DATE = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35):
    """As drawing.project_views, edge by edge, so a degenerate projected edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    dl = 11  # room the kit leaves left of and above the views for overall dimensions
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    parts = build_parts(P)
    # pole stub around the counter only (the notice plate at eye height is listed in the notes, not drawn),
    # so the sheet reaches a readable scale; heights above the road are given as labels
    z_cut = D["enc_bot"] - P["whip"][1] - 60
    pole = Pos(P["pole_x"], 0, (z_cut + D["pole_top"]) / 2) * Cylinder(D["pole_r"], D["pole_top"] - z_cut)
    asm = Compound(children=[v for kk, v in parts.items() if kk != "notice"] + [pole])
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="CurbCount", title="General arrangement", dwg_no="CBC-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Aluminium mounts, ASA head; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "DDR-002: 6 W panel, one cell, no head processor", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = [_t(M + 6, M + 14, "PRELIMINARY, NOT FOR FABRICATION", 3.0, 600, "#B45309")]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    L.append(_t(X(P["pole_x"]) + D["pole_r"] * k + 2, Z(z_cut) - 2, "POLE CONTINUES TO SIDEWALK", 1.9, 400, MUTED, "start"))
    xr_lab = c["right"][0] + (bb.max.Y - bb.min.Y) * k + 8
    xl = X(bb.min.X) - 13
    L += [ext(X(D["enc_xc"]), Z(D["enc_top"]), xl - 1, Z(D["enc_top"])), ext(X(D["enc_xc"]), Z(D["enc_bot"]), xl - 1, Z(D["enc_bot"]))]
    L += dim_v(xl, Z(D["enc_top"]), Z(D["enc_bot"]), f"{P['enc'][2]:.0f}")
    L += [ext(X(P["pole_x"]), Z(D["arm_z"]), xl - 8, Z(D["arm_z"])), ext(X(D["enc_xc"]), Z(P["enc_zc"]), xl - 8, Z(P["enc_zc"]))]
    L += dim_v(xl - 7, Z(D["arm_z"]), Z(P["enc_zc"]), f"{D['arm_z'] - P['enc_zc']:.0f}")
    zt = D["arm_z"] + 180
    L += [ext(X(P["pole_x"]), Z(D["arm_z"]) - 2, X(P["pole_x"]), Z(zt) - 1), ext(X(P["head_x"]), Z(D["head_zc"]) - 2, X(P["head_x"]), Z(zt) - 1)]
    L += dim_h(X(P["pole_x"]), X(P["head_x"]), Z(zt), f"{D['reach']:.0f} reach")
    L += leader(X(P["head_x"]), Z(P["window_z"]), xr_lab - 1, Z(P["window_z"] - 250),
                f"WINDOW {P['window_z']:.0f} ABOVE ROAD,")
    L.append(_t(xr_lab, Z(P["window_z"] - 250) + 3.8, f"TILT {P['tilt']:.1f} DEG", 2.1, 400, INK, "start"))
    L += leader(X(P["pole_x"] + 150), Z(D["arm_z"]), X(P["pole_x"] - 150) - 9, Z(D["arm_z"] + 260),
                f"ARM AXIS {D['arm_z']:,.0f} ABOVE ROAD", "end")
    L += leader(X(D["panel_c"][0]), Z(D["panel_c"][2]), X(D["panel_c"][0]) - 20, Z(D["panel_top"] + 40),
                f"PANEL TOP {D['panel_top']:,.0f} ABOVE ROAD", "end")
    L += leader(X(D["enc_xc"]), Z(D["enc_bot"] - 80), X(D["enc_xc"]) - 14, Z(D["enc_bot"] - 250), "M12 PORTS, ANTENNA DOWN", "end")

    # right view (from +X): Y across the sheet
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    pl = P["panel"][1]
    L += dim_h(Yr(-pl / 2), Yr(pl / 2), Zr(D["panel_top"] + 100), f"{pl:.0f}")
    L += [ext(Yr(-pl / 2), Zr(D["panel_top"] - 50), Yr(-pl / 2), Zr(D["panel_top"] + 110)),
          ext(Yr(pl / 2), Zr(D["panel_top"] - 50), Yr(pl / 2), Zr(D["panel_top"] + 110))]
    L.append(_t(Yr(bb.max.Y) + 8, Zr(P["window_z"]), "ARRAY: 110 DEG ACROSS,", 1.9, 400, INK, "start"))
    L.append(_t(Yr(bb.max.Y) + 8, Zr(P["window_z"]) + 3, "75 DEG ALONG THE STREET", 1.9, 400, INK, "start"))

    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 100, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Pole {P['pole_od']} OD, {-P['pole_x']:.0f} behind the curb (site supplied, not in BOM)",
        f"Head {P['head'][0]:.0f} x {P['head'][1]:.0f} x {P['head'][2]:.0f}, window {P['window_z']:.0f} above road, tilt {P['tilt']} deg",
        f"Arm 40 x 40 x 2 Al, {D['arm_len']:.0f} long; reach {D['reach']:.0f} from pole axis",
        f"FieldNode enclosure {P['enc'][0]:.0f} x {P['enc'][1]:.0f} x {P['enc'][2]:.0f}, center {P['enc_zc']:.0f}",
        f"Panel 6 W (FieldNode) {P['panel'][0]:.0f} x {P['panel'][1]:.0f}, tilt {P['panel_tilt']:.0f} deg on a {P['sleeve'][0]:.0f} sleeve",
        "Four 12 mm stainless bands; no drilling of the pole",
        "M12 5-pin cable, enclosure port to head (FieldNode pinout)",
        f"Footprint {D['fp_x_min'] / 1000:.1f} to {D['fp_x_max'] / 1000:.1f} m across the street (CBC-CAL-001)",
        f"Notice plate {P['notice'][1]:.0f} x {P['notice'][2]:.0f} at {P['notice_z']:.0f} (not drawn); lanyards on panel and head",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "CBC-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
