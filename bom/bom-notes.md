# BOM notes

- Item numbers match the callouts in `media/exploded.png` and `media/cutaway.png`. Item 16 has no callout. Item 6 (metering) is small and sits under its callout in the exploded view.
- All costs are indicative USD prices for single prototype quantities, with a supplier or supplier type on every line. No supplier quotes have been obtained; replace them before any purchase decision.
- Total at TRL 3: **$130.00** for 16 lines: controller (items 1 to 9) $68.00, sensor head, cable and ports (items 10 to 15) $56.00, hardware (item 16) $6.00. The `project.yaml` budget is $150, unchanged; margin $20.00. `docs/04-calcs/sizing.py` reads this file and checks the total (LPN-CAL-001 section 13).
- Changes from TRL 2 ($124): TCXO real-time clock and charge-pump relay coil drive in line 7 (+$3); normally closed relay rated for 80 A inrush in line 5 (+$2); 385 V class varistor with TVS diodes and no gas discharge tube in line 3 (+$1), because the twist-lock socket has no earth contact. The M12 connectors in lines 10 and 14 are now 5-pole to match FieldNode (same price); the radar in line 12 now needs I/Q output (same price). These are engineering proposals from LPN-CAL-001, awaiting Amish's confirmation (LPN-DDR-001 O4 to O8).
- The luminaire, its receptacle, the arm and the pole are existing street furniture and are not costed.
- Installation labor (bucket truck, electrician, traffic management) is not included.
- Metering is indicative, not revenue grade; each unit needs a one-point calibration against a bench power meter (R8).
