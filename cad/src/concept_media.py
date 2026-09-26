"""LampNode concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Ground at Z = 0, the pole at the origin, the arm running along +X over the
road. The existing pole, arm and cobra-head luminaire are grey context (no BOM number); LampNode
parts are colored and numbered to match bom/bom.csv.

The kit renderer frames the parts it is given, so a 90 mm controller on an 8 m pole would be a
few pixels wide. render_all() therefore runs on the LampNode parts with the luminaire head as
context (exploded view, cutaway, blueprint, 3D model), and a street-scene hero with the 1.75 m
figure and a close-up inset is composed afterwards in make_hero().
"""
import math
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch
from build123d import Box, Cylinder, Cone, Pos, Rot, Solid, Plane, Vector, Axis, fillet
import concept
from concept import Part, render_all, human_figure, export_web_model

GREY = "#A3A9B1"
DARK = "#4B5563"

# ---------------- existing street furniture (context) ----------------
POLE_H = 7700.0            # pole shaft top
ARM_Z = 7800.0             # arm centerline height
ARM_R = 30.0
LUM_X0, LUM_L, LUM_W, LUM_H = 1500.0, 650.0, 320.0, 130.0   # cobra-head luminaire
LUM_ZC = ARM_Z
LUM_TOP = LUM_ZC + LUM_H / 2
REC_X = 1620.0             # ANSI C136.41 receptacle on the luminaire top
REC_H = 20.0
Z0 = LUM_TOP + REC_H       # underside of the LampNode twist-lock base


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def polyline_tube(pts, r):
    s = None
    for a, b in zip(pts[:-1], pts[1:]):
        t = tube3(a, b, r)
        s = t if s is None else s + t
    return s


pole = Pos(0, 0, POLE_H / 2) * Cone(95, 60, POLE_H)
arm_full = (tube3((0, 0, POLE_H - 250), (320, 0, ARM_Z), ARM_R)
            + tube3((320, 0, ARM_Z), (LUM_X0 + 40, 0, ARM_Z), ARM_R))
arm_seg = tube3((880, 0, ARM_Z), (LUM_X0 + 40, 0, ARM_Z), ARM_R)
lum_body = Pos(LUM_X0 + LUM_L / 2, 0, LUM_ZC) * Box(LUM_L, LUM_W, LUM_H)
lum_body = fillet(lum_body.edges().filter_by(Axis.X), 40)
lens = Pos(LUM_X0 + LUM_L / 2 + 40, 0, LUM_ZC - LUM_H / 2 - 8) * Box(LUM_L - 180, LUM_W - 70, 16)
receptacle = Pos(REC_X, 0, LUM_TOP + REC_H / 2) * Cylinder(52, REC_H)

# ---------------- LampNode controller (twist-lock, on the luminaire) ----------------
X = REC_X
base = Pos(X, 0, Z0 + 12.5) * Cylinder(47, 25)
for ang in (0, 120, 240):  # three power blades into the receptacle
    t = math.radians(ang)
    base = base + Pos(X + 26 * math.cos(t), 26 * math.sin(t), Z0 - 6) * Box(4, 12, 14)

dome_out = Pos(X, 0, Z0 + 25 + 36) * Cylinder(45, 72)
dome_out = fillet(dome_out.edges().group_by(Axis.Z)[-1], 20)
dome_in = Pos(X, 0, Z0 + 25 + 34) * Cylinder(42, 70)
dome_in = fillet(dome_in.edges().group_by(Axis.Z)[-1], 17)
dome = dome_out - dome_in

surge = Pos(X, 0, Z0 + 28) * Cylinder(40, 2) + Pos(X - 18, 18, Z0 + 34) * Cylinder(7, 10) \
    + Pos(X - 18, -18, Z0 + 34) * Cylinder(7, 10)
psu = Pos(X + 10, 0, Z0 + 41) * Box(44, 30, 22)
relay = Pos(X - 22, 0, Z0 + 40) * Box(18, 24, 20)
meter = Pos(X + 35, 8, Z0 + 33) * Box(8, 12, 8)
ctrl = Pos(X, 0, Z0 + 60) * Cylinder(40, 2) + Pos(X + 8, 6, Z0 + 63) * Box(16, 16, 4)
antenna = Pos(X - 28, 14, Z0 + 76) * Cylinder(3, 28)
light = Pos(X, 0, Z0 + 76) * Cylinder(4, 28) + Pos(X, 0, Z0 + 89) * Cylinder(6, 4)
# side M12 port and cable to the sensor head, routed back along the arm
port = Pos(X - 52, 0, Z0 + 12) * Rot(0, 90, 0) * Cylinder(8, 16)

# ---------------- sensor head (clamped under the arm) ----------------
HX = 1150.0
H_TOP = ARM_Z - ARM_R - 15
head_c = (HX, 0, H_TOP - 30)
head_out = Pos(*head_c) * Box(120, 90, 60)
head = head_out - Pos(*head_c) * Box(114, 84, 54)
radar = Pos(HX + 50, 0, H_TOP - 32) * Rot(0, -25, 0) * Box(6, 50, 44)
head_board = Pos(HX - 10, 0, H_TOP - 44) * Box(70, 70, 3)
exp_ports = Pos(HX - 30, 20, H_TOP - 68) * Cylinder(10, 18) + Pos(HX - 30, -20, H_TOP - 68) * Cylinder(10, 18)
clamps = None
for dx in (-45, 45):
    ring = Pos(HX + dx, 0, ARM_Z) * Rot(0, 90, 0) * (Cylinder(ARM_R + 5, 20) - Cylinder(ARM_R, 22))
    clamps = ring if clamps is None else clamps + ring
clamps = clamps + Pos(HX, 0, ARM_Z - ARM_R - 7) * Box(130, 30, 14)

cable = port + polyline_tube([(X - 58, 0, Z0 + 12), (X - 90, 0, Z0 + 4), (LUM_X0 - 10, 0, ARM_Z + ARM_R + 6),
                              (HX + 90, 0, ARM_Z + ARM_R + 6), (HX + 90, 42, ARM_Z), (HX + 55, 42, H_TOP - 20)], 4)

parts = [
    Part("Twist-lock base, 7-contact", base, "#374151", 1, (0, 0, -40)),
    Part("Dome cover, UV-stable", dome, "#E5E7EB", 2, (0, 0, 320)),
    Part("Surge protection, fuse", surge, "#C2410C", 3, (0, 0, 10)),
    Part("Isolated power supply", psu, "#7C3AED", 4, (40, 0, 60)),
    Part("Fail-on relay", relay, "#D4A017", 5, (-60, 0, 55)),
    Part("Energy metering", meter, "#2563EB", 6, (60, 70, 30)),
    Part("Controller, LoRaWAN radio", ctrl, "#0F766E", 7, (0, 0, 115)),
    Part("Antenna", antenna, "#111827", 8, (-40, 0, 150)),
    Part("Light sensor and pipe", light, "#16A34A", 9, (0, 0, 190)),
    Part("M12 port and cable", cable, "#1F2937", 10, (0, 0, 0)),
    Part("Sensor head enclosure", head, "#CBD5E1", 11, (0, -260, -40)),
    Part("24 GHz radar presence sensor", radar, "#0EA5E9", 12, (130, 0, -60)),
    Part("Sensor head board", head_board, "#115E59", 13, (-20, 0, -150)),
    Part("Expansion ports (2)", exp_ports, "#9333EA", 14, (0, 0, -270)),
    Part("Arm band clamps", clamps, "#94A3B8", 15, (0, 0, 70)),
]

context = [Part("Existing luminaire and arm", lum_body + receptacle + arm_seg, GREY),
           Part("Luminaire lens", lens, "#F3F4F6")]

KEY_FIGURES = [
    "Plugs into ANSI C136.41 7-contact receptacle (proposed)",
    "120 to 277 V AC; 0 to 10 V dimming; fails on at night",
    "100 W luminaire: about 243 kWh/yr vs 410 (estimate)",
    "24 GHz radar: presence only, no images or audio",
    "LoRaWAN; about $124 in parts (indicative)",
]

FLOW = {"title": "annual energy per 100 W luminaire, kWh per year (estimates)", "unit": "kWh",
        "stages": [("Full power, photocell", 410), ("Schedule only", 300), ("Presence dimming", 236),
                   ("With controller use", 243)],
        "losses": [(0, "Saved by schedule", 110), (1, "Saved by presence", 64)]}


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
    street = [Part("Pole, arm and luminaire", pole + arm_full + lum_body + receptacle, GREY),
              Part("Luminaire lens", lens, "#F3F4F6"),
              Part("Sidewalk", sidewalk, "#D6D3D1"), Part("Curb", curb, "#A8A29E"), Part("Road", road, "#6B7280"),
              human_figure(1750, x=-900, y=-700, z=150)]
    scene = street + parts
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
    ox, oy = max(x0 - m, 0), max(y0 - 3 * m, 0)
    for pt, txt, dx, dy in (((REC_X, 0, Z0 + 95), "LampNode controller\n(twist-lock, items 1 to 9)", -120, -12),
                            ((HX, 0, H_TOP - 75), "Sensor head\n(items 11 to 15)", 0, 45)):
        u, v = pc(pt)
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


def local(ps):
    """Shift parts so the controller sits near the origin. concept.cutaway_parts() builds its cutter
    around X = Z = 0, so parts 7.9 m up the pole would otherwise miss it."""
    sh = Pos(-REC_X, 0, -Z0 - 50)
    return [Part(p.name, sh * p.shape, p.color, p.bom, p.explode, p.alpha) for p in ps]


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    concept.ROOT = ROOT
    render_all(local(parts), project="LampNode", title="Streetlight controller concept", dwg_no="LPN-DWG-010",
               key_figures=KEY_FIGURES, scale_figure=False, context=local(context), flow=FLOW,
               cut_exclude=("M12 port and cable", "Sensor head enclosure", "24 GHz radar presence sensor",
                            "Sensor head board", "Expansion ports (2)", "Arm band clamps"))
    # cutaway again with numbered callouts matching the BOM (render_all draws it unlabeled)
    head_names = ("M12 port and cable", "Sensor head enclosure", "24 GHz radar presence sensor",
                  "Sensor head board", "Expansion ports (2)", "Arm band clamps")
    concept._render(concept.cutaway_parts([p for p in local(parts) if p.name not in head_names]),
                    ROOT / "media" / "cutaway.png", azim=-90, elev=18, labels=True,
                    title="LampNode: cutaway of the controller")
    # 3D viewer with the luminaire head for context
    export_web_model(local(parts + context), "media", title="LampNode: Streetlight controller concept")
    make_hero()
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
