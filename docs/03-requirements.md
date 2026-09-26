---
doc_id: LPN-REQ-001
title: LampNode requirements
project: LampNode
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# LampNode requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with a lighting authority or users, and will be checked by calculation at TRL 3 and revised after co-design (see LPN-PRB-001). The status column gives the TRL 2 position from the estimates in LPN-PRC-001.

The **reference case** used throughout is a 100 W LED cobra-head luminaire with a 0 to 10 V driver, mounted about 7.8 m above a residential street, lit about 4,100 h per year (about 11.2 h per night on average).

Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 2 status |
| --- | --- | --- | --- | --- |
| R1 | Fit the existing socket | Plugs into an ANSI C136.41 7-contact twist-lock receptacle; replaces a photocontrol with no tools and no luminaire rewiring in 5 min or less at height | Dimensional check against the standard; fit trial on a donor luminaire | Met by design (proposed socket) |
| R2 | Mains supply range | 120 to 277 V AC nominal, 50 or 60 Hz, operating from 100 to 305 V | Power supply datasheet; design review | Met for 120 to 277 V; **not met** for 347 V and 480 V circuits |
| R3 | Switch the luminaire | Switch LED luminaire loads up to 400 W at 277 V, with a relay rated for the driver's inrush current, for 100,000 or more cycles | Relay datasheet against driver inrush data | Met by selection, inrush to be confirmed per driver |
| R4 | Dim the luminaire | 0 to 10 V dimming output, 10 to 100 % in 1 % steps, sinking at least 10 mA, isolated from mains | Circuit review; bench check at TRL 4 | Met by design; DALI-2 D4i variant **not in base design** |
| R5 | Schedule without the network | Astronomical clock (dusk and dawn from latitude and longitude) and at least 8 dimming steps per night; keeps running with no network for 30 days or more, clock drift 2 min or less | Firmware sketch review; RTC drift calculation | Met by design |
| R6 | Detect presence | Detect a walking pedestrian at 15 m or more and a cyclist or car at 25 m or more along the street; raise the lamp to full within 1 s; hold for a set time (default 60 s) | Radar range calculation; field trial | **At risk**, radar range from 7.7 m height unverified |
| R7 | Save energy | 35 % or more annual energy reduction versus photocell full-power operation in the reference case, controller use included | Energy calculation (LPN-PRC-001) | Met by estimate: about 41 % |
| R8 | Measure energy | Active power within ±2 % from 10 to 400 W; also voltage, current, power factor and cumulative energy; reported every 15 min | Metering IC datasheet; calibration method at TRL 3 | Met by selection, unverified |
| R9 | Report faults | Detect lamp out, day burning, cycling, tilt or knock-down, and loss of mains; report within 30 min; the server flags a node silent for 1 h | Fault logic review | Met by design |
| R10 | Low self-consumption | 1.0 W or less average from the mains, sensor head included, expansion ports unloaded | Power budget | Met by estimate: about 0.6 W, 0.8 W with margin |
| R11 | Survive the environment | IP66; operate from -30 to +70 °C; UV-stable housing; proposed surge target 10 kV / 5 kA combination wave, final level taken from ANSI C136.2 at TRL 3 | Datasheets and design review | Unverified |
| R12 | Fail safe | Lamp on at night if the controller, firmware or network fails; lamp on within 2 s of power-up at dusk without the network; open 0 to 10 V line gives full output | Circuit and firmware review | Met by design; driver open-line behavior to be confirmed |
| R13 | Host other sensors | Two sealed M12 expansion ports with the FieldNode pinout (proposed), 12 V SELV, 3 W total, cable up to 10 m | Power budget; design review | Met at night; **not met** in daytime on cabinet-switched feeders |
| R14 | Privacy | Presence only: no images, audio or personal identifiers are captured or leave the device; optional 15 min presence counts | Design review; open firmware | Met by design |
| R15 | Secure and open | LoRaWAN 1.0.4 or later with AES-128 session keys; signed firmware; published payload format; works with any LoRaWAN network server | Firmware sketch review | Met by design; TALQ bridge **not met** at TRL 2 |
| R16 | Affordable | Controller and one sensor head $150 or less in parts at prototype quantities | Priced BOM (`bom/bom.csv`) | Met: about $124 |

## Requirements not met or at risk

- **R2:** 347 V (common in Canada) and 480 V lighting circuits need a different power supply and relay; not covered.
- **R4:** only 0 to 10 V dimming in the base design; D4i luminaires would need a DALI-2 variant.
- **R6:** presence range is the least certain figure in the concept.
- **R13:** on feeders switched at a cabinet, hosted sensors lose power in daytime unless they carry their own storage.
- **R15:** no TALQ bridge yet; interoperability rests on open LoRaWAN and a published payload.
- **R8 and R11** are unverified until TRL 3 and later testing.

## Assumptions

- Dusk-to-dawn operation of about 4,100 h per year, a mid-latitude average; high latitudes differ strongly by season.
- Luminaire power is taken as proportional to commanded light output; real drivers are less efficient when dimmed, so savings may be a few percentage points lower.
- Reference dimming profile (proposed, for estimates only): full output from dusk to 22:00, then a 30 % floor with presence boosts to full from 22:00 to 06:00, and full output from 06:00 to dawn when dawn is later. Presence boosts are assumed to occupy 15 % of the dimmed hours on a residential street (estimate).
- For comparison, a schedule-only profile (full output except 50 % from 23:00 to 05:00, no presence sensing) is also estimated in LPN-PRC-001.
- The road owner sets the floor level and hold time. Nothing here proposes a light level for any road.

> **Safety:** LampNode connects to mains voltage and is installed at height beside traffic. Any requirement change that affects fail-safe behavior (R12) or light levels must be reviewed with the road owner.
