# AIGC Video Flow

Use an LLM agent as director and producer to make high-quality, commercial-grade video.
The agent writes the story and shot list, builds a Blender previs, generates and checks asset sheets and keyframes,
routes each shot to the best video model, scores the results, and cuts picture and sound with scripts.
A human sets the direction, approves spend and gives the final notes.

## Projects

| # | Project | Length | Models | Status |
|---|---|---|---|---|
| 01 | [GOLDEN HOUR, scene 38 "The Squeeze"](01-golden-hour-s38/) — 1997 car chase with a nuclear device | 13.0 s, 16 shots | GPT Image 2.5, Kling 3.0 Turbo Pro, H3 Max Turbo, Lyria 3.5, Sonilo, ElevenLabs | Rough cut v3 done |

## Method docs

- [`docs/blender-to-cinema-ads.html`](docs/blender-to-cinema-ads.html) — the guide: Blender previs to cinema-grade ads (three handoff modes, prompt architecture, failure table). Translations in [`docs/i18n/`](docs/i18n).
- [`docs/workflow-review.html`](docs/workflow-review.html) — review of the workflow and the verification plan (V1–V9).
- [`docs/notes/`](docs/notes) — external workflow notes.

## Log summary · 01 GOLDEN HOUR s38 (2026-10-02 → 2026-10-04)

| Phase | What happened | Outcome |
|---|---|---|
| Previs | Blender clay scene: two cars, real lanes, cameras per shot; readable colour pass; posed collision stills | Layout truth for every frame |
| First video tries | Local MiniMax H3 reference-to-video on clay (takes 1–2) | All shots present, but timing drift and design swaps |
| Re-direction | Guide-driven plan; 90s look; nuclear device with countdown; "STOP OR DIE!"; collision beat; Kaz's grin; clock jump | 16 shots, 13.0 s |
| Assets | GPT Image 2.5 sheets: cast, cars, device, 90s props, plates, grade key, damage (one mirrored to fix the side) | Consistent cast and cars |
| Keyframes | 28 images for 16 keys; fixes for mirrored roads, extra red cars, wrong cabin side; user caught a car standing across the road | 16/16 approved, new QA check 11 |
| Video | Kling 3.0 Turbo Pro + H3 Max Turbo on fal for all 16 shots; local H3 stopped | 2 complete sets, A/B on every shot |
| Sound | Lyria 3.5 score (take 1), Sonilo synced SFX + ElevenLabs layers, Eleven v4 shouted line | Mix at −14 LUFS, effects bed lowered |
| Review | Metrics (keyframe PSNR, detail kept, grain, flicker) + 100 % crops | Kling ≈ 8.4, H3 ≈ 7.6; H3 9× cheaper and better at action |
| Final | Mixed cut (H3 for inserts and action moves, Kling elsewhere) + all-Kling, all-H3 and 2×2 compare cuts | [`01-golden-hour-s38/final/`](01-golden-hour-s38/final) |

**Conclusion:** spend on input quality (previs, sheets, keyframe QA), mix models per shot, and check every take
for hidden cuts and drift. Image-to-video copies keyframe flaws: the more exactly a model follows the keyframe,
the more its defects glitch in motion, so clean keyframes come first.

**Human final comment (2026-10-04):** "The more precisely the model uses the interim pictures, the more glitchy
scenes are created, not smooth pictures, because the model reproduces exactly the bad quality of the interim pictures."

Approximate fal spend for 01: Kling ≈ $9.7, H3 Max Turbo ≈ $0.75, audio ≈ $0.5, plus image tokens for sheets and keyframes.

## Repository layout

```
01-golden-hour-s38/
  README.md  RETRO.md
  docs/        bible, workflow, director plan, QA log
  previs/      Blender scripts, clay frames, collision stills
  assets/      asset sheets v1–v4, fal URL list
  keyframes/   16 approved keyframes, contact sheet, job builder
  board/       scene design board (HTML)
  video/       Kling and H3 takes (720p copies), local H3 script
  sound/       score takes, voice, SFX
  edit/        conform and mix scripts
  final/       mixed, all-Kling, all-H3, 2x2 compare, rough v2
  review/      metrics, strips, A/B crops
docs/          method guide, workflow review, translations, notes
```
