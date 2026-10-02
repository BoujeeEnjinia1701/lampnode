---
doc_id: LPN-PRC-001
title: LampNode design precis
project: LampNode
doc_type: Design precis
version: "0.6"
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
  change: Concept for TRL 2, main components, first-order numbers, design choices, safety and open questions
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update. Design choices adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review (LPN-DDR-001); numbers replaced by LPN-CAL-001; relay, clock, surge stage, radar and port changes; parametric model and drawing LPN-DWG-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design made constructable (LPN-DDR-003); component descriptions, mass and cost updated; budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Decisions of 2026-10-02 (LPN-DEC-001): first partner and band, port pinout proposed to FieldNode'
---

# LampNode design precis

## Summary

LampNode is a twist-lock controller that replaces the photocell on top of an LED streetlight, plus a small sensor head clamped under the lamp arm. The controller switches and dims the luminaire over its standard 0 to 10 V input, follows a night schedule held on the device, raises the light when the sensor head's radar sees someone approaching, measures the lamp's energy and reports faults over LoRaWAN. The sensor head also offers two powered, sealed ports for other city sensors.

The TRL 3 calculations (LPN-CAL-001) put the energy of a 100 W luminaire at 40° N at about 432 kWh a year under a photocell and about 275 to 285 kWh with the reference presence profile, a saving of **34.1 to 36.4 %** against the 35 % target of R7. The TRL 2 estimate of about 41 % assumed nights that were too uniform. The controller draws 0.68 W on average, and the parts are estimated at USD 143.00 against a USD 150 value-engineering target (USD 7.00 under it). Four requirements are at risk on paper (R3, R6, R7, R11); none is clearly not met. R13 is met on paper once the firmware limits the hosted ports to 2.5 W above 50 °C inside. The design choices below were decided by Amish on 2026-09-25 (LPN-DDR-001, LPN-DDR-002).

Figure 1 (`media/hero.png`) shows LampNode on a 7.8 m street pole with a 1.75 m person for scale; Figure 2 (`media/exploded.png`) numbers the parts to match `bom/bom.csv`; Figure 3 (`media/cutaway.png`) shows the inside of the controller; Figure 4 (`media/flow.png`) shows the annual energy; Figure 5 (`cad/drawings/LPN-DWG-001.pdf`) is the general arrangement at Rev P3, generated from `cad/src/model.py`. The design was made constructable on 2026-09-30 (LPN-DDR-003); how each part is made and fitted is in the prototype build plan, LPN-BLD-001 (`docs/05-build-plan.md`).

## How it works

1. **At dusk** the light sensor sees the light level fall below a set threshold, or the astronomical clock reaches dusk. The controller treats it as day only when both the clock and the light sensor say day, so a failed sensor or a wrong clock leaves the lamp on. The lamp starts at the level the road owner set; the default is full output.
2. **During the night** the controller steps the 0 to 10 V output through the road owner's schedule, for example full output until 22:00, then a lower floor.
3. **When someone approaches** the radar in the sensor head sees motion toward the lamp. The radar has I/Q (direction) output, so rain, which always moves away from a downward-looking beam, is ignored. The head tells the controller over the M12 cable, and the controller ramps the lamp to full output in about 0.63 s, holds it for a set time and ramps back down.
4. **Every 15 min** the controller sends a 24-byte LoRaWAN status message: energy, power, voltage, dimming level, presence count and fault flags. Schedules and settings come back as downlinks, and the network also sets the clock, but the lamp never depends on the network to run. A TCXO real-time clock keeps drift under 10 s a month without the network.
5. **When something goes wrong** the controller sends a fault message at once: lamp out, lamp burning in daylight, cycling, pole tilted or knocked down, or mains lost (a 0.22 F supercapacitor holds about 9 times the energy of a last message). A gateway such as TwinKit, or any LoRaWAN network server, flags a node that goes silent.
6. **When the dome gets hot** the controller limits the two expansion ports to 2.5 W in total while its interior is above 50 °C, so the 5 W supply stays within its derated output (LPN-DDR-002). Hosted sensors must tolerate the lower allowance.
7. **If the controller fails** the relay closes and the lamp stays on. The relay coil is driven through a charge pump that needs a toggling signal from the controller, so a stopped or hung controller drops the coil. An open 0 to 10 V line leaves typical drivers at full output.
8. **When the relay switches** it closes at a zero crossing of the mains voltage, timed from the metering IC, which cuts the LED driver inrush from about 72 A to about 20 A.

## Main components

Numbers match Figure 2 and `bom/bom.csv`.

| No. | Component | Role |
| --- | --- | --- |
| 1 | Twist-lock base, 7-contact | ANSI C136.41 plug: line, neutral and switched load blades; four low-voltage contacts for dimming and two auxiliary lines. There is no earth contact. Six countersunk screws from underneath hold the dome and the board stack |
| 2 | Dome cover | UV-stabilized ASA, 90 mm diameter, 72 mm tall on a 1 mm gasket, 97 mm tall with the base; three screw bosses, a flat pad for the M12 socket and an 8 mm light-pipe hole |
| 3 | Surge protection and fuse | Thermal fuse and a thermally protected 20 mm, 385 V class varistor line to neutral; TVS diodes on the low-voltage leads |
| 4 | Isolated power supply | 85 to 305 V AC in, 12 V out, 5 W; creates the SELV side that feeds the electronics, the dimming output and the expansion ports |
| 5 | Fail-on relay | Normally closed, 16 A, rated for 80 A inrush or better; coil (about 0.4 W) energized in daytime only |
| 6 | Energy metering | Single-phase metering IC with a 2 mΩ shunt on the mains side, linked to the controller through a digital isolator; one-point calibration at build |
| 7 | Controller and LoRaWAN radio | STM32WL-class module shared with FieldNode, TCXO real-time clock, accelerometer, 0 to 10 V output stage, charge-pump coil drive, 0.22 F supercapacitor for the last message |
| 8 | Antenna | Sub-GHz antenna inside the dome, above the luminaire's metal body |
| 9 | Light sensor and pipe | Ambient light sensor under a clear 8 mm rod sealed through the dome top, for dusk and dawn and for day-burner checks |
| 10 | M12 port and cable | 5-pole M12 socket in a flat pad on the pole side of the dome and about 1 m of cable along the arm to the sensor head: 12 V and a two-wire serial link |
| 11 | Sensor head enclosure | IP66 box 120 x 90 x 60 mm clamped under the arm, 470 mm from the receptacle toward the pole |
| 12 | 24 GHz radar presence sensor | Doppler module with I/Q output, tilted 25° below horizontal along the street; motion, speed and direction only |
| 13 | Sensor head board | Small microcontroller that turns the radar signal into presence events, and switches power to the expansion ports |
| 14 | Expansion ports (2) | Sealed 5-pole M12 sockets with the pinout proposed to FieldNode (pin 1 supply, pin 3 ground, pins 2 and 4 RS-485, pin 5 wake), 12 V SELV, 3 W total |
| 15 | Arm band clamps | Two stainless band clamps for 50 to 80 mm arms through slots in a folded aluminium bracket, with rubber strips where the arm rests; no drilling of the arm |
| 17 | Controller boards and fixings | Round mains board on three spacers carrying items 3 to 6, standoffs to the controller board, screws, inserts and the dome gasket |
| 18 | Head internal plate | Printed plate on the box bosses, carrying the head board and a 25° cradle for the radar |

The luminaire, its receptacle, the arm and the pole are existing street furniture and are not part of LampNode. The model shows the receptacle and a length of arm as grey reference parts.

## Numbers at TRL 3

All values come from LPN-CAL-001 and `docs/04-calcs/sizing.py`. They are calculations with typical part values, not measurements.

*Table 1. Annual energy for one 100 W luminaire at 40° N (4,323 h a year).*

| Case | Energy per year | Saving |
| --- | --- | --- |
| Photocell, full power | 432 kWh | |
| Schedule only (50 % from 23:00 to 05:00) | 324 kWh | 25.0 % |
| Reference presence profile with controller use, ideal driver | 275 kWh | 36.4 % |
| Same, dimmed driver model | 285 kWh | 34.1 % |

The saving depends mostly on traffic. With the dimmed driver model it is 40.4 % with no traffic, 34.4 % at 8 isolated passes an hour and 22.0 % at 30. At 60° N it falls to 31.8 %. The saving is of the same order as the 49 % that Jägerbrand estimated for a dimming schedule on Swedish roads ([Jägerbrand, 2016](https://www.mdpi.com/1996-1073/9/5/357)).

*Table 2. Other key figures.*

| Quantity | Value | Requirement |
| --- | --- | --- |
| Average draw from the mains | 0.68 W | R10 met |
| 12 V peak, ports limited to 2.5 W above 50 °C inside | 3.40 W against 3.57 W available at 64 °C (3.90 W against 3.55 W without the limit) | R13 met on paper |
| Inrush, 100 W driver at 277 V | 72 A at random closing, about 20 A at zero-cross closing | R3 at risk |
| Clock drift without the network, 30 days | 9.1 s with the TCXO clock (160 s at -10 °C with a plain crystal) | R5 met on paper |
| Radar | Beam covers 7.5 to 47.9 m for a walking person; 36 dB signal to noise at 15 m; 0.63 s to full | R6 at risk |
| Metering error | 1.65 % worst case with a one-point calibration | R8 met on paper |
| Status airtime | 267 ms per message, 25.7 s a day at SF9 | R15 |
| Interior temperature at 45 °C in sun | 63 to 65 °C | R11 at risk |
| Varistor energy at 5 kA | 118 J | R11 |
| Mass | Controller 0.33 kg; head with clamps and cable 0.42 kg | |
| Parts cost | USD 143.00 (controller USD 75.00, head USD 61.00, hardware USD 7.00) against the USD 150 value-engineering target | R16: USD 7.00 under the target |
| Payback on parts | 3.9 to 9.7 years at USD 0.25 to 0.10 per kWh, before labor | |

## Key design choices

Each choice below is **Decided by Amish, 2026-09-25: go with recommendation** (LPN-DDR-001, LPN-DDR-002).

1. **Socket:** ANSI C136.41 7-contact first, since it is the photocontrol socket widely used on existing roadway luminaires in North America and suits retrofits; a Zhaga Book 18 variant later for newer D4i luminaires.
2. **Presence sensor:** 24 GHz Doppler radar, which senses motion through a plastic cover, is not blinded by heat and cannot form an image; schedule-only operation stays as a firmware mode.
3. **Sensor head link:** a cable from the controller to a head under the arm, so one mains connection powers both.
4. **Radio:** LoRaWAN on the STM32WL-class module shared with FieldNode and TwinKit.
5. **Dimming:** 0 to 10 V only; DALI-2 D4i on the auxiliary contacts only if a partner's stock needs it.
6. **Fail-on relay:** normally closed contact, energized to turn the lamp off in daytime.
7. **Hosted sensor power:** 12 V SELV, 3 W total on two ports, limited by firmware to 2.5 W above 50 °C inside, whenever the luminaire feed is live. Sibling sensors such as AirStreet and NoiseMap stay on FieldNode solar and may use LampNode power as an option.
8. **Default policy:** the controller ships with photocell-equivalent behavior (full output all night); any dimming profile is set by the road owner.
9. **Mains range:** 120 to 277 V; a 347 V and 480 V variant later if a partner needs it.
10. **Interoperability:** open LoRaWAN and a published payload; a TALQ bridge belongs to CityTwin.

The TRL 3 calculations added engineering changes, also decided by Amish on 2026-09-25 (LPN-DDR-001 O4 to O8): the TCXO clock, the high-inrush relay with zero-cross closing, the 385 V surge stage without a gas discharge tube, the charge-pump coil drive and two-signal day logic, the I/Q radar and 5-pole M12 ports to match FieldNode. Amish also decided to keep R7 at 35 % with the reference profile and accept the risk until real traffic counts exist (O2), and to meet R13 at high temperature with the firmware port limit rather than a 10 W supply (O3).

## Safety

> **Safety:** LampNode connects to mains voltage (up to 277 V AC nominal, 305 V maximum) inside the luminaire's receptacle. Only qualified electricians may fit or remove it, with the circuit isolated where local rules require. The prototype must not be plugged into a public lighting network until it has passed the surge, insulation and safety tests that the asset owner requires.

> **Safety:** Work on streetlights is work at height beside traffic. Use a bucket truck or a suitable access platform, fall protection and traffic management as local rules require, and only with the asset owner's permission.

> **Safety:** A controller fault must never leave a street dark. The normally closed relay, the charge-pump coil drive and the open-line behavior of the 0 to 10 V driver must be checked on every driver model used. Light levels and dimming floors are the road owner's decision, not LampNode's.

> **Safety:** Surges on long street lighting feeders can destroy electronics and start fires. The socket has no earth contact, so LampNode clamps line to neutral only; the varistor must be thermally protected and fused, and the housing material flame-rated. Relay contacts welded by inrush would leave a lamp burning in daylight; the day-burner check must report it.

- **Privacy:** the radar reports motion, speed and direction only. No images, audio or personal identifiers are captured or leave the device. Check local data protection law before any deployment.
- **Radio:** 24 GHz radar and sub-GHz LoRa modules must be used within local radio regulations; use certified modules.
- **Expansion ports:** 12 V SELV only, fused per port, 2.5 W in total above 50 °C inside. Hosted devices must not connect to mains.
- **Heat:** in 45 °C sun the inside of the dome reaches about 65 °C; the supercapacitor and supply must be rated for it.

## Open questions after TRL 3

1. Radar false triggers from rain, wind-blown trees and passing traffic, and the real cross-section of a person seen from 7.7 m (R6). Needs a field trial.
2. A normally closed relay with an 80 A or better inrush rating, and the partner's driver inrush data (R3).
3. Surge level and test standard: ANSI C136.2 and the asset owner's specification (R11). The standard was not read in this session.
4. R7 shortfall: the risk is accepted by Amish's decision (LPN-DDR-002); real traffic counts from a first partner would settle it. The first partner is to be a US partner on the 915 MHz band; the first candidate to approach is a university campus or municipal utility in the Dallas-Fort Worth area that runs LED streetlights with ANSI C136.41 sockets (decided 2026-10-02, LPN-DEC-001).
5. Sensor port pinout: LampNode proposes to FieldNode pin 1 supply (12 V on LampNode), pin 3 ground, pins 2 and 4 a two-wire RS-485 pair, pin 5 a wake line; hosted sensors accept 5 to 12 V and regulate down themselves (decided 2026-10-02, LPN-DEC-001); FieldNode and the adopting teams still have to agree it (FieldNode O2).
6. Whether neighboring lamps should also brighten ahead of a pedestrian, which needs a lamp-to-lamp message path.
7. A DALI-2 D4i variant and a Zhaga Book 18 form, if a partner needs them.

## Key design decisions

Decisions are recorded in [decisions/](decisions/). [0001: TRL 2 review decisions](decisions/0001-trl2-review-decisions.md) (LPN-DDR-001) lists the TRL 2 recommendations and their status. [0002: Recommendations accepted](decisions/0002-recommendations-accepted.md) (LPN-DDR-002) records Amish's 2026-09-25 acceptance of every recommendation and the one item still open.
