"""LampNode general arrangement drawing LPN-DWG-001 (Rev P4).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/LPN-DWG-001.svg, .pdf and .png from the parametric model.
LPN-DWG-001 is free because the concept blueprint uses LPN-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts, envelope, head_frame  # noqa: E402

parts = build_parts()
asm = assemblies(parts)
work = ROOT / "cad/drawings/_views"
views = project_views(asm["lampnode-installed-reference"], work)
cx, cy, cz = envelope(asm["lampnode-controller"])
hx_, hy_, hz_ = envelope(asm["lampnode-sensor-head"])
hx, htop, hzc = head_frame(P)

s = Sheet(project="LampNode", title="General arrangement, controller and sensor head", dwg_no="LPN-DWG-001",
          rev="P4", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Dome ASA; base and head box PC; clamps stainless; bracket 2 mm Al. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from cad/src/model.py (LPN-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Port power note: 2.5 W above 50 C inside (LPN-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Design for construction: fixings, boards, bracket (LPN-DDR-003)", "2026-09-30", "AC"),
                     ("P4", "Decisions of 2026-10-02: 915 MHz radio band and the M12 port pinout added to the notes", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale; grey = existing receptacle and arm")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Controller {cx:.0f} dia. x {cz:.0f} incl. blades; dome {P['dome_d']:.0f} x {P['dome_h']:.0f}",
    "Base: ANSI C136.41 7-contact twist-lock (representative),",
    "  3 power blades, 4 low-voltage contacts, no earth",
    f"Sensor head {P['head'][0]:.0f} x {P['head'][1]:.0f} x {P['head'][2]:.0f}, center {abs(hx):.0f} from",
    f"  receptacle toward the pole; {P['head_gap']:.0f} below a {P['arm_d']:.0f} dia. arm",
    f"Radar tilted {P['radar_tilt']:.0f} deg down, looking along the street",
    "M12 5-pole: dome pad to head, 1 m cable; 2 ports in head lid",
    f"Band clamps for 50 to 80 arms, pitch {P['clamp_pitch']:.0f}, through",
    "  slots in a folded 2 mm bracket; arm rests on rubber strips",
    "Dome and board stack: 6 x M3 from under the base",
    "Mains 120 to 277 V AC; 0 to 10 V dimming; relay normally closed",
    "Ports 12 V SELV, 3 W total; 2.5 W above 50 C inside",
    "US915 radio; port pins 1 12 V, 3 gnd, 2 and 4 RS-485, 5 wake",
    "Mass: controller 0.33 kg, head 0.42 kg (LPN-CAL-001)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/LPN-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/LPN-DWG-001.svg, .pdf, .png")
