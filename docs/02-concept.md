---
doc_id: LPN-PRC-001
title: LampNode design precis
project: LampNode
doc_type: Design precis
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
  change: Concept for TRL 2, main components, first-order numbers, design choices, safety and open questions
---

# LampNode design precis

## Summary

LampNode is a twist-lock controller that replaces the photocell on top of an LED streetlight, plus a small sensor head clamped under the lamp arm. The controller switches and dims the luminaire over its standard 0 to 10 V input, follows a night schedule held on the device, raises the light when the sensor head's radar detects someone approaching, measures the lamp's energy and reports faults over LoRaWAN. The sensor head also offers two powered, sealed ports for other city sensors. For a 100 W luminaire on a residential street, the estimated annual use falls from about 410 kWh to about 243 kWh (about 41 % less), for about $124 in parts. All figures are TRL 2 estimates to be checked at TRL 3.

Figure 1 (`media/hero.png`) shows LampNode on a 7.8 m street pole with a 1.75 m person for scale; Figure 2 (`media/exploded.png`) numbers the parts to match `bom/bom.csv`; Figure 3 (`media/cutaway.png`) shows the inside of the controller; Figure 4 (`media/flow.png`) shows the annual energy estimate.

## How it works

1. **At dusk** the light sensor sees the light level fall below a set threshold, or the astronomical clock reaches dusk, whichever the policy chooses. The relay closes and the lamp starts at the scheduled level.
2. **During the night** the controller steps the 0 to 10 V output through the schedule that the road owner set, for example full output until 22:00, then a lower floor.
3. **When someone approaches** the radar in the sensor head sees motion along the street. The head tells the controller over the M12 cable, and the controller ramps the lamp to full output within 1 s, holds it for a set time and ramps back down.
4. **Every 15 min** the controller sends a short LoRaWAN status message: energy, power, voltage, dimming level, presence count and fault flags. Schedules and settings come back as downlinks, but the lamp never depends on the network to run.
5. **When something goes wrong** the controller sends a fault message at once: lamp out, lamp burning in daylight, cycling, pole tilted or knocked down, or mains lost (a supercapacitor holds enough energy for a last message). A gateway such as TwinKit, or any LoRaWAN network server, flags a node that goes silent.
6. **If the controller fails** the relay drops to its closed state and an open 0 to 10 V line leaves typical drivers at full output, so the lamp stays on.

## Main components

Numbers match Figure 2 and `bom/bom.csv`.

| No. | Component | Role |
| --- | --- | --- |
| 1 | Twist-lock base, 7-contact | ANSI C136.41 plug: line, neutral, switched load, two dimming contacts and two auxiliary contacts |
| 2 | Dome cover | UV-stabilized polycarbonate or ASA, with a clear window over the light sensor; about 90 mm diameter, 100 mm tall overall |
| 3 | Surge protection and fuse | Thermal fuse, MOVs and a gas discharge tube on the mains side |
| 4 | Isolated power supply | 100 to 305 V AC in, 12 V out, 5 W; creates the SELV side that feeds the electronics, the dimming output and the expansion ports |
| 5 | Fail-on relay | Normally closed contact held open by the coil in daytime, so a dead controller leaves the lamp on |
| 6 | Energy metering | Single-phase metering IC with a shunt on the mains side, linked to the controller through a digital isolator |
| 7 | Controller and LoRaWAN radio | STM32WL-class module shared with FieldNode, real-time clock, accelerometer, 0 to 10 V output stage, supercapacitor for the last message |
| 8 | Antenna | Sub-GHz antenna inside the dome, above the luminaire's metal body |
| 9 | Light sensor and pipe | Ambient light sensor under the dome window, for dusk and dawn and for day-burner checks |
| 10 | M12 port and cable | 4-pole M12 on the controller base and about 1 m of cable along the arm to the sensor head: 12 V and a two-wire serial link |
| 11 | Sensor head enclosure | IP66 box about 120 x 90 x 60 mm clamped under the arm near the luminaire |
| 12 | 24 GHz radar presence sensor | Doppler motion sensor tilted about 25° below horizontal along the street; motion and speed only |
| 13 | Sensor head board | Small microcontroller that turns the radar signal into presence events, and switches power to the expansion ports |
| 14 | Expansion ports (2) | Sealed M12 sockets with the FieldNode sensor pinout (proposed), 12 V SELV, 3 W total |
| 15 | Arm band clamps | Two stainless band clamps and a bracket; no drilling of the arm |

The luminaire, its receptacle, the arm and the pole are existing street furniture and are not part of LampNode.

## First-order numbers

All values are estimates at TRL 2, with assumptions stated. They will be checked at TRL 3.

### Energy per luminaire

Assumptions: 100 W luminaire; about 4,100 h of darkness per year, or about 11.2 h per night on average (about 366 night-equivalents); luminaire power proportional to light output.

Table 1. Annual energy for one 100 W luminaire (estimates)

| Case | Profile | Energy per night | Energy per year | Saving |
| --- | --- | --- | --- | --- |
| Photocell, full power | 100 % all night | 1.12 kWh | about 410 kWh | |
| Schedule only | 100 %, but 50 % from 23:00 to 05:00 | 0.82 kWh | about 300 kWh | about 27 % |
| Schedule and presence | 100 % to 22:00; 30 % floor from 22:00 to 06:00 with full output 15 % of that time | 0.64 kWh | about 236 kWh | about 42 % |
| Same, with controller use | adds 0.8 W for 8,760 h (about 7 kWh) | | about 243 kWh | **about 41 %** |

The presence case works out as 3.2 h x 100 W + 8 h x (0.15 x 100 W + 0.85 x 30 W) = 320 Wh + 324 Wh = 644 Wh per night. The saving is of the same order as the 49 % that Jägerbrand estimated for a dimming schedule on Swedish roads ([Jägerbrand, 2016](https://www.mdpi.com/1996-1073/9/5/357)). Drivers are less efficient when dimmed, so the real saving may be a few percentage points lower.

### Self-consumption

Table 2. Average power drawn by LampNode (estimates)

| Load | Average |
| --- | --- |
| Controller and radio, mostly asleep | about 0.05 W |
| Metering IC | about 0.05 W |
| Relay coil, energized only in daytime (about 12.8 h of 24 h) | about 0.13 W |
| Radar and head board, on only at night | about 0.12 W |
| Subtotal on the 12 V side | about 0.35 W |
| From the mains, at about 70 % light-load supply efficiency, plus about 0.1 W no-load loss | **about 0.6 W** |

The energy estimate uses 0.8 W to leave margin. On a cabinet-switched feeder the controller is unpowered in daytime, the relay coil draws nothing, and self-consumption falls further.

### Radio

A status message of about 24 bytes at spreading factor 9 takes about 0.2 s on air (estimate). Ninety-six messages a day use about 20 s of airtime, about 0.02 % of the day, well inside the 1 % duty cycle that applies in the EU868 sub-bands. Fault messages are rare and short.

### Presence geometry

With the radar at about 7.7 m and tilted about 25° below horizontal, the beam center reaches the ground about 16.5 m along the street (7.7 m / tan 25°). A pedestrian 15 m away is about 17 m from the sensor in a straight line. Whether a low-cost 24 GHz Doppler module detects a walking person reliably at that range, in rain and with passing cars, is the main technical risk (R6 at risk).

### Cost, payback and mass

- Parts: about $124 for the controller and one sensor head (`bom/bom.csv`); the controller alone is about $65.
- Energy saving: about 167 kWh per year. At $0.10 to $0.25 per kWh this is about $17 to $42 per year, so the parts cost pays back in about 3 to 7 years (estimate), before installation labor. Fitting during planned photocell replacement keeps the labor cost low.
- Mass: controller about 0.25 kg, sensor head with clamps about 0.45 kg (estimates).

## Key design choices

Each choice below is **proposed, awaiting Amish**. Options and a recommendation for each are in `docs/REVIEW.md`.

1. **Socket:** ANSI C136.41 7-contact first, since it is the photocontrol socket widely used on existing roadway luminaires in North America and suits retrofits; a Zhaga Book 18 variant later for newer D4i luminaires.
2. **Presence sensor:** 24 GHz Doppler radar, which senses motion through a plastic cover, is not blinded by heat and cannot form an image; PIR is the lower-cost alternative.
3. **Sensor head link:** a cable from the controller to a head under the arm, so one mains connection powers both. Alternatives: a Zhaga bottom-socket module, or a solar FieldNode head linked by radio.
4. **Radio:** LoRaWAN on the STM32WL-class module shared with FieldNode and TwinKit, rather than a proprietary mesh.
5. **Dimming:** 0 to 10 V in the base design; DALI-2 D4i on the auxiliary contacts as a later variant.
6. **Fail-on relay:** normally closed contact, energized to turn the lamp off in daytime.
7. **Hosted sensor power:** 12 V SELV, 3 W total on two ports, available whenever the luminaire feed is live.
8. **Default policy:** the controller ships with photocell-equivalent behavior (full output all night); any dimming profile is set by the road owner.

## Safety

> **Safety:** LampNode connects to mains voltage (up to 277 V AC, 305 V maximum) inside the luminaire's receptacle. Only qualified electricians may fit or remove it, with the circuit isolated where local rules require. The prototype must not be plugged into a public lighting network until it has passed the surge, insulation and safety tests that the asset owner requires.

> **Safety:** Work on streetlights is work at height beside traffic. Use a bucket truck or a suitable access platform, fall protection and traffic management as local rules require, and only with the asset owner's permission.

> **Safety:** A controller fault must never leave a street dark. The fail-on relay and the open-line behavior of the 0 to 10 V driver must be checked on every driver model used. Light levels and dimming floors are the road owner's decision, not LampNode's.

> **Safety:** Surges on long street lighting feeders can destroy electronics and start fires. The surge stage, fuse and housing material must be chosen and tested for this at TRL 3 and later.

- **Privacy:** the radar reports motion only. No images, audio or personal identifiers are captured or leave the device. Check local data protection law before any deployment.
- **Radio:** 24 GHz radar and sub-GHz LoRa modules must be used within local radio regulations; use certified modules.
- **Expansion ports:** 12 V SELV only, fused per port. Hosted devices must not connect to mains.

## Open questions for TRL 3

1. Radar range and false triggers from 7.7 m in rain, wind-blown trees and passing traffic (R6).
2. Relay rating against the inrush current of the partner's LED drivers (R3).
3. Surge level and test standard: ANSI C136.2 and the asset owner's specification (R11).
4. Metering accuracy at low dimmed power, and a simple field calibration method, possibly with CalRig (R8).
5. Power for hosted sensors on cabinet-switched feeders: a small LiFePO4 buffer in the head, or rely on FieldNode solar cores (R13).
6. A DALI-2 D4i variant and a Zhaga Book 18 form (R4).
7. A TALQ bridge in TwinKit or CityTwin (R15).
8. Whether neighboring lamps should also brighten ahead of a pedestrian, which needs a lamp-to-lamp message path.
9. Thermal check of the dome in full sun on a dark luminaire top at 45 °C ambient.

## Key design decisions

Record each significant decision as a file in [decisions/](decisions/) once Amish has made it. None has been recorded yet.
