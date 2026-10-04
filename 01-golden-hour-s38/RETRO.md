# GOLDEN HOUR, scene 38 "The Squeeze": retrospective (v6, 2026-10-03/04)

Final deliverable: `edit/golden_hour_s38_v3_mixed.mp4` (13.0 s, 312 frames, 1920x1080, 24 fps, -13.9 LUFS).
Comparison set: `edit/golden_hour_s38_v3_{kling,h3,mixed}.mp4` and `edit/golden_hour_s38_v3_compare_2x2.mp4`.
Design board: https://claude.ai/artifact/HEExV5Snv6sADSVNL59SiK

## 1. Ideas (story and direction)

- 1997 spy thriller. A stolen, armed Soviet suitcase nuke has an anti-tamper clock. Eli must deliver it; Kaz wants it back.
- 16 shots, 13.0 s: the lid opens (00:41:12), the mirror, Kaz pulls level, the stare, "STOP... OR DIE!",
  the ram, sparks, a near miss with a civilian sedan, Eli catches the slide, Kaz grins, Eli's eyes,
  the clock jumps to 00:09:59, the shifter, the squeeze past the truck, out under the bridge.
- Look: 35mm Kodak stock, anamorphic flare, golden-hour amber with olive-teal shadows, 60:30:10 colour ratio.
- Sound: Lyria 3.5 spy score (take 1), the music cuts out on the impact, synced SFX, one shouted line.

## 2. Pipeline that worked

| Stage | Tool | Notes |
|---|---|---|
| Layout truth | Blender clay previs (+ posed collision stills `ref_collision.py`) | Lanes, contact point and camera are drawn, not described |
| Asset sheets | GPT Image 2.5 (fal) | Characters, device, 90s props, plates, grade key, damage sheets for both cars |
| Keyframes | GPT Image 2.5 edit, 1920x1088, clay frame as image 1 + sheets | 16/16 approved after 3 rounds (28 images) |
| Video | Kling 3.0 Turbo Pro + H3 Max Turbo (fal) | Image-to-video from the approved keyframe |
| Music | Google Lyria 3.5 (fal) | Ignores requested length; cut on the beat in the edit |
| SFX | Sonilo v1.1 video-to-SFX + ElevenLabs SFX v2 layers | Sonilo left holes (mirror shot, sparks); layered fixes |
| Voice | ElevenLabs Eleven v4 ("Callum", [shouting][furious]) | Pause shortened; "STOP" as a lead-in over the stare |
| Edit | ffmpeg scripts (`edit/variants_v3.py`) | Frame-count checks per piece; two-step audio render |

## 3. Improvements made during the run (lessons)

1. GPT Image mirrors "camera looking back" layouts and adds red cars ahead -> state frame-left/right positions and
   positive "only X in frame" statements.
2. Side-on cars with a road receding behind them = car across the road (missed by me, caught by the user on shot 6)
   -> new QA check 11 in `BIBLE.md`: background direction must match travel.
3. Damage continuity needs its own sheets (car A left rear, car B front-right). A mirrored sheet fixed a wrong side for free.
4. Approved frames make good layout references for re-makes (shot 1 from shot 10's cabin; shot 6 from shot 5's geometry).
5. Precise edits (one display changed to 00:09:58) are cheaper and safer than a full re-make.
6. Kling inserts hidden cuts inside takes -> scene-detect every take before editing.
7. Edit pieces can run past the source end (lost a frame) -> assert frame counts.
8. ffmpeg one-pass mixes with reused inputs and `-shortest` truncated the cut -> render the mix to WAV first, then mux.
9. Local H3 was stopped by the user; fal-hosted H3 Max Turbo is far better and nearly free.

## 4. Comparison step (Kling 3.0 Turbo Pro vs H3 Max Turbo)

Method: all 16 shots generated on both models from the same keyframes and prompts; the same timeline and mix for
all cuts; numpy metrics per take (`review/metrics.py`); 100 % crop review; A/B pairs on shot 7 (car action) and
shot 12 (face).

| | Kling 3.0 Turbo Pro | H3 Max Turbo |
|---|---|---|
| Image quality (detail, grain) | 8.6 | 7.3 |
| Realism (skin, metal, physics) | 8.4 | 7.4 |
| Stability inside a take | 8.0 (3/16 hidden cuts) | 7.4 (no cuts; background/face drift) |
| First frame = keyframe | 9.1 (PSNR 39-43 dB) | 7.0 (PSNR 22-26 dB) |
| Performs the asked action | 7.6 | 8.9 |
| Weighted total | ~8.4 | ~7.6 |
| Price / speed | $0.14/s, 3-7 min per shot | $0.015/s, ~1-3 s GPU per shot |

Measured patterns: Kling keeps detail and grain (detail_keep ~1.0, grain 0.4-0.56); H3 softens over the clip
(0.46-0.99), is smoother/waxier (grain 0.24-0.43) and over-sharpens early frames.

## 5. Conclusion

- Use the mixed approach: Kling for faces and car action (photoreal, exact keyframe); H3 Max Turbo for inserts,
  props with text and moves where action matters more than texture (shots 1, 5, 10, 13, 14 here).
- H3 Max Turbo is the best value for drafts and previews; Kling for hero shots.
- Spend on input quality (clay layout, sheets, keyframe QA), not on re-rolling video.
- Post: DaVinci Resolve has no Linux ARM build, so it cannot run on this DGX Spark. Use Kdenlive here,
  or Resolve on an x86/Windows/Mac machine with exported stems.
- Total fal spend for this pass (approx.): keyframes/sheets (image tokens), Kling ~$9.7, H3 ~$0.75,
  audio ~$0.5.

## 6. Open items

- Grade pass: add grain to the H3 shots to match Kling; final two-pass loudness (-14 LUFS, TP <= -1.5 dBTP).
- Shot 2 background coupe (H3 drift) is avoided in the mixed cut by using Kling.
- Optional: Kdenlive project or Resolve stems for hand finishing.

## 7. Human final comments

> "It seems that the more precisely the model uses the interim pictures, the more glitchy scenes are created,
> not smooth pictures, because the model reproduces exactly the bad quality of the interim pictures."
> (user, 2026-10-04)

What this means for the next run:
- The keyframe sets a ceiling on quality. A model that copies the keyframe exactly (Kling: first frame PSNR 39-43 dB)
  also copies its flaws: odd geometry, AI texture, wrong details. Those flaws then move and glitch over the clip.
- A model that re-renders the first frame (H3: 22-26 dB) hides some keyframe flaws, but drifts from the approved design.
- Next time: raise keyframe quality before video (full-size QA for texture as well as layout, a clean-up or
  upscale pass, real photo plates or real 3D car models where possible), or use reference-to-video with sheets
  instead of a pixel-exact first frame for shots where the keyframe is weak.

