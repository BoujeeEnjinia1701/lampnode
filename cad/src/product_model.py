"""LampNode product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the twist-lock controller with a charcoal base (grip
grooves, orientation mark, tin-plated power blades, gold low-voltage pads and a rubber gasket), an
M12 panel socket and plug, and a filleted UV-stable dome with a teal accent band, a printed label
and a clear light-pipe rod through its top. Inside: the surge stage with its varistor and thermal
fuse, the encapsulated supply, the fail-on relay, the metering chip, and the controller board with
its shielded radio module, 0 to 10 V dimming stage, supercapacitor and antenna. The sensor head
has a filleted housing with a parting line, a dark radar-transparent front face, lid screws, a
cable gland, two M12 expansion ports with caps, the tilted 24 GHz radar module and its board, a
folded bracket and two stainless band clamps with rubber liners and worm housings. Context is a
compact LED luminaire head with its receptacle and a short, cut section of the lamp arm.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, head_frame() and build_parts() in model.py,
in the same local frame: origin at the center of the receptacle's top face, Z up, X along the arm
away from the pole, Y across the arm. The luminaire head is the concept_media.py reference head
(650 mm) shortened to a compact body for the render. Updated 2026-10-02 to the constructable design
(LPN-DDR-003): M12 socket in the flat pad on the dome, dome gasket, bosses and inserts, the boards on
spacers and standoffs, the varistor standing on the mains board, the flexible antenna on the dome wall,
the 8 mm light pipe rod, the printed internal plate with the radar cradle, the folded bracket with
band slots and rubber strips, the bands through the slots, and the model.py cable route.
See docs/REVIEW.md, sessions 2026-09-26 and 2026-10-02.

Groups: the controller is "shell" and "internal"; the sensor head, bracket, clamps, M12 plug and
cable are "accessory", so the detail view shows the controller alone; the luminaire head, its
receptacle, the arm section and the cable ties are "context".

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, LV_ANGLES, build_components, build_parts, derived, head_frame

TITLE = "LampNode: open streetlight controller with a radar presence head"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 28, "az": -30,
     "note": "Product render from the front right and above (about 28 deg elevation), looking back along the arm; controller on the "
             "luminaire's twist-lock socket at right, radar sensor head clamped under the lamp arm at left"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): dome cover, controller "
             "board with radio and dimming stage, relay, supply and surge stage, twist-lock socket base; "
             "sensor head with the 24 GHz radar, board, lid and expansion ports"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 22, "az": -135,
     "note": "Detail of the controller from the front left, slightly above (about 22 deg elevation), without "
             "the luminaire: dome with its clear light-pipe rod, twist-lock base and the M12 socket "
             "in the flat pad on the pole side of the dome"},
]

# Colours (restrained product palette; kit accent)
C_DOME = "#ECEDEF"
C_BASE = "#2B2F36"
C_HEAD = "#E3E6EA"
C_HEAD2 = "#CDD2D8"
C_RADOME = "#3A4048"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_METAL = "#B8BEC6"
C_TIN = "#C9CDD2"
C_GOLD = "#C9A227"
C_STEEL = "#A9AFB6"
C_PCB = "#166534"
C_CHIP = "#111827"
C_RELAY = "#1E3A5F"
C_MOV = "#1E40AF"
C_LABEL = "#F4F4F2"
C_PIPE = "#EEF2F5"
C_WINDOW = "#DCEBF5"
C_LUM = "#B1B6BC"
C_LUM2 = "#A2A8AF"
C_LENS = "#F3F4F6"
C_ARM = "#C0C4C9"
C_REC = "#7D848C"


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


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _bx(x0, x1, y0, y1, z0, z1):
    return _box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _ring_z(x, y, z, r0, r1, h):
    return Pos(x, y, z) * (Cylinder(r1, h) - Cylinder(r0, h + 2))


def _ring_x(x, y, z, r0, r1, w):
    return Pos(x, y, z) * Rot(0, 90, 0) * (Cylinder(r1, w) - Cylinder(r0, w + 2))


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)


def _hex_x(x, y, z, af, length):
    return Pos(x - length / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / math.sqrt(3), 6), amount=length)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _polar(r, ang_deg):
    t = math.radians(ang_deg)
    return r * math.cos(t), r * math.sin(t)


def product_parts(P=PARAMS):
    ref = {n: s for n, s, _, bom, _ in build_parts(P) if bom is None}
    MC = build_components(P)                              # model.py components, used as they are where they are plain
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ============================================================ controller (BOM 1 to 10)
    bh, R0 = P["base_h"], P["base_d"] / 2
    dh, dw, dr = P["dome_h"], P["dome_wall"], P["dome_d"] / 2
    bz = P["board_z"]                                   # controller board center height, as model.py
    top_in = bh + dh - dw

    # 1 twist-lock base: body with grip grooves, orientation mark; blades, pads and gasket
    base = _zcyl(0, 0, bh / 2, R0, bh)
    base = _fillet_try(base, _bottom(base), [2.0, 1.2])
    base = _fillet_try(base, _top(base), [1.5, 1.0])
    grooves = []
    for k in range(32):
        ang = k * 360 / 32 + 5.625
        x, y = _polar(R0, ang)
        grooves.append(Pos(x, y, 10.5) * Rot(0, 0, ang) * Box(2.4, 2.2, 13.0))
    base -= _union(grooves)
    for ang in tuple(P["dome_boss_ang"]) + tuple(P["stack_ang"]):      # six M3 holes, countersunk from below, as model.py
        hx_, hy_ = _polar(P["boss_r"], ang)
        base -= _zcyl(hx_, hy_, bh / 2, 1.7, bh + 2) + _zcyl(hx_, hy_, 0.85, 3.0, 1.7)
    add("Twist-lock base body", base, C_BASE, "plastic", 1, "shell", (0, 0, 0))

    mark = Pos(0, -R0 - 0.15, 21.0) * Rot(90, 0, 0) * extrude(RegularPolygon(3.2, 3, rotation=90), amount=0.6)
    mark = Pos(0, 0.3, 0) * mark
    add("Base orientation mark", mark, C_LABEL, "painted", 1, "shell", (0, 0, 0))

    blades = []
    for ang in (90, 210, 330):
        x, y = _polar(P["blade_r"], ang)
        b = Pos(x, y, -P["blade_h"] / 2) * Rot(0, 0, ang) * Box(P["blade_w"], P["blade_l"], P["blade_h"])
        blades.append(_fillet_try(b, _bottom(b), [1.2, 0.6]))
    add("Power blades (tin-plated)", _union(blades), C_TIN, "metal", 1, "shell", (0, 0, -30))
    pads = []
    for ang in LV_ANGLES:
        x, y = _polar(P["lv_contact_r"], ang)
        pads.append(_zcyl(x, y, -P["lv_contact_h"] / 2, P["lv_contact_d"] / 2, P["lv_contact_h"]))
    add("Low-voltage contact pads (gold)", _union(pads), C_GOLD, "metal", 1, "shell", (0, 0, -30))
    g = P["gasket_t"]
    gasket = _ring_z(0, 0, -g / 2, R0 - 12, R0 - 2, g)
    add("Base gasket", gasket, C_BLACK, "rubber", 1, "shell", (0, 0, -15))

    # 10 M12 panel socket in the flat pad on the pole side of the dome (LPN-DDR-003 P3, accepted 2026-10-02),
    #    the cable plug and the cable along the arm (P11)
    ml, pw, pt, zm = P["m12_l"], P["pad"][0], P["pad"][1], P["m12_z"]
    x_out = -(R0 + 0.5)                                       # pad face, as model.py
    x_plug = x_out - 2 - ml                                   # socket face, where the plug starts
    sock = _hex_x(x_out - 1.0, 0, zm, 22.0, 2.0) + _xcyl(x_out - 2 - ml / 2, 0, zm, P["m12_d"] / 2 - 0.5, ml)
    sock += _hex_x(x_out + pt + 1.5, 0, zm, 20.0, 3.0) + _xcyl(x_out + pt + 5.5, 0, zm, 6.0, 5.0)    # nut and contact body inside
    add("M12 panel socket", sock, C_METAL, "metal", 10, "shell", (-30, 0, 300))
    nut = _xcyl(x_plug - 6.0, 0, zm, 10.0, 12.0)
    for k in range(18):
        y, z = _polar(10.0, k * 20)
        nut -= _xcyl(x_plug - 6.0, y, zm + z, 0.8, 13.0)
    add("M12 plug coupling nut (knurled)", nut, C_METAL, "metal", 10, "accessory", (-45, 0, 0))
    mold = _xcyl(x_plug - 26.0, 0, zm, 7.0, 28.0)
    mold = _fillet_try(mold, mold.edges().sort_by(Axis.X)[:1], [3.0, 2.0])
    add("M12 plug overmold", mold, C_BLACK, "rubber", 10, "accessory", (-45, 0, 0))

    # cable: the model.py route (P11): level out of the plug, down to the top of the arm past the luminaire,
    # along the arm, round to the +Y side and down to the head gland
    hx, htop, hzc = head_frame(P)
    hl, hw, hh = P["head"]
    ar, az = P["arm_d"] / 2, P["arm_z"]
    cr = P["cable_d"] / 2
    zt = az + ar + cr + 0.5
    yd = ar + cr + 5
    yg = hw / 2
    gl = 16.0
    gz = htop - P["gland_z"]
    xg = hx + P["gland_x"]
    route = [(x_plug - 40, 0, zm), (-150, 0, zm), (-175, 0, zm - 25), (-175, 0, zt + 25), (-200, 0, zt),
             (hx + hl / 2 + 60, 0, zt),
             (hx + hl / 2 + 52, 37.5 * math.cos(math.radians(60)), az + 37.5 * math.sin(math.radians(60))),
             (hx + hl / 2 + 46, 38.5 * math.cos(math.radians(30)), az + 38.5 * math.sin(math.radians(30))),
             (hx + hl / 2 + 40, yd, az), (hx + hl / 2 + 40, yg + gl + 30, gz + 20),
             (xg + 30, yg + gl + 30, gz), (xg, yg + gl + 20, gz), (xg, yg + gl, gz)]
    add("M12 cable to sensor head", _pipe(route, cr), C_BLACK, "rubber", 10, "accessory", (0, 0, 0))
    ties = []
    for x in (-230, -330):
        t = _ring_x(x, 0, az, ar + 0.2, ar + 1.4, 4.5) + _ring_x(x, 0, zt, cr + 0.2, cr + 1.4, 4.5)
        ties.append(t)
    add("Cable ties", _union(ties), C_BLACK, "plastic", 16, "context", (0, 0, 0))   # shown with the arm


    # 2 dome cover (P2, P3, P4): foot on a 1 mm gasket, three screw bosses with heat-set inserts, the flat pad for
    #   the M12 socket, the sleeve and 8.2 mm hole for the light pipe rod
    d0, dtop = D["dome0"], D["dome_top"]
    ddh = dtop - d0
    zd = d0 + ddh / 2
    gk = _ring_z(0, 0, bh + P["dome_gasket_t"] / 2, dr - dw, dr, P["dome_gasket_t"])
    add("Dome gasket (EPDM)", gk, C_BLACK, "rubber", 17, "shell", (0, 0, 20))
    outer = _zcyl(0, 0, zd, dr, ddh)
    outer = fillet(outer.edges().group_by(Axis.Z)[-1], P["dome_fillet"])
    outer = _fillet_try(outer, outer.edges().group_by(Axis.Z)[0], [1.0, 0.6])
    inner = _zcyl(0, 0, zd - dw / 2 - 0.5, dr - dw, ddh - dw + 1)
    inner = fillet(inner.edges().group_by(Axis.Z)[-1], P["dome_fillet"] - dw)
    dome = outer - inner
    dome += _bx(x_out, x_out + pt + 1.5, -pw / 2, pw / 2, zm - pw / 2, zm + pw / 2)           # flat pad
    dome -= _bx(x_out + pt, x_out + pt + 8, -pw / 2, pw / 2, zm - pw / 2, zm + pw / 2)         # flat inner seat
    dome -= _xcyl(x_out + (pt + 3) / 2 - 1, 0, zm, 8.1, pt + 3)                                # socket hole
    sl = P["sleeve_l"]
    dome += _zcyl(0, 0, dtop - dw - sl + (sl + 0.5) / 2, P["sleeve_od"] / 2, sl + 0.5)         # light pipe sleeve
    for ang in P["dome_boss_ang"]:
        bx_, by_ = _polar(P["boss_r"], ang)
        boss = _zcyl(bx_, by_, d0 + P["boss_h"] / 2, P["boss_d"] / 2, P["boss_h"])
        rib = Rot(0, 0, ang) * _bx(P["boss_r"], dr - dw + 0.5, -2, 2, d0, d0 + P["boss_h"])
        dome += boss + rib
    dome -= _zcyl(0, 0, dtop - dw - sl - 1 + (sl + dw + 3) / 2, P["window_d"] / 2, sl + dw + 3)   # rod hole
    add("Dome cover (UV-stable ASA)", dome, C_DOME, "plastic", 2, "shell", (0, 0, 300))
    band = _ring_z(0, 0, bh + 5.5, dr - 0.2, dr + 0.4, 3.0)
    add("Dome accent band", band, C_ACCENT, "painted", 2, "shell", (0, 0, 300))
    sector = _box(0, -dr, bh + 26, 40, 20, 22)
    lab = _ring_z(0, 0, bh + 26, dr - 0.2, dr + 0.35, 20) & sector
    add("Dome label", lab, C_LABEL, "paper", 2, "shell", (0, 0, 300))
    ink = _union([_box(-6, -dr, bh + 31, 20, 20, 5), _box(10, -dr, bh + 31, 8, 20, 5),
                  _box(0, -dr, bh + 24, 30, 20, 1.6), _box(-4, -dr, bh + 20, 22, 20, 1.6)])
    ink = _ring_z(0, 0, bh + 26, dr + 0.3, dr + 0.6, 20) & ink
    add("Dome label print", ink, C_BASE, "paper", 2, "shell", (0, 0, 300))
    add("Heat-set inserts M3 (3)", MC["inserts"].shape, "#B8860B", "metal", 17, "internal", (0, 0, 300))
    add("M3 countersunk screws (6)", MC["dome_screws"].shape + MC["stack_screws"].shape, C_STEEL, "metal", 17, "shell", (0, 0, -40))


    # 17 board stack (P1): mains board on three 12 mm spacers, controller board on three 30 mm standoffs
    mb0, mb1, cb0, cb1 = D["mb0"], D["mb1"], D["cb0"], D["cb1"]
    rb = P["board_d"] / 2
    B = [_polar(P["boss_r"], a) for a in P["stack_ang"]]
    sp = _union([_zcyl(x, y, bh + P["spacer_h"] / 2, P["spacer_d"] / 2, P["spacer_h"]) for x, y in B])
    add("Nylon spacers 12 mm (3)", sp, C_LABEL, "plastic", 17, "internal", (0, 0, 35))
    ES = (0, 0, 70)
    mboard = _zcyl(0, 0, (mb0 + mb1) / 2, rb, P["board_t"])
    for ang in P["dome_boss_ang"]:
        mboard -= Rot(0, 0, ang) * _bx(P["notch_r"], rb + 2, -P["notch_w"] / 2, P["notch_w"] / 2, mb0 - 1, mb1 + 1)
    for x, y in B:
        mboard -= _zcyl(x, y, mb0 + 1, 1.7, 4)
    mboard -= _zcyl(P["lv_hole"][0], P["lv_hole"][1], mb0 + 1, 3.0, 4)
    add("Mains board", mboard, C_PCB, "plastic", 17, "internal", ES)
    so = _union([_hex_z(x, y, mb1 + P["standoff_h"] / 2, 5.5, P["standoff_h"]) for x, y in B])
    add("Brass standoffs 30 mm (3)", so, "#B8860B", "metal", 17, "internal", (0, 0, 110))

    # 3 surge stage: one standing 20 mm varistor and the thermal fuse against it (P6)
    md, mt = P["mov_d"], P["mov_t"]
    zmv = mb1 + 4 + md / 2
    mov = _ycyl(0, 29.0, zmv, md / 2, mt)
    mov = _fillet_try(mov, mov.edges().filter_by(Axis.Y), [1.5, 1.0])
    mov += _bx(-3, 3, 27, 31, mb1, mb1 + 4)
    add("Surge varistor", mov, C_MOV, "plastic", 3, "internal", (0, 55, 100))
    fuse = _xcyl(0, 34.5, zmv - 3, 2.0, 10.0)
    fuse = _fillet_try(fuse, fuse.edges(), [0.8, 0.4])
    add("Thermal fuse", fuse, "#E7E5E4", "plastic", 3, "internal", (0, 55, 100))

    # 4 isolated supply, encapsulated, with a label
    px, py, pz = P["psu"]
    psu = _bx(-2, -2 + px, -py / 2, py / 2, mb1, mb1 + pz)
    psu = _fillet_try(psu, _edges_par(psu, Axis.Z), [2.0, 1.0])
    psu = _fillet_try(psu, _top(psu), [1.0, 0.5])
    add("Isolated power supply (12 V, 5 W)", psu, C_CHIP, "plastic", 4, "internal", (50, 0, 100))
    plab = _bx(-2 + 4, -2 + px - 4, -12, 12, mb1 + pz, mb1 + pz + 0.3)
    add("Power supply label", plab, C_LABEL, "paper", 4, "internal", (50, 0, 100))

    # 5 fail-on relay
    rx, ry, rz = P["relay"]
    relay = _bx(-24, -24 + rx, -ry / 2, ry / 2, mb1, mb1 + rz)
    relay = _fillet_try(relay, relay.edges(), [1.2, 0.6])
    add("Fail-on relay (normally closed)", relay, C_RELAY, "plastic", 5, "internal", (-60, 0, 100))
    rlab = _bx(-24 + 3, -24 + rx - 3, -ry / 2 - 0.3, -ry / 2, mb1 + 4, mb1 + 14)
    add("Relay label", rlab, C_LABEL, "paper", 5, "internal", (-60, 0, 100))

    # 6 energy metering module: small carrier, IC and shunt
    mcar = _bx(-9, 7, -36, -24, mb1, mb1 + 1.6)
    add("Metering carrier", mcar, C_PCB, "plastic", 6, "internal", (45, -60, 100))
    mic = _bx(-6, 0, -33, -27, mb1 + 1.6, mb1 + 3.2) + _bx(2, 6, -34, -26, mb1 + 1.6, mb1 + 4.5)
    add("Metering IC and shunt", mic, C_CHIP, "plastic", 6, "internal", (45, -60, 100))

    # 7 controller board on the standoffs: radio module, dimming stage, supercapacitor standing on top
    EB = (0, 0, 160)
    bzc = (cb0 + cb1) / 2
    pcb = _zcyl(0, 0, bzc, rb, P["board_t"])
    for x, y in B:
        pcb -= _zcyl(x, y, bzc, 1.7, 4)
    add("Controller board PCB", pcb, C_PCB, "plastic", 7, "internal", EB)
    radio = _bx(8, 24, -2, 14, cb1, cb1 + 1.2)
    add("LoRaWAN radio module", radio, C_PCB, "plastic", 7, "internal", EB)
    can = _bx(9, 23, -1, 13, cb1 + 1.2, cb1 + 4.0)
    can = _fillet_try(can, _top(can), [0.6, 0.3])
    add("Radio shield can", can, C_METAL, "metal", 7, "internal", EB)
    dim = _union([_bx(-30, -22, -24, -16, cb1, cb1 + 1.8), _bx(-16, -8, -24, -16, cb1, cb1 + 1.4),
                  _bx(-4, 4, -30, -24, cb1, cb1 + 1.2), _bx(-30, -24, 2, 8, cb1, cb1 + 1.2),
                  _bx(12, 20, 20, 28, cb1, cb1 + 1.4)])
    add("Dimming stage and clock ICs", dim, C_CHIP, "plastic", 7, "internal", EB)
    sc = _zcyl(-24, -6, cb1 + P["supercap_h"] / 2, P["supercap_d"] / 2, P["supercap_h"])
    sc = _fillet_try(sc, _top(sc), [1.5, 1.0])
    add("Supercapacitor (0.22 F)", sc, C_CHIP, "plastic", 7, "internal", EB)
    sleeve = _ring_z(-24, -6, cb1 + 4, P["supercap_d"] / 2 - 0.1, P["supercap_d"] / 2 + 0.2, 6)
    add("Supercapacitor sleeve band", sleeve, C_ACCENT, "plastic", 7, "internal", EB)
    sens = _bx(-1.5, 1.5, -1.5, 1.5, cb1, cb1 + 1.0)
    add("Ambient light sensor", sens, C_CHIP, "plastic", 9, "internal", EB)

    # 8 antenna: flexible strip stuck inside the dome wall on the -Y side (P5)
    al, ah, at = P["antenna"]
    ri = dr - dw
    span = math.degrees(al / ri)
    za = P["antenna_z"]
    ant = _ring_z(0, 0, za + ah / 2, ri - at, ri, ah) & \
        (Rot(0, 0, -90) * _bx(0, ri + 5, -ri * math.sin(math.radians(span / 2)), ri * math.sin(math.radians(span / 2)), za - 1, za + ah + 1))
    add("Antenna (flexible strip, 915 MHz)", ant, C_BLACK, "plastic", 8, "internal", (0, 0, 300))

    # 9 light pipe: clear 8 mm rod through the dome top, 0.5 mm above the light sensor (P4)
    z0p = cb1 + 1.5
    rod = _zcyl(0, 0, (z0p + dtop) / 2, P["pipe_d"] / 2, dtop - z0p)
    add("Light pipe rod (clear acrylic)", rod, C_WINDOW, "clear", 9, "shell", (0, 0, 300))

    # ============================================================ sensor head (BOM 11 to 15)
    t = P["head_wall"]
    x0, x1 = hx - hl / 2, hx + hl / 2
    zb = htop - hh                                      # underside of the head, lid face down
    zp = zb + 15.0                                      # parting line between the housing and the lid
    outer = _bx(x0, x1, -hw / 2, hw / 2, zb, htop)
    outer = _fillet_try(outer, _edges_par(outer, Axis.Z), [8.0, 6.0, 4.0])
    outer = _fillet_try(outer, _top(outer), [3.0, 2.0])
    outer = _fillet_try(outer, _bottom(outer), [3.0, 2.0])
    cavity = _bx(x0 + t, x1 - t, -hw / 2 + t, hw / 2 - t, zb + t, htop - t)
    shell = outer - cavity
    upper = shell & _bx(x0 - 5, x1 + 5, -hw, hw, zp + 0.4, htop + 5)
    lower = shell & _bx(x0 - 5, x1 + 5, -hw, hw, zb - 5, zp - 0.4)
    # radar-transparent front face: shallow pocket on +X, filled by a dark panel
    upper -= _bx(x1 - 1.0, x1 + 5, -32, 32, zp + 6, htop - 8)
    upper -= _ycyl(xg, hw / 2 - t / 2, htop - 20, 5.0, t + 2)          # gland bore on the +Y side
    add("Sensor head housing", upper, C_HEAD, "plastic", 11, "accessory", (0, 0, -40))
    EL = (0, 0, -175)
    lids = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            lids.append((hx + sx * (hl / 2 - 9), sy * (hw / 2 - 9)))
    for (x, y) in lids:
        lower -= _zcyl(x, y, zb, 3.6, 1.6)
    for dy in (-P["port_pitch"] / 2, P["port_pitch"] / 2):
        lower -= _zcyl(hx - 30, dy, zb + t / 2, P["port_d"] / 2 - 2, t + 2)
    add("Sensor head lid", lower, C_HEAD2, "plastic", 11, "accessory", EL)
    face = _bx(x1 - 1.0, x1 - 0.2, -32, 32, zp + 6, htop - 8)
    face = _fillet_try(face, _edges_par(face, Axis.X), [3.0, 2.0])
    add("Radar window (radar-transparent)", face, C_RADOME, "plastic", 11, "accessory", (0, 0, -40))
    stripe = _bx(x1 - 0.2, x1 + 0.2, -30, 30, htop - 6.5, htop - 4.5)
    add("Head accent line", stripe, C_ACCENT, "painted", 11, "accessory", (0, 0, -40))
    hlab = _bx(hx - 20, hx + 20, -hw / 2 - 0.4, -hw / 2, zp + 12, zp + 34)
    add("Sensor head label", hlab, C_LABEL, "paper", 11, "accessory", (0, 0, -40))
    hink = _union([_bx(hx - 16, hx + 2, -hw / 2 - 0.6, -hw / 2 - 0.3, zp + 26, zp + 31),
                   _bx(hx - 16, hx + 14, -hw / 2 - 0.6, -hw / 2 - 0.3, zp + 20, zp + 21.6),
                   _bx(hx - 16, hx + 8, -hw / 2 - 0.6, -hw / 2 - 0.3, zp + 16, zp + 17.6)])
    add("Sensor head label print", hink, C_BASE, "paper", 11, "accessory", (0, 0, -40))
    lsc = []
    for (x, y) in lids:
        s = _zcyl(x, y, zb - 0.2, 3.3, 1.4)
        s = _fillet_try(s, _bottom(s), [0.5, 0.3])
        s -= _bx(x - 2, x + 2, y - 0.4, y + 0.4, zb - 1.2, zb - 0.6)
        lsc.append(s)
    add("Lid screws", _union(lsc), C_METAL, "metal", 16, "accessory", (0, 0, -200))
    gland = Pos(xg, hw / 2 + 2.0, htop - 20) * Rot(-90, 0, 0) * Pos(0, 0, -2.0) \
        * extrude(RegularPolygon(9.0, 6), amount=4.0)
    cap = _ycyl(xg, hw / 2 + 6.5, htop - 20, 7.5, 5.0)
    cap = _fillet_try(cap, cap.faces().sort_by(Axis.Y)[-1].edges(), [2.0, 1.2])
    add("Head cable gland", gland + cap, C_BLACK, "plastic", 11, "accessory", (0, 40, -40))

    # 12 radar module on the plate's cradle, tilted down the street, patch antennas facing +X (model.py position)
    rx_, ry_, rz_ = P["radar"]
    rloc = Pos(hx + P["radar_dx"], 0, D["radar_zc"]) * Rot(0, P["radar_tilt"], 0)
    add("24 GHz radar module", rloc * Box(rx_, ry_, rz_), C_PCB, "plastic", 12, "accessory", (60, 0, -95))
    patches = _union([Pos(rx_ / 2 + 0.2, py_, pz_) * Box(0.4, 7, 7) for py_ in (-15, -5, 5, 15) for pz_ in (-9, 9)])
    add("Radar patch antennas", rloc * patches, C_GOLD, "metal", 12, "accessory", (60, 0, -95))
    rchip = Pos(-rx_ / 2 - 0.8, 0, 0) * Box(1.6, 14, 10)
    add("Radar front-end IC", rloc * rchip, C_CHIP, "plastic", 12, "accessory", (60, 0, -95))

    # 18 printed internal plate with the radar cradle, on the four box bosses (P8): model.py shape
    add("Head internal plate with radar cradle", MC["hplate"].shape, "#9AA1A9", "plastic", 18, "accessory", (0, 0, -75))

    # 13 head board under the plate on four 6 mm standoffs (P8); parts on its underside
    hbl, hbw = P["hboard"]
    hb_top = D["pl_bot"] - P["hboard_standoff"]
    x0b = hx + P["hboard_x0"]
    hboard = _bx(x0b, x0b + hbl, -hbw / 2, hbw / 2, hb_top - 1.6, hb_top)
    add("Sensor head board", hboard, C_PCB, "plastic", 13, "accessory", (0, 0, -120))
    hso = _union([_zcyl(x0b + dx, sy * (hbw / 2 - 4), hb_top + P["hboard_standoff"] / 2, 2.5, P["hboard_standoff"])
                  for dx in (4, hbl - 4) for sy in (-1, 1)])
    add("Head board standoffs (4)", hso, "#B8860B", "metal", 18, "accessory", (0, 0, -100))
    zl = hb_top - 1.6
    hcomp = _union([_bx(hx - 40, hx - 24, -10, 6, zl - 1.4, zl), _bx(hx - 20, hx, 10, 24, zl - 3.0, zl),
                    _bx(hx - 46, hx - 38, 16, 26, zl - 1.6, zl), _bx(hx - 8, hx + 8, -26, -16, zl - 5.5, zl)])
    add("Head board components", hcomp, C_CHIP, "plastic", 13, "accessory", (0, 0, -120))

    # 14 two sealed M12 expansion ports with caps
    pl = P["port_l"]
    pn, pb, pc = [], [], []
    for k, dy in enumerate((-P["port_pitch"] / 2, P["port_pitch"] / 2)):
        pn.append(_hex_z(hx - 30, dy, zb - 2.0, 19.0, 4.0))
        pb.append(_zcyl(hx - 30, dy, zb - 4 - 3.0, 7.5, 6.0))
        c = _zcyl(hx - 30, dy, zb - pl + 5.0, P["port_d"] / 2 - 0.5, 10.0)
        c = _fillet_try(c, _bottom(c), [2.5, 1.5])
        pc.append(c)
    EP = (0, 0, -235)
    add("Expansion port sockets (2)", _union(pn) + _union(pb), C_METAL, "metal", 14, "accessory", EP)
    add("Expansion port cap", pc[0], C_BLACK, "rubber", 14, "accessory", (0, 0, -275))
    add("Expansion port cap (accent)", pc[1], C_ACCENT, "rubber", 14, "accessory", (0, 0, -275))

    # 15 folded bracket (P10): web on the box top, flanges with band slots, 5 x 1.5 mm rubber strips on the flanges,
    #    two band clamps through the slots and over the web; model.py shapes, with worm-screw heads added
    add("Head bracket (folded aluminum)", MC["bracket"].shape, C_METAL, "metal", 15, "accessory", (0, 0, -20))
    add("Bracket screws, sealing washers and nuts (4)", MC["brk_screws"].shape, C_STEEL, "metal", 16, "accessory", (0, 0, -20))
    heads = _union([_hex_x(hx + dx + 8.5, 0, az + ar + P["band_t"] + 4, 6.0, 3.0) for dx in (-P["clamp_pitch"] / 2, P["clamp_pitch"] / 2)])
    add("Band clamps (stainless)", MC["bands"].shape + heads, C_STEEL, "metal", 15, "accessory", (0, 0, 45))
    add("Rubber strips on the bracket flanges", MC["liners"].shape, C_BLACK, "rubber", 15, "accessory", (0, 0, 45))

    # ============================================================ context (existing street furniture)
    rec = ref["Luminaire receptacle (reference)"]
    rec = _fillet_try(rec, _top(rec), [1.5, 1.0])
    add("Luminaire receptacle (existing)", rec, C_REC, "plastic", None, "context", (0, 0, 0))
    ltop = -g - P["receptacle_h"]                        # luminaire top face under the receptacle
    lbot = ltop - 100
    body = _bx(-60, 330, -125, 125, lbot, ltop)
    body = _fillet_try(body, _edges_par(body, Axis.Z), [60.0, 40.0])
    body = _fillet_try(body, _top(body), [12.0, 8.0])
    body = _fillet_try(body, _bottom(body), [6.0, 4.0])
    neck = _bx(-140, -30, -48, 48, lbot + 6, az + ar + 12)
    neck = _fillet_try(neck, neck.edges().filter_by(Axis.X), [12.0, 8.0])
    fins = _union([_bx(85, 300, y - 1.5, y + 1.5, ltop - 2, ltop + 12) for y in range(-75, 76, 25)])
    fins = _fillet_try(fins, _top(fins), [1.4, 1.0])
    add("LED luminaire head (existing)", body + neck, C_LUM, "painted", None, "context", (0, 0, 0))
    add("Luminaire heat-sink fins", fins, C_LUM2, "metal", None, "context", (0, 0, 0))
    lens = _bx(-10, 295, -100, 100, lbot - 4, lbot + 0.5)
    lens = _fillet_try(lens, _edges_par(lens, Axis.Z), [30.0, 20.0])
    add("Luminaire lens", lens, C_LENS, "plastic", None, "context", (0, 0, 0))
    arm = _xcyl((-600 - 100) / 2, 0, az, ar, 500)
    add("Lamp arm section (existing)", arm, C_ARM, "metal", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
