---
doc_id: CBC-BLD-001
title: CurbCount prototype build plan
project: CurbCount
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (CBC-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target; cross-references updated
---

# CurbCount prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The three groups (enclosure, arm and head, pole-top mount) are drawn closer together than they sit on the pole.*

The prototype is one CurbCount counter built on a 2 m length of street pole in the workshop. It has three groups that each clamp to the pole without drilling it: a FieldNode enclosure on an aluminium saddle plate on the sidewalk side; an aluminium arm on a second saddle plate on the road side, carrying a printed sensor head with the thermal array looking down through a plastic film window; and a 6 W solar panel on a bolted pole-top mount. Two cables join them, tied to the pole, and a small notice plate tells the public what is counted. Figure 1 shows the 26 components in the order you make or fit them. Sixteen are made in a small workshop by sawing, drilling, filing, tapping and bending aluminium sheet, angle, bar and tube, and by 3D printing three parts; the FieldNode enclosure is bought and drilled; the rest is bought. Nothing is welded. The parts cost about $274 from the bill of materials.

> **Safety:** The prototype holds a lithium iron phosphate cell of about 19 Wh; follow the cell stops in section 6 and FieldNode's build plan, never charge it below 0 °C or above 45 °C, and never leave a first build charging unattended. Cut aluminium edges are sharp: deburr everything and wear gloves. Printing ASA gives off fumes; print in a ventilated space. A heat-set insert iron runs at over 200 °C. The finished prototype weighs about 5.3 kg with the panel at the top of a 2 m stub: the stub must stand in a base that cannot tip (stop S4). Installing on a real street pole is work at height beside traffic and is outside this plan (stop S6).

## 2. What changed to make it buildable

The concept showed what the counter does; some of its parts could not be made or fixed as drawn. Each change below keeps what the counter does, and all of them are recorded in decision record CBC-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Saddle plates | Flat plates against the round pole; bands drawn as rings that held nothing | Bent V-saddles on the back of each plate, and bands that pass through slots in the plate and across its front (Figures 4 and 5) | The pole seats on the faces of a 90° V; the band pulls the plate onto the pole |
| Enclosure | No fixing to its plate; parts floating inside | FieldNode's buildable core: four lugs on M5 screws, internal plate on bosses, two rows of holes in the bottom (Figures 7 to 10) | CurbCount uses FieldNode's core unchanged |
| Arm | Butted to its plate, "welded or bolted" | Two angle brackets, four M6 bolts through the plate and two down through the tube on crush spacers (Figure 15) | Bolted, no welding; the tube walls cannot crush |
| Sensor head | Floating under the arm; film loose in a larger opening; no cable entry | Printed wedge pad with two M5 bolts into inserts; film clamped to an inner ledge by a printed frame; array on standoffs; a gland under the hood (Figures 17 to 20) | Every part held; window height and tilt unchanged |
| Pole-top mount | Welded cap and post; hinge plate and panel floating | Sleeve with rivet-nut set screws, a cap disc on radial screws, post on angle clips with plugs, a tilted rail plate, panel bolted through its frame lip (Figures 21 to 31) | All bolted; the frame lip is the only part of a panel that takes a bolt |
| Cables | Sensor cable off the pole and under the bands; no panel lead | Both cables tied to the pole and over the bands; sensor cable beside the arm into the head gland; a 1.5 m panel extension lead (Figure 34) | Nothing clamps a cable; the panel's own lead is too short |
| Notice plate | No fixing | Two stainless ties through four slots (Figures 32 and 33) | Nothing drilled |

The changes add about 0.8 kg: the counter weighs 5.26 kg on the pole, within the 6 kg limit.

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Road side" and "sidewalk side" are as the counter stands at the site: the arm points to the road, the enclosure faces the sidewalk. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Enclosure saddle plate

![Figure 2. Making sketch of the enclosure saddle plate](../cad/drawings/CBC-DWG-101.png)

*Figure 2. Enclosure saddle plate making sketch (CBC-DWG-101).*

![Figure 3. Hole and cut-out positions on the enclosure saddle plate](05-build-plan/enc-plate-holes.png)

*Figure 3. Every hole, slot and cut-out, full size figures, measured up from the bottom edge and sideways from the centre line.*

**What it is and what it is made from.** The plate the FieldNode enclosure hangs on, clamped to the sidewalk side of the pole. Aluminium sheet 3 mm thick, 5052 or 6061 class, cut to 160 x 300 mm.

**How to make it.**

1. Cut the blank to 160 x 300 mm, square. File the edges and round the corners to about 2 mm.
2. Scribe a centre line down the long side. Mark one face as the front (the enclosure side).
3. Mark every hole from Figure 3: heights up from the bottom edge, sideways from the centre line.
4. Band slots: four slots 3 wide and 15 tall, 66 each side of centre, centred 17 and 283 up. Chain drill with a 3 mm drill and file square.
5. Lug screw holes: four 5.5 mm holes, 62 each side of centre, 41 and 259 up.
6. V-saddle screw holes: four 4.5 mm holes on the centre line, 42, 62, 238 and 258 up. Countersink them from the front so M4 countersunk screws sit flush.
7. Window: 100 wide and 150 tall, centred, from 75 to 225 up. Drill a 12 mm hole in each corner, cut between the holes with a jigsaw and a metal blade, and file straight.
8. Deburr every hole on both faces.

**How it fits the parts next to it.**

![Figure 4. Joint 1: V-saddle on the pole](05-build-plan/joint-01.png)

*Figure 4. Seen from above at the upper saddle: the pole touches both wings of the V and never the flat.*

![Figure 5. Joint 2: band clamp through the slots](05-build-plan/joint-02.png)

*Figure 5. Seen from above at the upper band: the band goes round the road side of the pole, through both slots and across the front of the plate; the two cables pass over it.*

The two V-saddles sit flat on the back, their flats over the screw holes (Figure 4). The enclosure's back sits flat on the front, centred, between the band slots, held by its four lugs (section 3.3). Each band passes round the pole, through the slots on both sides and across the front, 33 mm above the box's top or below its bottom. The saddles sit 35 mm in from the bands, so the bands never touch the saddle wings on any pole from 60 to 140 mm.

**Check before moving on.** Lay the saddles and the enclosure's lugs on the plate and look through each hole: the holes must line up without forcing a screw.

### 3.2 V-saddles (make 4)

![Figure 6. Making sketch of the V-saddle](../cad/drawings/CBC-DWG-102.png)

*Figure 6. V-saddle making sketch (CBC-DWG-102).*

**What it is and what it is made from.** A bent strip with a V that seats a saddle plate on the round pole. Four are needed, all the same: two for the enclosure plate, two for the arm plate. Aluminium sheet 3 mm, 5052-H32, which bends cold without cracking.

**How to make it.**

1. Cut four blanks 150 x 40 mm. Deburr.
2. Scribe two bend lines across each blank, 10 mm each side of the centre: a 20 mm flat in the middle and a 65 mm wing each side.
3. Clamp the blank in a vice with soft jaws on a bend line and bend the wing 45°, inside radius about 3 mm. Repeat for the other wing, bending the same way, so the wings meet at 90°.
4. On the centre line of the flat, 10 mm each side of the middle, drill 3.3 mm and tap M4.

**How it fits the parts next to it.** The flat sits on the back of a saddle plate, the V opening toward the pole, held by two M4 countersunk screws put in from the plate's front with a drop of medium threadlocker; file the screw tails flush with the flat. The 114 mm design pole touches both wings 43 mm out from the bends (Figure 4); poles from 60 to 140 mm also seat on both wings, and a 60 mm pole still clears the flat by 2 mm.

**Check before moving on.** Each wing is at 45° to the flat, within 1°: check with a protractor or the 45° face of a combination square.

### 3.3 FieldNode enclosure, drilled, with its glands, ports, vent, antenna and lugs

![Figure 7. Drilling sketch of the FieldNode enclosure](../cad/drawings/CBC-DWG-103.png)

*Figure 7. FieldNode enclosure drilling sketch (CBC-DWG-103), drawn upside down so the top view shows the bottom face.*

![Figure 8. Bottom face drilling layout](05-build-plan/base-holes.png)

*Figure 8. Drilling layout, with the box standing upside down on its top and its back face toward you.*

**What it is and what it is made from.** CurbCount's power, radio and processor: the standard FieldNode core, a bought grey polycarbonate box 150 x 90 x 200 mm (IP65) with a gasketed lid, four moulded bosses inside its back wall and the maker's kit of four external lugs, holding the internal plate with the cell, charger and protection modules, the STM32WL controller and a plug-in connector strip. It is made exactly as FieldNode's build plan (FND-BLD-001) says, in its sections 3.3 and 3.4 and steps 2, 4, 5 and 6; this section lists only what is particular to CurbCount.

**How to make it.**

1. Drill the bottom face as Figure 8 shows: back row, 27 from the back face: gland 1 at 40 left, gland 2 at 8 left (16.2 mm holes), vent at 24 right (12.2 mm); front row, 55 from the back face: port A at 54 left, port B at 22 left (16.2 mm), antenna at 30 right (6.5 mm). Left and right are as seen from the front (the lid). Pilot 3 mm slowly with wood behind, open out with a step drill, no solvents.
2. Fit the four lugs to the box's back corners as the lug kit's maker describes.
3. Fit the glands, vent, ports and antenna from below, sealing washers outside, nuts inside. In CurbCount gland 1 takes the panel lead and port A the sensor cable; put the blanking plug in gland 2 and the cap on port B.
4. Build and wire the internal plate as FieldNode's build plan says, with the cell out and the fuse out, with one difference: the array runs on 3.3 V, so in place of FieldNode's boost converter for port A fit a 3.3 V load switch module fed from the 3.3 V converter and enabled by the same controller pin, still through its resettable fuse. Port A's signal pins go to the controller's I²C pins (Figure 11).

**How it fits the parts next to it.**

![Figure 9. Joint 3: enclosure lug on the saddle plate](05-build-plan/joint-03.png)

*Figure 9. Each lug lies flat on the plate beside the box and is held by one M5 button-head screw from behind the plate, nyloc nut in front.*

![Figure 10. Joint 4: the enclosure's bottom face with both cables](05-build-plan/joint-04.png)

*Figure 10. The sensor cable's M12 plug on port A and the panel lead in gland 1; both cables run to the pole below the plate's bottom edge.*

The box's back sits flat on the saddle plate's front, over the window, centred between the band slots; the lid faces away from the pole. The four lug screws can all be reached with the lid shut. The cables leave from the bottom face (Figure 10).

![Figure 11. Block-level wiring](05-build-plan/wiring.png)

*Figure 11. What CurbCount adds to FieldNode's wiring: the sensor cable to the array and the panel extension lead. No circuit board is laid out at this stage.*

**Check before moving on.** FieldNode's checks for the core all pass (its section 3.4): every wire continues end to end; with the cell out and the fuse out, the pack terminals and every rail read open to ground.

### 3.4 Arm saddle plate

![Figure 12. Making sketch of the arm saddle plate](../cad/drawings/CBC-DWG-104.png)

*Figure 12. Arm saddle plate making sketch (CBC-DWG-104).*

![Figure 13. Hole positions on the arm saddle plate](05-build-plan/arm-plate-holes.png)

*Figure 13. Every hole and slot, measured up from the bottom edge and sideways from the centre line.*

**What it is and what it is made from.** The plate the arm butts against, clamped to the road side of the pole. Aluminium sheet 3 mm, 5052 or 6061 class, cut to 160 x 250 mm.

**How to make it.**

1. Cut the blank to 160 x 250 mm, square; file the edges and round the corners to about 2 mm. Scribe the centre line; mark the front.
2. Band slots: four slots 3 x 15 mm, 66 each side of centre, centred 15 and 235 up. Chain drill and file square.
3. Bracket bolt holes: four 6.6 mm holes, 10 each side of centre, 83 and 167 up.
4. V-saddle screw holes: four 4.5 mm holes on the centre line, 40, 60, 190 and 210 up, countersunk from the front.
5. Deburr every hole on both faces.

**How it fits the parts next to it.** Two V-saddles on the back, exactly as on the enclosure plate (Figure 4). The arm tube butts the front at mid height (125 up), held by the two brackets (Figure 14). The bands cross the front 15 mm from each end, clear of the brackets by 44 mm.

**Check before moving on.** Offer the brackets up to the front and look through the bolt holes.

### 3.5 Arm brackets (make 2)

![Figure 14. Making sketch of the arm bracket](../cad/drawings/CBC-DWG-105.png)

*Figure 14. Arm bracket making sketch (CBC-DWG-105).*

**What it is and what it is made from.** A short angle that joins the arm tube to its plate; one goes on top of the tube and one underneath. Aluminium equal angle 40 x 40 x 4 mm.

**How to make it.**

1. Cut two 40 mm lengths; square and deburr the ends.
2. Upright leg (on the plate): two 6.6 mm holes 10 each side of the middle, 22 from the heel (the outside corner).
3. Flat leg (on the tube): two 6.6 mm holes on the middle line, 15 and 30 from the heel.
4. Both brackets are the same: drill them clamped together.

**How it fits the parts next to it.**

![Figure 15. Joint 5: arm tube on the arm saddle plate](05-build-plan/joint-05.png)

*Figure 15. Cut on the arm's centre line: one bracket above and one below the tube; M6 bolts through each upright leg and the plate, nuts behind the plate; two M6 bolts down through both flat legs and the tube, each on a crush spacer inside the tube.*

The heel of each bracket sits in the corner between the plate and the tube: the upright leg flat on the plate's front, the flat leg flat on the tube's top (or bottom) face. The nuts behind the plate clear a 114 mm pole by 10 mm.

**Check before moving on.** Each bracket sits flat on both the plate and the tube with no rocking.

### 3.6 Arm tube

![Figure 16. Making sketch of the arm tube](../cad/drawings/CBC-DWG-106.png)

*Figure 16. Arm tube making sketch (CBC-DWG-106).*

**What it is and what it is made from.** The arm that holds the sensor head out over the curb, 530 mm from the pole's centre. Aluminium square tube 40 x 40 x 2 mm, 6063 class, 498 mm long.

**How to make it.**

1. Cut 498 mm and square both ends; the plate end must sit flat. Deburr.
2. Plate end: two 6.6 mm holes straight down through the top and bottom walls on the centre line, 15 and 30 from the end.
3. Head end: two 5.5 mm holes straight through on the centre line, 418 and 478 from the plate end.
4. Drill each hole through both walls in one pass, with the tube in a V-block on a drill press.
5. Cut four crush spacers 36 mm long from 10 mm aluminium tube (6 mm bore).
6. Push a plastic end cap into the head end.

**How it fits the parts next to it.** The plate end butts the arm saddle plate between the brackets (Figure 15). The head hangs under the far end on two M5 bolts (Figure 18). The sensor cable runs along the tube's side, tied to it (Figure 34).

**Check before moving on.** On a flat bench the tube does not rock, and a rod passes straight down through each pair of holes.

### 3.7 Head housing

![Figure 17. Making sketch of the head housing](../cad/drawings/CBC-DWG-107.png)

*Figure 17. Head housing making sketch (CBC-DWG-107), drawn level; it hangs tilted 7.5° toward the road.*

**What it is and what it is made from.** The box that holds the thermal array, open underneath for the window, with a sun hood on top and a wedge pad that sets the tilt. ASA, printed in one piece: housing 110 x 90 x 70 mm, walls 3 mm, hood 150 x 120 x 4 mm.

**How to make it.**

1. Print in ASA in an enclosed printer, hood down on the bed, four perimeters, 40 % infill. Support the 8 mm window ledge inside the open bottom. Let it cool on the bed.
2. Clean up the ledge's underside so it is flat: the film seals against it.
3. With a heat-set insert tool, press an M3 insert into each of the four corner bosses from below (47 and 37 mm each side of centre), and an M5 insert into each of the two holes in the wedge pad (60 apart).
4. Ream the 16.2 mm gland hole in the pole-side end wall, 15 mm off centre.
5. Drill a 5 mm lanyard hole through the hood's road-side overhang, 10 mm in from its edge.

**How it fits the parts next to it.**

![Figure 18. Joint 6: head on the arm](05-build-plan/joint-06.png)

*Figure 18. Cut on the centre line: the wedge pad's level top sits against the arm's underside; two M5 bolts come down through the arm on crush spacers into the inserts; the array hangs from its standoffs above the window.*

The wedge pad's top is level when the housing hangs at 7.5°, and sits flat against the underside of the arm's far end. The arm's end cap stops 2 mm short of the hood. The array breakout sits on the four standoffs from the roof on M2.5 screws, its lens looking straight down 8 mm above the film.

**Check before moving on.** The wedge top and the ledge face are flat (a steel rule shows no light); the inserts are square and flush.

### 3.8 Window frame and film

![Figure 19. Making sketch of the window frame](../cad/drawings/CBC-DWG-108.png)

*Figure 19. Window frame and film making sketch (CBC-DWG-108).*

**What it is and what it is made from.** The window the array looks through: a 0.5 mm unpigmented HDPE film, 100 x 80 mm, clamped to the housing's ledge by a printed ASA frame 110 x 90 x 3 mm with an 88 x 68 mm opening.

**How to make it.**

1. Print the frame flat in ASA with its four 3.4 mm screw holes, 47 and 37 mm each side of centre.
2. Cut the film 100 x 80 mm with a sharp knife on a sheet of glass. Handle it by the edges; keep fingerprints off the middle.
3. Lay the frame on the film as a template and punch four 3.5 mm holes through the film at the screw holes.

**How it fits the parts next to it.**

![Figure 20. Joint 7: window corner](05-build-plan/joint-07.png)

*Figure 20. Cut through a corner screw: the film is clamped between the housing's ledge and the frame; the M3 screw passes through the punched hole into the insert.*

The film lies on the ledge, the frame over it, and four M3 screws go up through the frame and film into the inserts, tightened evenly in a cross pattern until the film is flat. The array needs only about 30 x 20 mm of the 88 x 68 mm opening.

**Check before moving on.** The film is taut and flat, with no creases or marks in the opening.

### 3.9 Sleeve

![Figure 21. Making sketch of the sleeve](../cad/drawings/CBC-DWG-109.png)

*Figure 21. Sleeve making sketch (CBC-DWG-109).*

**What it is and what it is made from.** The short tube that slips over the top of the pole and carries the panel mount. Aluminium round tube about 128 mm outside with a 3 mm wall; its bore must be 122 mm or more. Cut 100 mm long.

**How to make it.**

1. Cut 100 mm; square and deburr both ends.
2. Mark four points round the top edge at 45°, 135°, 225° and 315° (wrap a paper strip round the tube, mark it in quarters and offset by an eighth). Drill 4.5 mm, 4 mm down from the top edge, and countersink for M4.
3. Mark three points round the bottom at 0°, 120° and 240°, 25 mm up from the bottom edge. Drill 11 mm and set an M8 stainless rivet nut in each with a rivet nut tool.
4. Put a paint mark at 0°: it goes on the road side.

**How it fits the parts next to it.**

![Figure 22. Joint 8: sleeve and cap disc on the pole top](05-build-plan/joint-08.png)

*Figure 22. Cut away at the front: the cap disc sits on the pole top inside the sleeve; three set screws centre the sleeve with about 4 mm all round.*

The cap disc fits inside the sleeve's top, flush (section 3.10). On the pole, the disc carries the load onto the pole top and three M8 cup-point set screws in the rivet nuts centre the sleeve and stop it turning.

**Check before moving on.** The sleeve slides over a 114 mm tube with 3 to 4 mm all round, and each set screw turns freely in its rivet nut.

### 3.10 Cap disc

![Figure 23. Making sketch of the cap disc](../cad/drawings/CBC-DWG-110.png)

*Figure 23. Cap disc making sketch (CBC-DWG-110).*

**What it is and what it is made from.** The lid inside the sleeve top that rests on the pole top and carries the post. Aluminium plate 8 mm, 6082 or 5083 class, 122 mm across.

**How to make it.**

1. Cut a 122 mm disc (hole saw, or bandsaw and file); it must be a close sliding fit in the sleeve's bore.
2. Eight 5.5 mm holes for the lower clips: 40 mm each side of a centre line and 9 mm either side of the cross line. Countersink them from below so the screw heads sit flush: the pole top bears on the underside.
3. Push the disc into the sleeve's top, flush. Drill through the sleeve's four holes into the disc's edge, 3.3 mm and 12 deep, and tap M4. Fit four M4 countersunk screws.

**How it fits the parts next to it.** The disc's underside bears on the pole top; its top carries the two lower clips and the post's foot (Figure 26).

**Check before moving on.** The underside is flat and no screw head stands proud of it.

### 3.11 Post and post plugs (make 2 plugs)

![Figure 24. Making sketch of the post](../cad/drawings/CBC-DWG-111.png)

*Figure 24. Post making sketch (CBC-DWG-111).*

![Figure 25. Making sketch of the post plug](../cad/drawings/CBC-DWG-112.png)

*Figure 25. Post plug making sketch (CBC-DWG-112).*

**What it is and what it is made from.** The short column that lifts the panel above the pole top. Aluminium round tube 42.4 x 3.0 mm, 6063 class, 150 mm long, with a 40 mm plug of 36 mm aluminium round bar in each end so the thin wall does not crush under the bolts.

**How to make it.**

1. Cut the post 150 mm; square and deburr both ends.
2. Cut two plugs 40 mm long from 36 mm round bar; face both ends; file or turn to a push fit in the post's bore.
3. Push a plug into each end, flush.
4. With the post in a V-block on a drill press, drill straight across through post and plug, 8.5 mm: at the bottom end 12 and 28 up from the end; at the top end 10 and 26 down from the end. All four holes lie in one plane.

**How it fits the parts next to it.**

![Figure 26. Joint 9: post foot on the lower clips](05-build-plan/joint-09.png)

*Figure 26. The post stands on the cap disc between the two lower clips; two M8 bolts pass through clip, post, plug, post and clip.*

The foot stands on the cap disc between the lower clips (Figure 26); the head sits between the upper clips under the rail plate, 4 mm clear of it (Figure 30).

**Check before moving on.** A rod passes straight through each pair of holes.

### 3.12 Lower post clips (make 2)

![Figure 27. Making sketch of the lower post clip](../cad/drawings/CBC-DWG-113.png)

*Figure 27. Lower post clip making sketch (CBC-DWG-113).*

**What it is and what it is made from.** A short angle that holds the post's foot on the cap disc. Aluminium equal angle 50 x 50 x 5 mm.

**How to make it.**

1. Cut two 35 mm lengths. Trim the flat leg of each to 30 mm wide from the heel so it fits inside the disc.
2. Upright leg: two 8.5 mm holes at mid-length, 12 and 28 up from the underside of the flat leg.
3. Flat leg: two 5.5 mm holes 19 out from the upright leg's inside face, 9 either side of mid-length.

**How it fits the parts next to it.** The flat leg lies on the cap disc, held by two M5 countersunk screws up through the disc with nyloc nuts on top; the upright leg stands against the post (Figure 26). The two clips face each other across the post.

**Check before moving on.** Both clips stand square to the disc, 42.4 mm apart inside.

### 3.13 Upper post clips (make 2) and rail plate

![Figure 28. Making sketch of the upper post clip](../cad/drawings/CBC-DWG-114.png)

*Figure 28. Upper post clip making sketch (CBC-DWG-114).*

![Figure 29. Making sketch of the rail plate](../cad/drawings/CBC-DWG-115.png)

*Figure 29. Rail plate making sketch (CBC-DWG-115).*

**What they are and what they are made from.** The rail plate is the tilted plate the panel bolts to: aluminium sheet 3 mm, 290 x 150 mm, at 35° to level. The two upper clips hold it on the post's head and set the tilt: aluminium equal angle 50 x 50 x 5 mm.

**How to make them.**

1. Rail plate: cut 290 x 150 mm; the long side runs up the slope. Four 4.5 mm lip bolt holes 6 in from each short end, 50 each side of the centre line. Four 5.5 mm clip screw holes 51 each side of the centre line, 15 and 30 below the middle (toward the low edge). Two lightening windows 90 x 90 mm with 6 mm corners, centred 85 each side of the middle. A 6 mm lanyard hole on the middle line, 12 in from one long edge. Deburr.
2. Upper clips: cut two 35 mm lengths. In each flat leg, two 5.5 mm holes 30 out from the upright leg's inside face, 10 and 25 from one end. Screw both clips under the rail plate with M5 screws, nuts under the clips, upright legs 42.4 mm apart.
3. Set the drilled post between the clips with the rail plate at 35° (check with an angle finder) and the post's head 4 mm below the plate. Clamp, and drill the clips' upright legs 8.5 mm through the post's two top holes. The holes fall about 12 and 21 from the clips' upper ends, 25 and 38 down from the plate.

**How they fit the parts next to them.**

![Figure 30. Joint 10: post head under the rail plate](05-build-plan/joint-10.png)

*Figure 30. Seen from below: the upper clips are screwed under the rail plate and bolted through the post's head; the two bolts fix the 35° tilt.*

![Figure 31. Joint 11: panel frame lip on the rail plate](05-build-plan/joint-11.png)

*Figure 31. The panel frame's back lip sits on the end of the rail plate; two M4 bolts at each end, the nuts inside the frame, never through the glass.*

**Check before moving on.** The rail plate sits at 35°, give or take 1°, and the panel's lip holes line up with the plate's end holes.

### 3.14 Notice plate

![Figure 32. Making sketch of the notice plate](../cad/drawings/CBC-DWG-116.png)

*Figure 32. Notice plate making sketch (CBC-DWG-116).*

**What it is and what it is made from.** The public notice: what is counted, that no images are kept, and where the design is published. Aluminium sheet 2 mm, 150 x 200 mm, with a UV-stable printed face.

**How to make it.**

1. Cut 150 x 200 mm; round the corners 5 mm.
2. Four tie slots 3 x 10 mm, 60 each side of the centre line, centred 30 and 170 up from the bottom edge. Chain drill and file.
3. Print or apply the UV-stable face.

**How it fits the parts next to it.**

![Figure 33. Joint 13: notice plate tie](05-build-plan/joint-13.png)

*Figure 33. The plate lies against the pole; a stainless steel tie runs round the pole and through both slots.*

**Check before moving on.** The printed face reads correctly and is not scratched.

### 3.15 Cables

![Figure 34. Joint 12: the sensor cable leaves the pole for the arm](05-build-plan/joint-12.png)

*Figure 34. Both cables run up the pole's side, tied to it and over the bands; the sensor cable turns round the arm plate's edge, under the lower bracket and along the side of the arm.*

**What they are.** The sensor cable is a bought M12 5-pin cable, about 2 m, with a moulded plug at one end and open cores at the other; it runs from port A, up the pole, round the edge of the arm saddle plate, along the side of the arm, and into the head through the gland under the hood. The modelled run is 1.48 m. The panel extension lead is 1.5 m of two-core 0.75 mm² UV-rated cable with a sealed inline connector; it joins the panel's own 1 m lead at the post and runs down the pole into gland 1.

**What to do to them.** Pass the sensor cable's open end through the head gland, strip it back 30 mm, cut the fifth core back, and solder the other four to the array breakout's 3.3 V, ground, SDA and SCL pins as the port pinout gives them, with heat-shrink on every joint (Figure 11). Check each core with a meter from the plug's pins to the breakout's labels before soldering, not by wire colour. Fit the extension lead's inline connector to the panel lead, with the lead's other end stripped for the connector strip inside the enclosure.

**Check before moving on.** Every core continues end to end and no two cores touch.

### 3.16 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **FieldNode enclosure, glands, ports, vent, antenna and internal plate (line 1); power and radio modules (line 2); cell and fused holder (line 3); connector strip and rail fuses (line 14).** As FieldNode's build plan, section 3.10.
- **Solar panel (line 4).** 6 W monocrystalline, 9 V class, about 290 x 200 x 17 mm, aluminium frame with a flat back lip at least 12 mm wide at its short ends, 1 m lead.
- **Band clamps (line 6).** Four 12 mm stainless worm-drive band clamps that close on the loop for the site pole: about 470 mm on a 114 mm pole (about 330 mm on 60 mm, 545 mm on 140 mm).
- **Thermal array (line 10).** MLX90640 class, 32 x 24 pixels, 110 x 75° lens, on an I²C breakout with four mounting holes.
- **Window film (line 9).** 0.5 mm unpigmented HDPE sheet.
- **Sensor cable (line 11).** M12 5-pin A-coded, single-ended, about 2 m, PUR, 6 mm, IP67.
- **Notice plate ties (line 12).** Two stainless steel cable ties 8 mm wide, at least 500 mm long.
- **Fixings and sundries (line 13).** Stainless: 8 x M4 x 8 countersunk screws (V-saddles); 4 x M4 x 10 countersunk screws (cap disc); 6 x M6 x 20 hex bolts with nyloc nuts and 2 x M6 x 60 with nyloc nuts (arm); 2 x M5 x 50 hex bolts (head); 4 x M3 x 10 screws; 4 x M3 and 2 x M5 heat-set inserts; 4 x M2.5 x 6 screws (array); 3 x M8 rivet nuts and 3 x M8 x 25 cup-point set screws; 4 x M8 x 65 bolts with nyloc nuts (post); 4 x M5 x 20 countersunk screws and 4 x M5 x 16 screws with nyloc nuts (clips); 4 x M4 x 12 bolts with nuts (panel lip); four crush spacers (10 mm aluminium tube); an M16 cable gland for 4 to 8 mm cable; a 40 x 40 mm plastic end cap; the panel extension lead; two stainless wire-rope lanyards about 1 m long with ferrules; UV-stable cable ties; medium threadlocker; FieldNode's hardware set.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 12 are done on the bench. Steps 13 to 17 are done on a 2 m length of 114.3 mm steel tube standing upright in a heavy base, which stands in for the street pole; measure the heights on it down from its top, which stands in for the pole top.

### Step 1: V-saddles onto the enclosure saddle plate

![Step 1](05-build-plan/step-01.png)

Two M4 countersunk screws each, from the plate's front, with medium threadlocker. The V opens away from the plate. File the screw tails flush with the saddle flats.

### Step 2: build the FieldNode core

![Step 2](05-build-plan/step-02.png)

Glands, vent, ports and antenna into the bottom face, sealing washers outside and nuts inside; internal plate on its bosses, wired, cell out and fuse out; desiccant; lid closed. All as FieldNode's build plan, steps 2, 4, 5 and 6. **Hold point:** FieldNode's wiring checks pass.

### Step 3: enclosure onto the saddle plate

![Step 3](05-build-plan/step-03.png)

Hold the box's back flat on the plate's front, centred over the window and between the band slots, lid outward. Four M5 button-head screws through the lugs from behind the plate, nyloc nuts in front, snug.

### Step 4: V-saddles onto the arm saddle plate

![Step 4](05-build-plan/step-04.png)

As step 1.

### Step 5: arm tube and brackets onto the arm plate

![Step 5](05-build-plan/step-05.png)

Stand the tube's square end on the plate's front at mid height. Upper bracket on top of the tube and lower bracket underneath, heels in the corners. Four M6 x 20 bolts through the brackets' upright legs and the plate, nuts behind; then two M6 x 60 bolts down through the upper bracket, the tube (with a crush spacer inside on each) and the lower bracket. Check the tube is square to the plate with a square, then tighten all six.

### Step 6: array and gland into the head

![Step 6](05-build-plan/step-06.png)

Array breakout on the four standoffs, lens down, on four M2.5 screws; gland into the end wall, nut inside. Pass the sensor cable's open end through the gland and solder it to the breakout (section 3.15) before step 7, then tighten the gland's dome on the cable.

### Step 7: window film and frame onto the head

![Step 7](05-build-plan/step-07.png)

Film on the ledge, frame over it, four M3 screws into the inserts, tightened evenly in a cross pattern until the film is flat.

### Step 8: head onto the arm

![Step 8](05-build-plan/step-08.png)

With the arm assembly on its back on the bench, hold the head's wedge pad up against the underside of the arm's far end, end cap toward the road. Put the two crush spacers into the tube at the head-end holes, then two M5 x 50 bolts down through the arm into the inserts, snug: the inserts are in plastic, so do not overtighten. Clip the head lanyard through the hood's hole now; it is tied to the pole in step 16.

### Step 9: cap disc into the sleeve

![Step 9](05-build-plan/step-09.png)

Rivet nuts already set. Disc into the top of the sleeve, flush; four M4 countersunk screws through the sleeve into the disc's edge.

### Step 10: lower clips and post onto the disc

![Step 10](05-build-plan/step-10.png)

Each clip on two M5 countersunk screws up through the disc, nyloc nuts on top. Stand the post between the clips and fit two M8 bolts through clip, post and clip, nyloc nuts, tight.

### Step 11: rail plate onto the post

![Step 11](05-build-plan/step-11.png)

The upper clips are already screwed under the rail plate (section 3.13). Lower the clips over the post's head and fit two M8 bolts, nyloc nuts, tight. The rail plate leans 35°, its low edge on the sidewalk side, away from the sleeve's paint mark.

### Step 12: panel onto the rail plate

![Step 12](05-build-plan/step-12.png)

Lay the panel's frame lip on the rail plate's ends, panel face up, junction box clear of the clips. Drill the lip through the plate's end holes if it is not already drilled, keeping well clear of the glass, and fit four M4 bolts with the nuts inside the frame. Tie the panel's lead down the post with UV-stable ties.

### Step 13: enclosure assembly onto the pole

![Step 13](05-build-plan/step-13.png)

On the stub, the plate's centre goes 1,300 mm below the top. Hold the plate with both saddles against the pole. Pass each band round the pole, through its two slots and across the plate's front (the upper band above the box, the lower band below it), worm drive on the road side of the pole where a screwdriver reaches it. Tighten both to the band maker's torque and record it.

### Step 14: arm assembly onto the pole

![Step 14](05-build-plan/step-14.png)

On the stub, the arm's axis goes 747 mm below the top, on the side opposite the enclosure. Band it as step 13. Before the final tightening, turn the arm square to the street (at the site) or square to the enclosure (on the stub), and level it within 1° with a spirit level on the tube.

### Step 15: pole-top mount onto the pole top

![Step 15](05-build-plan/step-15.png)

With a helper, lower the mount over the pole top until the disc sits on it. Turn the panel toward the equator (on the stub, toward the enclosure side). Tighten the three set screws evenly with a hex key so the sleeve sits centred, then add threadlocker. Pass the panel lanyard through the rail plate's hole and round the pole below the sleeve; close it with a ferrule.

### Step 16: sensor cable and panel lead

![Step 16](05-build-plan/step-16.png)

Seen from the street. Plug the sensor cable into port A. Run it under the enclosure plate to the pole's side, up the pole, round the edge of the arm plate, under the lower bracket and along the side of the arm to the head (Figure 34). Run the panel extension lead from the panel's inline connector down the same side of the pole, beside the sensor cable, to gland 1, and into the connector strip. Tie both to the pole every 150 mm with UV-stable ties, over the bands, never under them. Leave a drip loop below each entry. Tie the head lanyard round the pole above the arm plate.

### Step 17: public notice plate

![Step 17](05-build-plan/step-17.png)

Back of the plate against the pole, face outward (at the site, at eye height, about 2.6 m up, facing the sidewalk; on the stub, below the enclosure). Pass each tie round the pole and through its two slots, pull tight and cut the tail flush.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of CBC-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Saddles seat on the pole | R12 | Fit each saddle plate to 60, 114 and 140 mm tubes before banding | Both wings of both saddles touch the tube; the plate does not rock |
| Band torque | R12 | Torque screwdriver on each band | The maker's torque is reached without the band slipping; value recorded |
| Arm level and square | R6 | Spirit level and square on the arm | Level and square within 1°; the window is 4.3 m above the road when installed |
| Head and window | R4, R10 | Look at the film and frame; shine a lamp from inside | Film taut and flat; light shows only through the opening, not at the frame edges |
| FieldNode core | R8, R9 | FieldNode's first checks: charge voltage, charge stops, rail switching | All pass as FieldNode's build plan states |
| Array over the cable | R1, R4 | Controller reads frames over the 2 m cable at 16 subpages a second with the calibration jumper fitted, shown on a laptop through the service port only | Frames read without errors for 10 minutes; nothing is stored or sent by radio |
| Count record and uplink | R5, R15 | Run the counting firmware sketch; watch the gateway | One 10-byte record every 15 minutes, no frame data |
| Sealing | R10 | Look at every gland, the gasket and the window seal under a lamp | Washers evenly squeezed; gland domes tight on their cables (the spray test comes later) |
| Mass | R11 | Weigh each group before it goes on the stub | 5.3 kg or less in all (5.26 kg estimated) |
| Mount and wind | R12 | Push on the panel corners and the head by hand | Nothing moves at any joint; lanyards fitted |
| Install time | R12 | Time steps 13 to 17 with two people | 60 minutes or less |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the cell comes into the workshop.** FieldNode's stops S1 to S5 apply in full: cell voltage and condition checked, a datasheet, fuse out, a charging spot on a non-combustible surface with an extinguisher for electrical fires.
- **S2. Before the cell goes in.** The core's wiring checks pass with the cell out and the fuse out; the sensor cable's cores are checked to the breakout's labels; nothing on the port A rail is shorted to ground.
- **S3. Before the radio transmits.** The antenna is connected and matches the region's band.
- **S4. Before anything goes on the stub.** The stub stands in a base that cannot tip under 5.3 kg at 2 m with a 0.06 m² panel at the top (a steel base plate at least 600 x 600 mm bolted to the floor, or two wall clamps). Work from a stable step platform, not a ladder leaning on the stub. Every bolt has a nyloc nut or threadlocker; the panel glass is whole; all edges are deburred.
- **S5. Before any frame is looked at.** Frames are shown only on a laptop through the calibration jumper on FieldNode's service header, never stored and never sent by radio. Do not point the head at people who have not been told what it is for.
- **S6. Before any installation on a street pole (outside this plan).** The pole owner's written permission and a check that the pole can carry about 52 N of wind load at 5.3 m (279 N·m at its base); a trained crew with fall protection and traffic management as local rules require; clear of overhead power lines and street-light wiring; the pole's electrical hatch never opened; both lanyards fitted; the notice plate fitted at the same visit; bands and set screws checked after the first storm.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade (or a bandsaw); bench vice with soft jaws; bench drill or a drill in a stand, with a V-block; drills 2.5 to 12 mm; step drill to 20 mm; countersink; M4 tap and tap drill; jigsaw with a metal blade; flat and half-round files; deburring tool; scriber, engineer's square, combination square with a 45° face, protractor, steel rule and calipers; digital angle finder; spirit level; rivet nut tool for M8; hole saw about 122 mm (or bandsaw) for the cap disc; 3D printer with an enclosure and a 160 x 130 mm bed that prints ASA; heat-set insert tool or a soldering iron with insert tips; soldering iron; ferrule crimper and wire strippers; multimeter; bench power supply with an adjustable current limit; torque screwdriver about 1 to 6 N·m; hex keys; scale to 10 kg; stopwatch; laptop with the calibration viewer.

**Skills.** No certified trade is needed. Basic metalwork (marking out, sawing, drilling, filing, tapping, bending thin sheet, setting rivet nuts), 3D printing in ASA, through-hole soldering and crimping, safe use of a bench power supply and care with lithium cells. All circuits are extra-low voltage: 3.6 V at the cell, 3.3 V on the sensor rail, under about 15 V from the panel. No mains wiring is part of this build.

**Workspace.** A bench about 1.5 x 0.6 m; a metalwork corner kept apart from the electronics; a ventilated place for the printer; the charging spot of S1; floor space about 1.5 x 1.5 m for the stub in its base, with 2.5 m of headroom.

**Personal protective equipment.** Safety glasses for cutting, drilling, bending and soldering; cut-resistant gloves for sheet, bar and the panel; hearing protection when sawing; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 106 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/CBC-DWG-101` to `CBC-DWG-116`.
- General arrangement: `cad/drawings/CBC-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (CBC-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; wind and mount [H1] to [H4], mass [H5], install time [H6], cost [J1].
- Bill of materials: `bom/bom.csv`.
- FieldNode core: FieldNode's build plan FND-BLD-001 and decision record FND-DDR-003.
- Decisions: `docs/decisions/0003-design-for-construction.md` (CBC-DDR-003), with CBC-DDR-001 and CBC-DDR-002; open decisions in `docs/06-design-decisions.md` (CBC-DEC-001).
- Requirements: `docs/03-requirements.md` (CBC-REQ-001 v0.6).
