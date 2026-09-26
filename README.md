# LampNode

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $150 USD · **Difficulty:** 3 of 5

An open streetlight controller that dims LED streetlights by schedule and presence, reports faults and hosts other city sensors on the lamp pole.

![LampNode concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement LPN-DWG-001 (PDF)](cad/drawings/LPN-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Many LED streetlights already have a twist-lock socket on top, built for a photocell, and the D4i driver standard supports both the NEMA/ANSI C136.41 and the Zhaga Book 18 sockets ([DALI Alliance](https://www.dali-alliance.org/d4i/)). A controller that plugs into that socket can dim the lamp, measure its energy and report faults without anyone opening the luminaire or the pole. LampNode uses that socket, the 0 to 10 V dimming input most LED drivers already have, and a small radar head under the arm that raises the light only when someone is coming. Because the controller already has mains power and a radio on the pole, the same head offers two powered ports for other city sensors, so a street can gain air, noise or traffic sensing without new wiring.

It is open and garage-buildable because the main problem with smart streetlights is not the electronics but lock-in: the controller, network and software usually come from one supplier. LampNode uses a standard socket, the same LoRaWAN radio as the lab's FieldNode, and a published message format, so a city, a utility or a campus can build, inspect or replace any part of it and read its data with any LoRaWAN server, including TwinKit and CityTwin.

## Burning platform

Streetlights mostly burn at full power all night, and cities often cannot see what they use: the US Energy Information Administration says it has no estimate of electricity use for public street and highway lighting ([EIA](https://www.eia.gov/tools/faqs/faq.php?id=99&t=3)). Yet the savings from dimming are large. On 14 LED-lit Swedish roads, a dimming schedule alone could save about 49 % of the energy ([Jägerbrand, 2016](https://www.mdpi.com/1996-1073/9/5/357)). Meanwhile citizen observations from 2011 to 2022 are consistent with the night sky brightening by 7 to 10 % per year ([Kyba et al., 2023, via GFZ](https://www.gfz.de/en/press/news/details/citizen-scientists-report-global-rapid-reductions-in-the-visibility-of-stars-from-2011-to-2022)).

Faults are still found by people. New York City maintains nearly 400,000 streetlights and asks residents to call 311 to report problems ([NYC DOT](https://www.nyc.gov/html/dot/html/infrastructure/streetlights.shtml)). Networked controllers exist, but the industry's own interoperability body describes its protocol as a way to "avoid vendor-lock-in" ([TALQ](https://www.talq-consortium.org/)), which is why an open device matters.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal street lighting and public works | Night dimming, fault lists for crews, and energy data per lamp on residential and collector roads |
| Electric utilities that own streetlights | Day-burner detection, measured energy per lamp, remote switching during grid events |
| Road and highway authorities | Adaptive lighting on low-traffic roads within the lighting class they set |
| Campuses, ports, car parks and industrial sites | Presence dimming on private roads and yards with their own LoRaWAN gateway |
| Smart city sensing | A powered, networked mount for air, noise and traffic sensors (AirStreet, NoiseMap, CurbCount) |
| Housing associations and private estates | Lower lighting bills and fault reports on private streets |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | Large networks with faults still reported by residents: New York City maintains nearly 400,000 streetlights and asks residents to call 311 about problems ([NYC DOT](https://www.nyc.gov/html/dot/html/infrastructure/streetlights.shtml)); LampNode targets the NEMA/ANSI C136.41 socket, which D4i drivers also support ([DALI Alliance](https://www.dali-alliance.org/d4i/)) |
| Sweden and the Nordic countries | Long winter nights; a dimming schedule could save about 49 % on the Swedish roads studied ([Jägerbrand, 2016](https://www.mdpi.com/1996-1073/9/5/357)) |
| European Union | Luminaires with Zhaga Book 18 sockets and D4i drivers can power and host a module with no rewiring ([DALI Alliance](https://www.dali-alliance.org/d4i/)); a Zhaga variant of LampNode is an open question |
| India | By June 2024 the Street Lighting National Programme had installed more than 13 million LED streetlights in 29 states and union territories, saving an estimated 8,806 GWh a year ([PIB, 2024](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2040102&reg=48&lang=2)); a retrofit controller could add presence dimming and fault reports to that installed base |
| Philippines | In Quezon City, street lighting made up 65 % of the city's electricity costs and 5 % of its overall budget ([World Bank, 2017](https://blogs.worldbank.org/en/energy/led-street-lighting-unburdening-our-cities); [case study](https://documents.worldbank.org/curated/en/842031477930270833/)), so every hour of dimming shows up in the city's accounts |
| Brazil | Public lighting uses about 4 % of the country's electricity and 10 to 40 % of municipal energy budgets; Belo Horizonte is upgrading 178,000 streetlights to LED under a 20-year PPP contract ([ESMAP](https://www.esmap.org/node/57541)), a term over which open, multi-vendor controllers would let a city change suppliers |

## What sparked the idea

The starting point was Detroit. By mid-2013 more than half of the city's 88,000 streetlights were estimated to be out; the relighting that began in April 2014 replaced them with 65,000 LED lights for $185 million ([US Department of Energy](https://www.energy.gov/eere/ssl/articles/detroit-street-lighting-report)) and was finished in December 2016 ([Michigan Public, 2016](https://www.michiganpublic.org/news/2016-12-16/detroit-celebrates-65-000-new-led-streetlights)). In May 2019 the city's Public Lighting Authority sued the manufacturer over about 20,000 of those fixtures, a third of the new system, that were dimming and burning out early ([Michigan Public, 2019](https://www.michiganpublic.org/law/2019-05-07/some-of-detroits-new-led-streetlights-are-burning-out-city-sues-manufacturer)). Even a brand-new, efficient network could degrade at scale before its owner had the data to see it. A small controller on each lamp that measures its power and reports a lamp that is out, cycling or drawing the wrong power would let the owner see such faults as they develop, and an open design would let any city fit, inspect and repair it without tying the network to one supplier.

## Problem

Streetlights burn at full power all night, faults are reported by residents, and proprietary controllers lock cities into one vendor.

## Concept

An open streetlight controller that dims LED streetlights by schedule and presence, reports faults and hosts other city sensors on the lamp pole.

A twist-lock controller replaces the photocell on the luminaire and drives its 0 to 10 V dimming input; a sensor head clamped under the arm carries a 24 GHz radar for presence and two powered M12 ports for other sensors; status and faults go out every 15 min over LoRaWAN.

TRL 3 calculations ([LPN-CAL-001](docs/04-calcs/01-sizing.md)) put a 100 W luminaire at 40° N at about 432 kWh a year under a photocell and 275 to 285 kWh with the reference presence profile, a saving of 34 to 36 % against a 35 % target. The controller draws 0.68 W on average and the parts cost $130 against the $150 budget. No requirement is clearly missed, but four are at risk on paper: relay inrush, presence detection in rain and wind, the energy saving (kept at a 35 % target with the risk accepted) and the temperature margin in full sun. Power for hosted sensors is met on paper because the firmware limits the ports to 2.5 W above 50 °C inside. 347 V and 480 V circuits, DALI-2 D4i dimming and a TALQ bridge are later variants or sibling scope. The design choices were decided by Amish on 2026-09-25 ([LPN-DDR-001](docs/decisions/0001-trl2-review-decisions.md), [LPN-DDR-002](docs/decisions/0002-recommendations-accepted.md)); only the first co-design partner is still open. See the [requirements](docs/03-requirements.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Twist-lock base for the ANSI C136.41 7-contact receptacle
- 385 V class surge stage, isolated 12 V power supply and a normally closed (fail-on) relay closed at the voltage zero crossing
- Energy metering (indicative, not revenue grade), calibrated once at build
- STM32WL-class controller with LoRaWAN radio (shared with FieldNode), TCXO clock and tilt sensor
- 0 to 10 V dimming output and ambient light sensor
- Sensor head under the arm with a 24 GHz radar presence sensor with direction (I/Q) output
- Two sealed 5-pole M12 expansion ports, 12 V SELV, 3 W total (2.5 W above 50 °C inside)

The parametric model is in [cad/src/model.py](cad/src/model.py), with STEP and STL exports in `cad/step/` and `cad/stl/`. The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Mains wiring must be done or checked by a qualified electrician and follow local electrical code. LampNode connects to up to 277 V AC in the luminaire socket; a prototype must not go on a public lighting network until it has passed the tests the asset owner requires. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.
>
> A controller fault must never leave a street dark: the relay fails on, and light levels are set by the road owner, not by LampNode. The socket has no earth contact, so surge protection is line to neutral only. Privacy by design: the radar reports motion only; no images, audio recordings or personal identifiers leave the device.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (LPN-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `LPN-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
