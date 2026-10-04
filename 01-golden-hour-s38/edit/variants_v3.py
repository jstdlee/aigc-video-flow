#!/usr/bin/env python3
"""GOLDEN HOUR s38 v3: three cuts with the same timeline and the same mix, so only the video model differs.

  kling : every shot from Kling 3.0 Turbo Pro
  h3    : every shot from H3 Max Turbo (fal)
  mixed : per shot, the model that won the review (H3 for action inserts + the stare's wheel motion, Kling elsewhere)
Also writes a 2x2 split-screen (Kling | H3 / Mixed | legend) for side-by-side viewing.
Mix v3: background SFX bed lowered ~6 dB vs v2, hits lowered ~2-3 dB, voice up.
"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); F2 = os.path.dirname(HERE)
K, H, SND = f"{F2}/kling6", f"{F2}/h3fal", f"{F2}/sound"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# shot: ((kling file, windows), (h3 file, windows)); window = (in_s, out_s, speed)
TAKES = {
 1:  ((f"{K}/s01_k1.mp4", [(1.40, 2.65, 1)]), (f"{H}/s01_h3.mp4", [(1.00, 2.25, 1)])),
 2:  ((f"{K}/s02_k1.mp4", [(1.60, 2.85, 1)]), (f"{H}/s02_h3.mp4", [(1.50, 2.75, 1)])),
 3:  ((f"{K}/s03_k1.mp4", [(1.50, 2.25, 1)]), (f"{H}/s03_h3.mp4", [(1.60, 2.35, 1)])),
 4:  ((f"{K}/s04_k1.mp4", [(1.00, 4.00, 3)]), (f"{H}/s04_h3.mp4", [(1.00, 4.00, 3)])),
 5:  ((f"{K}/s05_k1.mp4", [(0.50, 1.25, 1)]), (f"{H}/s05_h3.mp4", [(0.60, 1.35, 1)])),
 6:  ((f"{K}/s06_k1.mp4", [(0.50, 1.50, 1)]), (f"{H}/s06_h3.mp4", [(1.90, 2.90, 1)])),
 7:  ((f"{K}/s07_k1.mp4", [(0.00, 0.75, 1)]), (f"{H}/s07_h3.mp4", [(0.00, 0.75, 1)])),
 8:  ((f"{K}/s08_k1.mp4", [(1.00, 1.50, 1)]), (f"{H}/s08_h3.mp4", [(1.00, 1.50, 1)])),
 9:  ((f"{K}/s09_k1.mp4", [(1.00, 2.50, 2)]), (f"{H}/s09_h3.mp4", [(1.00, 2.50, 2)])),
 10: ((f"{K}/s10_k1.mp4", [(0.60, 1.10, 1)]), (f"{H}/s10_h3.mp4", [(0.30, 0.80, 1)])),
 11: ((f"{K}/s11_k1.mp4", [(0.80, 1.30, 1)]), (f"{H}/s11_h3.mp4", [(1.00, 1.50, 1)])),
 12: ((f"{K}/s12_k1.mp4", [(1.70, 2.20, 1)]), (f"{H}/s12_h3.mp4", [(0.80, 1.30, 1)])),
 13: ((f"{K}/s13_k1.mp4", [(2.40, 2.90, 1)]), (f"{H}/s13_h3.mp4", [(1.80, 2.30, 1)])),
 14: ((f"{K}/s14_k1.mp4", [(0.80, 1.30, 1)]), (f"{H}/s14_h3.mp4", [(0.50, 1.00, 1)])),
 15: ((f"{K}/s15_k1.mp4", [(0.40, 1.90, 1)]), (f"{H}/s15_h3.mp4", [(0.60, 2.10, 1)])),
 16: ((f"{K}/s16_k1.mp4", [(0.30, 0.90, 1), (3.70, 4.10, 1)]), (f"{H}/s16_h3.mp4", [(2.00, 3.00, 1)])),
}
MIXED_H3 = {1, 5, 10, 13, 14}      # review winners for H3 Max Turbo; everything else Kling
CHOICE = {"kling": lambda n: 0, "h3": lambda n: 1, "mixed": lambda n: 1 if n in MIXED_H3 else 0}

def run(cmd): subprocess.run(cmd, check=True)
def nframes(p):
    return int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries",
                               "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

def picture(name):
    tmp = os.path.join(HERE, f"pieces_{name}"); os.makedirs(tmp, exist_ok=True); pieces = []
    for n in range(1, 17):
        src, segs = TAKES[n][CHOICE[name](n)]
        for j, (a, b, sp) in enumerate(segs):
            p = os.path.join(tmp, f"s{n:02d}_{j}.mp4"); fr = round((b - a) / sp * 24)
            vf = (f"trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{sp},fps=24,"
                  f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1")
            run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vf", vf, "-frames:v", str(fr), "-an",
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", p])
            assert nframes(p) == fr, f"{name} shot {n}.{j}: {nframes(p)} != {fr}"
            pieces.append(p)
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in pieces))
    pic = os.path.join(tmp, "picture.mp4")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic])
    assert nframes(pic) == 312, f"{name}: {nframes(pic)} frames"
    return pic

def mix():
    out = os.path.join(HERE, "mix_v3.wav")
    af = ("[1:a]asplit=3[m1][m2][m3];[6:a]asplit=2[o1][o2];"
          "[m1]atrim=0.5:6.5,asetpts=PTS-STARTPTS,afade=t=out:st=5.6:d=0.4,volume='if(between(t,4.4,6.0),0.45,1)':eval=frame[a1];"
          "[m2]atrim=6.5:10.5,asetpts=PTS-STARTPTS,volume=0.10,adelay=6000|6000[a2];"
          "[m3]atrim=26.0:29.0,asetpts=PTS-STARTPTS,afade=t=out:st=2.85:d=0.15,adelay=10000|10000[a3];"
          "[a1][a2][a3]amix=inputs=3:normalize=0:duration=longest,volume=0.60[mus];"
          "[2:a]volume=0.45[sfx];"                                               # background bed: was 0.9 (-6 dB)
          "[3:a]atrim=0:0.8,asetpts=PTS-STARTPTS,afade=t=in:d=0.1,afade=t=out:st=0.6:d=0.2,volume=0.45,adelay=2500|2500[mir];"
          "[4:a]atrim=0:0.9,asetpts=PTS-STARTPTS,afade=t=out:st=0.6:d=0.3,volume=0.75,adelay=6000|6000[crash];"
          "[5:a]atrim=0:0.7,asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st=0.5:d=0.2,volume=0.55,adelay=6750|6750[grind];"
          "[o1]atrim=0.25:0.65,asetpts=PTS-STARTPTS,afade=t=out:st=0.34:d=0.06,volume=1.6,adelay=4550|4550[v1];"
          "[o2]atrim=1.05:2.12,asetpts=PTS-STARTPTS,afade=t=out:st=0.95:d=0.12,volume=1.6,adelay=5050|5050[v2];"
          "[mus][sfx][mir][crash][grind][v1][v2]amix=inputs=7:normalize=0:duration=longest,"
          "alimiter=limit=0.85,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-t", "13", "-i", "anullsrc=r=48000:cl=stereo",
         "-i", f"{SND}/lyria_t1.mp3", "-i", f"{SND}/sfx_sonilo_v1.wav", "-i", f"{SND}/sfx_mirror.mp3",
         "-i", f"{SND}/sfx_crash.mp3", "-i", f"{SND}/sfx_grind.mp3", "-i", f"{SND}/vo_callum.mp3",
         "-filter_complex", af, "-map", "[a]", "-t", "13", "-ar", "48000", out])
    return out

if __name__ == "__main__":
    wav = mix(); outs = {}
    for name in ("kling", "h3", "mixed"):
        out = os.path.join(HERE, f"golden_hour_s38_v3_{name}.mp4")
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", picture(name), "-i", wav, "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", "13", out])
        outs[name] = out; print("wrote", out, flush=True)
    # 2x2 split-screen: Kling | H3 / Mixed | legend
    legend = "Mixed cut uses H3 Max Turbo for shots 1, 5, 10, 13, 14\\nand Kling 3.0 Turbo Pro for all other shots"
    lab = lambda t: f"drawtext=fontfile={FONT}:text='{t}':x=20:y=18:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=10"
    fc = (f"[0:v]scale=960:540,{lab('KLING 3.0 TURBO PRO')}[a];[1:v]scale=960:540,{lab('H3 MAX TURBO')}[b];"
          f"[2:v]scale=960:540,{lab('MIXED (BEST PER SHOT)')}[c];"
          f"color=c=0x15181b:s=960x540:r=24:d=13,drawtext=fontfile={FONT}:text='{legend}':x=40:y=200:fontsize=28:"
          f"fontcolor=0xe7e4de:line_spacing=14,"
          f"drawtext=fontfile={FONT}:text='%{{eif\\:floor(t*24)\\:d}} / 312 fr':x=40:y=420:fontsize=40:fontcolor=0xe39a3b[d];"
          "[a][b][c][d]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[v]")
    split = os.path.join(HERE, "golden_hour_s38_v3_compare_2x2.mp4")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", outs["kling"], "-i", outs["h3"], "-i", outs["mixed"],
         "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "copy", "-t", "13", split])
    print("wrote", split)
