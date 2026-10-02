# Review note: LampNode

## Session 2026-10-01: build plan and design for construction (kit 1.7.0)

On 2026-09-30 Amish approved the build plan format and asked for it across all repos, with outstanding decisions kept in a separate design decisions register, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." On 2026-10-01 he asked for budgets to be treated as value-engineering targets. This session ran the `/build-plan` work on LampNode. This section is placed at the top to keep this note's newest-first order.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Constructability review of every part with build123d: `cad/src/model.py` rebuilt as `build_components()` with every part as made or bought and fixed to its neighbours, and 80 constructability checks (`python cad/src/model.py --check`), all passing.
- `docs/decisions/0003-design-for-construction.md` (LPN-DDR-003 v0.1, Draft): the eleven changes below, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `bom/bom.csv`: lines 17 (controller boards and fixings) and 18 (head internal plate) added; lines 15 and 16 repriced; specifications updated. `bom/bom-notes.md` updated.
- Calculations rerun: LPN-CAL-001 v0.3 (mass, cost and R16 against the value-engineering target); `docs/04-calcs/results.csv` regenerated. LPN-PRC-001 v0.5 and LPN-REQ-001 v0.5 updated to match.
- STEP and STL regenerated; general arrangement LPN-DWG-001 bumped to Rev P3; concept media regenerated (`media/hero.png`, `exploded.png`, `cutaway.png`, `flow.png`, `concept-blueprint.*`, `model.glb`).
- `cad/src/build_plan_media.py`: overview, eight making sketches (LPN-DWG-101 to 108), two layouts (base drilling, mains board), eight joint close-ups, eleven step pictures and a wiring diagram.
- `docs/05-build-plan.md` (LPN-BLD-001 v0.1) and `docs/06-design-decisions.md` (LPN-DEC-001 v0.1) written; both added to `trl_evidence`; `design_state: constructable` in `project.yaml`; README links and a "Building the prototype" section added.

### Design changes made for construction (LPN-DDR-003)

1. **P1, board stack.** The supply, relay, surge parts and controller board no longer float: an 80 mm mains board on three 12 mm spacers and an 80 mm controller board on three 30 mm standoffs, clamped by three M3 x 45 screws from under the base. Controller board centre 69.4 mm (was 66).
2. **P2, dome fixing.** Three printed bosses with M3 heat-set inserts, three M3 x 30 screws from under the base, a 1 mm EPDM gasket; the dome body is 71 mm on the gasket, so the controller stays 97 mm tall. The mains board is notched for the bosses.
3. **P3, M12 socket.** Moved from the curved side of the bought base to a flat printed pad on the pole side of the dome, between the boards.
4. **P4, light window.** An 8 mm clear rod sealed through an 8.2 mm hole replaces the open 16 mm window.
5. **P5, antenna.** A flexible strip stuck inside the dome wall replaces the rod on the board, matching BOM line 8.
6. **P6, part envelopes.** Supply 23 x 38 x 18 mm (a real 5 W module size); one standing 20 mm varistor with the thermal fuse.
7. **P7, base.** Six holes on a 60 mm circle between the blades, inside the gasket ring, countersunk from below.
8. **P8, sensor head inside.** Box and 15 mm lid; a printed internal plate on the four box bosses carrying the head board and a 25° radar cradle. Radar centre 34.2 mm below the box top (was 30).
9. **P9, ports and gland.** Ports through the lid with nuts inside and plug-in leads; an M16 cable gland on the side wall.
10. **P10, bracket.** A folded 2 mm aluminium channel 110 mm long (the concept block was 130 mm, longer than the box), rubber strips on the flanges, band slots; the bands pass over the arm, through the slots and across the web; four M4 screws with sealing washers into the box top.
11. **P11, cable route.** Level out of the dome, past the luminaire, along the top of the arm with ties; about 0.7 m of the 1 m cordset used.

### Key results

- Value-engineering target: USD 150. Estimated cost of the constructable design: USD 143.00 (USD 7.00 under the target); the concept was USD 130.00. `budget_usd` unchanged.
- Mass: controller 0.33 kg (was 0.34 kg); sensor head with clamps and cable 0.42 kg (was 0.45 kg).
- Requirement status unchanged: 0 not met, 4 at risk (R3, R6, R7, R11), 11 met on paper, by design review or under the value-engineering target, 1 not verifiable at TRL 3 (R1).
- Energy, power, inrush, radar, metering, surge and thermal results unchanged.

### Proposed, awaiting Amish

All open items are in the design decisions register (`docs/06-design-decisions.md`): accept LPN-DDR-003 (recommended); the hand-wired mains board for bench work only (A1, recommended); the M12 socket on the dome and the renders (A2, recommended); the first partner (O1, no recommendation); the port pinout with FieldNode; and the 2026-09-26 appearance-model differences.

### Stale media

The photoreal renders `media/render-*.png`, `media/card.png` and `media/social-preview.png`, and the appearance model `cad/src/product_model.py`, still show the concept: the M12 socket on the base, the solid bracket block and the 16 mm window. They are made on Amish's Mac and were not regenerated here. (The render files referenced by the README are not present in this cloud copy.)

### Safety

The design changes do not touch the fail-on relay, the surge stage or the isolation between the mains and 12 V sides. The build plan keeps the first prototype on the bench: unpowered checks, an insulation check, first power only through an isolating transformer and an RCD with the dome on, dummy loads only, and no street installation of the hand-wired board (safety stops S1 to S7).

### Recommended next step

Amish reviews LPN-DDR-003 and the register. TRL 4 (buying parts, building and testing to the plan) stays on hold.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This section is placed at the top to keep this note's newest-first order.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (58 parts: 11 shell, 18 internal, 23 accessory, 6 context), `TITLE` and `RENDER_VIEWS` (hero from the front right looking back along the arm, exploded, and a detail view of the controller alone from the front left). It reuses PARAMS, LV_ANGLES, head_frame() and the reference receptacle from `cad/src/model.py`, in the same local frame; every main dimension and interface (twist-lock base, blades and contacts, gasket, dome, window, M12 socket position, board height, sensor head position and size, radar tilt, port pitch, clamp pitch) is as model.py. It adds:

- Controller base: fillets, grip grooves, a raised orientation mark, tin-plated power blades, gold low-voltage pads, a separate rubber gasket, and a hex M12 panel socket with a knurled plug and overmold.
- Dome: filleted top and foot, a teal accent band, a raised label with print, and a clear window over the light pipe.
- Controller internals in the model.py envelopes: surge carrier with two varistors and the thermal fuse; encapsulated supply with a label; fail-on relay with a label; metering carrier and IC; controller board with the shielded radio module, dimming stage and clock ICs, the supercapacitor with a sleeve band, the antenna, the light pipe and the light sensor.
- Sensor head: filleted housing with a parting line to a 15 mm lid (face down), a dark radar-transparent window on the +X face with a teal accent line, a label, four lid screws, the cable gland on the +Y side, the tilted radar module with patch antennas and front-end IC, the head board and components, two M12 expansion sockets with caps (one teal), a folded bracket with bolts, and two band clamps with rubber liners and worm housings.
- M12 cable along the arm with two cable ties.
- Context (existing street furniture, not in the BOM): a compact LED luminaire head with heat-sink fins and lens, the receptacle from model.py, and a 500 mm section of the lamp arm.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files.

### Differences from model.py (Proposed, awaiting Amish)

1. **Luminaire head.** concept_media.py uses a 650 x 320 mm cobra head; the appearance model uses a compact 390 x 250 mm LED head with fins and a neck round the arm, so the 94 mm controller is not lost in the hero render. The receptacle position and height are unchanged. Proposed, awaiting Amish. Recommendation: accept for the product renders only; the concept media and drawing keep the reference head.
2. **M12 cable route.** model.py runs the cable diagonally from the socket face; here it leaves straight through the plug, drops to the arm, and wraps diagonally round to the +Y side before the drop to the head gland, instead of right-angle steps. The socket, gland side and end points are unchanged. Proposed, awaiting Amish. Recommendation: accept; the route is not fixed at TRL 3.
3. **Band clamps.** model.py shows each clamp as one 5 mm by 20 mm ring. The appearance model splits it into a 1.5 mm rubber liner (20 mm wide) and a 1.5 mm stainless band (14 mm wide) with a worm housing, as BOM line 15 describes. The outer radius is 2 mm smaller than the model.py envelope. Proposed, awaiting Amish. Recommendation: accept.
4. **Bracket.** model.py shows a solid 130 x 30 x 15 mm block; the appearance model is a folded channel with saddles under the clamps and four bolts, inside the same envelope. Proposed, awaiting Amish. Recommendation: accept, matching "folded aluminum bracket" on BOM line 15.
5. **Added appearance details.** Grip grooves, orientation mark, accent band and labels, the M12 plug, port caps and cable ties are not separate BOM lines; they fall under BOM lines 1, 2, 10, 14 and 16. No new BOM lines are implied. No lit indicator was added, because the design has none. Proposed, awaiting Amish. Recommendation: accept.
6. **Render groups.** The sensor head, bracket, clamps, plug and cable are in the "accessory" group so the detail view shows the controller alone. Rendering choice only.

### Status

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. model.py, the BOM and the other documents were not edited.

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to fix the weaker sources. README changes only; no controlled document changed.

| Where | Old source | New source |
| --- | --- | --- |
| What sparked the idea (Detroit relighting) | The Detroit News, 2016 | [US Department of Energy, Detroit street lighting report](https://www.energy.gov/eere/ssl/articles/detroit-street-lighting-report) and [Michigan Public, 2016](https://www.michiganpublic.org/news/2016-12-16/detroit-celebrates-65-000-new-led-streetlights) |
| What sparked the idea (2019 lawsuit) | WXYZ Detroit, 2019 | [Michigan Public, 2019](https://www.michiganpublic.org/law/2019-05-07/some-of-detroits-new-led-streetlights-are-burning-out-city-sues-manufacturer); the unverified "excessive number of calls" detail was removed, and "40 % dark" became the DOE figure of more than half of 88,000 lights out by mid-2013 |
| Country row: United States | LA Bureau of Street Lighting (link redirects, could not be verified) | Los Angeles figure removed; row now cites [NYC DOT](https://www.nyc.gov/html/dot/html/infrastructure/streetlights.shtml) and [DALI Alliance](https://www.dali-alliance.org/d4i/) |
| Country row: India and South Asia | None | Replaced by India, citing [PIB, 2024](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2040102&reg=48&lang=2) (Street Lighting National Programme) |
| Country row: Sub-Saharan Africa | None | Replaced by Philippines (Quezon City), citing the [World Bank](https://blogs.worldbank.org/en/energy/led-street-lighting-unburdening-our-cities) and its [case study](https://documents.worldbank.org/curated/en/842031477930270833/) |
| Country row: Latin America | None | Replaced by Brazil (Belo Horizonte PPP), citing [ESMAP](https://www.esmap.org/node/57541) |

INSPIRATIONS.md line for LampNode updated to the new sources. No verified source for an African example was found within this session's search budget, so the region table no longer has an African row; worth adding one when a primary source is found.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every LampNode item with a recommendation is now **decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (LPN-DDR-002 v0.1). LPN-DDR-001 moved to v0.2 with the new status on D1 to D10 and O2 to O8.

### Decisions applied and what changed

- **D1 to D10** (socket, radar, head link, LoRaWAN, 0 to 10 V, fail-on relay, hosted power policy, default output, mains range, TALQ in CityTwin): decided. These were already built into the TRL 3 design, so only the status wording changed.
- **O2, R7 shortfall:** option (c). R7 stays at 35 % with the reference profile; the risk is accepted until real traffic counts exist. Numbers unchanged (34.1 to 36.4 %, at risk).
- **O3, R13 at high temperature:** option (a), firmware limits the two ports to 2.5 W in total above 50 °C inside the dome (no 10 W supply). 12 V peak against derated supply: before 3.90 W against 3.55 W at 65 °C (at risk); after 3.40 W against 3.57 W at 64.3 °C, margin 0.17 W (met on paper). R13 restated in LPN-REQ-001 v0.4; limited case added to `docs/04-calcs/sizing.py` and LPN-CAL-001 v0.2 section 11; firmware rule added to LPN-PRC-001 v0.4; drawing note changed, so LPN-DWG-001 moved from Rev P1 to P2 (geometry unchanged). No BOM change.
- **O4 to O7** (TCXO clock, 80 A inrush normally closed relay with zero-cross closing, 385 V varistor with TVS diodes and no gas discharge tube, charge-pump coil drive, two-signal day logic, I/Q radar): confirmed. Already in `bom/bom.csv`; wording updated in `bom/bom-notes.md`, LPN-PRC-001 and LPN-CAL-001. Checks on real parts (driver inrush, surge, fail-on behavior) are TRL 4 work, decided but on hold.
- **O8, 5-pole M12 ports:** confirmed; pinout is a cross-repo action with FieldNode.
- Budget: no recommendation touched it. `budget_usd` stays at 150; BOM $130.00. Pitch and problem unchanged.
- Documents bumped: LPN-DDR-001 v0.2, LPN-REQ-001 v0.4, LPN-PRC-001 v0.4, LPN-PRB-001 v0.4 (status wording), LPN-CAL-001 v0.2. README concept summary, key components and "What sparked the idea" updated. The new inspiration is Detroit: 40 % of its streetlights were dark before the 2014 to 2016 relighting, and in 2019 the city sued over about 20,000 early-failing LED fixtures first noticed through resident calls.
- All generated files re-rendered for the domain change (docs PDFs, LPN-DWG-001, all of `media/`), and model, sheet, media and CAL scripts re-run.

### Requirement status now (LPN-CAL-001 v0.2, Table 6)

0 not met, 4 at risk, 11 met on paper or by design review, 1 not verifiable at TRL 3 (before: 5 at risk, 10 met).

| ID | Status | Key number |
| --- | --- | --- |
| R3 Switch the luminaire | At risk | 72 A inrush per 100 W driver at random closing; about 20 A with zero-cross closing |
| R6 Detect presence | At risk | 36 dB signal to noise at 15 m; rain, trees and clutter need a field trial |
| R7 Save energy | At risk (accepted by Amish) | 34.1 to 36.4 % against 35 % |
| R11 Environment | At risk | 63 to 65 °C inside at 45 °C in sun against 70 °C; IP66 and surge need tests |
| R1 Fit the socket | Not verifiable at TRL 3 | Representative base only |
| R13 Host other sensors | Met on paper (firmware port limit) | 3.40 W peak against 3.57 W at 64 °C |
| R2, R4, R5, R8, R9, R10, R12, R14, R15, R16 | Met on paper or by design review | Unchanged from the TRL 3 session |

### Still awaiting Amish

1. **O1, first partner** (city, utility or campus) and region for co-design. No recommendation was made, so no choice is recorded.

### Cross-repo actions

Recorded here only; no other repo was edited.

- **FieldNode:** agree the 5-pole M12 port pinout (FieldNode O2) and the port supply voltage (FieldNode 3.3, 5 or 12 V at build; LampNode 12 V only).
- **AirStreet and NoiseMap:** mention LampNode 12 V ports as an optional power source, FieldNode solar staying the default (D7). Hosted sensors must accept 2.5 W total on hot days.
- **CityTwin:** add a TALQ bridge to CityTwin scope (D10).

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` unchanged. No part selection against datasheets, bench build, test, firmware beyond the documented rule, or purchasing was started.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed LampNode's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Nothing is recorded as decided or approved by him. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (LPN-DDR-001 v0.1, status proposed): ten items adopted as recommended for TRL 3 (D1 to D10), open for Amish's review, and eight left open (O1 to O8).
- `docs/04-calcs/01-sizing.md` (LPN-CAL-001 v0.1), `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: night hours and energy, self-consumption, relay inrush and zero-cross closing, 0 to 10 V output, clock drift, radar geometry, signal and Doppler, metering error budget, LoRaWAN airtime and last gasp, surge energy, dome temperature in sun, hosted power, mass and cost, with a status for every requirement (Table 6). The script imports the model, reads the BOM and `project.yaml`, and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model of the controller (base with three blades and four low-voltage contacts, gasket, dome with window, surge stage, supply, relay, metering, board with supercapacitor, antenna, light pipe, M12 port) and the sensor head (enclosure, tilted radar, board, two ports, band clamps and bracket, cable), with the receptacle and a length of arm as grey reference parts. Exports `cad/step/` and `cad/stl/` for `lampnode-assembly`, `lampnode-controller`, `lampnode-sensor-head` and `lampnode-installed-reference`; the clash check finds none.
- `cad/src/sheets.py` and `cad/drawings/LPN-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:5, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". LPN-DWG-001 was free because the concept blueprint is LPN-DWG-010.
- `bom/bom.csv` (16 lines, every line priced with a supplier or supplier type, $130.00 against the $150 budget) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model. All of `media/` was re-rendered (hero, blueprint, cutaway, exploded, flow, `model.glb`, `viewer.html`) and every image checked; temporary `media/_views*` folders deleted. The controller internals were rearranged so the cutaway shows the surge stage and metering.
- LPN-PRB-001, LPN-PRC-001 and LPN-REQ-001 revised to v0.3 (R2, R4, R13 and R15 redefined per D9, D5, D7 and D10). `README.md` (TRL badge, links, TRL 3 summary, key components, safety) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. Pitch, problem and `budget_usd` unchanged. PDFs rebuilt in `docs/pdf/`.

### Requirement status (LPN-CAL-001, Table 6)

0 not met, 5 at risk, 10 met on paper or by design review, 1 not verifiable at TRL 3.

| ID | Status | Key number |
| --- | --- | --- |
| R3 Switch the luminaire | At risk | 72 A inrush per 100 W driver at random closing, 289 A for four; about 20 A with zero-cross closing; a normally closed relay rated 80 A inrush still to be found |
| R6 Detect presence | At risk | Beam covers 7.5 to 47.9 m; 36 dB signal to noise at 15 m; 0.63 s to full; rain, trees and clutter need a field trial |
| R7 Save energy | At risk | 36.4 % with an ideal driver, 34.1 % with the dimmed driver model, target 35 % |
| R11 Environment | At risk | 63 to 65 °C inside at 45 °C in sun against a 70 °C rating; 118 J in the varistor at 5 kA; IP66 and surge need tests |
| R13 Host other sensors | At risk | 3.90 W peak against about 3.55 W from the 5 W supply at 65 °C |
| R1 Fit the socket | Not verifiable at TRL 3 | Representative base only |
| R2, R4, R9, R12, R14, R15 | Met (design review) | 85 to 305 V supply; 2.44 mV dimming steps; 1.32 J stored for a 0.144 J last gasp; toggling coil drive; 25.7 s airtime a day at SF9 |
| R5, R8, R10 | Met on paper | 9.1 s drift in 30 days with the TCXO clock; 1.65 % metering error with a one-point calibration; 0.68 W average |
| R16 Affordable | Met | $130.00 against $150 |

Corrections to TRL 2 numbers: lit hours 4,100 to 4,323 h a year at 40° N; photocell energy 410 to 432 kWh; presence saving about 41 % to 34.1 to 36.4 %; schedule-only saving 27 % to 25.0 %; self-consumption 0.6 to 0.68 W (coil 0.40 W, not 0.24 W); airtime 0.2 s to 267 ms per message and 20 to 25.7 s a day; controller mass 0.25 to 0.34 kg; parts $124 to $130; payback 3 to 7 years to 3.5 to 8.8 years. The TRL 2 plan to calibrate metering "possibly with CalRig" does not work: CalRig is a climate chamber for air sensors; a bench power meter is needed.

Design changes found by the calculations (engineering proposals, in the BOM, awaiting Amish's confirmation): TCXO clock (a plain crystal drifts 160 s in a cold month against 2 min); normally closed relay rated for 80 A inrush, closed at the zero crossing; 385 V class varistor with TVS diodes and no gas discharge tube (the socket has no earth contact); charge-pump coil drive and a day decision that needs both clock and light sensor; I/Q radar to reject rain; 5-pole M12 ports to match FieldNode.

### Decisions recorded (LPN-DDR-001)

*Status update, 2026-09-25: every item below that carries a recommendation is now decided by Amish, 2026-09-25: go with recommendation (LPN-DDR-002). Only the first partner (O1, item 11 at TRL 2) remains proposed, awaiting Amish.*

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 ANSI C136.41 socket first, Zhaga Book 18 later; D2 24 GHz Doppler radar, schedule-only as a firmware mode; D3 cable to a head under the arm; D4 LoRaWAN on the STM32WL-class module; D5 0 to 10 V only, D4i if a partner needs it; D6 fail-on normally closed relay; D7 siblings stay on FieldNode solar, LampNode power optional, hosted sensors on cabinet-switched feeders bring storage; D8 ships at photocell-equivalent full output; D9 120 to 277 V now, 347 V and 480 V later; D10 TALQ bridge is CityTwin scope. No budget, pitch or problem change was recommended, so none was made.

### Still awaiting Amish

*Status update, 2026-09-25: every item below that carries a recommendation is now decided by Amish, 2026-09-25: go with recommendation (LPN-DDR-002). Only the first partner (O1, item 11 at TRL 2) remains proposed, awaiting Amish.*

1. **O1, first partner** (city, utility or campus) and region. No recommendation was made.
2. **O2, R7 shortfall.** Options: relax R7 to 30 %; move the reference floor start to 21:00; or keep both and accept the risk until traffic counts exist. Recommendation: keep both and accept the risk. Not applied.
3. **O3, R13 at high temperature.** Options: firmware limits the ports to 2.5 W above 50 °C inside, or a 10 W supply (about +$3). Recommendation: the firmware limit. Not applied.
4. **O4 to O7, engineering proposals** listed above (TCXO clock, relay and zero-cross closing, surge stage, coil drive and day logic, I/Q radar). Applied in the BOM and precis for TRL 3 work, awaiting his confirmation.
5. **O8, 5-pole M12 ports** to match FieldNode; the pinout itself waits on FieldNode O2.

### Cross-repo consistency

- FieldNode (FND-DDR-001): STM32WL-class module, LoRaWAN, 15 min interval and TwinKit first all match. FieldNode uses two M12 5-pin ports; LampNode's 4-pole ports were changed to 5-pole to match (O8). Conflict noted, FieldNode not edited: FieldNode ports carry one of 3.3, 5 or 12 V chosen at build, while LampNode ports carry 12 V only, so a FieldNode-pinout sensor built for 3.3 or 5 V needs its own regulator on a LampNode pole. FieldNode's 100 to 115 mW sensor allowance is far below LampNode's 3 W, so no conflict there.
- TwinKit (TWK REVIEW): 8-channel LoRaWAN gateway; LampNode's 96 messages a day at 267 ms (SF9) are a light load. TwinKit's adaptive data rate proposal suits LampNode too. No conflict.
- CalRig (CLR REVIEW): a climate chamber for air sensors; it cannot calibrate power metering. LampNode no longer cites it.
- CityTwin: D10 puts a TALQ bridge in CityTwin scope, but CityTwin's review does not mention TALQ. Noted here; CityTwin not edited.
- AirStreet and NoiseMap stay on FieldNode solar (D7); NoiseMap's review already notes LampNode power as an option. No other repo was edited.

### Safety concerns

- Mains up to 277 V nominal (305 V maximum) in the receptacle; the socket has no earth contact, so LampNode clamps only line to neutral. The varistor must be thermally protected and fused; a failing varistor is a fire risk on the luminaire top.
- Fail-on behavior depends on the coil drive dropping out when the controller stops, and on each driver giving full output with an open 0 to 10 V line. Both need checking on real parts.
- Relay contacts welded by inrush would leave a lamp burning by day; the day-burner check must report it.
- About 65 °C inside the dome in 45 °C sun leaves little margin for the supercapacitor and the supply.
- Work at height beside traffic; radio compliance for the 24 GHz radar and the sub-GHz module; privacy (motion, speed and direction only).

### Gaps and notes

- Citations: the TRL 2 note flagged no unchecked citations (it left out figures from pages that could not be read). No WebFetch checks were run this session and no figure was added to the README. ANSI C136.2 surge levels and ANSI C136.10 and C136.41 dimensions were not read; the model's base geometry is representative.
- Assumptions only tests can settle: driver inrush and dimmed efficiency, radar false triggers, luminaire top temperature, supply derating, relay release-time spread.
- The kit's cutaway cutter is centered on X = Z = 0. The model's local frame already puts the controller at the origin, so no shift is needed any more; the street-scene hero places the model on the pole with a transform. The metering part (item 6) is small and sits under its callout in the exploded view.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `electronics/` and `firmware/` are empty. No test, build, purchasing or firmware material was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. The next step is Amish's review of LPN-DDR-001 (D1 to D10), a choice on O1 to O3 and confirmation of the engineering proposals O4 to O8, plus agreement of the port pinout with FieldNode. For the record only, TRL 4 would need: named parts with datasheets (normally closed relay with its inrush rating, supply with its derating curve, radar module, metering IC); a bench build of the controller on a donor luminaire; a lab test report (TST, `environment: lab`) covering fail-on behavior, zero-cross inrush, metering accuracy against a bench meter, dome temperature under a sun lamp and self-consumption; and build log entries. None of this has been started.

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (LPN-PRB-001 v0.2): problem with cited facts, users, operating environment, constraints, out of scope, prior work (ANSI C136.41, Zhaga Book 18, D4i, TALQ), open questions; co-design checklist kept.
- `docs/03-requirements.md` (LPN-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, verification and a TRL 2 status column, a reference case and assumptions.
- `docs/02-concept.md` (LPN-PRC-001 v0.2): how it works, 15 numbered components, annual energy, self-consumption, radio airtime, presence geometry, cost and payback, proposed design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of the twist-lock controller (base, dome, surge stage, power supply, relay, metering, controller board, antenna, light pipe) and the sensor head under the arm (enclosure, radar, board, two ports, clamps, cable), with the luminaire, arm and 7.8 m pole as grey context.
- `media/`: `hero.png` (street scene with the 1.75 m figure and a labeled close-up inset), `concept-blueprint` (PNG, PDF, SVG), `exploded.png` and `cutaway.png` with callouts matching the BOM, `flow.png` (annual energy, estimates), `model.glb` and `viewer.html` (controller, sensor head and luminaire head).
- `bom/bom.csv`: 16 lines with indicative USD prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; Concept rationale, Burning platform, Where it could be used (6 industries, 6 regions), What sparked the idea, Concept and Key components expanded; Safety extended.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` unchanged: the pitch and problem still match the numbers found.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Annual energy, 100 W luminaire, photocell | about 410 kWh | |
| Schedule only (50 % from 23:00 to 05:00) | about 300 kWh (about 27 % saving) | |
| Schedule and presence (30 % floor 22:00 to 06:00), controller included | about 243 kWh (about 41 % saving, about 167 kWh per year) | R7 met |
| Controller self-consumption | about 0.6 W (0.8 W used with margin) | R10 met |
| LoRaWAN airtime, 96 status messages per day | about 20 s per day, about 0.02 % | R15 |
| Radar beam center on the ground | about 16.5 m along the street from 7.7 m height at 25° tilt | R6 at risk |
| Parts cost, controller and one sensor head | about $124 (controller about $62, head about $56) | R16 met, $150 budget |
| Payback on parts at $0.10 to $0.25 per kWh | about 3 to 7 years, before labor | |
| Mass | controller about 0.25 kg; head with clamps about 0.45 kg | |

Requirements not met or at risk:

- **R2 not met** for 347 V and 480 V lighting circuits (120 to 277 V only).
- **R4 partly met:** 0 to 10 V only; no DALI-2 D4i in the base design.
- **R6 at risk:** presence detection range and false triggers from 7.7 m are unverified.
- **R13 not met in daytime** on cabinet-switched feeders: hosted sensors lose power when the lamp circuit is off.
- **R15 partly met:** open LoRaWAN and payload, but no TALQ bridge.
- **R8 and R11 unverified:** metering accuracy at low dimmed power, and the surge level.

### Proposed, awaiting Amish

*Status update, 2026-09-25: every item below that carries a recommendation is now decided by Amish, 2026-09-25: go with recommendation (LPN-DDR-002). Only the first partner (O1, item 11 at TRL 2) remains proposed, awaiting Amish.*

1. **Socket.** Options: (a) ANSI C136.41 7-contact; (b) Zhaga Book 18; (c) both from the start. Recommendation: (a) first for retrofits, (b) as a later variant.
2. **Presence sensor.** Options: (a) 24 GHz Doppler radar; (b) PIR; (c) no presence, schedule only. Recommendation: (a), keeping (c) as a firmware mode.
3. **Sensor head link.** Options: (a) cable from the controller to a head under the arm; (b) Zhaga bottom-socket module; (c) solar FieldNode head linked by radio. Recommendation: (a).
4. **Radio.** Options: (a) LoRaWAN on the FieldNode STM32WL-class module; (b) an IEEE 802.15.4 mesh such as Wi-SUN. Recommendation: (a), for portfolio consistency with FieldNode and TwinKit.
5. **Dimming interface.** Options: (a) 0 to 10 V only; (b) 0 to 10 V plus DALI-2 D4i on the auxiliary contacts. Recommendation: (a) now, (b) at TRL 3 if a partner's stock needs it.
6. **Fail-on relay** (normally closed, coil energized in daytime), rather than a latching relay. Recommendation: fail-on, accepting about 0.13 W average coil power.
7. **Hosted sensor power.** LampNode would offer 12 V SELV, 3 W, from the luminaire socket. AirStreet and NoiseMap currently state that they run only on FieldNode solar and never tap pole mains. Options: (a) keep siblings on FieldNode, with LampNode power as an option for them; (b) make LampNode the default host; (c) drop the power ports and host by radio only. Recommendation: (a), and coordinate the wording with those repos rather than changing them here.
8. **Default policy.** Ship with photocell-equivalent full output; the 30 % floor profile is for estimates only. Recommendation: yes, the road owner sets any dimming.
9. **Mains range.** 120 to 277 V now; a 347 V and 480 V variant later. Recommendation: defer until a partner needs it.
10. **Interoperability.** Add a TALQ bridge in TwinKit or CityTwin at TRL 3, or leave it to users. Recommendation: note it as TRL 3 scope for CityTwin.
11. **First partner** (city, utility or campus) and region for co-design.

### Safety concerns

- Mains voltage (up to 277 V AC, 305 V maximum) in the receptacle; surges on long feeders; fire risk from a failed surge stage.
- Work at height beside traffic for fitting and removal.
- A failed controller or bad setting could leave a street dark; fail-on behavior must be checked on each driver model, and light levels stay with the road owner.
- Radio compliance for the 24 GHz radar and sub-GHz LoRa modules.
- Privacy: motion only, no images or audio; check local data protection law.

### Problems and notes

- The kit's `cutaway_parts()` builds its cutter around X = Z = 0, so parts 7.9 m up a pole were missed. `concept_media.py` shifts the parts to the origin before rendering. A kit fix may help other pole-mounted repos (suggestion only; `.kit/` not changed).
- `render_all()` frames the parts it is given, so the street-scene hero is composed separately in `make_hero()`; the cutaway is re-rendered with callouts.
- Sources: pages that could not be read this session (for example a Europe PMC query, which was rate limited, and several US DOE and ESMAP pages that returned errors) were left out. The India, sub-Saharan Africa and Latin America rows in the README carry no cited figures for that reason.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1, 2, 3 and 7. If approved, run `/advance-trl3` to check the energy, radar range, relay inrush, surge and thermal estimates by calculation and produce the parametric model and drawing sheet.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: open-decision recommendations approved

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation for every open decision in the design decisions register. 6 decisions were recorded: each moved to Decisions made, dated 2026-10-02, with the approved recommendation and its record. trl stays 3; no build or test work was done, and the CAD model, BOM quantities and prices, and pictures were not changed.

### Documents changed

- `docs/06-design-decisions.md` (LPN-DEC-001 v0.2): the six open decisions moved to Decisions made; Open decisions now reads none; tables renumbered
- `docs/decisions/0003-design-for-construction.md` (LPN-DDR-003 v0.2): status accepted with Amish's words; A1 accepted on strict bench-only terms, A2 accepted; safety note updated
- `docs/decisions/0001-trl2-review-decisions.md` (LPN-DDR-001 v0.3): O1 (first partner and region) decided
- `docs/decisions/0002-recommendations-accepted.md` (LPN-DDR-002 v0.2): O1 decided; the FieldNode cross-repo action records the pinout LampNode proposes
- `docs/03-requirements.md` (LPN-REQ-001 v0.6): R13 states the pinout proposed to FieldNode; no status changed
- `docs/02-concept.md` (LPN-PRC-001 v0.6): expansion port pinout, first partner and band stated as decided
- `docs/01-problem.md` (LPN-PRB-001 v0.5): first partner and port pinout stated as decided
- `docs/05-build-plan.md` (LPN-BLD-001 v0.2): antenna band set to 915 MHz for the US partner; no design change
- `bom/bom-notes.md`: 915 MHz antenna and US915 band, and the port pinout, noted; no quantity or price changed
- PDFs regenerated with `python3 .kit/render.py`; superseded PDF versions removed by the render.

### Follow-up actions to carry approved decisions into the design

1. Decision 3 (pictures): Update `cad/src/product_model.py`, the photoreal renders, `media/card.png` and `media/social-preview.png` with the M12 socket on the dome pad (on Amish's Mac)
2. Decision 6 (pictures): When the renders are next made, redraw appearance items 2, 3 and 4 (cable route, band clamps, folded bracket with EPDM strips) to the constructable design of P10 and P11; items 1, 5 and 6 stay as render-only details
3. Decision 4 (bom): Change the description of BOM line 8 from "868 or 915 MHz" to a 915 MHz antenna, and set the LoRaWAN module order for US915
4. Decision 4 (calcs): Recheck the time on air and duty limits in LPN-CAL-001 for the US915 band (FCC dwell time of 400 ms per channel) instead of the EU868 duty cycle
5. Decision 5 (drawings): Mark the port pinout (pin 1 supply, pin 3 ground, pins 2 and 4 RS-485, pin 5 wake) on the block-level wiring diagram (build plan Figure 8) and the head board making sketch
6. Decision 5 (docs): Propose the pinout to FieldNode (its O2) in the FieldNode repo; it was not edited from here

### Points found in the review

- The render files referenced by the README are not present in this cloud copy, and the existing renders still show the M12 socket on the base, the solid bracket and the 16 mm window.
