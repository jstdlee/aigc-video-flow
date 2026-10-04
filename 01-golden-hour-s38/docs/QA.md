# Keyframe QA log (checklist in BIBLE.md)

## v4 / grok image_edit, clay2 + refs → start frames: 1 of 8 pass
| Shot | Result | Failed checks |
|---|---|---|
| s1 | FAIL | camera moved outside the car (should be inside at the passenger door); right-hand-drive seating; red car ahead instead of behind (3, 4) |
| s2 | FAIL? | median side looks mirrored vs clay (2) |
| s3 | FAIL | right-hand-drive seating; a face in the mirror; a duplicate black car (4, 5, 6) |
| s4 | FAIL | cars face the camera (headlights) although the clay shows red taillights (1) |
| s5 | FAIL | camera outside the car; a second person in Eli's car (4) |
| s6 | FAIL | exterior shot instead of the console insert (framing) |
| s7 | FAIL | cars face the camera (1) |
| s8 | PASS | — |

Finding: grok image_edit uses image 1 as loose inspiration and re-composes, with a strong bias toward front-facing hero shots. It is reliable
for **minimal edits of a photo** (e.g. s4 "move car B back" kept every pixel), not for clay → photo.
Workflow change: **agy (Gemini) does clay → photo for start frames; grok does minimal photo edits for end frames.**

## v4 final: start = agy (s3, s4, s6) or Qwen-edit + grok design swap (s1, s2, s5, s7, s8); end = minimal grok edit of the start
| Shot | Start | End | Notes |
|---|---|---|---|
| s1 | PASS (Qwen) | PASS | left-hand drive, cooler belted in the passenger seat, hand moves to the shifter |
| s2 | PASS (Qwen → grok interior) | PASS | Eli looks to his left (frame-right) at the mirror; red car far behind |
| s3 | PASS (agy) | PASS | mirror shows the road behind and the coupe growing; no faces |
| s4 | PASS (agy → grok removed a stray car) | PASS | fast lane empty, then Kaz level on the left; seen from behind |
| s5 | PASS (Qwen seed 11) | PASS (subtle) | the coupe's nose at frame-right, Kaz on the far side, the back of Eli's head in the foreground |
| s6 | PASS (agy → grok interior + road side) | PASS | wood-rim wheel, chrome gauges; the truck's lane is slightly ambiguous behind the glass (minor) |
| s7 | PASS (Qwen → grok car swap) | PASS | boxed behind the truck → right lane |
| s8 | PASS (Qwen → grok car swap) | PASS | Eli nearer, screen-left; Kaz screen-right; truck and gantry behind |
Bible change: the sun is **ahead** (most approved frames show it; also the stronger look).

## Keyframes v6 (2026-10-03) — GPT Image 2.5 flare/edit, 1920×1088, 16 shots (90s / nuclear device / collision cut)
Inputs per shot: clay frame as image 1 (layout truth) + sheets + grade key. Jobs: keys6/jobs.json, request IDs: keys6/requests*.txt.

| Shot | R1 | R2 | R3 | Fail reason → fix |
|---|---|---|---|---|
| 1 Lid opens | fail | fail | pass | R1 arm from passenger side + red car ahead; R2 built a RHD cabin → R3 used approved shot 10 cabin as image 1 |
| 2 Eli calm | minor | pass | | background lanes mirrored (looking back) → explicit frame-left/right wording |
| 3 Mirror | pass | | | |
| 4 Drone | pass | | | |
| 5 Stare | fail | pass* | | car B faced backward → "rear wing frame-LEFT, nose frame-RIGHT" (*car A mirror in wrong corner, minor) |
| 6 Stop or die | pass | | | |
| 7 Ram | fail | pass | | lanes swapped → explicit "red coupe on the LEFT between median and black car" |
| 8 Sparks | fail | pass | | cars faced camera while traffic drove away (hflip tried, rejected) → "camera BEHIND both cars, taillights nearest" |
| 9 Inches | fail | pass | | looking-back view mirrored → explicit screen sides |
| 10 Catch it | fail | pass | | red car ahead → "only the white truck ahead" |
| 11 Kaz grins | pass | | | |
| 12 Eli's eyes | fail | pass | | red car with taillights behind him → "no cars behind" |
| 13 Clock | pass | | | |
| 14 Shifter | fail | fix | pass | red car ahead; then display 00:41:12 after the jump → precise edit to 00:09:58 |
| 15 Squeeze | fail | pass | | sedan blocking the right lane → "right lane completely empty" |
| 16 Bridge | pass | | | |

Lesson: GPT Image 2.5 mirrors "camera looking back" layouts and adds red cars ahead. Always state frame-left/frame-right positions and what is NOT in the frame as a positive statement ("only the truck ahead"). 28 images for 16 keys.
| 6 Stop or die (post-approval) | — | — | fix | USER CAUGHT: background road receded into depth behind Kaz = car B at 90° to the road. Re-made from approved shot 5 geometry with "background streams ACROSS the frame". |

**New QA check 11 (added after shot 6):** background direction must match travel. Side-by-side shots: background streaks sideways (parallel to the car). Front/back views: road recedes to a vanishing point. A receding road behind a side-on car = car across the road = reject.
