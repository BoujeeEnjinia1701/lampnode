---
doc_id: LPN-DDR-002
title: LampNode recommendations accepted
project: LampNode
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all recommendations in LPN-DDR-001 and docs/REVIEW.md, what changed in the repo, and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item with a recommendation is decided by Amish; one item without a recommendation stays open.

## Context

LPN-DDR-001 v0.1 and the TRL 3 session of `docs/REVIEW.md` held ten items adopted for TRL 3 work, open for Amish's review (D1 to D10), and eight open items (O1 to O8), seven of which carried a recommendation or an engineering proposal. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore **decided by Amish, 2026-09-25: go with recommendation**. Where a recommendation offered several options, the recommended option is the decision. Items with no recommendation stay "Proposed, awaiting Amish". TRL 4 remains on hold by Amish's instruction, so decisions that need building, testing or purchasing are recorded but not carried out.

## Decision

*Table 1. Items decided by Amish on 2026-09-25 and what changed in the repo.*

| # | Decision | What changed in the repo |
| --- | --- | --- |
| D1 | ANSI C136.41 7-contact socket first; Zhaga Book 18 as a later variant | Status wording only; the model already uses the C136.41 base |
| D2 | 24 GHz Doppler radar; schedule-only kept as a firmware mode | Status wording only |
| D3 | Cable from the controller to a head clamped under the arm | Status wording only; geometry unchanged |
| D4 | LoRaWAN on the STM32WL-class module shared with FieldNode and TwinKit | Status wording only |
| D5 | 0 to 10 V only; DALI-2 D4i only if a partner's stock needs it | Status wording only; R4 already redefined in LPN-REQ-001 v0.3 |
| D6 | Fail-on, normally closed relay, coil energized in daytime (0.203 W average) | Status wording only |
| D7 | Sibling sensors stay on FieldNode solar; LampNode ports optional for them; hosted sensors on cabinet-switched feeders bring storage | Status wording; wording in AirStreet and NoiseMap listed as a cross-repo action |
| D8 | Ships at photocell-equivalent full output; the road owner sets any dimming | Status wording only |
| D9 | 120 to 277 V now; 347 V and 480 V deferred until a partner needs them | Status wording only; R2 already redefined |
| D10 | A TALQ bridge is CityTwin scope | Status wording; listed as a cross-repo action for CityTwin |
| O2 | R7 shortfall: option (c), keep the 35 % target and the reference profile and accept R7 at risk until real traffic counts exist | R7 target unchanged (35 %); status stays at risk (34.1 to 36.4 %); LPN-REQ-001 v0.4 and LPN-CAL-001 v0.2 note the decision |
| O3 | R13 at high temperature: option (a), firmware limits the two ports to 2.5 W in total when the interior is above 50 °C (no 10 W supply) | R13 target restated in LPN-REQ-001 v0.4; LPN-CAL-001 v0.2 section 11 and `sizing.py` add the limited case: peak 3.90 W against 3.55 W becomes 3.40 W against 3.57 W at 64.3 °C; R13 moves from at risk to met on paper; firmware rule added to LPN-PRC-001 v0.4. No BOM, geometry or drawing change |
| O4 | TCXO real-time clock (+$3) | Confirmed; already in `bom/bom.csv` line 7; wording updated in `bom/bom-notes.md` |
| O5 | Normally closed relay rated 80 A inrush or better, closed at the zero crossing (+$2) | Confirmed; already in `bom/bom.csv` line 5. Checking the rating against real driver inrush is TRL 4 work, decided but on hold |
| O6 | 385 V class varistor and TVS diodes, no gas discharge tube (+$1) | Confirmed; already in `bom/bom.csv` line 3. Surge testing is TRL 4, on hold |
| O7 | Charge-pump coil drive, day decision needing both clock and light sensor, I/Q radar | Confirmed in LPN-PRC-001; firmware beyond a sketch and bench checks are TRL 4, on hold |
| O8 | 5-pole M12 expansion ports to match FieldNode | Confirmed; already in `bom/bom.csv` lines 10 and 14. The pinout is a cross-repo action with FieldNode (its O2) |

No recommendation changed the budget, the pitch or the problem, so `budget_usd` stays at 150 and the pitch and problem in `project.yaml` and `README.md` are unchanged. The BOM total stays at $130.00. `trl` and `trl_target` stay at 3.

## Items still open

*Table 2. Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner (city, utility or campus) and region for co-design | Proposed, awaiting Amish. No recommendation was made |

## Cross-repo actions

These are recorded here and in `docs/REVIEW.md`; no other repo was edited.

- **FieldNode:** agree the 5-pole M12 port pinout (FieldNode O2) and the supply voltage on the ports (FieldNode offers 3.3, 5 or 12 V at build; LampNode offers 12 V only).
- **AirStreet and NoiseMap:** mention LampNode 12 V ports as an optional power source, keeping FieldNode solar as the default (D7).
- **CityTwin:** add a TALQ bridge to CityTwin scope (D10).

## Consequences

- Requirement status: 0 not met, 4 at risk (R3, R6, R7, R11), 11 met on paper or by design review, 1 not verifiable at TRL 3 (R1). Before: 5 at risk and 10 met.
- Hosted sensors must accept 2.5 W in total, not 3 W, on hot days.
- Controlled documents changed: LPN-DDR-001 v0.2, LPN-REQ-001 v0.4, LPN-PRC-001 v0.4, LPN-PRB-001 v0.4, LPN-CAL-001 v0.2.
- TRL 4 work (parts selection against datasheets, bench build, tests, firmware) stays on hold.
