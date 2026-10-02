---
doc_id: CBC-PRB-001
title: CurbCount problem statement
project: CurbCount
doc_type: Problem statement
version: "0.8"
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; cost constraint and open questions reflect CBC-CAL-001 and CBC-DDR-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Stronger sources
- version: "0.6"
  date: '2026-09-30'
  author: Amish Chadha
  change: Parts cost updated to the design for construction (CBC-DDR-003, CBC-CAL-001 v0.3)
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "First partner question answered by Amish's 2026-10-02 decision (first candidate to approach: City of Toronto transportation services)"
---

# CurbCount problem statement

Cities decide how to share street space with little evidence of how many people walk and cycle there, and the tools that could supply that evidence either cost too much to deploy widely or rely on cameras that residents reasonably distrust.

## The problem

Walking and cycling carry a large share of trips and a large share of road deaths, yet they are the least counted modes. More than half of the 1.19 million road deaths each year are pedestrians, cyclists and motorcyclists; pedestrians alone account for 23 % and cyclists for 6 % ([WHO, 2023](https://www.who.int/news/item/13-12-2023-despite-notable-progress-road-safety-remains-urgent-global-issue)). In England, walking makes up 29 % of all trips ([Department for Transport, 2024](https://www.gov.uk/government/statistics/walking-and-cycling-statistics-england-2023)). In Africa, more than a billion people walk or cycle every day, yet most countries still lack policies, infrastructure and budgets for these users ([UNEP](https://www.unep.org/resources/report/walking-and-cycling-africa-evidence-and-good-practice-inspire-action)).

Motor traffic is counted routinely with loops and tubes. People on foot and on bicycles are usually counted by hand for a few hours a year, or not at all. Without continuous counts a city cannot show whether a new bike lane or a wider sidewalk changed anything, cannot compute crash exposure at a crossing, and cannot defend a street redesign against the claim that "nobody walks here."

Video analytics can count all modes, but a camera on a pole captures faces, number plates and behavior. Even when the vendor processes video on the device, residents cannot inspect that claim, and a firmware change can turn a counter into a surveillance camera. In the European Union, data protection law requires data protection by design and by default ([Regulation (EU) 2016/679, Article 25](https://eur-lex.europa.eu/eli/reg/2016/679/oj); [text of Article 25](https://gdpr-info.eu/art-25-gdpr/)), and the AI Act prohibits real-time remote biometric identification in publicly accessible spaces for law enforcement except in narrow cases ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj); [text of Article 5](https://artificialintelligenceact.eu/article/5/)). Public tolerance for image capture on streets is low and falling.

The gap is a counter that sees too little to identify anyone, by physics rather than by policy, that is cheap enough to deploy on many poles, and that is open so a city or a residents' group can check exactly what it does.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| City transport planner | Continuous counts by mode and direction, before and after a change | Main streets, school routes, new bike lanes |
| Road safety engineer | Exposure (people per hour) at crossings and junctions to turn crash counts into rates | Crossings, often paired with CrossSafe |
| Residents' group or NGO | Independent evidence to bring to a council meeting, from a device they can inspect | Neighborhood streets, community-led audits |
| Business district or market manager | Footfall by hour and day | High streets, markets |
| Researcher or student | Open, documented count data and a device they can reproduce | Universities, active travel research |
| Asset owner (pole, utility) | A light, clamp-on device that needs no drilling or wiring changes | Street lighting and signal poles |

Operating context: mounted on an existing street pole at 4 to 5 m, outdoors for years, in sun, rain, dust and temperatures from about -20 °C to +50 °C (estimate of the design range), often with no power available at the pole during the day (street lights switch off).

## Constraints

- Garage-buildable prototype, a value-engineering target of $275 USD in parts (a hypothetical control target, not a limit), set by Amish on 2026-09-25 (CBC-DDR-002). The estimated cost of the constructable design is $274.00, $1.00 under the target (CBC-CAL-001 v0.4).
- Built on the lab's shared **FieldNode** power and radio core, as the FieldNode README lists CurbCount among its intended users.
- Privacy by design: no images, audio recordings or personal identifiers leave the device; only aggregate counts are stored or sent.
- Clamp-on mounting with no drilling, welding or electrical connection to the pole.
- Open hardware (CERN-OHL-S-2.0) and open firmware (MIT), so any city or group can audit the device.

## Prior work

- **Commercial counters.** Inductive loops, pneumatic tubes, passive infrared beams and camera analytics are all in service. Loops and tubes count vehicles and bicycles well but not people on foot; infrared beams count people but not direction or mode reliably; cameras count everything but capture images. Most commercial units are closed and priced for city procurement.
- **Low-resolution thermal arrays.** Parts such as the Melexis MLX90640 give a 32 x 24 pixel far-infrared image with a 110 x 75 degree wide-angle option ([Melexis](https://www.melexis.com/en/product/MLX90640/Far-Infrared-Thermal-Sensor-Array)). At pole height each pixel covers roughly 0.3 m of ground, too coarse to show a face.
- **mmWave radar.** Single-chip 60 GHz radars such as the TI IWR6843 are offered with a people counting and tracking reference design for indoor and outdoor use ([Texas Instruments](https://www.ti.com/product/IWR6843)). Radar works in darkness and heat but costs more and draws more power.

No open, auditable, pole-mounted counter combining these parts with a solar-powered LoRaWAN core was found.

## Out of scope

- Identifying, re-identifying or tracking individuals across sensors.
- Speed enforcement or any enforcement use.
- Counting more than the nearest traffic lane of motor vehicles.
- Occupancy of parking or loading bays (see LoadZone).

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

## Open questions

- Which partner and street first: a city transport department, a residents' group or a university? Decided by Amish, 2026-10-02 (CBC-DDR-002, O1): a city transport department that already runs manual or loop counts on a street with a bike lane and 60 to 140 mm poles, so its counts can check the counter, with the first trial in a season with air under 20 °C. The first candidate to approach is the City of Toronto's transportation services, which publishes its traffic count data; nothing is agreed.
- Count interval: 15-minute bins, decided by Amish on 2026-09-25 (CBC-DDR-001 D5). A partner should confirm planners do not need a finer interval.
- Public notice: a plate on each pole with a link to this repository, decided by Amish on 2026-09-25 (CBC-DDR-001 D7).
- Hot climates: CBC-CAL-001 shows a thermal-only counter goes blind for much of a hot day. Amish decided on 2026-09-25 that the thermal build is for temperate sites and that the radar variant is brought forward for any hot partner city (CBC-DDR-002). Which partner cities are hot enough to need it depends on the partner choice above.
