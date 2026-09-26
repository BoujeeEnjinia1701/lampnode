# Review note: LampNode

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
