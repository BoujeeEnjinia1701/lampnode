---
doc_id: LPN-REQ-001
title: LampNode requirements
project: LampNode
doc_type: Requirements
version: "0.7"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: R2, R4, R13 and R15 redefined per LPN-DDR-001 (adopted for TRL 3, open for Amish's review); reference case night hours from LPN-CAL-001; status column now gives the TRL 3 result
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: R16 reported against the value-engineering target for the constructable design (LPN-DDR-003)
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'R13 states the port pinout proposed to FieldNode on 2026-10-02 (LPN-DEC-001); no status changed'
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: R15 airtime restated for the US915 band (400 ms dwell limit; status at SF9 or faster); no status changed
---

# LampNode requirements

These are the requirements for the concept at TRL 3. Targets are proposals for review, not yet validated with a lighting authority or users, and will be revised after co-design (see LPN-PRB-001). R2, R4, R13 and R15 were redefined on 2026-09-25 to match the TRL 2 recommendations, which Amish accepted the same day (LPN-DDR-001, LPN-DDR-002). R13 was restated again to include the firmware port limit he decided (LPN-DDR-001 O3), and R7 is kept at 35 % with its risk accepted (O2). The status column gives the result of the TRL 3 calculations in LPN-CAL-001.

The **reference case** used throughout is a 100 W LED cobra-head luminaire with a 0 to 10 V driver, its arm about 7.8 m above a residential street at 40° N, lit from sunset to sunrise: 4,323 h a year, 11.84 h a night on average (LPN-CAL-001; TRL 2 assumed about 4,100 h).

Table 1. Requirements

| ID | Requirement | Target | Verification | TRL 3 status (LPN-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Fit the existing socket | Plugs into an ANSI C136.41 7-contact twist-lock receptacle; replaces a photocontrol with no tools and no luminaire rewiring in 5 min or less at height | Dimensional check against the standard; fit trial on a donor luminaire | Not verifiable at TRL 3: representative base in the model |
| R2 | Mains supply range | 120 to 277 V AC nominal, 50 or 60 Hz, operating from 100 to 305 V. 347 V and 480 V circuits are a later variant, out of scope until a partner needs them (redefined, LPN-DDR-001 D9) | Power supply datasheet; design review | Met (design review): 85 to 305 V supply, 385 V class varistor |
| R3 | Switch the luminaire | Switch LED luminaire loads up to 400 W at 277 V, with a relay rated for the driver's inrush current, for 100,000 or more cycles | Relay datasheet against driver inrush data | **At risk:** 72 A inrush per 100 W driver at random closing; about 20 A with zero-cross closing |
| R4 | Dim the luminaire | 0 to 10 V dimming output, 10 to 100 % in 1 % steps, sinking at least 10 mA, isolated from mains. DALI-2 D4i is a later variant, added only if a partner's stock needs it (redefined, LPN-DDR-001 D5) | Circuit review; bench check at TRL 4 | Met (design review): 2.44 mV steps, 5 drivers per output |
| R5 | Schedule without the network | Astronomical clock (dusk and dawn from latitude and longitude) and at least 8 dimming steps per night; keeps running with no network for 30 days or more, clock drift 2 min or less | Firmware sketch review; clock drift calculation | Met on paper with the TCXO clock: 9.1 s in 30 days (a plain crystal drifts 160 s at -10 °C) |
| R6 | Detect presence | Detect a walking pedestrian at 15 m or more and a cyclist or car at 25 m or more along the street; raise the lamp to full within 1 s; hold for a set time (default 60 s) | Radar calculation; field trial | **At risk:** 36 dB signal to noise at 15 m and 0.63 s to full, but rain, trees and clutter unverified |
| R7 | Save energy | 35 % or more annual energy reduction versus photocell full-power operation in the reference case, controller use included. Target and reference profile kept, risk accepted until real traffic counts exist (LPN-DDR-002, O2) | Energy calculation (LPN-CAL-001) | **At risk:** 36.4 % with an ideal driver, 34.1 % with the dimmed driver model |
| R8 | Measure energy | Active power within ±2 % from 10 to 400 W; also voltage, current, power factor and cumulative energy; reported every 15 min | Error budget; calibration method | Met on paper: 1.65 % worst case, with a one-point calibration of each unit |
| R9 | Report faults | Detect lamp out, day burning, cycling, tilt or knock-down, and loss of mains; report within 30 min; the server flags a node silent for 1 h | Fault logic review; last-gasp energy | Met (design review): 1.32 J stored against 0.144 J needed |
| R10 | Low self-consumption | 1.0 W or less average from the mains, sensor head included, expansion ports unloaded | Power budget | Met on paper: 0.68 W |
| R11 | Survive the environment | IP66; operate from -30 to +70 °C; UV-stable housing; proposed surge target 10 kV / 5 kA combination wave, final level taken from ANSI C136.2 | Datasheets, thermal and surge calculations; tests at TRL 4 | **At risk:** 63 to 65 °C inside at 45 °C in sun; 118 J in the varistor at 5 kA; IP66 and surge need tests |
| R12 | Fail safe | Lamp on at night if the controller, firmware or network fails; lamp on within 2 s of power-up at dusk without the network; open 0 to 10 V line gives full output | Circuit and firmware review | Met (design review): normally closed relay, toggling coil drive; driver open-line behavior to be confirmed |
| R13 | Host other sensors | Two sealed 5-pole M12 expansion ports with the FieldNode sensor port pinout (as proposed to FieldNode on 2026-10-02, LPN-DEC-001: pin 1 supply, pin 3 ground, pins 2 and 4 a two-wire RS-485 pair, pin 5 a wake line; hosted sensors accept 5 to 12 V), 12 V SELV, 3 W total, limited by firmware to 2.5 W total when the controller interior is above 50 °C (LPN-DDR-002, O3), cable up to 10 m, whenever the luminaire feed is live. Hosted sensors that need power around the clock on cabinet-switched feeders bring their own storage, such as a FieldNode core (redefined, LPN-DDR-001 D7) | Power budget; design review | Met on paper with the firmware port limit: 3.40 W peak against 3.57 W at 64 °C (3.90 W against 3.55 W without it) |
| R14 | Privacy | Presence only: no images, audio or personal identifiers are captured or leave the device; optional 15 min presence counts | Design review; open firmware | Met (design review) |
| R15 | Secure and open | LoRaWAN 1.0.4 or later with AES-128 session keys; signed firmware; published payload format; works with any LoRaWAN network server. A TALQ bridge belongs to CityTwin, not to LampNode (redefined, LPN-DDR-001 D10) | Firmware sketch review | Met (design review): US915 band; 25.7 s of airtime a day at SF9, with every message inside the 400 ms dwell limit per channel (status at SF9 or faster) |
| R16 | Affordable | Controller and one sensor head $150 or less in parts at prototype quantities | Priced BOM (`bom/bom.csv`) | USD 143.00 for the constructable design, USD 7.00 under the USD 150 value-engineering target |

Summary: 0 not met, 4 at risk (R3, R6, R7, R11), 11 met on paper, by design review or under the value-engineering target, 1 not verifiable at TRL 3 (R1). The `budget_usd` figure behind R16 is a value-engineering target, not a spending limit.

## Requirements at risk

- **R3:** relay inrush. A normally closed relay with an 80 A inrush rating has to be found, and several drivers on one relay need zero-cross closing.
- **R6:** the signal budget and timing are met, but false triggers from rain, trees and traffic can only be settled in the field. The radar needs I/Q output to reject rain.
- **R7:** the saving sits close to the target and depends on traffic and driver behavior. Amish decided to keep the 35 % target and the reference profile and accept the risk until real traffic counts exist (LPN-DDR-002).
- **R11:** thermal margin in sun is about 5 to 7 K; surge and IP66 need tests.

## Assumptions

- Lit from sunset to sunrise at 40° N: 4,323 h a year (LPN-CAL-001 section 2). At 60° N it is 4,277 h. Photocells switch within minutes of sunset; the exact threshold changes the hours slightly.
- Luminaire power is either proportional to light output (ideal) or 6 % of rated plus 94 % times the light level (dimmed driver model). Real drivers vary.
- Reference dimming profile (for estimates only): full output from dusk to 22:00, then a 30 % floor with presence boosts to full from 22:00 to 06:00, and full output from 06:00 to dawn when dawn is later. Presence boosts are assumed to occupy 15 % of the dimmed hours, about 7.8 isolated passes an hour.
- For comparison, a schedule-only profile (full output except 50 % from 23:00 to 05:00) is also calculated in LPN-CAL-001.
- LampNode ships with photocell-equivalent full output (LPN-DDR-001 D8). The road owner sets the floor level and hold time. Nothing here proposes a light level for any road.

> **Safety:** LampNode connects to mains voltage and is installed at height beside traffic. Any requirement change that affects fail-safe behavior (R12) or light levels must be reviewed with the road owner.
