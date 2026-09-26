---
doc_id: LPN-DDR-001
title: LampNode TRL 2 review decisions
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
  change: Record the TRL 2 review recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, open for his review, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items D1 to D10 are adopted for TRL 3 work pending Amish's review; items O1 to O8 remain proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed eleven LampNode design questions as "Proposed, awaiting Amish", ten of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the LampNode items one by one. Under that instruction, every item that carried a recommendation is adopted as recommended for TRL 3, open for his review. Items without a recommendation stay open. Nothing here is decided or approved by Amish. TRL 4 is on hold by his instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and LPN-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Status and recommendation adopted | Where it now lives |
| --- | --- | --- | --- |
| D1 | Socket | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. ANSI C136.41 7-contact first, for retrofits; Zhaga Book 18 as a later variant | LPN-PRC-001 v0.3, LPN-REQ-001 R1, `cad/src/model.py` |
| D2 | Presence sensor | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. 24 GHz Doppler radar, with schedule-only operation kept as a firmware mode | LPN-PRC-001 v0.3, LPN-REQ-001 R6 |
| D3 | Sensor head link | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Cable from the controller to a head clamped under the arm | LPN-PRC-001 v0.3, `cad/src/model.py`, LPN-DWG-001 |
| D4 | Radio | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. LoRaWAN on the STM32WL-class module shared with FieldNode and TwinKit | LPN-PRC-001 v0.3, LPN-REQ-001 R15 |
| D5 | Dimming interface | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. 0 to 10 V only; DALI-2 D4i on the auxiliary contacts only if a partner's stock needs it. No partner has been named, so D4i is not in the TRL 3 design | LPN-REQ-001 R4 (redefined) |
| D6 | Fail-on relay | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Normally closed contact, coil energized in daytime. LPN-CAL-001 puts the average coil power at 0.203 W, not about 0.13 W | LPN-PRC-001 v0.3, LPN-CAL-001 section 3 |
| D7 | Hosted sensor power | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Sibling sensors (AirStreet, NoiseMap) stay on FieldNode solar; LampNode's 12 V ports are an option for them. Hosted sensors that need power around the clock on cabinet-switched feeders bring their own storage. Wording in sibling repos is to be coordinated, not changed here | LPN-REQ-001 R13 (redefined) |
| D8 | Default policy | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Ships with photocell-equivalent full output; any dimming profile is set by the road owner; the reference profile is for estimates only | LPN-PRC-001 v0.3, LPN-REQ-001 assumptions |
| D9 | Mains range | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. 120 to 277 V now; a 347 V and 480 V variant deferred until a partner needs it | LPN-REQ-001 R2 (redefined) |
| D10 | Interoperability | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. A TALQ bridge is CityTwin scope, not a LampNode requirement | LPN-REQ-001 R15 (redefined) |

No budget change, and no reworded pitch or problem line, was recommended at TRL 2, so `budget_usd` (150), the pitch and the problem in `project.yaml` and `README.md` are unchanged.

### Items that remain open

*Table 2. Open items, proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner (city, utility or campus) and region for co-design | Proposed, awaiting Amish. No recommendation was made at TRL 2 |
| O2 | R7 shortfall. LPN-CAL-001 gives 34.1 to 36.4 % against 35 %. Options: (a) relax R7 to 30 % with the reference profile; (b) keep 35 % and move the floor start to 21:00 in the reference profile; (c) keep both and accept R7 at risk until real traffic counts exist. Recommendation: (c), because the road owner sets the profile and the traffic assumption dominates | Proposed, awaiting Amish. Not applied |
| O3 | R13 hosted power at high temperature (3.90 W peak against 3.55 W at 65 °C). Options: (a) firmware limits the ports to 2.5 W above 50 °C inside; (b) a 10 W supply module (about +$3, slightly more no-load loss). Recommendation: (a) | Proposed, awaiting Amish. Not applied |
| O4 | TCXO real-time clock for R5 (+$3) | Engineering proposal from LPN-CAL-001, in `bom/bom.csv` line 7, awaiting Amish's confirmation |
| O5 | Relay: normally closed with an 80 A or better inrush rating, closed at the voltage zero crossing (+$2) | Engineering proposal from LPN-CAL-001, in `bom/bom.csv` line 5, awaiting Amish's confirmation |
| O6 | Surge stage: 385 V class 20 mm varistor line to neutral and TVS diodes on the low-voltage leads, no gas discharge tube, since the socket has no earth contact (+$1) | Engineering proposal from LPN-CAL-001, in `bom/bom.csv` line 3, awaiting Amish's confirmation |
| O7 | Fail-safe logic: a charge-pump coil drive that drops the relay (lamp on) if the controller stops toggling it, and a day decision that needs both the clock and the light sensor; I/Q radar to reject rain | Engineering proposals from LPN-CAL-001, awaiting Amish's confirmation |
| O8 | Expansion ports change from 4-pole to 5-pole M12 to match FieldNode's two M12 5-pin ports (FND-DDR-001 D5); the pinout itself is open at FieldNode (O2 there) | Proposed for consistency, awaiting Amish and FieldNode |

## Consequences

- R2, R4, R13 and R15 are redefined in LPN-REQ-001 v0.3 to match D9, D5, D7 and D10. The TRL 2 "not met" entries for 347 V and 480 V, D4i, daytime hosted power and TALQ become scope notes, not failures.
- The TRL 3 design costs $130.00 against the unchanged $150 budget (LPN-CAL-001 section 13).
- R3, R6, R7, R11 and R13 are at risk on paper and are listed in `docs/REVIEW.md`.
- None of the adopted items is final. Amish may reverse any of them on review.
