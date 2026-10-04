# GOLDEN HOUR, scene 38 "The Squeeze": director's plan v3 (redirected to the "Blender to Cinema Ads" guide)

Starting point: the finished clay previs (`clay_anim/`, `clay2/` boundary frames) and the asset library (`assets/`, `refs/`).
Handoff: **mode B, keyframe → image-to-video** for every shot (decision 2026-10-03). Keyframes: GPT Image 2.5 (fal).
Video: H3 image-to-video locally (free), Kling 3.0 Turbo Pro 1080p (fal, $0.14/s) when H3 fails a shot twice.

## The story (unchanged spine, sharpened beats)
Wildfire smoke grounds the medevac helicopter. Ex-rally driver **Eli Navarro** has 60 minutes to drive a donor heart across the
valley; his estranged daughter is already on the table. The broker who lost the heart sends his wheelman **Kaz** to take it back.
Scene 38 is the midpoint: the hunter finds the courier. **Dramatic question:** does Eli give up the heart or run?
**Turn:** Kaz offers him the easy way out ("pull over"). Eli answers with the shifter. **Button:** they vanish under the overpass, neck and neck.
Rhythm: calm → threat seen → threat arrives → stare (time stretches) → decision → explosion → release.

## Gaps from the guide, closed in this pass
| Guide gap (WORKFLOW.md v3) | How v3 closes it |
|---|---|
| One handoff mode for everything | Mode B for all eight shots: a checked start keyframe (and end keyframe where the move matters) per shot |
| Prompt architecture missing | Every prompt uses the guide's sections: global style · active refs · camera with numbers + what it is NOT · light (source, direction, Kelvin) · timecoded beats · physics · 60:30:10 colour · positive locks · frame rate |
| Camera numbers not repeated | Lens, camera height and move come from the clay cameras (table below) and are written into the image and video prompts |
| Slow motion not controlled | "24 fps real time, no slow motion" in every shot except 5, which is "4× slow motion" |
| Negative locks | Positive states only ("the coupe drives forward in the fast lane", not "nothing reverses") |
| Timing drift | Each shot is generated long (≥ 4 s) and **conformed** to its clay frame count in the edit (stage 6b) |
| Light only in the prompt | One light key for the whole scene: low sun ahead, 3200 K warm key with 6500 K skylight fill, rim light on every car and face |
| Grade not matched | One reference still (the shot 4 keyframe) is the grade target for every shot |
| Fail loop | Two failures the same way → change the keyframe or prompt, not the seed |

## Scene-wide settings (the "global style" block, identical in every prompt)
Live-action feature film, anamorphic 35 mm, 2.39:1 framing safe, 24 fps, 180° shutter. Low golden-hour sun ahead of the cars, 3200 K warm key,
6500 K sky fill, warm rim light, light haze, gentle lens flare. Colour ratio 60 % warm asphalt and dry grass ochre, 30 % deep pine green and
shadow teal, 10 % accent: Kaz's candy red and the cooler's red LED. Real physics: cars stay planted, tyres grip, suspension and bodies move,
the background streams past with motion blur at highway speed.

## Shot plan (clay timing is the cut; generation is longer and conformed)
| # | Clay frames | Length | Lens / camera (from clay) | Move | Beat | Performance | Keys |
|---|---|---|---|---|---|---|---|
| 1 | 1–30 | 1.25 s | 30 mm, inside car A at the passenger door, 1.4 m | static, slight cabin vibration | The stakes: the donor-heart cooler belted in, red LED blinking | Eli's hand slides from wheel to shifter | start |
| 2 | 31–66 | 1.5 s | 44→52 mm, camera car in front of car A, 1.4 m, looking back | slow push in, NOT a zoom | Eli calm, then eyes flick to his left mirror, brow tightens | calm → wary | start + end |
| 3 | 67–84 | 0.75 s | 78→86 mm, Eli's eye-line into the left door mirror | locked to the door | Kaz's red coupe head-on in the mirror, headlights on, growing | — | start + end |
| 4 | 85–114 | 1.25 s | 30 mm drone, 3.6–4.8 m high, 11–17 m behind | descending track, constant speed | Eli boxed behind the truck; Kaz surges up the fast lane, pulls level under the gantry | — | start + end |
| 5 | 115–144 | 1.25 s | 32→38 mm, inside car A behind Eli's right shoulder, looking left | handheld drift, 4× slow motion | The stare: Kaz smirks, points across his empty passenger seat at Eli's cooler, mouths "pull over" | Kaz cocky; Eli still | start + end |
| 6 | 145–162 | 0.75 s | 32 mm over the console | static, jolts on the lunge | The answer: Eli rams the shifter forward | decisive | start + end |
| 7 | 163–210 | 2.0 s | 24 mm bumper camera 7–10 m behind car A, 0.9→1.8 m high | chase, swings right, rises | Eli darts into the right lane and passes the truck along its right side; Kaz holds the fast lane | — | start + end |
| 8 | 211–240 | 1.25 s | 55→26 mm long lens, right shoulder 0.9 m, looking back | locked off, whip pan at the end | Both cars charge at camera under the overpass and rip past the lens | — | start |

## Quality gates
1. Keyframe gate: the 10-point checklist in BIBLE.md, at full size, logged in QA.md.
2. Shot gate: every 3rd frame checked for identity, car design, lane, direction, physics; failures are re-made with a fixed input.
3. Cut gate: after the conform, every cut on its clay frame (±0 after conform), checked with scene detection.
