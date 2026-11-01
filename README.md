# CurbCount

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827) [![DOI](https://zenodo.org/badge/1388476064.svg)](https://zenodo.org/badge/latestdoi/1388476064) [![REUSE compliant](https://github.com/BoujeeEnjinia1701/curbcount/actions/workflows/reuse.yml/badge.svg)](https://github.com/BoujeeEnjinia1701/curbcount/actions/workflows/reuse.yml) [![Archived in Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/BoujeeEnjinia1701/curbcount/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/BoujeeEnjinia1701/curbcount)

**Area:** Smart Cities · **TRL:** 3 of 9 (proof of concept on paper) · **Value-engineering target:** about $275 USD · **Difficulty:** 3 of 5

A privacy-safe counter for people, bicycles and vehicles at street level that uses on-device detection and sends only counts, never images.

![CurbCount: privacy-safe street counter for people, bikes and vehicles, product render](media/render-hero.png)

[Exploded render](media/render-exploded.png) · [Detail render](media/render-detail.png) · [Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/CBC-DWG-001.pdf) · [Prototype build plan](docs/05-build-plan.md) · [Design decisions](docs/06-design-decisions.md) · [Calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Counts without images give planners evidence while respecting residents. CurbCount uses a 32 x 24 pixel thermal array instead of a camera: from 4.3 m up it images a person's head at about 7.6 pixels per meter (8.5 for a 2 m person) and a number plate at under 2 pixels, so the sensor cannot capture a face or a plate even if its firmware were changed. The FieldNode core's own processor turns heat blobs into counts of people, cyclists and vehicles by direction, and only 15-minute counts leave the device.

It is open and garage-buildable because trust is the point. A city, a residents' group or a researcher can read the firmware, inspect the hardware and build their own from off-the-shelf parts, clamped to an existing pole on the lab's shared FieldNode power and radio core.

## Burning platform

Street redesign decisions are contested, and counts of people walking and cycling are usually missing. Road crashes kill about 1.19 million people a year, and more than half are pedestrians, cyclists and motorcyclists; pedestrians alone are 23 % and cyclists 6 % ([WHO, 2023](https://www.who.int/news/item/13-12-2023-despite-notable-progress-road-safety-remains-urgent-global-issue)). WHO also reports that 80 % of the world's roads fail to meet pedestrian safety standards (same source), and 92 % of road deaths occur in low- and middle-income countries ([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries)).

Fixing streets for people on foot and on bicycles needs evidence of how many use them, before and after a change. Motor traffic is counted routinely; walking and cycling rarely are, and the camera systems that could count them raise privacy concerns that stall deployment. The global goal of at least halving road deaths and injuries by 2030 ([WHO Global status report on road safety 2023](https://www.who.int/publications/i/item/9789240086517)) leaves little time.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal transport planning | Before and after counts for new bike lanes, wider sidewalks and school streets |
| Road safety engineering | Pedestrian and cyclist exposure at crossings, to turn crash counts into risk rates (with CrossSafe) |
| Retail and business districts | Footfall by hour and day on high streets and markets |
| Parks, trails and tourism | Use of promenades, greenways and trail heads without cameras |
| Transit operators | Walking and cycling flows on station access routes |
| Research and education | Open, reproducible active travel counts for universities and schools |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Sub-Saharan Africa | More than a billion people in Africa walk or cycle every day, about 56 minutes a day against a global average of about 44 minutes, yet most countries lack policies and budgets for them ([UNEP](https://www.unep.org/resources/report/walking-and-cycling-africa-evidence-and-good-practice-inspire-action)) |
| India | Road crashes took about 300,000 lives in 2016, and most of those dying are pedestrians, cyclists and motorcyclists ([WHO India](https://www.who.int/india/health-topics/road-safety)) |
| Latin America and the Caribbean | In the Americas, motorcyclists, pedestrians and cyclists rose from 39 % to 47 % of road deaths between 2009 and 2021 ([PAHO](https://www.paho.org/en/topics/road-safety)) |
| United States | 7,522 pedestrians were killed in 2022, 18 % of all traffic deaths ([NHTSA](https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813590)) |
| England | Walking is 29 % of all trips and cycling 2 % ([Department for Transport, 2024](https://www.gov.uk/government/statistics/walking-and-cycling-statistics-england-2023)); councils need counts to justify active travel schemes |
| European Union | Data protection by design is a legal duty ([Regulation (EU) 2016/679, Article 25](https://eur-lex.europa.eu/eli/reg/2016/679/oj); [text of Article 25](https://gdpr-info.eu/art-25-gdpr/)), which favors counters that cannot capture personal data at all |

## What sparked the idea

The idea traces back to Toronto's Quayside waterfront project. In October 2018 Ann Cavoukian, the former Ontario privacy commissioner who wrote the privacy-by-design framework the project had adopted, resigned as its adviser because the proposed data trust could approve collection of data that was not de-identified at source. In her resignation letter she warned that such data would create "another central database of personal information (controlled by whom?)" ([The Globe and Mail, 2018](https://www.theglobeandmail.com/business/article-privacy-expert-ann-cavoukian-resigns-from-sidewalk-toronto-smart-city/)). CurbCount takes the lesson literally: de-identification at source should be a property of the sensor, not a policy promise, so it uses a sensor too coarse to capture a face in the first place.

## Problem

Cities plan streets with little data on walking and cycling, and camera-based counting raises privacy concerns.

## Concept

A privacy-safe counter for people, bicycles and vehicles at street level that uses on-device detection and sends only counts, never images.

A thermal array on a short arm looks down over the sidewalk, bike lane and nearest traffic lane; a standard FieldNode core (one LiFePO4 cell, 6 W panel) reads the array, tracks heat blobs in fixed-point firmware on its STM32WL, counts them by class and direction, and sends a 10-byte record every 15 minutes over LoRaWAN to TwinKit or any LoRaWAN server. The TRL 3 calculations ([CBC-CAL-001](docs/04-calcs/01-sizing.md)) give 0.10 W average from the cell, 6.2 days of counting without sun, a footprint 12.8 m across the street and 6 to 7 m along it, which covers a 3 m sidewalk, a 2 m bike lane and the nearest lane, 5.3 kg on the pole and an estimated $274.00 in parts against the $275 value-engineering target. No requirement is unmet on paper; three are at risk: counting fast cars (4.2 frames at 50 km/h), people walking close together, and counting on sunlit pavement. The thermal build is for temperate sites; a hot-climate city would use a radar variant. See the [requirements](docs/03-requirements.md) and the [decision record](docs/decisions/0002-recommendations-accepted.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## STEM check

Thirty-one claims are checked ([CBC-STM-001](docs/01b-stem-check.md)): 13 are within known science, 14 are plausible and need a measurement at TRL 4, and 4 fail with a fix proposed to Amish, so the check stays open. The failures all touch the shared FieldNode core: a car's warm hood is in the thermal array's field for 3.2 frames, not the 4 the tracker needs (S5); a LiFePO4 cell may not be charged below 0 degrees C, so the node is energy neutral only where the winter air stays above about 0 degrees C (S8); and, for the radar option, a shared cell above its charge limit on hot days (S26) and a charger set for 1.5 A under a 20 W panel (S28). The radar option's first energy budget also failed (the radar drew 32 Wh/day against 14.5 Wh/day stored) and was fixed under Amish's standing instruction by running it in frame bursts (CBC-DEC-001 C1). An independent reviewer refuted three rows (S5, S20, S23) and weakened several more; all were corrected or restated.

## Concept options

![Two ways to count people at the curb, side by side at one scale](media/options.png)

Option A, the thermal array head (the current design, unchanged), scores 121 of 165; option B, a 60 GHz radar head, scores 110. They are within 10 %, so both go to Amish without a pick (CBC-OPT-001, CBC-DDR-004). Both are modelled at the same level of detail (A 127 parts, 4.8 kg; B 128 parts, 5.2 kg, from `cad/fidelity.json`).

## Key components

- Low-resolution thermal array (32 x 24 px, 110 x 75° lens, wide axis across the street) behind an HDPE window; mmWave radar as the hot-climate variant (option B, modelled)
- FieldNode power and radio core, standard: one LiFePO4 cell, 6 W panel, STM32WL running the tracker (an ESP32-S3 head is kept on paper as a fallback)
- Aluminum sensor arm, pole-top panel mount and stainless band clamps
- Public notice plate on the pole

The priced bill of materials is in [bom/bom.csv](bom/bom.csv); the parametric model of both options, with every bolt, nut and screw as its own part, is [cad/src/model.py](cad/src/model.py).

## Building the prototype

The [prototype build plan](docs/05-build-plan.md) shows how to build the first CurbCount, component by component, with a making sketch for each made part and a picture for every assembly step. Nothing is welded: the saddle plates seat on the pole through bent V-saddles and are held by band clamps, the arm and the pole-top mount are bolted from aluminium sheet, angle, bar and tube, and the sensor head and its window frame are 3D printed. The FieldNode core is built to FieldNode's own plan. Decisions still open are listed in the [design decisions register](docs/06-design-decisions.md).

![CurbCount prototype: every component, pulled apart and numbered in build order](docs/05-build-plan/overview.png)

## Safety

> Privacy by design: no images, audio recordings or personal identifiers leave the device; only aggregate counts or levels are stored. Check local data protection law before any deployment. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.
>
> The node contains a LiFePO4 cell: keep it fused and charge only within the cell maker's temperature limits. Fit safety lanyards to the panel and sensor head so nothing can fall on people below.

## Repository layout

```
docs/                 controlled documents (PRB, STM, OPT, PRC, URS, PRS, RTM, CAL, BLD, DEC, REG, FEA, RSK, MKT, PLN, DDR) and REVIEW.md
docs/04-calcs/        sizing.py (CBC-CAL-001) and stem_check.py (CBC-STM-001)
cad/src/model.py      parametric model of options A and B (kit 1.9, detail level D3)
cad/src/              cc_parts.py, sheets.py, build_plan_media.py, concept_media.py, product_model.py
cad/step/, cad/stl/   STEP per part and per assembly for every option; STL of each option
cad/drawings/         CBC-DWG-001 general arrangement and CBC-DWG-101 to 116 making sketches
bom/bom.csv           priced bill of materials
media/                concept media and renders
.kit/                 shared documentation kit 1.9.1 (do not edit here)
```

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CBC-PRC-001 for the precis), a version and a revision history. Run `python .kit/render.py --check` to validate them, `python .kit/cad_check.py --export` for the CAD fidelity check and `python docs/04-calcs/sizing.py` for the calculations. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CBC-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
