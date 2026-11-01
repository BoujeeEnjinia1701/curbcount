---
doc_id: CBC-URS-001
title: CurbCount user requirements
project: CurbCount
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: Opened in the kit 1.9.1 upgrade; the needs of the six users in CBC-PRB-001 written from their side, split out of the old requirements
---

# CurbCount user requirements

What the people who would use or live with a CurbCount counter need, written from their side. Product requirements that meet these needs are in CBC-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix (`03b-traceability.md`). Method: STANDARDS section 22. These needs were drawn from the user table in CBC-PRB-001 and have not yet been checked with a co-design partner (CBC-DDR-002, O1 names the first candidate).

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Deployment and assembly | Fit to an existing pole | Two people can fit the counter to a street pole that is already there, without drilling, welding or touching its wiring | High | Asset owner (PRB users table) |
| UR-002 | Deployment and assembly | Light enough to carry up | The parts can be lifted and fitted from a mobile platform by one person at a time | Medium | Asset owner (PRB users table) |
| UR-003 | Performance | Count by mode and direction | People on foot, people on bicycles and scooters, and motor vehicles are counted separately, for each direction along the street | High | City transport planner; road safety engineer |
| UR-004 | Performance | Counts close to a manual count | The counts are close enough to a manual count to show whether a change to the street made a difference | High | City transport planner; researcher or student |
| UR-005 | Performance | Whole street from one pole | One counter sees the sidewalk, the bike lane and the nearest traffic lane | High | City transport planner |
| UR-006 | Safety | No images, no identity | No image, sound or personal identifier leaves the device, and the sensor cannot show a face or a number plate even if someone wanted it to | High | Residents' group or NGO |
| UR-007 | Usability | Open, documented counts | The counts arrive in a short record whose format is published, in fixed time bins | Medium | Researcher or student; city transport planner |
| UR-008 | Usability | Set up and aim check on site | The crew can check the aim and confirm an uplink on site with a laptop or phone, with no special software | Medium | City transport planner |
| UR-009 | Environment and durability | Counts through the seasons | The counter works in the temperatures of the site through the year, in sun and in shade | High | City transport planner; business district manager |
| UR-010 | Environment and durability | Runs without pole power | The counter runs from its own panel and cell, including through dull winter days and short spells with no sun | High | Asset owner (street lights switch off in the day) |
| UR-011 | Environment and durability | Survives five years outdoors | Rain, dust, sun and wind do not stop it working for years | High | Asset owner |
| UR-012 | Maintenance | Rare, simple service | A cell change is the only routine service in five years | Medium | Asset owner |
| UR-013 | Cost | Cheap enough for many poles | The parts cost is low enough that a city, a group or a university can deploy several counters | High | City transport planner; residents' group; business district manager |
| UR-014 | Regulatory | Legal radio use | The radio link stays within the licence-free limits where it is used | Medium | City transport planner |
| UR-015 | Safety | Stays on the pole, safe to pass | The counter does not fall, twist or shed parts onto the street in wind, and adds no hazard for a person below | High | Asset owner; residents' group or NGO |
| UR-016 | Usability | Public can see what it is | A resident can read what the device counts and find the open design from the pole | Medium | Residents' group or NGO |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
