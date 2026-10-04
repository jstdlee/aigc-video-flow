#!/usr/bin/env python3
"""GOLDEN HOUR s38: rough cut v2 (picture conform + music take 1 + SFX + "STOP OR DIE!"), 13.0 s at 24 fps, 1920x1080.

Each entry: (shot, source file, [(in_s, out_s, speed), ...]). Output length of a piece = (out - in) / speed.
Shots 1, 2, 10-14 are H3 Max Turbo (fal); 3-9, 15, 16 are Kling 3.0 Turbo Pro (fal).
"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); F2 = os.path.dirname(HERE)
K, H = os.path.join(F2, "kling6"), os.path.join(F2, "h3fal")
CUT = [
    (1,  f"{H}/s01_h3.mp4", [(1.00, 2.25, 1)]),     # lid lifts, panel revealed
    (2,  f"{H}/s02_h3.mp4", [(1.50, 2.75, 1)]),     # eyes flick to the mirror
    (3,  f"{K}/s03_k1.mp4", [(1.50, 2.25, 1)]),     # Kaz grows in the mirror
    (4,  f"{K}/s04_k1.mp4", [(1.00, 4.00, 3)]),     # surge to level, 3x
    (5,  f"{K}/s05_k1.mp4", [(0.50, 1.25, 1)]),     # the stare (generated in slow motion)
    (6,  f"{K}/s06_k1.mp4", [(0.50, 1.50, 1)]),     # STOP OR DIE
    (7,  f"{K}/s07_k1.mp4", [(0.00, 0.75, 1)]),     # the ram
    (8,  f"{K}/s08_k1.mp4", [(1.00, 1.50, 1)]),     # sparks
    (9,  f"{K}/s09_k1.mp4", [(1.00, 2.50, 2)]),     # inches, 2x
    (10, f"{H}/s10_h3.mp4", [(0.30, 0.80, 1)]),     # catch the slide
    (11, f"{H}/s11_h3.mp4", [(1.00, 1.50, 1)]),     # Kaz grins
    (12, f"{K}/s12_k1.mp4", [(1.70, 2.20, 1)]),     # Eli's eyes: Kling take (photoreal skin; H3 take looked waxy)
    (13, f"{H}/s13_h3.mp4", [(1.80, 2.30, 1)]),     # the clock: end of the glitch, settles on 00:09:58
    (14, f"{H}/s14_h3.mp4", [(0.50, 1.00, 1)]),     # shifter
    (15, f"{K}/s15_k1.mp4", [(0.40, 1.90, 1)]),     # the squeeze (before Kling's hidden cut at 2.1 s)
    (16, f"{K}/s16_k1.mp4", [(0.30, 0.90, 1), (3.70, 4.10, 1)]),  # under the bridge + past the lens (Kling's own cut)
]
MUSIC = os.path.join(F2, "sound", "lyria_t1.mp3")
OUT = os.path.join(HERE, "golden_hour_s38_rough_v2.mp4")
tmp = os.path.join(HERE, "pieces_v2"); os.makedirs(tmp, exist_ok=True)

def run(cmd): subprocess.run(cmd, check=True)

pieces, total = [], 0.0
for n, src, segs in CUT:
    for j, (a, b, sp) in enumerate(segs):
        p = os.path.join(tmp, f"s{n:02d}_{j}.mp4"); frames = round((b - a) / sp * 24)
        vf = (f"trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{sp},fps=24,"
              f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1")
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vf", vf, "-frames:v", str(frames), "-an",
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", p])
        got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries",
                                  "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
        assert got == frames, f"shot {n} piece {j}: {got} frames, expected {frames} (window past the source end?)"
        pieces.append(p); total += frames / 24
lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in pieces))
pic = os.path.join(tmp, "picture.mp4")
run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic])

SND = os.path.join(F2, "sound")
# Stems: Sonilo synced SFX (whole cut) + ElevenLabs layers where Sonilo was thin + Lyria take 1 + Kaz's line.
# Kaz: "STOP..." starts over the end of the stare (4.55 s, sound lead-in), "...OR DIE!" lands with the finger jab (5.05 s);
# the crash hits at 6.0 s right on the tail of "DIE".
af = ("[1:a]asplit=3[m1][m2][m3];[6:a]asplit=2[o1][o2];[m1]atrim=0.5:6.5,asetpts=PTS-STARTPTS,afade=t=out:st=5.6:d=0.4,volume='if(between(t,4.4,6.0),0.45,1)':eval=frame[a1];"
      "[m2]atrim=6.5:10.5,asetpts=PTS-STARTPTS,volume=0.10,adelay=6000|6000[a2];"
      "[m3]atrim=26.0:29.0,asetpts=PTS-STARTPTS,afade=t=out:st=2.85:d=0.15,adelay=10000|10000[a3];"
      "[a1][a2][a3]amix=inputs=3:normalize=0:duration=longest,volume=0.55[mus];"
      "[2:a]volume=0.9[sfx];"
      "[3:a]atrim=0:0.8,asetpts=PTS-STARTPTS,afade=t=in:d=0.1,afade=t=out:st=0.6:d=0.2,volume=0.7,adelay=2500|2500[mir];"
      "[4:a]atrim=0:0.9,asetpts=PTS-STARTPTS,afade=t=out:st=0.6:d=0.3,volume=1.0,adelay=6000|6000[crash];"
      "[5:a]atrim=0:0.7,asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st=0.5:d=0.2,volume=0.8,adelay=6750|6750[grind];"
      "[o1]atrim=0.25:0.65,asetpts=PTS-STARTPTS,afade=t=out:st=0.34:d=0.06,volume=1.4,adelay=4550|4550[v1];"
      "[o2]atrim=1.05:2.12,asetpts=PTS-STARTPTS,afade=t=out:st=0.95:d=0.12,volume=1.4,adelay=5050|5050[v2];"
      "[mus][sfx][mir][crash][grind][v1][v2]amix=inputs=7:normalize=0:duration=longest,"
      "alimiter=limit=0.89,loudnorm=I=-14:TP=-1.0:LRA=11[a]")
mix = os.path.join(tmp, "mix.wav")
run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-t", "13", "-i", "anullsrc=r=48000:cl=stereo", "-i", MUSIC,
     "-i", f"{SND}/sfx_sonilo_v1.wav", "-i", f"{SND}/sfx_mirror.mp3", "-i", f"{SND}/sfx_crash.mp3", "-i", f"{SND}/sfx_grind.mp3",
     "-i", f"{SND}/vo_callum.mp3", "-filter_complex", af, "-map", "[a]", "-t", "13", "-ar", "48000", mix])
run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", pic, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
     "-c:a", "aac", "-b:a", "256k", "-t", "13", OUT])
print(f"{len(pieces)} pieces, picture {total:.3f} s -> {OUT}")
