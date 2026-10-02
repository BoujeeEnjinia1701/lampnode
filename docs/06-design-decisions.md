---
doc_id: LPN-DEC-001
title: LampNode design decisions register
project: LampNode
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions, items to confirm, value engineering and decisions made; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Amish approved the recommendations for all six open decisions on 2026-10-02 (LPN-DDR-003 accepted); moved to decisions made; tables renumbered'
---

# LampNode design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 1. Assumed sizes and ratings to check against the real parts.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The base kit has solid material or bosses at the six screw positions on the 60 mm circle, and its blades have crimp or solder terminals inside | The dome and board stack screw through it | LPN-DDR-003, P2, P7 |
| 2 | The head box's four internal bosses are 94 x 54 mm apart and 6 mm long, and its lid is 15 mm deep | They set the internal plate holes and the radar height | LPN-DDR-003, P8 |
| 3 | The supply module fits 23 x 38 x 18 mm and the relay 18 x 24 x 20 mm, with an inrush rating of 80 A or more | The mains board layout and the notches depend on these sizes; R3 needs the rating | LPN-DDR-003, P6; LPN-CAL-001 |
| 4 | The M12 panel socket's thread suits a 6 mm wall and a 16.2 mm hole | The dome pad is 6 mm thick | LPN-DDR-003, P3 |
| 5 | The radar module fits 50 x 44 mm and has two mounting holes | The cradle holes are drilled to suit | LPN-DDR-003, P8 |
| 6 | The band clamp size: the band loop is about 190 mm for a 50 mm arm, 220 mm for a 60 mm arm and 280 mm for an 80 mm arm (worm-drive clamps of about 60 to 90 mm nominal range) | One clamp size may not cover 50 to 80 mm arms | LPN-DDR-003, P10 |
| 7 | The flexible antenna's datasheet allows sticking it to 3 mm of plastic | Range and tuning | LPN-DDR-003, P5 |
| 8 | The driver model's inrush and its open-line dimming behaviour (full output with the 0 to 10 V line open) | Fail-on behaviour (R12) and relay sizing (R3) | LPN-CAL-001; LPN-PRC-001 |

## Value engineering

Value-engineering target: USD 150 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 143.00 (USD 7.00 under the target). Main cost drivers and savings worth trying:

- The largest lines are the controller board with its LoRaWAN module, clock and coil drive (USD 25), the 24 GHz radar (USD 18), the twist-lock base kit (USD 10), the M12 socket and cordset (USD 10), and the supply and head board (USD 8 each).
- Making the design constructable added line 17, the controller boards and fixings (USD 7), and line 18, the printed head plate (USD 4), and raised lines 15 and 16 by USD 1 each; the total rose from USD 130 to USD 143.
- Savings worth trying: one laid-out board carrying both the mains and controller sides would replace two prototype boards, the harness and most of line 17; a cable glanded straight into the dome would save the M12 socket and plug (about USD 6) but make the head harder to swap; radar module prices fall steeply above prototype quantities.

## Decisions made

*Table 2. Decisions made, with Amish's words where recorded.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: ANSI C136.41 socket first, 24 GHz Doppler radar, cable to a head under the arm, LoRaWAN on the STM32WL-class module, 0 to 10 V dimming, fail-on normally closed relay, sibling sensors on FieldNode solar, photocell-equivalent default, 120 to 277 V, TALQ bridge in CityTwin | Amish: "i accept all your recommendations, go with them across all repos." | LPN-DDR-001, LPN-DDR-002 |
| 2026-09-25 | R7 kept at 35 % with the reference profile and its risk accepted (O2); firmware port limit of 2.5 W above 50 °C inside (O3) | Amish, same instruction | LPN-DDR-002 |
| 2026-09-25 | Engineering changes O4 to O8: TCXO clock, 80 A inrush relay with zero-cross closing, 385 V surge stage without a gas discharge tube, charge-pump coil drive and two-signal day logic, I/Q radar, 5-pole M12 ports | Amish, same instruction | LPN-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | LPN-DDR-003 (accepted on 2026-10-02, below) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; LPN-CAL-001 v0.3 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | LPN-DDR-003 |
| 2026-10-02 | Mains board of the first prototype: hand-wired boards (option a) on strict terms: bench only, powered only through an isolating transformer and an RCD with the dome on, the 6 mm gap between mains and low voltage checked before first power, and a laid-out board before any outdoor or luminaire-powered test | Amish: "i approve your recommendations for all 555 open decisions." | LPN-DDR-003, A1 |
| 2026-10-02 | M12 socket on the dome pad accepted (option a); the appearance model and renders are to be updated on Amish's Mac | Amish: "i approve your recommendations for all 555 open decisions." | LPN-DDR-003, A2 |
| 2026-10-02 | First co-design partner and region: a US partner on the 915 MHz band; first candidate to approach: a university campus or municipal utility in the Dallas-Fort Worth area that runs LED streetlights with ANSI C136.41 sockets | Amish: "i approve your recommendations for all 555 open decisions." | LPN-DDR-001, O1 |
| 2026-10-02 | Sensor port pinout proposed to FieldNode: pin 1 supply (12 V on LampNode), pin 3 ground, pins 2 and 4 a two-wire RS-485 pair, pin 5 a wake line; hosted sensors accept 5 to 12 V and regulate down themselves | Amish: "i approve your recommendations for all 555 open decisions." | LPN-DDR-002 cross-repo actions; FieldNode O2 |
| 2026-10-02 | Appearance model: items 1, 5 and 6 accepted for the renders only; items 2, 3 and 4 (cable route, band clamps, bracket) are to be redrawn to the constructable design of P10 and P11 when the renders are next made | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, session 2026-09-26 |
