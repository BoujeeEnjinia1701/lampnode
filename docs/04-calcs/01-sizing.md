---
doc_id: LPN-CAL-001
title: LampNode sizing calculations
project: LampNode
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (energy, self-consumption, switching and inrush, dimming, clock, radar, metering, radio and last gasp, surge, temperature, hosted power, mass, cost) with a status for every requirement
---

# LampNode sizing calculations

On paper, LampNode meets ten of its sixteen requirements, and none is clearly not met. Five are **at risk**: R3 (relay inrush), R6 (presence detection), R7 (energy saving), R11 (environment) and R13 (hosted sensor power at high temperature). R1 (socket fit and a 5 min change at height) cannot be verified until a base is tried on a real receptacle.

The largest correction to TRL 2 is the energy saving. Integrating the reference profile over real night lengths at 40° N gives **34.1 to 36.4 %**, not about 41 %, against the 35 % target of R7. The TRL 2 estimate assumed every night had 8 dimmed hours and 3.2 h at full output; in fact the dimmed window 22:00 to 06:00 averages 7.52 h a night, summer nights are shorter than it, and the photocell baseline runs 4,323 h a year, not 4,100 h. The calculations also found three design changes, now in `bom/bom.csv` and proposed for Amish's review: a temperature-compensated (TCXO) real-time clock, since an ordinary 32 kHz crystal drifts 160 s in a cold month against the 2 min limit of R5; a normally closed relay rated for 80 A inrush and closed at the voltage zero crossing; and a 385 V class surge stage without a gas discharge tube, because the twist-lock socket has no earth contact.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads geometry and part volumes from `cad/src/model.py`, costs from `bom/bom.csv` and the budget from `project.yaml`. All values are first-principles estimates with typical part values; nothing is measured and no part has been chosen from a datasheet.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Reference luminaire | 100 W LED cobra head, 0 to 10 V driver, arm at 7.80 m | LPN-REQ-001 reference case |
| Location and switching | 40° N; lamp on from sunset to sunrise (sun center at -0.833°); clock in local solar time | Mid-latitude city; photocells switch within minutes of sunset |
| Reference dimming profile | Full to 22:00, 30 % floor from 22:00 to 06:00 with full output 15 % of that time, full from 06:00 to dawn | LPN-REQ-001 assumptions (for estimates only; the road owner sets any profile) |
| Driver when dimmed | Ideal (input proportional to light), or input = 6 % of rated + 94 % x light level | Typical drivers lose efficiency when dimmed |
| 12 V loads | Controller, clock, accelerometer and light sensor 0.05 W; metering 0.05 W; relay coil 0.40 W by day only; radar 0.20 W and head board 0.03 W by night only | Typical parts |
| Power supply | 5 W module, 0.10 W no-load input, 72 % incremental efficiency at light load, 80 % near full load; full output to 50 °C, falling linearly to 60 % at 70 °C | Typical encapsulated 5 W modules |
| Hosted sensors | 3 W total on two ports; 0.40 W radio transmit transient | LPN-REQ-001 R13 |
| Driver inrush | 60 A cold-start peak at 230 V for a typical 100 W outdoor driver, 47 µF bulk capacitor | Typical driver datasheets; no driver chosen |
| Radar | 24.125 GHz; 8 dBm, 11 dBi each way; half-power elevation half-width 17°; walking person 0.5 m²; 35 dB effective noise figure at low Doppler, 10 Hz bins, 15 dB detection threshold | Typical low-cost K-band modules |
| Tariff | $0.10 to $0.25 per kWh | Typical public lighting rates |

## 2. Energy (R7)

At 40° N the lamp is lit **4,323 h a year** (11.84 h a night on average, from 8.99 h at midsummer to 14.68 h at midwinter). The 100 W lamp then uses **432 kWh a year** under a photocell.

*Table 2. Annual energy for one 100 W luminaire.*

| Case | Energy per year | Saving |
| --- | --- | --- |
| Photocell, full power | 432 kWh | |
| Schedule only (50 % from 23:00 to 05:00) | 324 kWh | 25.0 % |
| Reference presence profile, ideal driver, with 5.9 kWh of controller use | 275 kWh | **36.4 %** |
| Same, dimmed driver model | 285 kWh | **34.1 %** |

The dimmed window covers 2,745 h a year, 7.52 h a night on average. With an ideal driver R7 is met with 1.4 points to spare; with the dimmed driver model it is missed by 0.9 points. **R7 is at risk.** The TRL 2 method, applied to the same inputs, reproduces its own 236 kWh, so the difference comes from the night lengths and not from an arithmetic slip. The energy saved is **148 kWh a year** with the dimmed driver model.

The presence assumption matters more than the driver. An isolated pedestrian keeps the lamp at full for about 70 s (8.6 s from detection at 15 m to the pole, a 60 s hold and 1 s of ramps), so the 15 % boost equals about 7.8 isolated passes an hour. With random arrivals and the dimmed driver model, the saving is 40.4 % with no traffic, 37.3 % at 4 events an hour, 34.4 % at 8, 29.3 % at 16 and 22.0 % at 30. At 60° N the lamp runs 4,277 h and uses 428 kWh, and the saving falls to 31.8 %, because long winter evenings before 22:00 stay at full output.

## 3. Self-consumption and supply loading (R10, R13)

The lamp is lit for 0.493 of the year. The relay coil averages 0.203 W, the radar and head board 0.113 W, and the 12 V side 0.416 W in all. The shunt adds 0.8 mW. From the mains LampNode draws **0.68 W** on average, against 1.0 W: R10 is met. The TRL 2 figure (about 0.6 W) used a 0.24 W coil; a typical 16 A relay coil is 0.40 W.

With both hosted ports at 3 W the 12 V side carries 3.50 W by day (coil on) and 3.33 W at night (radar on), or **3.90 W** at peak with a radio transmission: 78 % of the 5 W rating at 25 to 50 °C. Section 11 shows the problem at high temperature.

## 4. Switching and inrush (R3)

The steady current at 400 W, 100 V and PF 0.90 is 4.44 A (0.93 A for the reference lamp at 120 V), well inside a 16 A contact. The problem is inrush. A typical 100 W outdoor driver takes about 72 A for a few hundred microseconds when switched at a random point of the 277 V wave, and four such drivers on one relay would take about 289 A. Relays made for LED loads are rated for about 80 A inrush, and most are normally open; a normally closed contact with that rating must be found.

Closing at the voltage zero crossing cuts the inrush sharply. The metering IC gives the zero crossing; the relay release time is learned and the coil released early by that amount. With a 0.5 ms timing error the peak falls to about 17 A at 50 Hz and 20 A at 60 Hz for one driver. Contact life is not a concern: two switchings a day for 20 years are 14,600 cycles against 100,000. **R3 is at risk** until a normally closed relay with an 80 A or better inrush rating is found and the partner's driver inrush is known; 400 W from several drivers needs zero-cross closing.

## 5. Dimming output (R4)

A 12-bit PWM filtered to 0 to 10 V gives 2.44 mV steps against the 100 mV needed for 1 % steps. A 10 mA sink serves 5 drivers at 2 mA of control current, the high end for 0 to 10 V drivers, and dissipates at most 0.10 W. R4 is met by design review for 0 to 10 V; DALI-2 D4i is a later variant (LPN-DDR-001 item 5).

## 6. Clock without the network (R5)

A 32 kHz tuning-fork crystal (±20 ppm, falling 0.034 ppm/K² away from 25 °C) drifts 52 s in 30 days at 25 °C, **160 s at -10 °C** and 318 s at -30 °C (230 s at 70 °C). The 2 min limit of R5 is therefore not met in a cold month. A TCXO real-time clock (±3.5 ppm from -40 to 85 °C) drifts at most **9.1 s** in 30 days. The TCXO clock is now in `bom/bom.csv` line 7 (+$3), so R5 is met on paper; the change is an engineering proposal awaiting Amish. When the network is up, the controller also sets its clock from the LoRaWAN network time.

## 7. Presence detection (R6)

**Geometry.** The model puts the radar 7.72 m above the road; tilted 25° down, its beam center reaches the road 16.6 m along the street. A pedestrian (target center 1.0 m up) at 15 m is 24.1° below horizontal and a car or cyclist (0.7 m) at 25 m is 15.7° below, both inside the half-power beam, which covers a walking person from 7.5 to 47.9 m along the street.

**Signal.** A walking person at 15 m is 16.4 m from the radar in a straight line. With the Table 1 values the echo is -93 dBm against a -129 dBm noise floor: **36 dB** of signal to noise. The 15 dB threshold is reached at 56 m on the beam axis, or 40 m at the beam edge. Range is therefore not limited by signal strength.

**Motion and clutter.** An approaching pedestrian at 1.4 m/s gives a 205 Hz Doppler tone, a cyclist at 5 m/s 774 Hz and a car at 50 km/h 2,151 Hz. Falling rain gives 136 Hz (drizzle, 2 m/s) to 476 Hz (heavy rain, 7 m/s), which overlaps walkers and cyclists. Because the beam points down, rain always moves away from the radar, while people coming toward the lamp move toward it, so a radar with I/Q (direction) output can ignore receding targets. `bom/bom.csv` line 12 now calls for I/Q output. Trees moving in wind produce echoes in both directions and cannot be rejected by direction alone.

**Timing.** Two 128 ms detection frames, the serial link, the 0 to 10 V output and a 0.3 s driver response give **0.63 s** to full output, inside 1 s. A pedestrian detected at 15 m reaches the pole 10.7 s later.

**R6 is at risk.** The signal budget and timing are met, but rain, wind-blown trees and the real radar cross-section of a person at this angle can only be settled in the field.

## 8. Metering (R8)

The current ranges from 66 mA (10 W at 305 V and PF 0.5) to 4.44 A (400 W at 100 V). A 2 mΩ shunt gives 0.131 mV at the low end, 169 times below the metering IC's full scale and inside its 1000:1 range; it dissipates 0.040 W at 4.44 A.

*Table 3. Active power error budget (percent of reading).*

| Term | Error |
| --- | --- |
| Metering IC over 1000:1 | 0.50 |
| Shunt temperature coefficient, 50 ppm/K over 50 K | 0.25 |
| Voltage divider temperature coefficient | 0.10 |
| Phase error of 0.1° at PF 0.5 | 0.30 |
| Bench reference used for a one-point calibration | 0.50 |
| **Worst-case sum (RSS 0.81)** | **1.65** |

With a one-point calibration at build the worst case is 1.65 %, inside ±2 %. Without it (1 % shunt and 0.2 % divider tolerances) the worst case is 2.35 %. **R8 is met on paper, provided each unit is calibrated once** against a bench power meter. CalRig, which the TRL 2 note suggested, is a climate chamber for air sensors and cannot do this.

## 9. Radio, faults and last gasp (R9, R15)

*Table 4. Time on air of a 24-byte status message (13 bytes of LoRaWAN overhead, 125 kHz, coding rate 4/5).*

| Spreading factor | Per message | 96 per day |
| --- | --- | --- |
| SF7 | 82 ms | 7.9 s |
| SF9 | 267 ms | 25.7 s |
| SF10 | 494 ms | 47.4 s |
| SF12 | 1,974 ms | 189.5 s |

TRL 2 gave about 0.2 s and 20 s a day at SF9; the full LoRaWAN overhead makes it 267 ms and 25.7 s. Under the EU868 1 % duty cycle each SF9 status message needs 26 s of silence, far less than the 15 min interval. On a public network with a 30 s daily fair-use limit, lamps at SF10 or slower need a longer interval, as FieldNode found; on a private TwinKit gateway only the duty cycle applies. A 6-byte fault message takes 185 ms at SF9.

For the last message after mains loss, one transmission at SF10 and 22 dBm with two receive windows needs about 0.144 J. A 0.22 F supercapacitor discharged from 5.0 to 3.6 V gives 1.32 J, a margin of 9 times, and recharges in 55 s at 20 mA. R9 is met by design review. R15 is met by design review with the TALQ bridge moved to CityTwin (LPN-DDR-001 item 10).

## 10. Surge (R11)

The twist-lock socket has no earth contact, so LampNode can clamp only line to neutral; common-mode surges are the luminaire's job. A gas discharge tube to earth, as listed at TRL 2, has nowhere to connect and is dropped. An 8/20 µs surge carries 23.5 µs of charge per ampere of peak current. At 5 kA a 385 V class metal oxide varistor clamping at about 1,000 V absorbs **118 J**, within a 20 mm disc's single-surge rating; at 10 kA it absorbs 271 J, which is beyond it. The 320 V class chosen at TRL 2 has only 5 % of margin over the 305 V maximum line voltage; the 385 V class has 26 %. The surge level required by ANSI C136.2 was not read this session and stays to be confirmed. The surge part of R11 is not verifiable without tests.

## 11. Temperature in the sun (R11, R13)

At 45 °C ambient, with the sun 60° above the horizon, the dome and base present 99 cm² to the sun and absorb 3.46 W at an absorptance of 0.35. Their 338 cm² surface loses heat at 12.4 W/(m² K) in still air. With 0.79 W dissipated inside by day, and the luminaire top 20 K above ambient under the base, the shell rises 13.3 K; allowing 5 K from shell to parts, the inside reaches **63 °C** with the ports unloaded and **65 °C** with 3 W on the ports. That is inside the 70 °C rating, with little margin for a dark dome or a hotter luminaire. **R11 is at risk** (temperature margin, surge and IP66 all unverified).

At 65 °C the derated supply gives about 3.55 W, against the 3.90 W peak with both ports at 3 W. **R13 is at risk** at the hot end. Options, proposed for Amish: limit the ports to 2.5 W above 50 °C in firmware, or fit a 10 W supply module. The voltage drop is not a problem: one port at 3 W over 10 m of 0.34 mm² cable loses 0.25 V (2.1 %), and the 1 m cable to the head, at 0.27 A, loses 0.027 V.

## 12. Mass

*Table 5. Mass estimate.*

| Assembly | Mass | Basis |
| --- | --- | --- |
| Controller | 0.34 kg | Dome from the model volume in ASA (0.073 kg), base at 35 % of its solid envelope in PC plus brass blades (0.097 kg), estimates for the parts inside |
| Sensor head with clamps and 1 m cable | 0.45 kg | Enclosure from the model volume in PC (0.157 kg), 0.150 kg for clamps and bracket, estimates for the rest |

TRL 2 gave 0.25 kg for the controller; 0.34 kg is closer to typical photocontrols of this size. No requirement sets a mass.

## 13. Cost (R16)

`bom/bom.csv` has 16 lines, all priced: $68.00 for the controller (items 1 to 9), $56.00 for the sensor head, cable and ports (items 10 to 15) and $6.00 of hardware, **$130.00** in all against the $150 budget, a margin of $20.00. R16 is met. The total rose from $124 because of the TCXO clock (+$3), the high-inrush relay (+$2) and the 385 V surge stage with TVS diodes (+$1). At 148 kWh a year the parts pay back in 3.5 years at $0.25 per kWh and 8.8 years at $0.10 per kWh, before installation labor.

## 14. Results

*Table 6. Requirement status at TRL 3.*

| ID | Requirement | Result | Status |
| --- | --- | --- | --- |
| R1 | Fit the socket | Representative ANSI C136.41 base in the model; fit and a 5 min change cannot be checked on paper | Not verifiable at TRL 3 |
| R2 | Mains supply range | Supply 85 to 305 V; 385 V class varistor; scope 120 to 277 V (LPN-DDR-001 item 9) | Met (design review) |
| R3 | Switch the luminaire | 4.44 A steady at 400 W; inrush 72 A per 100 W driver, 289 A for four; about 20 A with zero-cross closing | **At risk** |
| R4 | Dim the luminaire | 2.44 mV steps; 10 mA sink serves 5 drivers | Met (design review) |
| R5 | Schedule without the network | Crystal 160 s at -10 °C and 318 s at -30 °C in 30 days; TCXO clock 9.1 s | Met on paper with the TCXO clock |
| R6 | Detect presence | Beam covers 7.5 to 47.9 m; 36 dB at 15 m; 0.63 s to full; rain, trees and cross-section unverified | **At risk** |
| R7 | Save energy | 36.4 % ideal driver, 34.1 % dimmed driver model, target 35 % | **At risk** |
| R8 | Measure energy | 1.65 % worst case with a one-point calibration (2.35 % without) | Met on paper, calibration required |
| R9 | Report faults | 0.144 J last gasp against 1.32 J stored | Met (design review) |
| R10 | Low self-consumption | 0.68 W average | Met on paper |
| R11 | Survive the environment | Inside 63 to 65 °C at 45 °C in sun (70 °C rating); 118 J in the varistor at 5 kA; IP66 and surge need tests | **At risk** |
| R12 | Fail safe | Normally closed relay; open 0 to 10 V line gives full output; coil drive needs a toggling signal; day needs both clock and light sensor | Met (design review) |
| R13 | Host other sensors | 0.25 V drop at 10 m; 3.90 W peak against 3.55 W available at 65 °C | **At risk** |
| R14 | Privacy | Doppler radar, no image; presence counts only | Met (design review) |
| R15 | Secure and open | LoRaWAN 1.0.4, published payload; 25.7 s a day at SF9; TALQ in CityTwin | Met (design review) |
| R16 | Affordable | $130.00 against $150 | Met |

Summary: 0 not met, 5 at risk, 10 met on paper or by design review, 1 not verifiable at TRL 3.

## 15. Limits of this note

- No part is chosen. Every load, inrush, efficiency and derating figure is typical, and each must be replaced by datasheet values before TRL 4.
- The radar model says nothing about false triggers from trees, rain intensity or traffic. Only a field trial can settle R6.
- The thermal model is a single node with a fixed film coefficient; the luminaire top temperature is assumed.
- The energy results depend on the reference profile, which is an estimate only. LampNode ships with photocell-equivalent output (LPN-DDR-001 item 8); the road owner sets any dimming.

> **Safety:** LampNode connects to mains voltage (up to 277 V AC nominal, 305 V maximum) and is installed at height beside traffic. The fail-on behavior in R12 depends on the coil drive dropping out when the controller stops, and on each driver model giving full output with an open 0 to 10 V line; both must be checked on real parts. Relay contacts welded by inrush would leave a lamp burning in daylight, not dark, but the fault must still be reported. Only qualified electricians may fit or remove the controller.
