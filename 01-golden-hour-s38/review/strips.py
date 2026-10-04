#!/usr/bin/env python3
"""strips.py OUT.jpg video1 [video2 ...]: one row per video, 6 frames spread evenly over its length, 320 px each."""
import json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
rows = []
for f in sys.argv[2:]:
    d = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", f],
                                        capture_output=True, text=True).stdout)["format"]["duration"])
    ims = []
    for k in range(6):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{d * k / 6 + 0.02:.2f}", "-i", f,
                        "-frames:v", "1", "-vf", "scale=320:-1", "/tmp/_strip.jpg"])
        ims.append(Image.open("/tmp/_strip.jpg").copy())
    row = Image.new("RGB", (320 * 6, ims[0].height))
    for k, im in enumerate(ims): row.paste(im, (320 * k, 0))
    ImageDraw.Draw(row).text((6, 4), f.split("/")[-1], font=font, fill=(255, 210, 120))
    rows.append(row)
out = Image.new("RGB", (1920, sum(r.height for r in rows))); y = 0
for r in rows: out.paste(r, (0, y)); y += r.height
out.save(sys.argv[1], quality=88)
