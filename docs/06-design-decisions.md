---
doc_id: LPN-DEC-001
title: LampNode design decisions register
project: LampNode
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions, items to confirm, value engineering and decisions made; budget treated as a value-engineering target
---

# LampNode design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, Proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P11 | Accept as made; or ask for changes item by item | Accept | Every component of the build plan | LPN-DDR-003 |
| 2 | Mains board of the first prototype | (a) hand-wired prototype board, bench work only, laid-out board before any outdoor or luminaire-powered test; (b) lay out the board first | (a) | Mains board (build plan section 3.2) and safety stops | LPN-DDR-003, A1 |
| 3 | M12 socket on the dome pad instead of the base, and the renders that still show it on the base | (a) accept and update the appearance model and renders on Amish's Mac; (b) look for a bought base with a socket boss | (a) | Dome and M12 socket; photoreal renders | LPN-DDR-003, A2 |
| 4 | First co-design partner (city, utility or campus) and region | Any partner Amish chooses | None made | Not part of the TRL 3 build; sets the radio band (868 or 915 MHz antenna and module) and the driver models to test | LPN-DDR-001, O1 |
| 5 | Sensor port pinout of the two expansion ports | Pinout agreed with FieldNode and the adopting teams | None yet | Port lead wiring on the head board | LPN-DDR-002 cross-repo actions; FieldNode O2 |
| 6 | Appearance-model differences recorded for the product renders (compact luminaire head, cable route, split band clamps, folded bracket, added details) | Accept for the renders; or redraw | Accept; items 3 and 4 now match the constructable design | Renders only | `docs/REVIEW.md`, session 2026-09-26 |

## To confirm when parts are bought

*Table 2. Assumed sizes and ratings to check against the real parts.*

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

*Table 3. Decisions made, with Amish's words where recorded.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: ANSI C136.41 socket first, 24 GHz Doppler radar, cable to a head under the arm, LoRaWAN on the STM32WL-class module, 0 to 10 V dimming, fail-on normally closed relay, sibling sensors on FieldNode solar, photocell-equivalent default, 120 to 277 V, TALQ bridge in CityTwin | Amish: "i accept all your recommendations, go with them across all repos." | LPN-DDR-001, LPN-DDR-002 |
| 2026-09-25 | R7 kept at 35 % with the reference profile and its risk accepted (O2); firmware port limit of 2.5 W above 50 °C inside (O3) | Amish, same instruction | LPN-DDR-002 |
| 2026-09-25 | Engineering changes O4 to O8: TCXO clock, 80 A inrush relay with zero-cross closing, 385 V surge stage without a gas discharge tube, charge-pump coil drive and two-signal day logic, I/Q radar, 5-pole M12 ports | Amish, same instruction | LPN-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | LPN-DDR-003 (Draft, open for his review) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; LPN-CAL-001 v0.3 |
