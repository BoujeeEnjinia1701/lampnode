# Review note: LampNode

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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 ANSI C136.41 socket first, Zhaga Book 18 later; D2 24 GHz Doppler radar, schedule-only as a firmware mode; D3 cable to a head under the arm; D4 LoRaWAN on the STM32WL-class module; D5 0 to 10 V only, D4i if a partner needs it; D6 fail-on normally closed relay; D7 siblings stay on FieldNode solar, LampNode power optional, hosted sensors on cabinet-switched feeders bring storage; D8 ships at photocell-equivalent full output; D9 120 to 277 V now, 347 V and 480 V later; D10 TALQ bridge is CityTwin scope. No budget, pitch or problem change was recommended, so none was made.

### Still awaiting Amish

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
