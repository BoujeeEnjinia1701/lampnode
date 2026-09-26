"""LampNode parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, prints the main envelopes, runs a clash
check between the main parts and prints part volumes for the mass budget in LPN-CAL-001.

Massing-plus detail: correct interfaces (twist-lock base with three power blades and four
low-voltage contacts on the ANSI C136.41 receptacle, M12 ports, arm band clamps, radar tilt)
and main dimensions; not fabrication detail. Blade and contact positions are representative
and must be checked against ANSI C136.10 and C136.41 before any part is made.

Local frame, units mm: origin at the center of the receptacle's top face on the luminaire,
Z up, X along the arm away from the pole (the pole is toward -X), Y across the arm. The
controller sits on the receptacle; the sensor head is clamped under the arm, between the
pole and the luminaire, with its radar looking along +X, tilted down the street.
"""
import math
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # Controller (items 1 to 9), LPN-PRC-001 v0.3
    "base_d": 94.0, "base_h": 25.0,            # twist-lock base
    "blade_r": 26.0, "blade_w": 4.0, "blade_l": 12.0, "blade_h": 14.0,   # three power blades, below the base
    "lv_contact_r": 14.0, "lv_contact_d": 5.0, "lv_contact_h": 2.0,       # four low-voltage contacts (C136.41)
    "gasket_t": 3.0,
    "dome_d": 90.0, "dome_h": 72.0, "dome_wall": 3.0, "dome_fillet": 20.0,
    "window_d": 16.0,                          # clear window over the light sensor
    "psu": (44.0, 30.0, 22.0),                 # isolated 12 V, 5 W module envelope
    "relay": (18.0, 24.0, 20.0),               # normally closed power relay
    "supercap_d": 10.0, "supercap_h": 20.0,
    "board_d": 80.0, "board_t": 1.6,           # controller board, horizontal, under the dome
    "board_z": 66.0,
    "antenna_h": 26.0,
    "m12_d": 16.0, "m12_l": 16.0,              # M12 panel socket on the side of the base (toward the pole)
    # Arm and receptacle (existing street furniture, reference only)
    "receptacle_d": 104.0, "receptacle_h": 20.0,
    "arm_d": 60.0, "arm_z": -85.0,             # arm centerline relative to the receptacle top
    "arm_x0": -900.0, "arm_x1": -120.0,        # arm segment shown for the clamp interface
    # Sensor head (items 11 to 15)
    "head_x": -470.0,                          # head center along the arm
    "head": (120.0, 90.0, 60.0), "head_wall": 3.0,
    "head_gap": 15.0,                          # bracket gap between the arm and the box
    "radar": (6.0, 50.0, 44.0), "radar_tilt": 25.0,   # 24 GHz module, tilted down from horizontal
    "clamp_pitch": 90.0, "clamp_w": 20.0, "clamp_t": 5.0,
    "port_d": 20.0, "port_l": 18.0, "port_pitch": 40.0,
    # Cable, controller to head (item 10)
    "cable_d": 8.0,
}

# Angles of the four low-voltage contacts (dimming +, dimming -, two auxiliary); representative
LV_ANGLES = (45, 135, 180, 0)


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def polyline_tube(pts, r):
    s = None
    for a, b in zip(pts[:-1], pts[1:]):
        t = tube(a, b, r)
        s = t if s is None else s + t
    return s


def head_frame(p=PARAMS):
    """Key coordinates of the sensor head: center x, top z, center z."""
    top = p["arm_z"] - p["arm_d"] / 2 - p["head_gap"]
    return p["head_x"], top, top - p["head"][2] / 2


def build_parts(p=PARAMS):
    """Return a list of (name, shape, color, bom_item, explode_offset). bom_item None = reference."""
    from build123d import Box, Cylinder, Pos, Rot, fillet, Axis
    b = _box
    parts = []

    # 1 Twist-lock base: body, three power blades, four low-voltage contacts, gasket
    bh = p["base_h"]
    base = Pos(0, 0, bh / 2) * Cylinder(p["base_d"] / 2, bh)
    for ang in (90, 210, 330):
        t = math.radians(ang)
        blade = Pos(p["blade_r"] * math.cos(t), p["blade_r"] * math.sin(t), -p["blade_h"] / 2) \
            * Rot(0, 0, ang) * Box(p["blade_w"], p["blade_l"], p["blade_h"])
        base = base + blade
    for ang in LV_ANGLES:
        t = math.radians(ang)
        base = base + Pos(p["lv_contact_r"] * math.cos(t), p["lv_contact_r"] * math.sin(t),
                          -p["lv_contact_h"] / 2) * Cylinder(p["lv_contact_d"] / 2, p["lv_contact_h"])
    # gasket ring, compressed between the base and the receptacle top face (Z = -gasket_t)
    gasket = Pos(0, 0, -p["gasket_t"] / 2) * (Cylinder(p["base_d"] / 2 - 2, p["gasket_t"])
                                              - Cylinder(p["base_d"] / 2 - 12, p["gasket_t"] + 1))
    base = base + gasket
    parts.append(("Twist-lock base, 7-contact", base, "#374151", 1, (0, 0, -40)))

    # 2 Dome cover, with a window over the light sensor
    dh, dw = p["dome_h"], p["dome_wall"]
    z_dome = bh + dh / 2
    outer = Pos(0, 0, z_dome) * Cylinder(p["dome_d"] / 2, dh)
    outer = fillet(outer.edges().group_by(Axis.Z)[-1], p["dome_fillet"])
    inner = Pos(0, 0, z_dome - dw / 2 - 0.5) * Cylinder(p["dome_d"] / 2 - dw, dh - dw + 1)
    inner = fillet(inner.edges().group_by(Axis.Z)[-1], p["dome_fillet"] - dw)
    dome = outer - inner - Pos(0, 0, bh + dh - dw / 2) * Cylinder(p["window_d"] / 2, dw * 2)
    parts.append(("Dome cover, UV-stable", dome, "#E5E7EB", 2, (0, 0, 320)))

    # 3 Surge stage: MOV and GDT carrier disc with two MOV discs
    surge = Pos(0, 0, bh + 3) * Cylinder(40, 2) + Pos(-5, 27, bh + 9) * Cylinder(7, 10) \
        + Pos(-5, -27, bh + 9) * Cylinder(7, 10) + Pos(-20, 25, bh + 8) * Cylinder(4, 8)
    parts.append(("Surge protection, fuse", surge, "#C2410C", 3, (0, 0, 10)))

    # 4 Isolated power supply
    px, py, pz = p["psu"]
    psu = b(10 - px / 2, 10 + px / 2, -py / 2, py / 2, bh + 14, bh + 14 + pz)   # raised above the surge stage
    parts.append(("Isolated power supply", psu, "#7C3AED", 4, (40, 0, 60)))

    # 5 Fail-on relay
    rx, ry, rz = p["relay"]
    relay = b(-26 - rx / 2, -26 + rx / 2, -ry / 2, ry / 2, bh + 5, bh + 5 + rz)
    parts.append(("Fail-on relay", relay, "#D4A017", 5, (-60, 0, 55)))

    # 6 Energy metering: shunt and metering IC carrier
    meter = b(10, 18, 20, 32, bh + 4, bh + 12)
    parts.append(("Energy metering", meter, "#2563EB", 6, (150, -40, 110)))

    # 7 Controller board with radio module and supercapacitor hanging below it
    bz = bh + p["board_z"] - bh
    ctrl = Pos(0, 0, bz) * Cylinder(p["board_d"] / 2, p["board_t"]) + b(8, 24, -2, 14, bz + 0.8, bz + 4.8) \
        + Pos(22, -24, bz - p["supercap_h"] / 2 - 0.8) * Cylinder(p["supercap_d"] / 2, p["supercap_h"])
    parts.append(("Controller, LoRaWAN radio", ctrl, "#0F766E", 7, (0, 0, 115)))

    # 8 Antenna, vertical, beside the light pipe
    ah = p["antenna_h"]
    antenna = Pos(-18, 14, bz + 0.8 + ah / 2) * Cylinder(3, ah)
    parts.append(("Antenna", antenna, "#111827", 8, (-40, 0, 150)))

    # 9 Light sensor and pipe up to the window
    top_in = bh + dh - dw
    lp = top_in - (bz + 0.8)
    light = Pos(0, 0, bz + 0.8 + lp / 2) * Cylinder(4, lp) + Pos(0, 0, top_in - 2) * Cylinder(6, 4)
    parts.append(("Light sensor and pipe", light, "#16A34A", 9, (0, 0, 190)))

    # Sensor head geometry
    hx, htop, hzc = head_frame(p)
    hl, hw, hh = p["head"]
    ar = p["arm_d"] / 2
    az = p["arm_z"]

    # 10 M12 port on the base and cable along the arm to the head
    r0 = p["base_d"] / 2
    port = Pos(-r0 - p["m12_l"] / 2, 0, bh / 2) * Rot(0, 90, 0) * Cylinder(p["m12_d"] / 2, p["m12_l"])
    cr = p["cable_d"] / 2
    x_end = -r0 - p["m12_l"]
    zt = az + ar + cr + 1                      # cable lying on top of the arm
    yd = ar + cr + 6                           # drop beside the arm
    xg = hx + 30                               # cable gland on the +Y side of the head
    cable = polyline_tube([(x_end, 0, bh / 2), (x_end - 30, 0, zt + 20), (hx + hl / 2 + 40, 0, zt),
                           (hx + hl / 2 + 30, yd, zt), (hx + hl / 2 + 30, yd, htop - 20), (hx + hl / 2 + 30, hw / 2 + 12, htop - 20),
                           (xg, hw / 2 + 12, htop - 20), (xg, hw / 2 + 1, htop - 20)], cr)
    parts.append(("M12 port and cable", port + cable, "#1F2937", 10, (0, 0, 0)))

    # 11 Sensor head enclosure (open shell, lid face down)
    t = p["head_wall"]
    head = b(hx - hl / 2, hx + hl / 2, -hw / 2, hw / 2, htop - hh, htop) \
        - b(hx - hl / 2 + t, hx + hl / 2 - t, -hw / 2 + t, hw / 2 - t, htop - hh + t, htop - t)
    parts.append(("Sensor head enclosure", head, "#CBD5E1", 11, (0, -260, -40)))

    # 12 24 GHz radar module behind the +X face, tilted down the street
    rx_, ry_, rz_ = p["radar"]
    radar = Pos(hx + hl / 2 - t - 15, 0, hzc) * Rot(0, p["radar_tilt"], 0) * Box(rx_, ry_, rz_)
    parts.append(("24 GHz radar presence sensor", radar, "#0EA5E9", 12, (130, 0, -60)))

    # 13 Sensor head board
    head_board = b(hx - 45, hx + 25, -35, 35, htop - hh + t + 10, htop - hh + t + 11.6)
    parts.append(("Sensor head board", head_board, "#115E59", 13, (-20, 0, -150)))

    # 14 Two expansion ports on the underside
    pl = p["port_l"]
    exp = None
    for dy in (-p["port_pitch"] / 2, p["port_pitch"] / 2):
        c = Pos(hx - 30, dy, htop - hh - pl / 2) * Cylinder(p["port_d"] / 2, pl)
        exp = c if exp is None else exp + c
    parts.append(("Expansion ports (2)", exp, "#9333EA", 14, (0, 0, -270)))

    # 15 Two band clamps round the arm and a bracket to the head
    clamps = None
    for dx in (-p["clamp_pitch"] / 2, p["clamp_pitch"] / 2):
        ring = Pos(hx + dx, 0, az) * Rot(0, 90, 0) * (Cylinder(ar + p["clamp_t"], p["clamp_w"])
                                                       - Cylinder(ar, p["clamp_w"] + 2))
        clamps = ring if clamps is None else clamps + ring
    clamps = clamps + b(hx - 65, hx + 65, -15, 15, htop, az - ar)
    parts.append(("Arm band clamps", clamps, "#94A3B8", 15, (0, 0, 70)))

    # Reference (existing street furniture, not in the BOM)
    g = p["gasket_t"]
    rec = Pos(0, 0, -g - p["receptacle_h"] / 2) * Cylinder(p["receptacle_d"] / 2, p["receptacle_h"])
    for ang in (90, 210, 330):  # blade slots
        tt = math.radians(ang)
        rec = rec - Pos(p["blade_r"] * math.cos(tt), p["blade_r"] * math.sin(tt), -p["blade_h"] / 2) \
            * Rot(0, 0, ang) * Box(p["blade_w"] + 1, p["blade_l"] + 1, p["blade_h"] + 0.5)
    for ang in LV_ANGLES:  # spring contact wells for the four low-voltage contacts
        tt = math.radians(ang)
        rec = rec - Pos(p["lv_contact_r"] * math.cos(tt), p["lv_contact_r"] * math.sin(tt), -g) \
            * Cylinder(p["lv_contact_d"] / 2 + 1, 4)
    parts.append(("Luminaire receptacle (reference)", rec, "#A3A9B1", None, (0, 0, -80)))
    arm = tube((p["arm_x0"], 0, az), (p["arm_x1"], 0, az), ar)
    parts.append(("Lamp arm (reference)", arm, "#A3A9B1", None, (0, 0, 0)))
    return parts


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts if bom}
    ref = [s for _, s, _, bom, _ in parts if bom is None]
    return {
        "lampnode-assembly": Compound([s for _, s, _, bom, _ in parts if bom]),
        "lampnode-controller": Compound([by[i] for i in range(1, 10)]),
        "lampnode-sensor-head": Compound([by[i] for i in range(11, 16)]),
        "lampnode-installed-reference": Compound([s for _, s, _, _, _ in parts]),
        "_ref": Compound(ref),
    }


def envelope(shape):
    bb = shape.bounding_box()
    return bb.size.X, bb.size.Y, bb.size.Z


if __name__ == "__main__":
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
    solids = [(n, s) for n, s, _, bom, _ in parts]
    worst = 0.0
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            v = (solids[i][1] & solids[j][1]).volume
            if v > 1.0:
                print(f"clash {solids[i][0]} / {solids[j][0]}: {v:.0f} mm3")
                worst = max(worst, v)
    print("clash check: none" if worst == 0 else "clash check: see above")
    for n, s, _, bom, _ in parts:
        print(f"volume {bom if bom else '-':>2} {n:34s} {s.volume / 1e3:8.1f} cm3")
