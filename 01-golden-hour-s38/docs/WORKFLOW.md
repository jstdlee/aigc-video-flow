# AI film workflow v3: aligned to "Blender to Cinema Ads"

Guide: `~/dev/aigc-video-flow/blender-to-cinema-ads.html` (8 stages, three handoff modes, prompt architecture, failure table).
Review: `~/dev/aigc-video-flow/workflow-review.html` (9 verification tests V1–V9).
Core rule from the guide: **lock assets first, generate video last; if takes fail the same way, fix the input, not the seed.**

## Stage status for GOLDEN HOUR s38

| # | Guide stage | Status | What we have | What is missing (→ action) |
|---|---|---|---|---|
| 1 | Brief + shot list | done | Story, 8-shot table with timecode (`BIBLE.md`, `scene.py` SHOTS) | Delivery spec in the brief: sizes (16:9, 9:16), master resolution, loudness target |
| 2 | Lock assets (@tags) | done | Car turnarounds, cast body + face sheets, interior, props, world (`assets/`, `refs/`) | One **size-anchor** reference (cars and people to scale) attached to every shot |
| 3 | Model + materials | partial | Real-scale clay, colour-coded | **Hero cars are boxes**: a real 3D model of car A and car B (from the design sheets, or Sketchfab / PolyHaven) so the shape cannot drift. Bevels. PBR materials (paint, chrome, glass) |
| 4 | Light + camera | partial | 36 mm sensor, real lenses, one move per shot | **Motivated golden-hour light** in Blender (low sun ahead, warm rim, matches the prompt). **AgX** view transform (now Standard). Depth of field. Lens / height / speed numbers **repeated in the prompt** |
| 5 | Render keys / previz | partial | Readable clay video, start and end clay frames | **Passes: depth (Z) and object masks** (Cryptomatte) per car, for compositing and ControlNet. Higher render quality for the master pass |
| 5→6 | Pick a handoff mode per shot | not done | Mode C (previs → video) for every shot | **Per-shot mode choice**: inserts (cooler, shifter) = **mode B** (keyframe → video); car shots = **mode C**; any design-critical frame = **mode A** (composite the Blender car with its mask) |
| 6 | Generate video | partial | H3 reference-to-video, two 5 s halves, fast mode for iterating (8 min/half) | **Prompt architecture**: global style · active refs · camera with numbers and "NOT a zoom" · light (source, direction, Kelvin) · timecoded beats · physics · **60:30:10 colour ratio** · **positive locks** (not "nothing stops") · **"24 fps real time, no slow motion"** on every shot except shot 5 · 180° shutter |
| 6b | **Conform to previs** (new) | not done | — | Timing fails V4 (4 of 7 cuts off by 4–15 frames, a double cut at the half-join). Edit step: detect each generated cut, trim or retime every shot to the clay's frame count, cut the halves at the clay boundary |
| 7 | Edit, grade, sound | not done | Hard cuts | **Per-shot grade matched to one reference still**; cut on action; **SFX before music**; loudness −14 LUFS, true peak ≤ −1 dBTP |
| 8 | Variants + sizes | not done | 1280×704 only | 1080p or 4K master (upscale tested on the cars), 9:16 and 1:1 reframes |

## Process gaps from the review (V1–V9)

| Test | Status | Action |
|---|---|---|
| V1 rights audit | not run | Licence table for H3, Qwen-Image 2.1, grok, agy outputs and any downloaded car models (no GPU) |
| V4 mode C two-half take | **ran 2026-10-03: shots pass, timing fails** | 8/8 shots present, no design swap, no prop in the wrong car. Cuts within ±2 frames: 3 of 7. Fix = stage 6b conform + timing-locked prompts |
| V6 take manifest | not done | Every take writes JSON: model, LoRA, seed, steps, fast flag, prompt, reference file hashes, time, peak memory |
| V7 cost per approved second | data exists | Full settings 33 min per 5 s half; fast settings 8.3 min per 5 s half. Log approvals to get min per usable second |
| V2, V3, V5, V8, V9 | not run | Product-spot tests; for this film V5 (delivery check) applies after stage 7 |

## Failure table (guide) applied to this film

| Failure seen | Guide cause | Our fix |
|---|---|---|
| Kaz's car swapped design (take 1) | no exact-product path | real 3D car models (stage 3); mode A for any shot where the design must be exact |
| Shot dropped / cuts drift (takes 1–2) | output too long; words leave timing open | ≤ 5 s pieces (done); conform edit (6b); beats with exact timecode |
| Mirror showed taillights (take 1) | ambiguous direction | positive description ("head-on, headlights toward us") — fixed in take 2 |
| Cooler appeared in Kaz's car (take 1) | object named in the wrong beat | name props only where they belong — fixed in take 2 |

## Order of work (next)
1. No GPU: V1 rights table; V6 manifest writer; prompt template with the guide's sections; conform script (6b) and re-conform take 2.
2. Blender (CPU, nothing else running): AgX + motivated sun + DOF; depth and car-mask passes; real car models for A and B.
3. GPU, one job at a time, under 97 GiB: mode B for shots 1 and 6, mode C fast takes for the rest; full-quality final.
4. Stage 7–8: grade, sound, loudness, sizes; V5 delivery check.
