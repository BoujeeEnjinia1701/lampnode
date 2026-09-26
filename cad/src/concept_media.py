"""LampNode concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

LampNode parts come from cad/src/model.py (local frame: origin at the underside of the
twist-lock base, X along the arm away from the pole), so the media match the STEP files and
drawing LPN-DWG-001. Parts are colored and numbered to match bom/bom.csv. The existing pole,
arm, receptacle and cobra-head luminaire are grey context (no BOM number). Figures on the
sheet and in the flow diagram come from docs/04-calcs/sizing.py (LPN-CAL-001).

The kit renderer frames the parts it is given, so a 90 mm controller on an 8 m pole would be a
few pixels wide. render_all() therefore runs on the LampNode parts in the local frame with the
luminaire head as context (exploded view, cutaway, blueprint, 3D model), and a street-scene hero
with the 1.75 m figure and a close-up inset is composed afterwards in make_hero(). The local
frame already puts the controller at the origin, where the kit's cutaway cutter is centered.
"""
import math
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch
from build123d import Box, Cone, Pos, Axis, fillet
import concept
from concept import Part, render_all, human_figure, export_web_model
from model import PARAMS as P, build_parts, head_frame, tube

GREY = "#A3A9B1"
DARK = "#4B5563"

# ---------------- placement of the local model on the street (mm) ----------------
REC_X = 1620.0             # receptacle position along the arm from the pole axis
ARM_Z = 7800.0             # arm centerline height above the road (reference case)
Z0 = ARM_Z - P["arm_z"]    # underside of the twist-lock base
PLACE = Pos(REC_X, 0, Z0)
POLE_H = 7700.0
ARM_R = P["arm_d"] / 2
LUM_X0, LUM_L, LUM_W, LUM_H = 1500.0, 650.0, 320.0, 130.0   # cobra-head luminaire
REC_TOP = Z0 - P["gasket_t"] - P["receptacle_h"]            # luminaire top under the receptacle
LUM_ZC = REC_TOP - LUM_H / 2

model = build_parts()
parts = [Part(n, s, c, b, e) for n, s, c, b, e in model if b is not None]
ref = {n: s for n, s, c, b, e in model if b is None}

# luminaire head in the local frame (for render_all) and on the street (for the hero)
lum_body = Pos(LUM_X0 + LUM_L / 2 - REC_X, 0, LUM_ZC - Z0) * Box(LUM_L, LUM_W, LUM_H)
lum_body = fillet(lum_body.edges().filter_by(Axis.X), 40)
lens = Pos(LUM_X0 + LUM_L / 2 + 40 - REC_X, 0, LUM_ZC - Z0 - LUM_H / 2 - 8) * Box(LUM_L - 180, LUM_W - 70, 16)
arm_to_lum = tube((P["arm_x1"], 0, P["arm_z"]), (LUM_X0 + 40 - REC_X, 0, P["arm_z"]), ARM_R)
context = [Part("Existing luminaire, receptacle and arm",
                lum_body + ref["Luminaire receptacle (reference)"] + ref["Lamp arm (reference)"] + arm_to_lum, GREY),
           Part("Luminaire lens", lens, "#F3F4F6")]

pole = Pos(0, 0, POLE_H / 2) * Cone(95, 60, POLE_H)
arm_full = (tube((0, 0, POLE_H - 250), (320, 0, ARM_Z), ARM_R)
            + tube((320, 0, ARM_Z), (LUM_X0 + 40, 0, ARM_Z), ARM_R))
HX, H_TOP, _ = head_frame(P)

KEY_FIGURES = [
    "Plugs into ANSI C136.41 7-contact receptacle",
    "120 to 277 V AC; 0 to 10 V dimming; fails on at night",
    "100 W lamp at 40 N: 432 kWh/yr to 275 to 285 (34 to 36 %)",
    "24 GHz radar: presence only, no images or audio",
    "LoRaWAN; 0.68 W average; $130 in parts (indicative)",
]

# LPN-CAL-001 section 2, dimmed driver model (estimates)
FLOW = {"title": "annual energy per 100 W luminaire at 40 N, kWh per year (estimates, LPN-CAL-001)",
        "unit": "kWh",
        "stages": [("Full power, photocell", 432), ("Schedule only", 324), ("Presence dimming", 279),
                   ("With controller use", 285)],
        "losses": [(0, "Saved by schedule", 108), (1, "Saved by presence", 45)]}


def _project(shapes, elev, azim, W, H, pad=0.06):
    """Replicates concept._zbuffer's orthographic framing so a world point can be placed on the image."""
    e, a = np.radians(elev), np.radians(azim)
    d = -np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    right = np.cross(d, [0, 0, 1.0]); right /= np.linalg.norm(right)
    up = np.cross(right, d)
    P = np.stack([right, up, -d])
    pts = []
    for s in shapes:
        v, t = concept._tris(s)
        pts.append(v[t].reshape(-1, 3))
    q = np.vstack(pts) @ P.T
    lo, hi = q[:, :2].min(0), q[:, :2].max(0)
    span = (hi - lo).max() * (1 + 2 * pad)
    c = (lo + hi) / 2
    scale = min(W, H) / span

    def proj(p):
        xy = (np.asarray(p, float) @ P.T)[:2]
        return (xy[0] - c[0]) * scale + W / 2, H / 2 - (xy[1] - c[1]) * scale
    return proj


def make_hero():
    """Street scene with the 1.75 m figure, plus an inset close-up of the luminaire head."""
    md = ROOT / "media"
    tmp = md / "_hero_tmp"; tmp.mkdir(exist_ok=True)
    sidewalk = Pos(-737.5, 0, 75) * Box(2525, 3200, 150)
    road = Pos(2800, 0, -10) * Box(4400, 3200, 20)
    curb = Pos(600, 0, 75) * Box(150, 3200, 150)
    lum_st = PLACE * (lum_body + ref["Luminaire receptacle (reference)"])
    street = [Part("Pole, arm and luminaire", pole + arm_full + lum_st, GREY),
              Part("Luminaire lens", PLACE * lens, "#F3F4F6"),
              Part("Sidewalk", sidewalk, "#D6D3D1"), Part("Curb", curb, "#A8A29E"), Part("Road", road, "#6B7280"),
              human_figure(1750, x=-900, y=-700, z=150)]
    placed = [Part(p.name, PLACE * p.shape, p.color, p.bom, p.explode) for p in parts]
    scene = street + placed
    elev, azim, size, dpi = 20, -62, (8, 6), 160
    concept._render(scene, tmp / "scene.png", elev=elev, azim=azim, size=size, dpi=dpi)
    concept._render(context + parts, tmp / "close.png", elev=22, azim=-58, size=(5, 4), dpi=160)
    W, H = size[0] * dpi, size[1] * dpi
    proj = _project([p.shape for p in scene], elev, azim, W, H)
    cx, cy = proj((REC_X - 150, 0, Z0))

    img = plt.imread(tmp / "scene.png"); close = plt.imread(tmp / "close.png")
    fig = plt.figure(figsize=size, dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(img); ax.set_axis_off()
    box = Rectangle((cx - 55, cy - 35), 110, 70, fill=False, ec=concept.ACCENT, lw=1.2)
    ax.add_patch(box)
    nz = np.where(close[..., :3].min(-1) < 0.97)
    y0, y1, x0, x1 = nz[0].min(), nz[0].max(), nz[1].min(), nz[1].max()
    m = 25
    crop = close[max(y0 - 3 * m, 0):y1 + 3 * m, max(x0 - m, 0):x1 + m]
    ins = fig.add_axes([0.55, 0.40, 0.43, 0.46])
    ins.imshow(crop); ins.set_xticks([]); ins.set_yticks([])
    for s in ins.spines.values():
        s.set_edgecolor(concept.ACCENT); s.set_linewidth(1.2)
    pc = _project([p.shape for p in context + parts], 22, -58, 800, 640)
    loc = lambda q: (q[0] - REC_X, q[1], q[2] - Z0)
    ox, oy = max(x0 - m, 0), max(y0 - 3 * m, 0)
    for pt, txt, dx, dy in (((REC_X, 0, Z0 + 95), "LampNode controller\n(twist-lock, items 1 to 9)", -120, -12),
                            ((REC_X + HX, 0, Z0 + H_TOP - 75), "Sensor head\n(items 11 to 15)", 0, 45)):
        u, v = pc(loc(pt))
        ins.annotate(txt, (u - ox, v - oy), (u - ox + dx, v - oy + dy), fontsize=6.5, color=concept.INK,
                     ha="center", va="bottom" if dy < 0 else "top",
                     arrowprops=dict(arrowstyle="-", color=concept.ACCENT, lw=0.8))
    ins.set_xlabel("Close-up: controller on the luminaire, sensor head under the arm", fontsize=7, color=concept.INK)
    fig.add_artist(ConnectionPatch((cx + 55, cy + 35), (0.0, 1.0), "data", "axes fraction", axesA=ax, axesB=ins,
                                   color=concept.ACCENT, lw=0.9))
    fig.text(0.02, 0.97, "LampNode", fontsize=9, fontweight="bold", color=concept.INK, va="top")
    fig.text(0.02, 0.93, "CONCEPT, NOT FOR FABRICATION", fontsize=6.5, color="#B45309", va="top")
    fig.text(0.02, 0.03, "Grey figure: 1.75 m person for scale; pole about 7.8 m", fontsize=7.5,
             color="#4B5563", va="bottom")
    fig.savefig(md / "hero.png", facecolor="white"); plt.close(fig)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    concept.ROOT = ROOT
    render_all(parts, project="LampNode", title="Streetlight controller concept", dwg_no="LPN-DWG-010", date="2026-09-25",
               key_figures=KEY_FIGURES, scale_figure=False, context=context, flow=FLOW,
               cut_exclude=("M12 port and cable", "Sensor head enclosure", "24 GHz radar presence sensor",
                            "Sensor head board", "Expansion ports (2)", "Arm band clamps"))
    # cutaway again with numbered callouts matching the BOM (render_all draws it unlabeled)
    head_names = ("M12 port and cable", "Sensor head enclosure", "24 GHz radar presence sensor",
                  "Sensor head board", "Expansion ports (2)", "Arm band clamps")
    concept._render(concept.cutaway_parts([p for p in parts if p.name not in head_names]),
                    ROOT / "media" / "cutaway.png", azim=-90, elev=18, labels=True,
                    title="LampNode: cutaway of the controller")
    # 3D viewer with the luminaire head for context
    export_web_model(parts + context, "media", title="LampNode: Streetlight controller concept")
    make_hero()
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
