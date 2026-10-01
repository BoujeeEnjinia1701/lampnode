"""LampNode prototype build plan pictures (LPN-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. A single picture can be drawn on its own with
"joint 3", "step 7" or "sheet 104", which keeps memory low. Every picture is drawn from
cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/LPN-DWG-101 to 108        making sketches for the made and drilled components
    docs/05-build-plan/base-holes.png      drilling layout of the twist-lock base, seen from below
    docs/05-build-plan/mains-layout.png    where each part sits on the mains board, seen from above
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, polar, zcyl, tube  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
D = derived(P)
C = build_components(P)
HX, HTOP = D["hx"], D["htop"]


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"base": "#374151", "blades": "#B8860B", "spacers": "#E7E5E4", "mboard": "#166534", "surge": "#C2410C",
       "psu": "#7C3AED", "relay": "#D4A017", "meter": "#2563EB", "standoffs": "#B8860B", "cboard": "#0F766E",
       "dome_gasket": "#111827", "dome": "#D1D5DB", "pipe": "#16A34A", "antenna": "#7C2D12", "socket": "#1F2937",
       "hbody": "#CBD5E1", "hlid": "#94A3B8", "gland": "#334155", "ports": "#9333EA", "hplate": "#64748B",
       "radar": "#0EA5E9", "hboard": "#115E59", "bracket": "#1D4ED8", "liners": "#111827", "bands": "#475569",
       "cable": "#1F2937", "bolt": "#111827", "ref": "#A3A9B1"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def cable_stub(length=70):
    """Plug and a short length of cable, for pictures where the whole 1 m run would swamp the view."""
    zm = P["m12_z"]
    x0 = -(P["base_d"] / 2 + 0.5) - 2 - P["m12_l"] - 40
    return win(C["cable"].shape, x0 - length, x0 + 41, -15, 15, zm - 15, zm + 15)


def arm(x0=-620, x1=-320):
    return tube((x0, 0, P["arm_z"]), (x1, 0, P["arm_z"]), P["arm_d"] / 2)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "base": part("Twist-lock base, drilled", S("base", "blades", "base_gasket"), COL["base"]),
        "mboard": part("Mains board with surge stage, supply, relay, metering", S("mboard", "surge", "psu", "relay", "meter"), COL["mboard"]),
        "spacers": part("Spacers, standoffs and M3 x 45 screws (3 each)", S("spacers", "standoffs", "stack_screws"), COL["standoffs"]),
        "cboard": part("Controller board with radio and supercapacitor", C["cboard"].shape, COL["cboard"]),
        "dome": part("Dome, printed, with 3 inserts", S("dome", "inserts"), COL["dome"]),
        "pipe": part("Light pipe rod", C["pipe"].shape, COL["pipe"]),
        "antenna": part("Antenna strip", C["antenna"].shape, COL["antenna"]),
        "socket": part("M12 socket", C["socket"].shape, COL["socket"]),
        "dgasket": part("Dome gasket and M3 x 30 screws (3)", S("dome_gasket", "dome_screws"), COL["dome_gasket"]),
        "hbody": part("Sensor head box, drilled", C["hbody"].shape, COL["hbody"]),
        "gland": part("Cable gland", C["gland"].shape, COL["gland"]),
        "hlid": part("Lid, drilled, with 2 expansion ports", S("hlid", "ports"), COL["hlid"]),
        "hplate": part("Internal plate with radar cradle", C["hplate"].shape, COL["hplate"]),
        "radar": part("Radar module", C["radar"].shape, COL["radar"]),
        "hboard": part("Head board on standoffs", C["hboard"].shape, COL["hboard"]),
        "bracket": part("Bracket, rubber strips, M4 screws (4)", S("bracket", "liners", "brk_screws"), COL["bracket"]),
        "bands": part("Band clamps (2)", C["bands"].shape, COL["bands"]),
        "cable": part("M12 plug and cable (shown cut short)", cable_stub(), COL["cable"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    import build123d as b
    M = made()
    sh = (330, 0, 120)             # the head group is drawn beside the controller, not 470 mm away
    off = {"base": (0, 0, -70), "mboard": (0, 0, 55), "spacers": (0, 0, 0), "cboard": (0, 0, 130), "dome": (0, 0, 270),
           "pipe": (0, 0, 390), "antenna": (0, -110, 210), "socket": (-110, 0, 210), "dgasket": (0, 0, -25),
           "hbody": (0, 0, 0), "gland": (0, 90, 0), "hlid": (0, 0, -230), "hplate": (0, 0, -90), "radar": (110, 0, -130),
           "hboard": (-30, 0, -150), "bracket": (0, 0, 70), "bands": (0, 0, 150), "cable": (-100, 0, 270)}
    head = {"hbody", "gland", "hlid", "hplate", "radar", "hboard", "bracket", "bands"}
    order = ["base", "spacers", "mboard", "cboard", "dome", "pipe", "antenna", "socket", "dgasket", "hbody", "gland",
             "hlid", "hplate", "radar", "hboard", "bracket", "bands", "cable"]
    parts = []
    for k in order:
        p = M[k]
        e = list(off[k])
        if k in head:
            e = [e[0] + sh[0], e[1] + sh[1], e[2] + sh[2]]
        p.explode = tuple(e)
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "LampNode prototype: every component, pulled apart",
                       subtitle="Numbered in build order: controller 1 to 9, sensor head 10 to 17, cable 18. The head is drawn beside the controller, not where it sits on the arm",
                       elev=16, azim=-76, size=(12, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="LampNode", date=DATE)
    out = []
    zc = D["mb0"]

    def want(n):
        return only is None or only == n

    if want(101):
        out.append(bv.component_sheet(
            Part("Twist-lock base", S("base", "blades", "base_gasket"), COL["base"]), [M["mboard"], M["spacers"], M["dome"]],
            dwg_no="LPN-DWG-101", title="LampNode twist-lock base (bought): drilling sketch",
            material="Bought ANSI C136.41 7-contact base kit, polycarbonate", view_shape=C["base"].shape, inset_view=(-35, -60),
            notes=["Bought base kit, 94 mm across, 25 mm tall. Drill six holes right through it.",
                   "All six sit on one 60 mm circle round the centre, between the blades:",
                   "  dome screws at 60, 180 and 300 degrees; stack screws at 0, 120 and",
                   "  240 degrees, anticlockwise from the street side seen from above.",
                   "  The base drilling layout picture shows them from below.",
                   "Drill 3.4 mm through, with a scrap block under the top face.",
                   "Countersink each hole from below, 6 mm across, so the screw heads sit",
                   "  flush inside the gasket ring and clear of the contact wells.",
                   "Keep the gasket ring (35 to 45 mm radius underneath) untouched.",
                   "Crimp a 150 mm lead on each blade (1.0 mm2) and each low-voltage",
                   "  contact (0.25 mm2) before anything is fitted on top.",
                   "Check: no hole breaks into a blade pocket or the gasket ring."], **base))

    if want(102):
        mb = C["mboard"].shape
        out.append(bv.component_sheet(
            Part("Mains board", mb, COL["mboard"]), [M["base"], M["spacers"], part("Parts", S("surge", "psu", "relay", "meter"), "#9CA3AF")],
            dwg_no="LPN-DWG-102", title="LampNode mains board: making sketch", material="Plated-hole FR4 prototype board 1.6 mm",
            view_shape=b.Pos(0, 0, -zc) * mb, inset_view=(30, -60),
            notes=["Cut an 80 mm disc from plated-hole prototype board (2.54 mm grid):",
                   "  scribe the circle, cut outside it with a coping saw, file to the line.",
                   "Three stack holes 3.4 mm on a 60 mm circle at 0, 120 and 240 degrees.",
                   "Three notches 11 mm wide, from 25 mm radius out to the edge, at 60, 180",
                   "  and 300 degrees: the dome bosses pass up through them.",
                   "Parts, from the mains board layout picture: supply 23 x 38 mm on the",
                   "  centre; relay on the pole side; varistor and thermal fuse at the left",
                   "  edge and metering module at the right edge, seen from the pole.",
                   "6 mm hole at 28 mm toward the street, 22 mm right: low-voltage leads.",
                   "Keep 6 mm of bare board between mains tracks and the 12 V side.",
                   "Fit a 3-way mains terminal block and a 6-way harness header.",
                   "Fit: sits on three 12 mm spacers; standoffs screw on top.",
                   "Check: flat; the dome bosses pass the notches freely."], **base))

    if want(103):
        cb = C["cboard"].shape
        out.append(bv.component_sheet(
            Part("Controller board", cb, COL["cboard"]), [M["mboard"], M["spacers"], M["base"]],
            dwg_no="LPN-DWG-103", title="LampNode controller board: making sketch", material="Plated-hole FR4 prototype board 1.6 mm",
            view_shape=b.Pos(0, 0, -D["cb0"]) * cb, inset_view=(30, -60),
            notes=["Cut an 80 mm disc as for the mains board; no notches.",
                   "Three holes 3.4 mm on a 60 mm circle at 0, 120 and 240 degrees.",
                   "Light sensor at the exact centre, on the top face; the light pipe",
                   "  ends 0.5 mm above it once the dome is on.",
                   "Radio module breakout 16 x 16 mm on the street side, its u.FL socket",
                   "  toward the right edge (seen from the pole) for the antenna lead.",
                   "Supercapacitor 10 mm across, 20 mm tall, standing 24 mm toward the pole",
                   "  and 6 mm to the right of the centre, clear of the screw heads.",
                   "Clock, accelerometer, 0 to 10 V stage and coil drive on the rest.",
                   "Fit: three M3 x 6 screws into the standoffs, top of board 70.2 mm",
                   "  above the underside of the base.",
                   "Check: nothing on the top face stands taller than 22 mm."], **base))

    if want(104):
        dm = C["dome"].shape
        out.append(bv.component_sheet(
            Part("Dome", S("dome", "inserts"), COL["dome"]), [M["base"], M["mboard"], M["cboard"], M["socket"]],
            dwg_no="LPN-DWG-104", title="LampNode dome: making sketch", material="ASA, 3D printed, 4 walls, 40 % infill",
            view_shape=b.Pos(0, 0, -D["dome0"]) * dm, inset_view=(22, -150),
            notes=["Print upside down on its top, in ASA in an enclosed printer.",
                   "Shell 90 mm across, 71 mm tall, 3 mm wall, 20 mm round top edge.",
                   "Three bosses 9 mm across, 10 mm tall, inside the foot on a 60 mm",
                   "  circle at 60, 180 and 300 degrees, each tied to the wall by a rib.",
                   "Press an M3 brass heat-set insert into each boss with a soldering iron.",
                   "Flat pad on the pole side (180 degrees): 24 x 24 mm, 6 mm thick, face",
                   "  0.5 mm outside the base edge, centre 27.6 mm above the dome foot.",
                   "  16.2 mm hole through it for the M12 socket.",
                   "Light pipe hole 8.2 mm at the top centre, with a 10 mm sleeve inside.",
                   "Gasket: cut a ring 90 mm outside, 84 mm inside from 1 mm EPDM sheet.",
                   "Fit: foot on the gasket; three M3 x 30 screws from under the base.",
                   "Check: the foot sits flat on the base all round, no light under it."], **base))

    if want(105):
        hb = C["hbody"].shape
        out.append(bv.component_sheet(
            Part("Sensor head box", hb, COL["hbody"]), [M["bracket"], M["hplate"], M["gland"], part("Arm", arm(), COL["ref"])],
            dwg_no="LPN-DWG-105", title="LampNode sensor head box (bought): drilling sketch",
            material="Bought IP66 polycarbonate box 120 x 90 x 60 mm", view_shape=b.Pos(-HX, 0, -HTOP) * hb, inset_view=(25, -60),
            notes=["Bought box; its base faces up and its 15 mm lid faces down.",
                   "The end wall facing the street end of the arm is the radar window:",
                   "  never drill it, paint it or put a label on it.",
                   "Top face: four 4.5 mm holes for the bracket screws, 25 mm each side",
                   "  of the middle along the box and 10 mm each side across it.",
                   "Left side wall, seen from the pole: one 16.2 mm hole for the cable gland,",
                   "  30 mm toward the street end from the middle, 20 mm below the top.",
                   "Tape the faces, pilot drill 3 mm slowly, open out with a step drill.",
                   "No solvents: polycarbonate crazes. Deburr inside and out.",
                   "Check the four inside bosses are 94 x 54 mm apart; if not, move the",
                   "  internal plate holes to suit."], **base))

    if want(106):
        lid = S("hlid", "ports")
        out.append(bv.component_sheet(
            Part("Lid with ports", lid, COL["hlid"]), [M["hbody"], M["hboard"]],
            dwg_no="LPN-DWG-106", title="LampNode sensor head lid (bought): drilling sketch",
            material="Lid of the bought IP66 box, polycarbonate", view_shape=b.Pos(-HX, 0, -D["hbot"]) * C["hlid"].shape, inset_view=(-35, -60),
            notes=["The lid is 15 mm deep and faces the street below.",
                   "Two 16.2 mm holes for the M12 expansion ports, 30 mm toward the pole",
                   "  end from the middle, 20 mm each side of the centre line (40 apart).",
                   "Drill as for the box: tape, 3 mm pilot, step drill, deburr.",
                   "Fit each port from outside with its seal, nut inside, maker's torque.",
                   "Solder a 150 mm lead set to each port and fit a plug-in connector,",
                   "  so the lid can come off without a soldering iron.",
                   "Check: each port seats flat on its seal; the lid gasket is unbroken."], **base))

    if want(107):
        pl = C["hplate"].shape
        out.append(bv.component_sheet(
            Part("Internal plate with radar cradle", pl, COL["hplate"]), [M["hbody"], M["radar"], M["hboard"]],
            dwg_no="LPN-DWG-107", title="LampNode head internal plate: making sketch", material="ASA, 3D printed, 100 % infill",
            view_shape=b.Pos(-HX, 0, -D["pl_bot"]) * pl, inset_view=(-55, -60),
            notes=["One print: a plate 104 x 64 x 3 mm and a cradle 4 mm thick, 46 mm wide,",
                   "  44 mm long, hanging below the street end at 25 degrees from upright.",
                   "Print with the plate flat on the bed and the cradle overhanging.",
                   "Four 3.4 mm holes 94 mm apart along and 54 mm apart across, to match",
                   "  the four bosses in the box (measure your box first).",
                   "Cradle: two 2.7 mm holes to match the radar module's mounting holes.",
                   "  The module sits 3 mm off the cradle on nylon spacers.",
                   "Head board: four M3 standoffs 6 mm long on the underside,",
                   "  at the board's corner holes, 4 mm in from each edge.",
                   "Fit: four M3 screws into the bosses from below.",
                   "Check: the radar face then tips 25 degrees down toward the street."], **base))

    if want(108):
        bk = C["bracket"].shape
        out.append(bv.component_sheet(
            Part("Bracket", bk, COL["bracket"]), [M["hbody"], M["bands"], part("Arm", arm(), COL["ref"])],
            dwg_no="LPN-DWG-108", title="LampNode arm bracket: making sketch", material="Aluminium sheet 2 mm, 5052 class",
            view_shape=b.Pos(-HX, 0, -HTOP) * bk, inset_view=(15, -50),
            notes=["Blank 110 x 70 mm from 2 mm sheet. Mark two fold lines 17 mm in from the",
                   "  long edges and fold both flanges up 90 degrees in a bending brake.",
                   "Folded: web 40 mm across outside; flanges 18 mm tall from the underside",
                   "  of the web (file the tops level if they come out taller).",
                   "Web: four 4.5 mm holes, 25 mm each side of the middle along the",
                   "  bracket and 10 mm each side of the centre line across it.",
                   "Band slots after folding: one through each flange, 14 x 3 mm, centred",
                   "  45 mm each side of the middle, just above the web: drill 3 mm at each",
                   "  end through the bend and file between. Deburr every edge.",
                   "Rubber strips: 110 x 5 mm, 1.5 mm EPDM, glued along each flange top,",
                   "  overhanging the flange 2 mm inside and 1 mm outside.",
                   "Check: the arm rests on both strips, not on the metal."], **base))
    return out


# ----------------------------------------------------------------- layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, Wedge
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    REPO = "github.com/BoujeeEnjinia1701/lampnode"
    res = []
    R = P["boss_r"]
    # base, seen from below: x to the right is +X as seen from below means mirror Y
    fig = plt.figure(figsize=(10, 8), dpi=150)
    ax = fig.add_axes([0.04, 0.06, 0.6, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    rb = P["base_d"] / 2
    ax.add_patch(Circle((0, 0), rb, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.add_patch(Wedge((0, 0), rb - 2, 0, 360, width=10, fc="#D1D5DB", ec=MUT, lw=0.6))
    ax.add_patch(Circle((0, 0), R, fc="none", ec=AC, lw=0.6, ls=(0, (6, 3))))

    def flip(x, y):          # seen from below: mirror across the X axis
        return x, -y
    for ang in P["blade_angles"]:
        x, y = flip(*polar(P["blade_r"], ang))
        t = matplotlib.transforms.Affine2D().rotate_deg_around(x, y, -ang) + ax.transData
        ax.add_patch(Rectangle((x - P["blade_w"] / 2, y - P["blade_l"] / 2), P["blade_w"], P["blade_l"], fc="#B8860B", ec=INK, lw=0.6, transform=t))
    for ang in (45, 135, 180, 0):
        x, y = flip(*polar(P["lv_contact_r"], ang))
        ax.add_patch(Circle((x, y), P["lv_contact_d"] / 2, fc="#FCD34D", ec=INK, lw=0.6))
    for angs, lab, col in ((P["dome_boss_ang"], "dome", "#B91C1C"), (P["stack_ang"], "stack", "#1D4ED8")):
        for a in angs:
            x, y = flip(*polar(R, a))
            ax.add_patch(Circle((x, y), 3.0, fc="white", ec=col, lw=1.0))
            ax.add_patch(Circle((x, y), 1.7, fc=col, ec=col, lw=0.5))
            lx, ly = flip(*polar(R + 22, a))
            ax.annotate(f"{lab} screw\n{a} degrees", (x, y), (lx, ly), ha="center", va="center", fontsize=7.5, color=col,
                        arrowprops=dict(arrowstyle="-", color=col, lw=0.6), bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    ax.annotate("pole side", (-rb, 0), (-rb - 8, -32), ha="right", va="center", fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    ax.annotate("street side", (rb, 0), (rb + 8, -32), ha="left", va="center", fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    ax.plot([-rb - 4, rb + 4], [0, 0], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.set_xlim(-rb - 45, rb + 45); ax.set_ylim(-rb - 25, rb + 25)
    fig.text(0.03, 0.965, "Twist-lock base: drilling layout, seen from below", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Six 3.4 mm holes on a 60 mm circle (dashed), countersunk from below. Angles counted from the street side, as seen from above.",
             fontsize=8.2, color=MUT, va="top")
    key = ["Red: dome screws, M3 x 30, into", "  the dome's three inserts", "Blue: board stack screws, M3 x 45,", "  through spacers and mains board",
           "Gold bars: power blades", "Yellow dots: low-voltage contacts", "Grey ring: gasket, leave untouched", "",
           "Seen from below, the angles run", "  clockwise. Mark them from above", "  and drill from the top face."]
    for i, t in enumerate(key):
        fig.text(0.67, 0.80 - i * 0.032, t, fontsize=8.5, color=INK, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "base-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "base-holes.png")

    # mains board, seen from above
    fig = plt.figure(figsize=(10, 8), dpi=150)
    ax = fig.add_axes([0.04, 0.06, 0.6, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    rb = P["board_d"] / 2
    ax.add_patch(Circle((0, 0), rb, fc="#DCFCE7", ec=INK, lw=1.2))
    for a in P["dome_boss_ang"]:
        t = matplotlib.transforms.Affine2D().rotate_deg_around(0, 0, a) + ax.transData
        ax.add_patch(Rectangle((P["notch_r"], -P["notch_w"] / 2), rb - P["notch_r"] + 1, P["notch_w"], fc="white", ec=INK, lw=0.8, transform=t))
    for a in P["stack_ang"]:
        x, y = polar(R, a)
        ax.add_patch(Circle((x, y), 1.7, fc="white", ec=INK, lw=0.8))
        ax.add_patch(Circle((x, y), 2.75 * 2 / math.sqrt(3), fc="none", ec="#B8860B", lw=0.8, ls="--"))
    ax.add_patch(Circle(P["lv_hole"], 3.0, fc="white", ec=INK, lw=0.8))
    ax.annotate("6 mm hole: low-voltage\ncontact leads pass up", P["lv_hole"], (P["lv_hole"][0] + 8, P["lv_hole"][1] - 16), ha="left", va="center",
                fontsize=7.5, color=MUT, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    boxes = {"psu": "Isolated supply\n23 x 38", "relay": "Relay\n18 x 24", "meter": "Metering module", "surge": "Varistor and\nthermal fuse"}
    cols = {"psu": "#7C3AED", "relay": "#D4A017", "meter": "#2563EB", "surge": "#C2410C"}
    for k, lab in boxes.items():
        bb = C[k].shape.bounding_box()
        ax.add_patch(Rectangle((bb.min.X, bb.min.Y), bb.size.X, bb.size.Y, fc="white", ec=cols[k], lw=1.6))
        lx = bb.center().X if k != "surge" else bb.center().X
        ly = bb.center().Y if k in ("psu", "relay") else (bb.max.Y + 6 if k == "surge" else bb.min.Y - 6)
        ax.text(lx, ly, lab, ha="center", va="center", fontsize=7.5, color=INK, linespacing=1.15,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none") if k not in ("psu", "relay") else None)
        ax.text(bb.max.X + 1 if k == "psu" else bb.min.X, bb.min.Y - 2.5 if k in ("psu", "relay") else bb.max.Y + 1, "", fontsize=1)
    ax.annotate("Pole side: the M12\nsocket sits above this\nnotch, in the dome", (-rb + 2, 3), (-rb - 12, 22), ha="right", va="center", fontsize=7.5, color=MUT,
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    ax.plot([-rb - 4, rb + 4], [0, 0], color=MUT, lw=0.4, ls=(0, (8, 3, 2, 3)))
    ax.plot([0, 0], [-rb - 4, rb + 10], color=MUT, lw=0.4, ls=(0, (8, 3, 2, 3)))
    ax.text(rb + 3, 1.5, "+X, street side", fontsize=7.5, color=MUT, va="bottom")
    ax.text(-1.5, rb + 9, "+Y", fontsize=7.5, color=MUT, va="bottom", ha="right")
    ax.set_xlim(-rb - 40, rb + 25); ax.set_ylim(-rb - 15, rb + 16)
    fig.text(0.03, 0.965, "Mains board: where each part sits, seen from above", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Outlines and positions from the model, mm. +X is the street side; +Y is the left side, seen from the pole. White cut-outs: notches\nfor the dome bosses. Dashed hexagons: standoffs.",
             fontsize=8.2, color=MUT, va="top")
    key = ["Supply: centred 9.5 mm toward +X", "Relay: 24 to 6 mm toward the pole,", "  centred on the X line",
           "Varistor: standing, 26 to 32 mm +Y;", "  thermal fuse taped against it", "Metering: 24 to 36 mm -Y",
           "", "Mains side (line, neutral, load):", "  keep 6 mm of bare board between", "  it and anything at 12 V",
           "Harness header to the controller", "  board beside the supply, +Y side"]
    for i, t in enumerate(key):
        fig.text(0.67, 0.80 - i * 0.032, t, fontsize=8.5, color=INK, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "mains-layout.png", facecolor="white"); plt.close(fig); res.append(OUT / "mains-layout.png")
    return res


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []
    zm = P["m12_z"]
    hx = HX

    def want(n):
        return only is None or only == n
    if want(1):
        bx_ = (-55, 55, -56, 26, -24, 26)
        out.append(bv.joint([
            part("Receptacle on the luminaire (existing)", win(C["receptacle"].shape, *bx_), COL["ref"]),
            part("Base gasket", win(C["base_gasket"].shape, *bx_), "#1F2937"),
            part("Twist-lock base (cut)", win(C["base"].shape, *bx_), "#9CA3AF"),
            part("Power blade in its slot", win(C["blades"].shape, *bx_), COL["blades"]),
            part("Countersunk screws from below (shown short)", win(S("dome_screws", "stack_screws"), *bx_), COL["bolt"])],
            OUT / "joint-01.png", "Joint 1: base on the receptacle (cut through a blade and two screws)",
            subtitle="The blades drop into the receptacle slots and a quarter turn locks them; the screw heads sit flush inside the gasket ring",
            elev=10, azim=80, size=(8, 6)))
    if want(2):
        x, y = polar(P["boss_r"], 0)
        bx_ = (x - 14, x + 14, -14, 0, -2, D["cb1"] + 2)
        out.append(bv.joint([
            part("Base", win(C["base"].shape, *bx_), "#9CA3AF"),
            part("Spacer 12 mm", win(C["spacers"].shape, *bx_), "#E7E5E4"),
            part("Mains board", win(C["mboard"].shape, *bx_), COL["mboard"]),
            part("Standoff 30 mm", win(C["standoffs"].shape, *bx_), COL["standoffs"]),
            part("Controller board", win(C["cboard"].shape, *bx_), COL["cboard"]),
            part("M3 x 45 screw from below", win(C["stack_screws"].shape, *bx_), COL["bolt"])],
            OUT / "joint-02.png", "Joint 2: the board stack (cut through one stack screw)",
            subtitle="One screw from under the base clamps base, spacer and mains board into the standoff; the top board screws on",
            elev=8, azim=75, size=(8, 6)))
    if want(3):
        x, y = polar(P["boss_r"], 180)
        bx_ = (-49, -18, -14, 0, -2, 42)
        out.append(bv.joint([
            part("Base", win(C["base"].shape, *bx_), "#9CA3AF"),
            part("Dome gasket 1 mm", win(C["dome_gasket"].shape, *bx_), "#4B5563"),
            part("Dome wall, boss and rib", win(C["dome"].shape, *bx_), COL["dome"]),
            part("Heat-set insert", win(C["inserts"].shape, *bx_), "#B8860B"),
            part("M3 x 30 screw from below", win(C["dome_screws"].shape, *bx_), COL["bolt"]),
            part("Mains board (notched round the boss)", win(C["mboard"].shape, *bx_), COL["mboard"])],
            OUT / "joint-03.png", "Joint 3: dome on the base (cut through the boss on the pole side)",
            subtitle="The boss stops 1 mm above the base, so the screw squeezes the dome foot onto the gasket",
            elev=10, azim=70, size=(8, 6)))
    if want(4):
        bx_ = (-112, -14, 0, 30, zm - 22, zm + 22)
        out.append(bv.joint([
            part("Dome wall and flat pad", win(C["dome"].shape, *bx_), "#E5E7EB"),
            part("M12 socket: seal outside, nut inside", win(C["socket"].shape, *bx_), "#9CA3AF"),
            part("M12 plug and cable", win(C["cable"].shape, *bx_), "#1F2937"),
            part("Mains board", win(C["mboard"].shape, *bx_), COL["mboard"]),
            part("Controller board", win(C["cboard"].shape, *bx_), COL["cboard"])],
            OUT / "joint-04.png", "Joint 4: M12 socket in the dome pad (cut along the socket)",
            subtitle="Flat 6 mm pad on the pole side, between the two boards; the cable plugs in after the controller is locked in",
            elev=12, azim=-80, size=(8, 6)))
    if want(5):
        bx_ = (-18, 18, -18, 0, D["cb0"] - 2, D["dome_top"] + 2)
        out.append(bv.joint([
            part("Dome top and sleeve", win(C["dome"].shape, *bx_), COL["dome"]),
            part("Light pipe rod, 8 mm", win(C["pipe"].shape, *bx_), COL["pipe"]),
            part("Controller board and light sensor", win(C["cboard"].shape, *bx_), COL["cboard"])],
            OUT / "joint-05.png", "Joint 5: light pipe through the dome top (cut through the middle)",
            subtitle="The rod is sealed into the hole flush with the top and ends 0.5 mm above the light sensor",
            elev=8, azim=75, size=(8, 6)))
    if want(6):
        x0 = hx + P["clamp_pitch"] / 2
        bx_ = (x0 - 30, x0, -55, 55, HTOP - 12, P["arm_z"] + 48)
        out.append(bv.joint([
            part("Lamp arm (existing)", win(arm(), *bx_), COL["ref"]),
            part("Rubber strips", win(C["liners"].shape, *bx_), "#111827"),
            part("Bracket, folded channel", win(C["bracket"].shape, *bx_), COL["bracket"]),
            part("Band clamp", win(C["bands"].shape, *bx_), "#6B7280"),
            part("Sensor head box", win(C["hbody"].shape, *bx_), COL["hbody"])],
            OUT / "joint-06.png", "Joint 6: bracket on the arm (cut across the arm at a band)",
            subtitle="The arm rests on the two rubber strips; the band goes over the arm, down outside the flanges, through the slots and across the web",
            elev=6, azim=8, size=(8, 6.5)))
    if want(7):
        sx, sy = P["brk_screw"]
        t = P["head_wall"]
        bx_ = (hx + sx - 14, hx + sx + 14, sy, sy + 22, HTOP - 12, HTOP + 6)
        scr = win(C["brk_screws"].shape, *bx_)
        x0, x1, y0, y1 = bx_[:4]
        out.append(bv.joint([
            part("Box top", win(C["hbody"].shape, *bx_), COL["hbody"]),
            part("Bracket web", win(C["bracket"].shape, *bx_), COL["bracket"]),
            part("M4 pan-head screw", win(scr, x0, x1, y0, y1, HTOP - t, HTOP + 6), COL["bolt"]),
            part("Bonded sealing washer", win(scr, x0, x1, y0, y1, HTOP - t - 1.5, HTOP - t), "#F59E0B"),
            part("Nut", win(scr, x0, x1, y0, y1, HTOP - 12, HTOP - t - 1.5), "#6B7280"),
            part("Internal plate, 1.3 mm below the nut", win(C["hplate"].shape, *bx_), COL["hplate"])],
            OUT / "joint-07.png", "Joint 7: bracket screwed to the box top (cut through one screw)",
            subtitle="Pan head on the web; the bonded sealing washer and nut inside the box keep the hole watertight",
            elev=8, azim=-75, size=(8, 6)))
    if want(8):
        bx_ = (hx - 62, hx + 62, 0, 50, D["hbot"] - 20, HTOP + 2)
        out.append(bv.joint([
            part("Box", win(C["hbody"].shape, *bx_), COL["hbody"]),
            part("Lid", win(C["hlid"].shape, *bx_), COL["hlid"]),
            part("Internal plate and radar cradle", win(C["hplate"].shape, *bx_), COL["hplate"]),
            part("Radar, tilted 25 degrees down", win(C["radar"].shape, *bx_), COL["radar"]),
            part("Head board on standoffs", win(C["hboard"].shape, *bx_), COL["hboard"]),
            part("Expansion port in the lid", win(C["ports"].shape, *bx_), COL["ports"]),
            part("Cable gland in the side wall", win(C["gland"].shape, *bx_), COL["gland"])],
            OUT / "joint-08.png", "Joint 8: inside the sensor head (cut along the middle)",
            subtitle="Plate on the four bosses; radar on its cradle facing the street end; ports in the lid; gland in the side",
            elev=8, azim=-80, size=(9, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only is None or only == n:
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    import build123d as b
    base = M["base"]
    st(1, [base], [mv(part("Spacers (3)", C["spacers"].shape, COL["spacers"]), (0, 0, 22)),
                   mv(part("Mains board", C["mboard"].shape, COL["mboard"]), (0, 0, 55)),
                   part("Supply", b.Pos(0, 0, 55) * C["psu"].shape, COL["psu"]),
                   part("Relay", b.Pos(0, 0, 55) * C["relay"].shape, COL["relay"]),
                   part("Varistor and thermal fuse", b.Pos(0, 0, 55) * C["surge"].shape, COL["surge"]),
                   part("Metering module", b.Pos(0, 0, 55) * C["meter"].shape, COL["meter"]),
                   mv(part("Standoffs (3)", C["standoffs"].shape, COL["standoffs"]), (0, 0, 95)),
                   mv(part("M3 x 45 screws from below (3)", C["stack_screws"].shape, COL["bolt"]), (0, 0, -60))],
       "board stack onto the base",
       "Plug the base leads into the mains board first; then three screws from below through base, spacer and board into each standoff",
       elev=30, azim=-55, label_done=False)
    stack = [base, part("Mains board", S("mboard", "surge", "psu", "relay", "meter", "spacers", "standoffs", "stack_screws"), COL["mboard"])]
    st(2, stack, [mv(M["cboard"], (0, 0, 80))], "controller board onto the standoffs",
       "Three M3 x 6 screws from above; plug in the harness from the mains board",
       elev=22, azim=-55, label_done=False)
    dome_alone = part("Dome (upside down on the bench)", S("dome", "inserts"), COL["dome"])
    import build123d as b
    flip = lambda s: b.Rot(180, 0, 0) * s  # noqa: E731
    st(3, [part("Dome, upside down", flip(S("dome", "inserts")), COL["dome"])],
       [mv(part("Light pipe rod, sealed in", flip(C["pipe"].shape), COL["pipe"]), (0, 0, 70)),
        mv(part("Antenna strip, stuck to the wall", flip(C["antenna"].shape), COL["antenna"]), (0, 0, 80)),
        mv(part("M12 socket, from outside", flip(C["socket"].shape), COL["socket"]), (-60, 0, 0))],
       "light pipe, antenna and M12 socket into the dome",
       "Dome upside down on a cloth. Rod flush with the top, sealed; antenna on the inside wall; socket nut inside",
       elev=30, azim=-55, label_done=False)
    st(4, stack + [M["cboard"]], [mv(part("Dome with pipe, antenna and socket", S("dome", "inserts", "pipe", "antenna", "socket"), COL["dome"]), (0, 0, 120)),
                                  mv(part("Dome gasket", C["dome_gasket"].shape, COL["dome_gasket"]), (0, 0, 12)),
                                  mv(part("M3 x 30 screws from below (3)", C["dome_screws"].shape, COL["bolt"]), (0, 0, -70))],
       "dome onto the base",
       "Plug the antenna and socket leads into the controller board, lower the dome over the stack, three screws from below",
       elev=20, azim=-55, label_done=False)
    hb = M["hbody"]
    st(5, [hb, part("Lid", C["hlid"].shape, COL["hlid"])],
       [mv(M["gland"], (0, 60, 0)), mv(part("Expansion ports (2)", C["ports"].shape, COL["ports"]), (0, 0, -60))],
       "gland into the box, ports into the lid",
       "Each from outside with its seal; nut inside, maker's torque. Lid shown in place; seen from below on the gland side",
       elev=-20, azim=40, label_done=False)
    st(6, [M["hplate"]], [mv(M["radar"], (40, 0, -40)), mv(M["hboard"], (0, 0, -40))],
       "radar and head board onto the internal plate",
       "Radar on two M2.5 screws and 3 mm nylon spacers; head board on four M3 screws into its standoffs. Seen from below",
       elev=-25, azim=-60, label_done=False)
    inner = part("Internal plate with radar and board", S("hplate", "radar", "hboard"), COL["hplate"])
    st(7, [hb, M["gland"]], [mv(part("Internal plate", C["hplate"].shape, COL["hplate"]), (0, 0, -90)),
                             part("Radar", b.Pos(0, 0, -90) * C["radar"].shape, COL["radar"]),
                             part("Head board", b.Pos(0, 0, -90) * C["hboard"].shape, COL["hboard"])],
       "internal plate into the box",
       "Seen from below. Stand the box upside down on the bench, lower the plate onto the four bosses, four M3 screws",
       elev=-25, azim=-55, label_done=False)
    st(8, [hb, M["gland"]], [mv(part("Bracket with rubber strips", S("bracket", "liners"), COL["bracket"]), (0, 0, 60)),
                             part("M4 pan-head screws (4); washers and nuts go inside", b.Pos(0, 0, 110) * win(C["brk_screws"].shape, HX - 70, HX + 70, -30, 30, HTOP - P["head_wall"], HTOP + 10), COL["bolt"])],
       "bracket onto the box top",
       "Four M4 pan-head screws down through the web and the box top; sealing washer and nut inside, snug",
       elev=25, azim=-55, label_done=False)
    head_closed = [hb, M["gland"], inner, part("Bracket", S("bracket", "liners", "brk_screws"), COL["bracket"])]
    st(9, head_closed, [mv(M["hlid"], (0, 0, -70)), mv(part("M12 cable end through the gland", win(C["cable"].shape, HX - 20, HX + 120, 40, 120, HTOP - 80, HTOP + 10), COL["cable"]), (0, 60, 0))],
       "cable in, leads plugged, lid on",
       "Cable through the gland to the head board; port leads plugged in; fresh desiccant; lid screws evenly. Seen from below on the gland side",
       elev=-15, azim=40, label_done=False)
    head_all = [part("Sensor head", S("hbody", "gland", "hplate", "radar", "hboard", "hlid", "ports", "bracket", "liners", "brk_screws"), COL["hbody"])]
    st(10, head_all, [mv(M["bands"], (0, 0, 70))], "sensor head onto the arm",
       "Hold the head up so the arm rests on both strips; each band over the arm, through its slots, across the web; tighten",
       context=[part("Lamp arm (bench length)", arm(-640, -300), COL["ref"])], elev=18, azim=-60, label_done=False)
    ctrl = part("Controller", S("base", "blades", "base_gasket", "dome", "inserts", "pipe", "antenna", "socket", "dome_gasket"), COL["dome"])
    st(11, [part("Donor receptacle and tube (bench mock-up)", C["receptacle"].shape + arm(-640, -120), COL["ref"]),
            part("Sensor head on the arm", S("hbody", "gland", "hlid", "ports", "bracket", "liners", "bands"), COL["hbody"])],
       [mv(ctrl, (0, 0, 80)), mv(part("M12 plug and cable", C["cable"].shape, COL["cable"]), (0, 0, 0))],
       "controller into the receptacle, cable along the arm",
       "Push the controller down and turn it clockwise until it locks; then plug in the cable and tie it to the arm",
       elev=22, azim=-60, label_done=True, size=(9, 6))
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.4), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 74); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 72, "LampNode prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 68.6, "Bought modules wired at block level on two round prototype boards; no circuit board is laid out. Stranded copper, ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/lampnode", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((20, 28), 46, 33, boxstyle="round,pad=0.4", fc="#FEF2F2", ec="#B91C1C", lw=1, ls="--"))
    ax.text(21, 60.3, "Mains board: MAINS VOLTAGE", fontsize=8, color="#B91C1C", va="top", fontweight="bold")
    ax.add_patch(FancyBboxPatch((70, 28), 30, 33, boxstyle="round,pad=0.4", fc="#F0FDFA", ec="#0F766E", lw=1, ls="--"))
    ax.text(71, 60.3, "Controller board: 12 V and 3.3 V", fontsize=8, color="#0F766E", va="top", fontweight="bold")
    ax.add_patch(FancyBboxPatch((70, 3), 38, 15, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#64748B", lw=1, ls="--"))
    ax.text(71, 17.3, "Sensor head (12 V)", fontsize=8, color="#475569", va="top", fontweight="bold")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.0, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 3.6, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.25)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, BRN, NEU, RF = "#B91C1C", "#1D4ED8", "#6B7280", "#92400E", "#1E3A8A", "#374151"
    blk(2, 38, 13, 18, "Twist-lock base", "line, neutral and\nload blades;\n4 low-voltage\ncontacts", "#374151")
    blk(22, 49, 14, 9, "Fuse and varistor", "thermal fuse,\n385 V class MOV", "#C2410C")
    blk(40, 49, 12, 9, "Relay", "normally closed,\n16 A", "#D4A017")
    blk(22, 31, 14, 10, "Metering module", "2 mOhm shunt,\nisolated data out", "#2563EB")
    blk(50, 31, 13, 12, "Supply", "85 to 305 V in,\n12 V 5 W out,\nisolated", "#7C3AED")
    blk(72, 46, 26, 12, "Controller", "LoRa module, clock,\naccelerometer, light\nsensor, supercapacitor", "#0F766E")
    blk(72, 31, 12, 8, "0 to 10 V", "dimming out", "#0F766E")
    blk(86, 31, 12, 8, "Coil drive", "charge pump", "#0F766E")
    blk(103, 49, 15, 9, "Antenna", "flex strip,\nu.FL lead", RF)
    blk(103, 32, 15, 9, "M12 socket", "dome pad,\n5 pins", "#1F2937")
    blk(72, 5, 15, 9, "Radar and ports", "radar module;\n2 x M12 ports", "#0EA5E9")
    blk(91, 5, 15, 9, "Head board", "radar input,\nport switches", "#115E59")
    # mains side
    wire([(15, 53.5), (22, 53.5)], BRN); lab(18.5, 55.6, "line 1.0 mm²", BRN, "center")
    wire([(36, 53.5), (40, 53.5)], BRN)
    wire([(46, 58), (46, 64), (8.5, 64), (8.5, 56)], BRN); lab(27, 64, "load back to the base blade, 1.0 mm²: lamp on when the relay rests", BRN, "center")
    wire([(29, 49), (29, 41)], BRN, 1.4); lab(29.6, 43.5, "shunt", BRN)
    wire([(15, 42), (18, 42), (18, 36), (22, 36)], NEU); lab(15.6, 40, "neutral 1.0", NEU)
    wire([(34, 49), (34, 46.5), (56, 46.5), (56, 43)], BRN, 1.4); lab(45, 45, "supply in, 0.5 mm²", BRN, "center")
    # isolation barrier
    ax.plot([67.5, 67.5], [28, 61], color="#B91C1C", lw=1.2, ls=(0, (4, 2)))
    ax.text(67.5, 62.2, "6 mm gap", fontsize=6.8, color="#B91C1C", ha="center", va="bottom")
    # 12 V and data
    wire([(63, 40), (69, 40), (69, 55), (72, 55)], RED); lab(64.2, 38.2, "12 V, 0.5", RED)
    wire([(29, 31), (29, 29), (71, 29), (71, 48.5), (72, 48.5)], BLU, 1.2); lab(48, 29, "metering data, isolated, 0.25 mm²", BLU, "center")
    wire([(78, 39), (78, 46)], GRY, 1.2)
    wire([(92, 39), (92, 46)], GRY, 1.2)
    wire([(92, 31), (92, 26), (44, 26), (44, 49)], GRY, 1.2); lab(57, 26, "relay coil, 0.25 mm²", GRY, "center")
    wire([(78, 31), (78, 23), (5, 23), (5, 38)], GRY, 1.2); lab(30, 23, "dimming to the low-voltage contacts, 0.25 mm²", GRY, "center")
    wire([(98, 53.5), (103, 53.5)], RF, 1.2)
    wire([(98, 50), (100.5, 50), (100.5, 36.5), (103, 36.5)], RED, 1.6); lab(100.0, 43, "12 V and\nserial", RED, "right")
    wire([(110.5, 32), (110.5, 9.5), (106, 9.5)], RED, 1.6); lab(111.2, 22, "M12 cable 1 m:\n12 V, 0 V,\n2-wire serial", RED)
    wire([(91, 9.5), (87, 9.5)], BLU, 1.2)
    ax.text(2, 15, "Safety: the mains board carries up to 305 V. Build and check it unpowered;", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(2, 12, "first power only through an isolating transformer and an RCD, dome on (section 6).", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(2, 8.4, "Brown: line and load. Dark blue: neutral. Red: 12 V. Blue: data. Grey: control.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    args = sys.argv[1:]
    if len(args) == 2 and args[0] in ("joint", "step", "sheet"):
        n = int(args[1])
        r = {"joint": joints, "step": steps, "sheet": sheets}[args[0]](only=n)
        print(args[0], n, "->", r)
        sys.exit(0)
    what = args or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
