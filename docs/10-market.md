---
doc_id: CBC-MKT-001
title: CurbCount market and viability
project: CurbCount
doc_type: Market and viability
version: '0.1'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-10-31'
  author: Amish Chadha
  change: Opened in the kit 1.9.1 upgrade; prices checked on 2026-10-31
---

# CurbCount market and viability

Cities, residents' groups, business districts and researchers need counts of people on foot and on bicycles that today are taken by hand or bought as closed products; an open counter at about 274 USD in parts that sends no images would be unusual among them. The cost has not been checked against real quotes, and no comparable product price was found for camera analytics, so the viability of the price advantage is still to assess. Method: STANDARDS section 23. Prices and benchmarks are cited with the date checked.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| City transport departments | Planners and road safety engineers in cities that already run manual or loop counts; first candidate City of Toronto transportation services (CBC-DDR-002 O1), nothing agreed | Cycle and traffic counters: 'most counters range in price from $3000 to $10,000' (NZ Transport Agency summary on cycle counting; currency not stated, New Zealand context; checked 2026-10-31). Camera analytics and people counters: to assess | 274.00 (BOM, option A, indicative prices) | Continuous counts of people on foot and on bicycles for a fraction of the cost of a commercial counter, from a device whose firmware and sensor limits the public can inspect |
| Residents' groups and NGOs | Neighbourhood and active-travel groups that want independent evidence for a council meeting; any region with LoRaWAN coverage | No comparable price found for a counter a group can buy and audit: to assess | 274.00 per counter, plus a gateway or network access (cost to assess) | Evidence from a device they can read and rebuild, with no camera on the pole |
| Business districts and market managers | Footfall by hour and day on high streets and markets | Footfall counters: no cited price; to assess | 274.00 | Footfall and mode split without images of customers |
| Researchers and students | Universities and active-travel research groups that need open, documented count data and a device they can reproduce | Sensor alone: SparkFun MLX90640 110 degree breakout 64.95 USD (checked 2026-10-31); a radar evaluation module (TI IWR6843ISK-ODS) is listed without a price (checked 2026-10-31) | 274.00 for option A; option B about 234 without the radar module (module price to assess) | A documented 10-byte record, open tracker and CAD to modify; a clean base for new sensors |

## Open route

Who would build it: a city's own workshop or traffic-count contractor, a university engineering lab, a makerspace working with a residents' group, or an NGO with a technical volunteer. The parts are catalogue items and stock aluminium sections, the housing is printed, and the build plan (CBC-BLD-001) lists the order of work. The design spreads as files: CAD, drawings, BOM and firmware sketch under CERN-OHL-S-2.0 (hardware) and MIT (software), so any improvement to the hardware that is shared has to be shared back. What keeps it open is that licence and the public notice on every pole that points to the repository. A seller who assembles and places units on the market would take on the rules in the regulatory register (CBC-REG-001, G13); that is not part of this design.

## Viability notes

- Margin: the BOM sits 1.00 USD under the 275 USD value-engineering target (a control figure, not a limit); a price rise on any line breaks it, which is why the estimate is called indicative.
- The expensive line is the thermal array (65.00 USD); the FieldNode share (lines 1 to 3, 14 and part of 13) is 105.00 USD (CBC-DEC-001).
- Radar variant: cannot yet be shown to fit, because the module price and the 60 GHz rules are unknown (CBC-REG-001 G9).
- No sales, pricing strategy or business plan is proposed here; it is outside the TRL 3 paper stage.

## Sources

- NZ Transport Agency, summary page on cycle counting in New Zealand, https://nzta2.cwp.govt.nz/resources/sustainable-transport/cycle-counting-in-nz/summary, accessed 2026-10-31 (the page gives no date or currency).
- SparkFun, IR Array Sensor 110 degree FOV MLX90640, https://www.sparkfun.com/ir-array-sensor-110-degree-fov-mlx90640.html, accessed 2026-10-31.
- Texas Instruments, IWR6843ISK-ODS, https://www.ti.com/tool/IWR6843ISK-ODS, accessed 2026-10-31 (no price listed).
- `bom/bom.csv` for the indicative parts prices (CBC-CAL-001 J1).
