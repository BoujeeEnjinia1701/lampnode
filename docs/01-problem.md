---
doc_id: LPN-PRB-001
title: LampNode problem statement
project: LampNode
doc_type: Problem statement
version: "0.3"
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
  change: Problem, users, operating environment, constraints, prior work and open questions for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Open questions updated for the choices adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review (LPN-DDR-001); out-of-scope items and sibling interfaces aligned
---

# LampNode problem statement

Most streetlights run at full power from dusk to dawn whether anyone is on the street or not, nobody knows a lamp has failed until someone complains, and the controllers that could fix both tie a city to one vendor's network and software. LampNode is an open controller that plugs into the standard socket on top of an LED streetlight to dim it by schedule and presence, report faults by itself and power other city sensors on the same pole.

## The problem

**Energy is spent on empty streets.** A photocell switches a luminaire fully on at dusk and fully off at dawn. On a residential street most of the hours between about 23:00 and 05:00 see little traffic, yet the lamp draws its full rated power. A study of 14 LED-lit roads in Sweden found that a dimming schedule alone could save about 49 % of the energy ([Jägerbrand, 2016](https://www.mdpi.com/1996-1073/9/5/357)).

**Light at night keeps growing.** Citizen observations of star visibility from 2011 to 2022 are consistent with the night sky brightening by 7 to 10 % per year ([Kyba et al., 2023, via GFZ](https://www.gfz.de/en/press/news/details/citizen-scientists-report-global-rapid-reductions-in-the-visibility-of-stars-from-2011-to-2022)). Street lighting is only one source, but dimming it when streets are empty is one of the few changes a city controls directly.

**Faults are found by residents.** New York City's Department of Transportation maintains nearly 400,000 streetlights and asks residents to call 311 to report a problem ([NYC DOT](https://www.nyc.gov/html/dot/html/infrastructure/streetlights.shtml)). A lamp that fails on a quiet street can stay dark until someone notices and bothers to report it; a lamp burning in daylight is rarely reported at all.

**Energy use is not even measured.** The US Energy Information Administration states that it has no estimate of electricity use specifically for public street and highway lighting ([EIA](https://www.eia.gov/tools/faqs/faq.php?id=99&t=3)). Many streetlights are billed on flat rates, so a city cannot see what a dimming policy saves.

**Controllers lock cities in.** Networked controllers exist, but the controller, the radio network and the central software usually come from one supplier. The TALQ Consortium defined its Smart City Protocol specifically to help "avoid vendor-lock-in" between central software and outdoor device networks ([TALQ](https://www.talq-consortium.org/)), which shows the problem is recognized but not solved at the device level.

## Users and context

| User | Need |
| --- | --- |
| Municipal street lighting and public works teams | Lower energy bills, fewer night patrols, a fault list that tells crews where to go, and freedom to change suppliers |
| Electric utilities that own streetlights | Measured energy per lamp, day-burner detection, remote switching during grid events |
| Road owners and lighting designers | Dimming that stays within the lighting class they set for each road |
| Residents and road users | Streets that are lit when people are on them, and fewer dark spots after faults |
| Smart city sensing projects (AirStreet, NoiseMap, CurbCount and others in this lab) | A powered, networked mounting point on existing poles |
| Community, campus and private-road operators (campuses, ports, car parks, housing associations) | The same functions at small scale without a city-wide contract |

### Operating environment

- Mounted on top of a cobra-head or post-top LED luminaire, typically 6 to 12 m above the road, in full sun, rain, ice and wind.
- Ambient temperature at the luminaire top from about -30 °C in winter to above 60 °C under summer sun (estimate; to be set per region).
- Supplied from the luminaire's mains feed, nominally 120 to 277 V AC at 50 or 60 Hz, with lightning and switching surges on long overhead or buried feeders.
- On some networks the feeder is switched at a cabinet, so the pole is unpowered in daytime; on others it is live 24 h.
- Radio path to a LoRaWAN gateway, often a TwinKit gateway or a public network, typically within 2 to 5 km in a city (estimate).
- Installed and replaced from a bucket truck by lighting crews, usually at the same time as other maintenance.

## Constraints

- Garage-buildable prototype for about $150 USD in parts (`project.yaml`), for the controller and one sensor head.
- Must plug into an existing standard receptacle with no rewiring of the luminaire.
- Must fail safe: if the controller or network fails at night, the lamp stays on.
- Must not reduce lighting below the level the road owner sets; LampNode implements a lighting policy, it does not choose one.
- Privacy: presence only. No images, audio or personal identifiers leave the device.
- Open interfaces: works with any LoRaWAN network server; payload format published.
- Mains work is done by qualified electricians; pole work by trained crews with the asset owner's permission.

## Out of scope

- Choosing lighting classes or light levels for roads; these belong to the road owner and local standards.
- Revenue-grade metering for billing; LampNode reports indicative energy, not a certified meter reading.
- Cameras, audio capture or identification of people or vehicles.
- A replacement for the luminaire's own surge protection or driver.
- 347 V and 480 V circuits in the first design; a later variant if a partner needs it (LPN-REQ-001 R2, LPN-DDR-001 D9).
- DALI-2 D4i dimming in the first design; a later variant if a partner's stock needs it (LPN-DDR-001 D5).
- A TALQ bridge; interoperability with central software belongs to CityTwin (LPN-DDR-001 D10).

## Prior work

- **Socket standards.** ANSI C136.41 defines the twist-lock photocontrol receptacle widely used on roadway luminaires in North America, including versions with extra contacts for dimming. Zhaga Book 18 defines "a standardized interface between an outdoor LED luminaire and a sensing/communication module that sits on the outside of the luminaire" ([Zhaga](https://www.zhagastandard.org/books/book18/)).
- **D4i drivers.** D4i LED drivers carry an intra-luminaire DALI bus with bus power for control devices, an optional 24 V auxiliary supply for higher-power devices such as radios, and data on energy, diagnostics and asset information (DALI Parts 251 to 253). D4i is compatible with both ANSI C136.41 and Zhaga Book 18 sockets ([DALI Alliance](https://www.dali-alliance.org/d4i/)).
- **Central software interoperability.** The TALQ Smart City Protocol links central management software with device networks from different vendors ([TALQ](https://www.talq-consortium.org/)).
- **Adaptive lighting evidence.** Dimming schedules can save more energy than lowering a road's lighting class ([Jägerbrand, 2016](https://www.mdpi.com/1996-1073/9/5/357)).
- **Commercial controllers.** Networked streetlight controllers are sold by many lighting and utility suppliers, generally as part of a proprietary network. A survey of open-hardware controllers has not yet been done (open question 1).
- **Lab siblings.** LampNode uses the same STM32WL-class LoRaWAN radio as FieldNode and the same 5-pole M12 sensor ports (the pinout is still open at FieldNode), and reports to TwinKit and CityTwin.

## Open questions

1. Are there open-hardware streetlight controllers to learn from or join, rather than start anew?
2. Socket: ANSI C136.41 7-contact first, Zhaga Book 18 later, is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (LPN-DDR-001 D1).
3. How common are cabinet-switched feeders in the first partner city? Hosted sensors there need their own storage (LPN-REQ-001 R13). The first partner itself is proposed, awaiting Amish (LPN-DDR-001 O1).
4. Will a lighting authority accept presence dimming on the roads chosen, and what floor level and hold time will it set?
5. Which 0 to 10 V and D4i drivers are in the partner's luminaire stock, and how do they behave when the control line is open?
6. What surge levels and certification does the asset owner require before a device is plugged into its network?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
