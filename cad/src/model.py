"""LampNode parametric model (build123d), TRL 3, constructable design (LPN-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl, prints the
                                       main envelopes, part volumes and the constructability checks
    python cad/src/model.py --check    prints the constructability checks only

Every component is modelled as it is made or bought and as it fixes to its neighbours: the
bought twist-lock base drilled for six screws, a printed dome with three screw bosses, an M12
pad and a light-pipe sleeve, two round prototype boards on spacers and standoffs, a drilled
sensor head box with its lid, a printed internal plate with a radar cradle, and a folded
aluminium bracket held to the lamp arm by two band clamps that pass through slots in its
flanges. Blade and contact positions are representative and must be checked against ANSI
C136.10 and C136.41 before any part is made.

Local frame, units mm: origin at the centre of the underside of the twist-lock base, Z up, X
along the arm away from the pole (the pole is toward -X), Y across the arm. The controller sits
on the receptacle; the sensor head is clamped under the arm, between the pole and the luminaire,
with its radar looking along +X, tilted down the street.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # Controller, LPN-PRC-001
    "base_d": 94.0, "base_h": 25.0,            # bought twist-lock base
    "blade_r": 26.0, "blade_w": 4.0, "blade_l": 12.0, "blade_h": 14.0,   # three power blades, below the base
    "blade_angles": (90, 210, 330),
    "lv_contact_r": 14.0, "lv_contact_d": 5.0, "lv_contact_h": 2.0,       # four low-voltage contacts (C136.41)
    "gasket_t": 3.0,                           # base gasket on the receptacle (part of the base kit)
    "dome_d": 90.0, "dome_h": 72.0, "dome_wall": 3.0, "dome_fillet": 20.0,
    "dome_gasket_t": 1.0,                      # flat EPDM ring under the dome foot (dome_h includes it)
    "window_d": 8.2,                           # hole in the dome top for the light pipe rod
    "pipe_d": 8.0, "sleeve_od": 14.0, "sleeve_l": 10.0,
    "boss_r": 30.0, "boss_d": 9.0, "boss_h": 10.0, "dome_boss_ang": (60, 180, 300),   # dome screw bosses
    "stack_ang": (0, 120, 240),                # stack screws, spacers and standoffs, at boss_r
    "spacer_h": 12.0, "standoff_h": 30.0, "spacer_d": 6.0,
    "psu": (23.0, 38.0, 18.0),                 # isolated 12 V, 5 W encapsulated module envelope (x, y, z)
    "relay": (18.0, 24.0, 20.0),               # normally closed power relay (x, y, z)
    "mov_d": 21.0, "mov_t": 6.0,               # 20 mm class varistor, standing
    "supercap_d": 10.0, "supercap_h": 20.0,
    "board_d": 80.0, "board_t": 1.6,           # both round boards
    "board_z": 69.4,                           # controller board centre height (was 66 in the concept)
    "notch_w": 11.0, "notch_r": 25.0,          # mains board notches that clear the dome bosses
    "lv_hole": (28.0, -22.0),                  # 6 mm hole in the mains board for the low-voltage leads
    "antenna": (70.0, 10.0, 0.3), "antenna_z": 46.0,   # flexible antenna on the dome wall, -Y side (arc length, height, thickness)
    "m12_d": 16.0, "m12_l": 14.0,              # M12 panel socket, outside part
    "m12_z": 53.6, "pad": (24.0, 6.0),         # socket height; flat pad width and thickness on the dome
    # Arm and receptacle (existing street furniture, reference only)
    "receptacle_d": 104.0, "receptacle_h": 20.0,
    "arm_d": 60.0, "arm_z": -85.0,             # arm centreline relative to the base underside
    "arm_x0": -900.0, "arm_x1": -120.0,        # arm segment shown for the clamp interface
    # Sensor head
    "head_x": -470.0,                          # head centre along the arm
    "head": (120.0, 90.0, 60.0), "head_wall": 3.0, "head_lid_h": 15.0,
    "head_gap": 15.0,                          # arm underside to the top of the box
    "head_boss": (47.0, 27.0, 6.0, 8.0),       # moulded bosses in the box: x and y from centre, length, diameter
    "hplate": (104.0, 64.0, 3.0),              # printed internal plate
    "radar": (6.0, 50.0, 44.0), "radar_tilt": 25.0, "radar_dx": 42.0, "radar_gap": 3.0,
    "hboard": (65.0, 56.0), "hboard_x0": -50.0, "hboard_standoff": 6.0,
    "port_d": 20.0, "port_l": 18.0, "port_pitch": 40.0, "port_x": -30.0,
    "gland_x": 30.0, "gland_z": 20.0,          # cable gland on the +Y wall: from head centre, below the box top
    # Bracket and band clamps
    "brk_l": 110.0, "brk_w": 40.0, "brk_t": 2.0,
    "liner": (5.0, 1.5), "liner_y": 16.0,      # rubber strip on each flange top: width, thickness, inner edge
    "clamp_pitch": 90.0, "band_w": 12.0, "band_t": 0.7, "slot": (14.0, 3.0),
    "brk_screw": (25.0, 10.0),                 # four M4 screws through the web into the box top
    # Cable, controller to head
    "cable_d": 8.0,
}

# Angles of the four low-voltage contacts (dimming +, dimming -, two auxiliary); representative
LV_ANGLES = (45, 135, 180, 0)


@dataclass
class Comp:
    name: str
    shape: object
    bom: int | None       # BOM line; None for reference parts
    kind: str             # made, bought, drilled, fixing, reference
    group: str            # build_parts group (one per BOM line)
    color: str


# ------------------------------------------------------------------ helpers
def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


bx = _box


def zcyl(x, y, z0, r, h):
    from build123d import Cylinder, Pos
    return Pos(x, y, z0 + h / 2) * Cylinder(r, h)


def xcyl(x0, y, z, r, h):
    from build123d import Cylinder, Pos, Rot
    return Pos(x0 + h / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def ycyl(x, y0, z, r, h):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, y0 + h / 2, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _hex(plane, xy, af, h):
    from build123d import RegularPolygon, extrude, Pos
    sk = plane * Pos(xy[0], xy[1], 0) * RegularPolygon(af / math.sqrt(3), 6)
    return extrude(sk, h)


def hex_z(x, y, z0, af, h):
    """Hex prism along +Z from z0, across-flats af."""
    from build123d import Plane
    return _hex(Plane.XY.offset(z0), (x, y), af, h)


def hex_x(x0, y, z, af, h):
    """Hex prism along +X from x0, across-flats af."""
    from build123d import Plane
    return _hex(Plane(origin=(x0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0)), (y, z), af, h)


def hex_y(x, y0, z, af, h):
    """Hex prism along +Y from y0, across-flats af."""
    from build123d import Plane
    return _hex(Plane(origin=(0, y0, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0)), (x, -z), af, h)


def tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def polyline_tube(pts, r):
    from build123d import Sphere, Pos
    s = None
    for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        t = tube(a, b, r)
        if i:
            t = t + Pos(*a) * Sphere(r)
        s = t if s is None else s + t
    return s


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def polar(r, ang):
    t = math.radians(ang)
    return r * math.cos(t), r * math.sin(t)


def head_frame(p=PARAMS):
    """Key coordinates of the sensor head: centre x, top z, centre z."""
    top = p["arm_z"] - p["arm_d"] / 2 - p["head_gap"]
    return p["head_x"], top, top - p["head"][2] / 2


def derived(p=PARAMS):
    bh = p["base_h"]
    mb0 = bh + p["spacer_h"]                       # mains board underside
    mb1 = mb0 + p["board_t"]
    cb0 = mb1 + p["standoff_h"]                    # controller board underside
    cb1 = cb0 + p["board_t"]
    hx, htop, hzc = head_frame(p)
    t = p["head_wall"]
    hl, hw, hh = p["head"]
    pl_top = htop - t - p["head_boss"][2]          # internal plate top face
    pl_bot = pl_top - p["hplate"][2]
    rt = math.radians(p["radar_tilt"])
    rx_, ry_, rz_ = p["radar"]
    half_z = rz_ / 2 * math.cos(rt) + rx_ / 2 * math.sin(rt)
    radar_zc = pl_bot - 1.0 - half_z              # radar hangs just below the plate
    web0 = htop
    web1 = htop + p["brk_t"]
    lw, lt = p["liner"]
    ar = p["arm_d"] / 2
    contact_z = p["arm_z"] - math.sqrt(ar ** 2 - p["liner_y"] ** 2)   # liner top, where the arm sits
    flange_top = contact_z - lt
    return dict(bh=bh, mb0=mb0, mb1=mb1, cb0=cb0, cb1=cb1, dome0=bh + p["dome_gasket_t"], dome_top=bh + p["dome_h"],
                hx=hx, htop=htop, hzc=hzc, lid_top=htop - hh + p["head_lid_h"], hbot=htop - hh,
                pl_top=pl_top, pl_bot=pl_bot, radar_zc=radar_zc, radar_half_z=half_z,
                web0=web0, web1=web1, contact_z=contact_z, flange_top=flange_top)


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component, keyed by a short name. Fixings that matter for the build are included."""
    from build123d import Box, Cylinder, Pos, Rot, fillet, Axis, Polygon, extrude, Plane
    D = derived(p)
    bh = p["base_h"]
    C = {}

    def add(key, name, shape, bom, kind, group, color):
        C[key] = Comp(name, shape, bom, kind, group, color)

    R = p["boss_r"]
    A = [polar(R, a) for a in p["dome_boss_ang"]]
    B = [polar(R, a) for a in p["stack_ang"]]

    # 1 twist-lock base: body, blades, low-voltage contacts, gasket; drilled for six M3 screws,
    #   countersunk from below, inside the gasket ring and between the blades
    base = zcyl(0, 0, 0, p["base_d"] / 2, bh)
    for x, y in A + B:
        base = base - zcyl(x, y, -1, 1.7, bh + 2) - zcyl(x, y, -0.01, 3.0, 1.7)
    blades = None
    for ang in p["blade_angles"]:
        x, y = polar(p["blade_r"], ang)
        bl = Pos(x, y, -p["blade_h"] / 2) * Rot(0, 0, ang) * Box(p["blade_w"], p["blade_l"], p["blade_h"])
        blades = bl if blades is None else blades + bl
    lv = fuse([zcyl(*polar(p["lv_contact_r"], a), -p["lv_contact_h"], p["lv_contact_d"] / 2, p["lv_contact_h"]) for a in LV_ANGLES])
    g = p["gasket_t"]
    gasket = zcyl(0, 0, -g, p["base_d"] / 2 - 2, g) - zcyl(0, 0, -g - 1, p["base_d"] / 2 - 12, g + 2)
    add("base", "Twist-lock base, drilled", base, 1, "drilled", "base", "#374151")
    add("blades", "Power blades and low-voltage contacts", blades + lv, 1, "bought", "base", "#B8860B")
    add("base_gasket", "Base gasket", gasket, 1, "bought", "base", "#1F2937")

    # 17 dome gasket: flat EPDM ring under the dome foot
    dg = p["dome_gasket_t"]
    ro = p["dome_d"] / 2
    add("dome_gasket", "Dome gasket", zcyl(0, 0, bh, ro, dg) - zcyl(0, 0, bh - 1, ro - p["dome_wall"], dg + 2), 17, "made", "boards", "#111827")

    # 2 dome: printed ASA, foot on the dome gasket, three screw bosses with ribs to the wall,
    #   a flat pad for the M12 socket, an 8.2 mm hole for the light pipe and a sleeve round it
    d0, dtop = D["dome0"], D["dome_top"]
    dh = dtop - d0
    dw = p["dome_wall"]
    outer = Pos(0, 0, d0 + dh / 2) * Cylinder(ro, dh)
    outer = fillet(outer.edges().group_by(Axis.Z)[-1], p["dome_fillet"])
    inner = Pos(0, 0, d0 - 0.5 + (dh - dw + 0.5) / 2) * Cylinder(ro - dw, dh - dw + 0.5)
    inner = fillet(inner.edges().group_by(Axis.Z)[-1], p["dome_fillet"] - dw)
    dome = outer - inner
    pw, pt = p["pad"]
    zm = p["m12_z"]
    x_out = -(p["base_d"] / 2 + 0.5)                       # pad face 0.5 mm outside the base edge
    dome = dome + bx(x_out, x_out + pt + 1.5, -pw / 2, pw / 2, zm - pw / 2, zm + pw / 2)
    dome = dome - bx(x_out + pt, x_out + pt + 8, -pw / 2, pw / 2, zm - pw / 2, zm + pw / 2)   # flat inner seat
    dome = dome - xcyl(x_out - 1, 0, zm, 8.1, pt + 3)
    sl = p["sleeve_l"]
    dome = dome + zcyl(0, 0, dtop - dw - sl, p["sleeve_od"] / 2, sl + 0.5)
    dome = dome - zcyl(0, 0, dtop - dw - sl - 1, p["window_d"] / 2, sl + dw + 3)
    for (x, y), ang in zip(A, p["dome_boss_ang"]):
        boss = zcyl(x, y, d0, p["boss_d"] / 2, p["boss_h"])
        rib = Pos(0, 0, 0) * Rot(0, 0, ang) * bx(R, ro - dw + 0.5, -2, 2, d0, d0 + p["boss_h"])
        dome = dome + boss + rib - zcyl(x, y, d0 - 1, 2.0, 7)        # 4.0 mm hole for the heat-set insert
    add("dome", "Dome, printed", dome, 2, "made", "dome", "#E5E7EB")
    add("inserts", "Heat-set inserts M3 (3)", fuse([zcyl(x, y, d0, 2.0, 5.7) - zcyl(x, y, d0 - 1, 1.5, 8) for x, y in A]), 17, "fixing", "boards", "#B8860B")

    # 17 mains board: round plated-hole prototype board on three 12 mm spacers, notched for the bosses
    mb0, mb1 = D["mb0"], D["mb1"]
    rb = p["board_d"] / 2
    mboard = zcyl(0, 0, mb0, rb, p["board_t"])
    for ang in p["dome_boss_ang"]:
        mboard = mboard - Rot(0, 0, ang) * bx(p["notch_r"], rb + 2, -p["notch_w"] / 2, p["notch_w"] / 2, mb0 - 1, mb1 + 1)
    for x, y in B:
        mboard = mboard - zcyl(x, y, mb0 - 1, 1.7, 4)
    mboard = mboard - zcyl(*p["lv_hole"], mb0 - 1, 3.0, 4)       # low-voltage contact leads pass up here
    add("mboard", "Mains board", mboard, 17, "made", "boards", "#166534")
    add("spacers", "Spacers 12 mm (3)", fuse([zcyl(x, y, bh, p["spacer_d"] / 2, p["spacer_h"]) - zcyl(x, y, bh - 1, 1.7, p["spacer_h"] + 2) for x, y in B]),
        17, "fixing", "boards", "#F5F5F4")
    add("standoffs", "Standoffs 30 mm (3)", fuse([hex_z(x, y, mb1, 5.5, p["standoff_h"]) - zcyl(x, y, mb1 - 1, 1.5, p["standoff_h"] + 2) for x, y in B]), 17, "fixing", "boards", "#B8860B")

    # 3 surge stage: standing varistor and a thermal fuse against it, on the mains board
    md, mt = p["mov_d"], p["mov_t"]
    mov = ycyl(0, 26.0, mb1 + 4 + md / 2, md / 2, mt) + bx(-3, 3, 27, 31, mb1, mb1 + 4)
    tfuse = xcyl(-5, 34.5, mb1 + 4 + md / 2 - 3, 2.0, 10)
    add("surge", "Surge protection, fuse", mov + tfuse, 3, "bought", "surge", "#C2410C")

    # 4 isolated power supply module
    px, py, pz = p["psu"]
    add("psu", "Isolated power supply", bx(-2, -2 + px, -py / 2, py / 2, mb1, mb1 + pz), 4, "bought", "psu", "#7C3AED")

    # 5 fail-on relay
    rx, ry, rz = p["relay"]
    add("relay", "Fail-on relay", bx(-24, -24 + rx, -ry / 2, ry / 2, mb1, mb1 + rz), 5, "bought", "relay", "#D4A017")

    # 6 energy metering module
    add("meter", "Energy metering", bx(-9, 7, -36, -24, mb1, mb1 + 5), 6, "bought", "meter", "#2563EB")

    # 7 controller board on three 30 mm standoffs; radio module, light sensor and supercapacitor on top
    cb0, cb1 = D["cb0"], D["cb1"]
    cboard = zcyl(0, 0, cb0, rb, p["board_t"])
    for x, y in B:
        cboard = cboard - zcyl(x, y, cb0 - 1, 1.7, 4)
    radio = bx(8, 24, -2, 14, cb1, cb1 + 4)
    sensor = bx(-1.5, 1.5, -1.5, 1.5, cb1, cb1 + 1)
    scap = zcyl(-24, -6, cb1, p["supercap_d"] / 2, p["supercap_h"])
    add("cboard", "Controller, LoRaWAN radio", cboard + radio + sensor + scap, 7, "made", "ctrl", "#0F766E")

    # 8 antenna: flexible strip stuck to the inside of the dome wall on the -Y side, between the boards
    al, ah, at = p["antenna"]
    ri = ro - dw
    span = math.degrees(al / ri)
    za = p["antenna_z"]
    ant = (zcyl(0, 0, za, ri, ah) - zcyl(0, 0, za - 1, ri - at, ah + 2)) & \
        (Rot(0, 0, -90) * bx(0, ri + 5, -ri * math.sin(math.radians(span / 2)), ri * math.sin(math.radians(span / 2)), za - 1, za + ah + 1))
    add("antenna", "Antenna", ant, 8, "bought", "antenna", "#111827")

    # 9 light pipe: clear rod through the dome top, ending 0.5 mm above the light sensor
    z_pipe0 = cb1 + 1.5
    add("pipe", "Light sensor and pipe", zcyl(0, 0, z_pipe0, p["pipe_d"] / 2, dtop - z_pipe0), 9, "made", "pipe", "#16A34A")

    # 10 M12 socket in the dome pad, plug and cable to the head
    ms = xcyl(x_out - 2, 0, zm, 11.0, 2.0) + xcyl(x_out - 2 - p["m12_l"], 0, zm, p["m12_d"] / 2, p["m12_l"])
    ms = ms + xcyl(x_out, 0, zm, 7.9, pt + 8)                      # thread through the pad
    ms = ms + hex_x(x_out + pt, 0, zm, 20.0, 3.0)                  # nut inside
    ms = ms + xcyl(x_out + pt + 3, 0, zm, 6.0, 5.0)                # contact body
    add("socket", "M12 socket", ms, 10, "bought", "cable", "#1F2937")
    hx, htop = D["hx"], D["htop"]
    hl, hw, hh = p["head"]
    ar, az = p["arm_d"] / 2, p["arm_z"]
    cr = p["cable_d"] / 2
    x_plug = x_out - 2 - p["m12_l"]
    plug = xcyl(x_plug - 40, 0, zm, 10.0, 40)
    zt = az + ar + cr + 0.5
    yd = ar + cr + 5
    yg = hw / 2
    gl = 16.0
    gz = htop - p["gland_z"]
    xg = hx + p["gland_x"]
    cable = polyline_tube([(x_plug - 40, 0, zm), (-150, 0, zm), (-175, 0, zm - 25), (-175, 0, zt + 25), (-200, 0, zt),
                           (hx + hl / 2 + 60, 0, zt), (hx + hl / 2 + 52, 37.5 * math.cos(math.radians(60)), az + 37.5 * math.sin(math.radians(60))),
                           (hx + hl / 2 + 46, 38.5 * math.cos(math.radians(30)), az + 38.5 * math.sin(math.radians(30))),
                           (hx + hl / 2 + 40, yd, az), (hx + hl / 2 + 40, yg + gl + 30, gz + 20),
                           (xg + 30, yg + gl + 30, gz), (xg, yg + gl + 20, gz), (xg, yg + gl, gz)], cr)
    add("cable", "M12 plug and cable", plug + cable, 10, "bought", "cable", "#1F2937")

    # 11 sensor head box: body (top 45 mm, with four moulded bosses inside its base, which faces up)
    #    and lid (bottom 15 mm, face down); drilled for the gland, the bracket screws and the ports
    t = p["head_wall"]
    hbot = D["hbot"]
    zl = D["lid_top"]
    body = bx(hx - hl / 2, hx + hl / 2, -hw / 2, hw / 2, zl, htop) - bx(hx - hl / 2 + t, hx + hl / 2 - t, -hw / 2 + t, hw / 2 - t, zl - 1, htop - t)
    bxo, byo, bl_, bd_ = p["head_boss"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body + zcyl(hx + sx * bxo, sy * byo, htop - t - bl_, bd_ / 2, bl_ + 0.5) - zcyl(hx + sx * bxo, sy * byo, htop - t - bl_ - 1, 1.3, 6)
    sxs, sys_ = p["brk_screw"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body - zcyl(hx + sx * sxs, sy * sys_, htop - t - 1, 2.25, t + 2)
    body = body - ycyl(xg, hw / 2 - t - 1, gz, 8.1, t + 2)
    lid = bx(hx - hl / 2, hx + hl / 2, -hw / 2, hw / 2, hbot, zl) - bx(hx - hl / 2 + t, hx + hl / 2 - t, -hw / 2 + t, hw / 2 - t, hbot + t, zl + 1)
    for dy in (-p["port_pitch"] / 2, p["port_pitch"] / 2):
        lid = lid - zcyl(hx + p["port_x"], dy, hbot - 1, 8.1, t + 2)
    add("hbody", "Sensor head box, drilled", body, 11, "drilled", "head", "#CBD5E1")
    add("hlid", "Sensor head lid, drilled", lid, 11, "drilled", "head", "#E2E8F0")
    gland = ycyl(xg, hw / 2, gz, 11.0, 4.0) + ycyl(xg, hw / 2 + 4, gz, 8.0, gl - 4) + ycyl(xg, hw / 2 - t, gz, 8.0, t) \
        + hex_y(xg, hw / 2 - t - 3, gz, 20.0, 3.0)
    add("gland", "Cable gland", gland, 11, "bought", "head", "#334155")

    # 18 internal plate with radar cradle, printed ASA, on the four bosses
    plx, ply, plt = p["hplate"]
    pl_top, pl_bot = D["pl_top"], D["pl_bot"]
    plate = bx(hx - plx / 2, hx + plx / 2, -ply / 2, ply / 2, pl_bot, pl_top)
    for sx in (-1, 1):
        for sy in (-1, 1):
            plate = plate - zcyl(hx + sx * bxo, sy * byo, pl_bot - 1, 1.7, plt + 2)
    rx_, ry_, rz_ = p["radar"]
    tilt = p["radar_tilt"]
    rzc = D["radar_zc"]
    rxc = hx + p["radar_dx"]
    nrm = (-math.cos(math.radians(tilt)), 0, math.sin(math.radians(tilt)))   # toward the back of the module
    off = rx_ / 2 + p["radar_gap"] + 2.0
    cradle = Pos(rxc + nrm[0] * off, 0, rzc + nrm[2] * off) * Rot(0, tilt, 0) * Box(4.0, ry_ - 4, rz_)
    cradle = cradle & bx(hx - 60, hx + 60, -50, 50, D["hbot"], pl_bot + 0.5)   # trimmed flush with the plate top
    plate = plate + cradle
    add("hplate", "Head internal plate with radar cradle", plate, 18, "made", "hplate", "#94A3B8")

    # 12 radar module on the cradle, 3 mm off it on nylon spacers
    radar = Pos(rxc, 0, rzc) * Rot(0, tilt, 0) * Box(rx_, ry_, rz_)
    add("radar", "24 GHz radar presence sensor", radar, 12, "bought", "radar", "#0EA5E9")

    # 13 head board under the plate on 6 mm standoffs
    hbl, hbw = p["hboard"]
    so = p["hboard_standoff"]
    hb_top = pl_bot - so
    x0b = hx + p["hboard_x0"]
    hboard = bx(x0b, x0b + hbl, -hbw / 2, hbw / 2, hb_top - 1.6, hb_top)
    hso = fuse([zcyl(x0b + dx, sy * (hbw / 2 - 4), hb_top, 2.5, so) for dx in (4, hbl - 4) for sy in (-1, 1)])
    add("hboard", "Sensor head board", hboard + hso, 13, "made", "hboard", "#115E59")

    # 14 two M12 expansion ports through the lid
    pts = []
    for dy in (-p["port_pitch"] / 2, p["port_pitch"] / 2):
        x = hx + p["port_x"]
        s = zcyl(x, dy, hbot - 2, 11.0, 2.0) + zcyl(x, dy, hbot - p["port_l"], p["port_d"] / 2 - 2, p["port_l"] - 2) \
            + zcyl(x, dy, hbot, 7.9, t) + hex_z(x, dy, hbot + t, 20.0, 3.0) + zcyl(x, dy, hbot + t + 3, 6.0, 6.0)
        pts.append(s)
    add("ports", "Expansion ports (2)", fuse(pts), 14, "bought", "ports", "#9333EA")

    # 15 bracket: folded aluminium channel, web on the box top, flanges with band slots, rubber strips
    L, W, bt = p["brk_l"], p["brk_w"], p["brk_t"]
    web0, web1 = D["web0"], D["web1"]
    ftop = D["flange_top"]
    brk = bx(hx - L / 2, hx + L / 2, -W / 2, W / 2, web0, web1)
    for sy in (-1, 1):
        y0, y1 = (W / 2 - bt, W / 2) if sy > 0 else (-W / 2, -W / 2 + bt)
        brk = brk + bx(hx - L / 2, hx + L / 2, y0, y1, web0, ftop)
    sl_l, sl_h = p["slot"]
    for dx in (-p["clamp_pitch"] / 2, p["clamp_pitch"] / 2):
        brk = brk - bx(hx + dx - sl_l / 2, hx + dx + sl_l / 2, -W / 2 - 1, W / 2 + 1, web1 + 0.5, web1 + 0.5 + sl_h)
    for sx in (-1, 1):
        for sy in (-1, 1):
            brk = brk - zcyl(hx + sx * sxs, sy * sys_, web0 - 1, 2.25, bt + 2)
    add("bracket", "Bracket", brk, 15, "made", "clamps", "#94A3B8")
    lw, lt = p["liner"]
    ly = p["liner_y"]
    liners = fuse([bx(hx - L / 2, hx + L / 2, sy * ly if sy > 0 else -ly - lw, ly + lw if sy > 0 else -ly, ftop, ftop + lt) for sy in (-1, 1)])
    add("liners", "Rubber strips (2)", liners, 15, "made", "clamps", "#1F2937")

    # 15 band clamps: round the top of the arm, down outside the flanges, through the slots and
    #    across the web; worm housing on top of the arm
    bands = []
    btk = p["band_t"]
    zb = web1 + 0.5 + sl_h / 2 + btk / 2       # band inner face across the web
    for dx in (-p["clamp_pitch"] / 2, p["clamp_pitch"] / 2):
        outer_pg = _hull_poly(ar + btk, (W / 2 + btk, zb - btk - az), (-W / 2 - btk, zb - btk - az))
        inner_pg = _hull_poly(ar / math.cos(math.pi / 120) + 0.005, (W / 2, zb - az), (-W / 2, zb - az))
        pl_ = Plane(origin=(hx + dx - p["band_w"] / 2, 0, az), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        ring = extrude(pl_ * Polygon(*outer_pg, align=None), p["band_w"]) - extrude(pl_ * Polygon(*inner_pg, align=None), p["band_w"])
        worm = bx(hx + dx - 7, hx + dx + 7, -6, 6, az + ar + btk, az + ar + btk + 8)
        bands.append(ring + worm)
    add("bands", "Band clamps (2)", fuse(bands), 15, "bought", "clamps", "#9CA3AF")

    # 16 bracket screws: four M4 pan heads on the web, sealing washers and nuts inside the box
    scr = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = hx + sx * sxs, sy * sys_
            scr.append(zcyl(x, y, web1, 3.5, 2.6) + zcyl(x, y, htop - t - 1.5, 2.0, t + bt + 1.5)
                       + zcyl(x, y, htop - t - 1.5, 4.5, 1.5) + hex_z(x, y, htop - t - 4.7, 7.0, 3.2))
    add("brk_screws", "M4 screws, sealing washers, nuts (4)", fuse(scr), 16, "fixing", None, "#111827")

    # 17 screws from under the base: three into the dome inserts, three through the stack
    add("dome_screws", "M3 x 30 countersunk screws, dome (3)", fuse([zcyl(x, y, 0.0, 1.5, d0 + 5.0) for x, y in A]), 17, "fixing", "boards", "#111827")
    add("stack_screws", "M3 x 45 countersunk screws, board stack (3)", fuse([zcyl(x, y, 0.0, 1.5, mb1 + 6.0) for x, y in B]), 17, "fixing", "boards", "#111827")

    # Reference (existing street furniture, not in the BOM)
    rec = zcyl(0, 0, -g - p["receptacle_h"], p["receptacle_d"] / 2, p["receptacle_h"])
    for ang in p["blade_angles"]:
        x, y = polar(p["blade_r"], ang)
        rec = rec - Pos(x, y, -p["blade_h"] / 2) * Rot(0, 0, ang) * Box(p["blade_w"] + 1, p["blade_l"] + 1, p["blade_h"] + 0.5)
    for ang in LV_ANGLES:
        x, y = polar(p["lv_contact_r"], ang)
        rec = rec - zcyl(x, y, -g - 4, p["lv_contact_d"] / 2 + 1, 4)
    add("receptacle", "Luminaire receptacle (reference)", rec, None, "reference", None, "#A3A9B1")
    add("arm", "Lamp arm (reference)", tube((p["arm_x0"], 0, az), (p["arm_x1"], 0, az), ar), None, "reference", None, "#A3A9B1")
    return C


def _hull_poly(r, *pts, n=120):
    """Convex hull (2D, y and z relative to the arm centre) of a circle of radius r and points."""
    P = [(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)) for k in range(n)] + list(pts)
    P = sorted(set((round(a, 6), round(b, 6)) for a, b in P))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(P):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


# BOM line names, colours and explode offsets for the concept media (one solid per line)
BOM_LINES = {
    1: ("Twist-lock base, 7-contact", "#374151", (0, 0, -40)),
    2: ("Dome cover, UV-stable", "#E5E7EB", (0, 0, 320)),
    3: ("Surge protection, fuse", "#C2410C", (0, 60, 40)),
    4: ("Isolated power supply", "#7C3AED", (60, 0, 60)),
    5: ("Fail-on relay", "#D4A017", (-70, 0, 55)),
    6: ("Energy metering", "#2563EB", (60, -80, 70)),
    7: ("Controller, LoRaWAN radio", "#0F766E", (0, 0, 150)),
    8: ("Antenna", "#111827", (0, 60, 210)),
    9: ("Light sensor and pipe", "#16A34A", (0, 0, 250)),
    10: ("M12 port and cable", "#1F2937", (0, 0, 0)),
    11: ("Sensor head enclosure", "#CBD5E1", (0, -260, -40)),
    12: ("24 GHz radar presence sensor", "#0EA5E9", (130, 0, -60)),
    13: ("Sensor head board", "#115E59", (-20, 0, -150)),
    14: ("Expansion ports (2)", "#9333EA", (0, 0, -270)),
    15: ("Arm band clamps", "#94A3B8", (0, 0, 70)),
    17: ("Controller boards and fixings", "#166534", (0, 0, 100)),
    18: ("Head internal plate", "#64748B", (0, 0, -100)),
}


def build_parts(p=PARAMS):
    """Return a list of (name, shape, color, bom_item, explode_offset), one per BOM line with
    geometry, then the reference parts (bom_item None). Line 16 (hardware) has no solid of its own."""
    C = build_components(p)
    by = {}
    for c in C.values():
        if c.bom in BOM_LINES:
            by[c.bom] = c.shape if c.bom not in by else by[c.bom] + c.shape
    parts = [(BOM_LINES[k][0], by[k], BOM_LINES[k][1], k, BOM_LINES[k][2]) for k in sorted(by)]
    parts += [(c.name, c.shape, c.color, None, (0, 0, 0)) for c in C.values() if c.kind == "reference"]
    return parts


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts if bom}
    ref = [s for _, s, _, bom, _ in parts if bom is None]
    return {
        "lampnode-assembly": Compound([s for _, s, _, bom, _ in parts if bom]),
        "lampnode-controller": Compound([by[i] for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 17)]),
        "lampnode-sensor-head": Compound([by[i] for i in (11, 12, 13, 14, 15, 18)]),
        "lampnode-installed-reference": Compound([s for _, s, _, _, _ in parts]),
        "_ref": Compound(ref),
    }


def envelope(shape):
    bb = shape.bounding_box()
    return bb.size.X, bb.size.Y, bb.size.Z


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm).
    Returns a list of (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # controller
    chk("Base gasket on the receptacle", S("base_gasket"), S("receptacle"), "touch")
    chk("Blades in the receptacle slots, clear of their walls", S("blades"), S("receptacle"), 0.2)
    chk("Dome gasket on the base", S("dome_gasket"), S("base"), "touch")
    chk("Dome on the dome gasket", S("dome"), S("dome_gasket"), "touch")
    chk("Dome bosses stop above the base (screws squeeze the gasket)", S("dome"), S("base"), 0.9)
    chk("Spacers on the base", S("spacers"), S("base"), "touch")
    chk("Mains board on the spacers", S("mboard"), S("spacers"), "touch")
    chk("Mains board clear of the dome bosses and wall", S("mboard"), S("dome"), 0.5)
    chk("Standoffs on the mains board", S("standoffs"), S("mboard"), "touch")
    chk("Controller board on the standoffs", S("cboard"), S("standoffs"), "touch")
    chk("Controller board clear of the dome", S("cboard"), S("dome"), 1.0)
    for k in ("surge", "psu", "relay", "meter"):
        chk(f"{C[k].name} on the mains board", S(k), S("mboard"), "touch")
        chk(f"{C[k].name} clear of the controller board", S(k), S("cboard"), 2.0)
        chk(f"{C[k].name} clear of the standoffs", S(k), S("standoffs"), 1.0)
        chk(f"{C[k].name} clear of the dome", S(k), S("dome"), 1.0)
        chk(f"{C[k].name} clear of the M12 socket", S(k), S("socket"), 3.0)
    comp = ["surge", "psu", "relay", "meter"]
    for i, a in enumerate(comp):
        for b_ in comp[i + 1:]:
            chk(f"{C[a].name} apart from {C[b_].name}", S(a), S(b_), 1.0)
    chk("M12 socket in the dome pad", S("socket"), S("dome"), "touch")
    chk("M12 socket clear of both boards", S("socket"), S("mboard") + S("cboard"), 2.0)
    chk("M12 socket clear of the standoffs", S("socket"), S("standoffs"), 3.0)
    chk("Antenna on the dome wall", S("antenna"), S("dome"), "touch")
    chk("Antenna clear of both boards", S("antenna"), S("cboard") + S("mboard"), 3.0)
    chk("Antenna clear of the mains parts", S("antenna"), S("meter") + S("surge") + S("standoffs"), 3.0)
    chk("Light pipe in the dome hole and sleeve", S("pipe"), S("dome"), 0.05)
    chk("Light pipe clear of the light sensor (0.5 mm)", S("pipe"), S("cboard"), 0.4)
    chk("Heat-set inserts in the bosses", S("inserts"), S("dome"), "touch")
    for k in ("dome_screws", "stack_screws"):
        chk(f"{C[k].name} clear of the blades", S(k), S("blades"), 3.0)
        chk(f"{C[k].name} clear of the base gasket", S(k), S("base_gasket"), 1.0)
        chk(f"{C[k].name} in their holes in the base", S(k), S("base"), 0.15)
    chk("Dome screws in the boss holes", S("dome_screws"), S("dome"), 0.4)
    chk("Stack screws through the spacers and mains board", S("stack_screws"), S("spacers") + S("mboard"), 0.15)
    chk("Supercapacitor clear of the dome", S("cboard"), S("dome"), 1.0)
    # sensor head
    chk("Lid on the box", S("hlid"), S("hbody"), "touch")
    chk("Internal plate on the bosses", S("hplate"), S("hbody"), "touch")
    chk("Radar clear of the internal plate and cradle", S("radar"), S("hplate"), 0.9)
    chk("Radar clear of the box and lid", S("radar"), S("hbody") + S("hlid"), 1.0)
    chk("Head board on its standoffs under the plate", S("hboard"), S("hplate"), "touch")
    chk("Head board clear of the radar", S("hboard"), S("radar"), 3.0)
    chk("Head board clear of the box and lid", S("hboard"), S("hbody") + S("hlid"), 3.0)
    chk("Expansion ports in the lid", S("ports"), S("hlid"), "touch")
    chk("Expansion ports clear of the head board and radar", S("ports"), S("hboard") + S("radar"), 10.0)
    chk("Cable gland in the box wall", S("gland"), S("hbody"), "touch")
    chk("Cable gland clear of the plate, board and radar", S("gland"), S("hplate") + S("hboard") + S("radar"), 2.0)
    chk("Bracket web on the box top", S("bracket"), S("hbody"), "touch")
    chk("Rubber strips on the flanges", S("liners"), S("bracket"), "touch")
    chk("Arm on the rubber strips", S("liners"), S("arm"), "touch")
    chk("Arm clear of the bracket", S("bracket"), S("arm"), 2.0)
    chk("Bands on the arm", S("bands"), S("arm"), "touch")
    chk("Bands through the flange slots and over the web, not cutting the bracket", S("bands"), S("bracket"), 0.0)
    chk("Bands clear of the rubber strips", S("bands"), S("liners"), 0.5)
    chk("Bands clear of the box", S("bands"), S("hbody"), 1.0)
    chk("Bracket screws clear of the bands", S("brk_screws"), S("bands"), 2.0)
    chk("Bracket screw nuts clear of the internal plate", S("brk_screws"), S("hplate"), 1.0)
    chk("Cable lies along the arm without cutting into it", S("cable"), S("arm"), 0.0)
    chk("Cable clear of the bracket and bands", S("cable"), S("bracket") + S("bands"), 5.0)
    chk("Cable clear of the box", S("cable"), S("hbody"), 1.0)
    chk("Cable clear of the receptacle", S("cable"), S("receptacle"), 10.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        if name.startswith("_"):
            continue
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        x, y, z = envelope(shape)
        print(f"{name:30s} {x:7.1f} x {y:6.1f} x {z:6.1f} mm")
    for n, s, _, bom, _ in parts:
        print(f"volume {bom if bom else '-':>2} {n:34s} {s.volume / 1e3:8.1f} cm3")
    D = derived()
    print(f"boards: mains {D['mb0']:.1f} to {D['mb1']:.1f} mm, controller {D['cb0']:.1f} to {D['cb1']:.1f} mm; "
          f"radar centre {D['radar_zc'] - D['htop']:.1f} mm below the box top; arm sits on the strips at {D['contact_z']:.2f} mm")
    print_checks()
