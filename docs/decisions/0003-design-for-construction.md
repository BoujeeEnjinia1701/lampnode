---
doc_id: LPN-DDR-003
title: LampNode design for construction
project: LampNode
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. Made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model (`cad/src/model.py` at LPN-DWG-001 Rev P2) showed what LampNode does and where its parts sit, and its clash check passed, but most of the parts inside the controller and the sensor head floated in the air with nothing holding them, the dome and the base had no fixing between them, the light window was an open hole, and the bracket was a solid block fused to two thick rings. Checking the model part by part with build123d (overlaps, contacts, clearances, fixings and assembly order) found the eleven problems in Table 1.

The changes keep what LampNode does: the same twist-lock base and socket, the same dome size and height (97 mm with the base), the same electronics, radar, tilt and ports, the same sensor head box and position under the arm, the same cable link and the same arm range. Nothing here changes the pitch, the requirements or the product's safety case. Every change is in `cad/src/model.py`, which now runs 80 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart are apart by at least the stated clearance. All 80 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The parts inside the controller floated: the supply sat 9 mm above the surge carrier with nothing under it, the relay 1 mm above it, and the controller board hung at 66 mm with no support. | Two 80 mm round boards. The mains board sits on three 12 mm spacers on the base and carries the surge stage, supply, relay and metering module; the controller board sits on three 30 mm standoffs above it. One M3 x 45 countersunk screw from under the base at each of three points clamps base, spacer and mains board into the standoff. The controller board centre moves from 66.0 to 69.4 mm. | A stack on spacers is how small mains controllers are built. One screw per corner holds both levels, and the screws sit inside the base gasket ring so the seal is untouched. |
| P2 | The dome had no fixing to the base and no seal between them. | Three bosses printed inside the dome foot on a 60 mm circle, tied to the wall by ribs, each with an M3 brass heat-set insert. Three M3 x 30 countersunk screws come up from under the base. A 1 mm EPDM ring sits under the dome foot; the bosses stop 1 mm above the base so the screws squeeze the ring. The dome body is 71 mm tall on the 1 mm ring, so the controller is still 97 mm tall. The mains board has three notches that the bosses pass through. | No screw is visible on the outside and none passes through the seal. The dome comes off with three screws from below once the controller is out of the socket. |
| P3 | The M12 socket was fixed to the curved side of the bought base, a 94 mm moulding whose wall and inside are unknown; a 16 mm panel socket cannot seal on that curve. | The socket moves to a flat printed pad on the pole side of the dome, 24 x 24 x 6 mm, its face 0.5 mm outside the base edge, socket centre 53.6 mm above the base underside, between the two boards. | The dome is printed, so the flat seat and hole cost nothing. The socket still faces the pole and the cable still runs down the arm. |
| P4 | The light window was a 16 mm open hole with the top of the light pipe 2 mm below it: rain would get in. | An 8 mm clear acrylic rod sealed into an 8.2 mm hole in the dome top, flush outside, held in a printed 10 mm sleeve, ending 0.5 mm above the light sensor on the controller board. | One part makes both the window and the pipe, and the seal is a short bead of clear sealant. |
| P5 | The antenna was drawn as a rod standing on the controller board, while BOM line 8 is a flexible PCB antenna. | A flexible antenna strip about 70 x 10 mm stuck to the inside of the dome wall on the side away from the pole, between the boards, 3 mm or more from every other part, its lead to the radio. | Matches the part bought; stuck to plastic, above the luminaire's metal body as LPN-PRC-001 intends. |
| P6 | Bought part envelopes did not fit together: a 44 x 30 x 22 mm supply, two 14 mm varistor discs and a thermal fuse lay on a carrier disc. | Supply envelope 23 x 38 x 18 mm, the size of common 5 W encapsulated 12 V modules; one 20 mm class varistor standing on the board with the thermal fuse against it, as BOM line 3 describes. The layout keeps the area under the M12 socket clear. | The concept envelope was a placeholder; real 5 W modules are this size, and the smaller footprint leaves room for the bosses, standoffs and socket. |
| P7 | The base was solid and undrilled, with nothing to fix to. | Six 3.4 mm holes through the bought base on a 60 mm circle between the blades and inside the gasket ring, countersunk from below: three for the dome, three for the board stack. | The only place inside the gasket and clear of the blade pockets and contact wells. |
| P8 | The sensor head box was a closed shell with no lid, and the head board and radar floated inside it. | Box body and 15 mm lid. A printed internal plate on the four moulded bosses in the box's base (which faces up) carries the head board below it on 6 mm standoffs and, at the street end, a cradle that holds the radar 25° down on 3 mm spacers. The radar centre sits 34.2 mm below the box top instead of 30 mm. | Uses the bosses a stock box already has. The radar keeps its 25° tilt and its place behind the radar-transparent end wall; 4 mm lower changes nothing in the radar calculation at 7.7 m height. |
| P9 | The two expansion ports were cylinders hanging under the box with no hole or nut, and the cable had no gland. | Ports through 16.2 mm holes in the lid with nuts inside and plug-in leads to the head board; an M16 cable gland on the side wall facing away from the arm, 30 mm toward the street end. | The lid comes off without unsoldering anything; every penetration has a seal outside and a nut inside. |
| P10 | The bracket was a solid 130 x 30 x 15 mm block, longer than the 120 mm box, fused to two 5 mm thick rings standing in for band clamps; the rings cut into the block. | A bracket folded from 2 mm aluminium: a 40 mm web screwed to the box top by four M4 screws with bonded sealing washers, and two flanges on which the arm rests on 1.5 mm EPDM strips. Each band clamp goes over the arm, down outside the flanges, through a 14 x 3 mm slot in each flange and across the web. The head keeps its 15 mm gap below a 60 mm arm. | A channel on a pipe is self-centring for arms from 50 to 80 mm; the band pulls the arm onto the strips and the bracket onto the arm; nothing is drilled in the arm. |
| P11 | The cable ran from the base through where the luminaire body is, and dipped into the arm on its way to the head. | The cable leaves the dome pad level, passes beyond the luminaire, drops to the top of the arm, runs along it with cable ties and comes round the side of the arm to the gland. Plugged in after the controller is turned into the socket. | Clears the luminaire and the arm; about 0.7 m of the 1 m cordset is used, leaving a slack loop for the quarter turn. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | New line 17, controller boards and fixings (USD 7.00): mains board, spacers, standoffs, inserts, screws, dome gasket, harness terminals. New line 18, head internal plate (USD 4.00, printed). Line 15 repriced to USD 7.00 (folded bracket, strips) and line 16 to USD 7.00 (sealing washers, cable ties). Specifications of lines 1 to 4, 6 to 11 and 13 updated to match the model. | Parts added for construction |
| Cost | Value-engineering target: USD 150. Estimated cost of the constructable design: USD 143.00 (USD 7.00 under the target); the concept was USD 130.00. `budget_usd` is unchanged. | Lines 17 and 18 and the repricing above |
| Mass | Controller 0.33 kg (was 0.34 kg); sensor head with clamps and cable 0.42 kg (was 0.45 kg). | Real supply size; folded bracket in place of the solid block; boards and fixings added |
| Calculations | LPN-CAL-001 v0.3: sections 12 and 13 and the R16 row. Energy, power, inrush, radar, metering, surge and thermal results are unchanged: the dome keeps its size, the radar its tilt and near enough its height, and the electronics their power figures. | Follows the model |
| Drawing | LPN-DWG-001 Rev P3; making sketches LPN-DWG-101 to 108 added. | Follows the model |
| Documents | LPN-PRC-001 v0.5 (component table, mass, cost), LPN-REQ-001 v0.5 (R16 against the value-engineering target). No requirement changed status: 0 not met, 4 at risk (R3, R6, R7, R11), 11 met on paper, by design review or under the value-engineering target, 1 not verifiable at TRL 3 (R1). | Follows the model |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The first prototype's mains board is a hand-wired plated prototype board carrying parts at up to 305 V. That is acceptable on a bench behind an isolating transformer and an RCD, but not on a street. | (a) build the first prototype on hand-wired boards for bench work only, and lay out a printed circuit board (TRL 4) before any outdoor or luminaire-powered test; (b) lay out the mains board before building anything. | (a): it tests the mechanics, fixings and fail-on behaviour soonest, and the build plan's safety stops keep it off the street. |
| A2 | The M12 socket moves from the base to the dome (P3), which changes the controller's look from the pole side. The photoreal renders and `cad/src/product_model.py` still show it on the base. | (a) accept, and update the appearance model and renders on Amish's Mac; (b) look for a bought base with a socket boss. | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan LPN-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register LPN-DEC-001.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: M12 socket on the base, solid bracket and the earlier window. They need updating on Amish's Mac, where Blender is.
- The base kit, the head box, the M12 socket, the supply, relay and radar module are chosen at TRL 4; the sizes this record assumes for them are listed as items to confirm in LPN-DEC-001.

> **Safety:** The controller carries mains voltage (up to 277 V AC nominal, 305 V maximum). None of the changes above alters the fail-on relay, the surge stage or the isolation between the mains and 12 V sides; the board layout keeps 6 mm of bare board between them. The hand-wired mains board of the first prototype is for bench work only (A1).
