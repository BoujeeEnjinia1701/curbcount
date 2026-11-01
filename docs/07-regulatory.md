---
doc_id: CBC-REG-001
title: CurbCount regulatory and standards register
project: CurbCount
doc_type: Regulatory and standards register
version: '0.1'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-10-31'
  author: Amish Chadha
  change: Opened in the kit 1.9.1 upgrade
---

# CurbCount regulatory and standards register

The design is a privacy-first counter, so the rules that matter most are data protection and radio use; the radar option adds a 60 GHz transmitter whose rules are still to assess. This register is not legal advice: anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Regulation (EU) 2016/679 (GDPR), Article 25, data protection by design and by default | European Union | Privacy built into the design; processing only what is needed | No image, audio or identifier leaves the device and thermal frames are held in RAM only (PR-004, STM S1 and S20). Whether a count record is personal data at all is to assess | Design lead; data protection adviser | Met by design; legal view to assess |
| G2 | Regulation (EU) 2024/1689 (AI Act) | European Union | Rules on AI systems and prohibited practices, including real-time remote biometric identification in public spaces | The counter identifies no one and cannot resolve a face (7.6 px/m). Classification of the tracker under the Act is to assess | Design lead; regulatory consultant | To assess |
| G3 | IEC 62676-4 (video surveillance systems, application guidelines), pixel density levels | International | Pixels per metre needed to detect, recognise or identify a person | Used as the yardstick for PR-004: 7.6 px/m against 25 px/m to detect and 250 to identify. Not a certification | Design lead | Met by design (CAL-001 B) |
| G4 | EU licence-free 863 to 870 MHz band and its 1 % duty-cycle rule for LoRaWAN uplinks | European Union | Airtime limit per device per hour | 0.82 s/h at SF9 against 36 s/h (PR-018). The governing ETSI standard and the regional LoRaWAN parameters are researched once in the FieldNode repo; the number is not repeated here | Design lead; FieldNode project | Met by design (CAL-001 G); standard number to assess |
| G5 | US licence-free 902 to 928 MHz band under 47 CFR Part 15 and the 400 ms dwell limit in the LoRaWAN US915 plan | United States | Dwell time and power of uplinks | 371 ms at DR0 against 400 ms (PR-018). Section of Part 15 and any certification of the radio module to assess; FieldNode owns the radio | Design lead; FieldNode project | Met by design (CAL-001 G); certification needed later |
| G6 | IEC 60529 (IP code), degrees of protection of enclosures | International | Ingress of dust and water | IP65 target for the enclosure and the gasketed head (PR-011). Tested at TRL 4, not now | Design lead | Applies; test at TRL 4 |
| G7 | Lithium iron phosphate cells: cell safety and transport rules (cell maker datasheet; transport classification of lithium cells) | International | Charge limits, protection and shipping of cells | One 6 Ah cell with a fused holder and NTC lockout (BOM lines 2 and 3); charging only above 0 degrees C (STM S8). Standard numbers for the cell and for transport to assess | Design lead; FieldNode project | To assess |
| G8 | Permission to attach equipment to a street pole | Local, set by the pole owner (city, utility or lighting authority) | Who may fit what to a pole, load and electrical rules | Clamp-on, no drilling or wiring (PR-014); the owner's attachment rules and any structural sign-off are to assess with the first partner | Partner city; asset owner | To assess |
| G9 | 60 GHz radar emission rules (option B only) | Each country of use | Transmit power, bandwidth and certification for short-range radar in the 60 GHz band | Option B adds a 60 GHz transmitter. The governing rules in the EU, the US and Canada are not researched or cited here; do not claim compliance | Design lead; regulatory consultant | To assess (option B only) |
| G10 | ICNIRP 2020 guidelines for limiting exposure to electromagnetic fields, 100 kHz to 300 GHz | International | Public exposure limits (10 W/m2 above 6 GHz) | Option B: about 12 mW/m2 at head height on a 1 W overestimate (STM S21), far below the limit. Value to confirm against the guideline text | Design lead | Met by design on a first-order check (option B only); to confirm |
| G11 | Local wind-load and roadside-object rules (height above the roadway, clearance from the carriageway) | Local | Loads on poles; clearances over road and sidewalk | Head at 4.3 m, 35 m/s gust check (PR-015, CAL-001 H). Local codes to assess with the partner | Partner city; asset owner | To assess |
| G12 | Local rules on signage and notice of public sensing | Local | Whether and how a public notice is required | A notice plate on every pole (PR-019, CBC-DDR-001 D7). Whether the wording meets local rules is to assess | Partner city; legal adviser | To assess |
| G13 | Substance and waste rules for electronics (for example the EU RoHS directive 2011/65/EU) | European Union | Restricted substances in electrical equipment | Applies to whoever places an assembled counter on the market; an open design published as files is not that. Bought parts are the maker's choice | Builder | To assess if sold |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Notes

- Standards shared across the FieldNode family (radio, cells, enclosure) are researched once in the FieldNode repo and are not copied here; this register names them and states how CurbCount meets them.
- No standard number, classification or limit in this register was invented: where the governing number was not confirmed in this session, the row says "to assess".
- Option B (G9, G10) applies only if the radar head is carried forward.

## Sources

- Regulation (EU) 2016/679, https://eur-lex.europa.eu/eli/reg/2016/679/oj, as cited in CBC-PRB-001.
- Regulation (EU) 2024/1689, https://eur-lex.europa.eu/eli/reg/2024/1689/oj, as cited in CBC-PRB-001.
- ICNIRP, Guidelines for limiting exposure to electromagnetic fields (100 kHz to 300 GHz), *Health Physics* 118(5), 2020.
- FieldNode repository documents for radio and cell rules (not copied).
- The remaining rows cite the rule by name only; their texts were not read in this session, hence "to assess".
