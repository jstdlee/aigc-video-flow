#!/usr/bin/env python3
"""GOLDEN HOUR s38: rough cut v1 (picture conform + music take 1), 13.0 s at 24 fps, 1920x1080.

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
    (12, f"{H}/s12_h3.mp4", [(0.80, 1.30, 1)]),     # Eli's eyes
    (13, f"{H}/s13_h3.mp4", [(1.80, 2.30, 1)]),     # the clock: end of the glitch, settles on 00:09:58
    (14, f"{H}/s14_h3.mp4", [(0.50, 1.00, 1)]),     # shifter
    (15, f"{K}/s15_k1.mp4", [(0.40, 1.90, 1)]),     # the squeeze (before Kling's hidden cut at 2.1 s)
    (16, f"{K}/s16_k1.mp4", [(0.30, 0.90, 1), (3.70, 4.10, 1)]),  # under the bridge + past the lens (Kling's own cut)
]
MUSIC = os.path.join(F2, "sound", "lyria_t1.mp3")
OUT = os.path.join(HERE, "golden_hour_s38_rough_v1.mp4")
tmp = os.path.join(HERE, "pieces"); os.makedirs(tmp, exist_ok=True)

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

# Music, take 1: [0.5-6.5] under shots 1-6 (its hit lands on the ram at 6.0 s), a low tail while metal and tyres
# take over (6.0-10.0, to be filled with SFX), then the orchestral re-entry at 26.0 s slams in on the shifter (10.0 s).
af = ("[1:a]atrim=0.5:6.5,asetpts=PTS-STARTPTS,afade=t=out:st=5.6:d=0.4[a1];"
      "[1:a]atrim=6.5:10.5,asetpts=PTS-STARTPTS,volume=0.12,adelay=6000|6000[a2];"
      "[1:a]atrim=26.0:29.0,asetpts=PTS-STARTPTS,afade=t=out:st=2.85:d=0.15,adelay=10000|10000[a3];"
      "[a1][a2][a3]amix=inputs=3:normalize=0,atrim=0:13,loudnorm=I=-16:TP=-1.5[a]")
run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", pic, "-i", MUSIC, "-filter_complex", af,
     "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", OUT])
print(f"{len(pieces)} pieces, picture {total:.3f} s -> {OUT}")
