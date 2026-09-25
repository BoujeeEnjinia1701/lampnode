# LampNode

**Area:** Smart Cities · **Status:** Concept · **Prototype budget:** about $150 USD · **Difficulty:** 3 of 5

An open streetlight controller that dims LED streetlights by schedule and presence, reports faults and hosts other city sensors on the lamp pole.

## Concept rationale

An open controller saves energy and turns every pole into a place to host sensors.

## Burning platform

Street lighting is often one of a city's largest electricity costs.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab.

## Problem

Streetlights burn at full power all night, faults are reported by residents, and proprietary controllers lock cities into one vendor.

## Concept

An open streetlight controller that dims LED streetlights by schedule and presence, reports faults and hosts other city sensors on the lamp pole.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Standard lamp pole connector module
- Dimming driver interface
- Presence sensor
- Energy metering
- Radio and controller
- Sensor expansion port

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Mains wiring must be done or checked by a qualified electrician and follow local electrical code. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
