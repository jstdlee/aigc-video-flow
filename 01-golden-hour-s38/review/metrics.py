#!/usr/bin/env python3
"""Objective image-quality metrics for every generated take (Kling 3.0 Turbo Pro vs H3 Max Turbo on fal).

Per take (luminance, numpy only):
  sharp_start / sharp_end : mean Laplacian magnitude at full res, first 10 % vs last 20 % of frames
  detail_keep             : sharp_end / sharp_start (1.0 = no softening over the clip)
  grain                   : std of the high-pass residual in the flattest 20 % of 32 px blocks (film-grain level)
  flicker                 : mean |delta| of per-frame mean luminance, frame to frame (0-255 scale)
  motion                  : mean |delta| between consecutive 480 px frames (how much moves)
  kf_psnr                 : PSNR of frame 0 vs the approved keyframe (how faithfully the start frame is kept)
  bitrate_mbps            : encoded video bitrate
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

F2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAKES = [(n, "kling", f"{F2}/kling6/s{n:02d}_k1.mp4") for n in (3, 4, 5, 6, 7, 8, 9, 15, 16)] + \
        [(n, "h3", f"{F2}/h3fal/s{n:02d}_h3.mp4") for n in (1, 2, 10, 11, 12, 13, 14, 7)]
if os.path.exists(f"{F2}/kling6/s12_k1.mp4"):
    TAKES.append((12, "kling", f"{F2}/kling6/s12_k1.mp4"))

def probe(f):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                                   "stream=width,height,bit_rate,nb_frames:format=duration", "-of", "json", f],
                                  capture_output=True, text=True).stdout)
    s = j["streams"][0]
    return int(s["width"]), int(s["height"]), float(j["format"]["duration"]), float(s.get("bit_rate", 0)) / 1e6

def frames(f, w, h):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f, "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)

def lap(y):
    return np.abs(4 * y[1:-1, 1:-1] - y[:-2, 1:-1] - y[2:, 1:-1] - y[1:-1, :-2] - y[1:-1, 2:]).mean()

def grain(y):
    blur = (y[:-2, 1:-1] + y[2:, 1:-1] + y[1:-1, :-2] + y[1:-1, 2:] + y[1:-1, 1:-1]) / 5
    hp = y[1:-1, 1:-1] - blur; b = 32
    H, W = (hp.shape[0] // b) * b, (hp.shape[1] // b) * b
    blocks = y[1:H + 1, 1:W + 1].reshape(H // b, b, W // b, b).std(axis=(1, 3)).ravel()
    hpb = hp[:H, :W].reshape(H // b, b, W // b, b).std(axis=(1, 3)).ravel()
    flat = blocks <= np.quantile(blocks, 0.2)
    return float(hpb[flat].mean())

def small(y):
    return np.asarray(Image.fromarray(y.astype(np.uint8)).resize((480, 270), Image.BILINEAR), np.float32)

def keyframe(n, w, h):
    im = Image.open(f"{F2}/keys6/final/s{n:02d}.jpg").convert("L").resize((w, h), Image.LANCZOS)
    return np.asarray(im, np.float32)

rows = []
for n, model, f in TAKES:
    w, h, dur, br = probe(f); Y = frames(f, w, h); N = len(Y)
    a, b = max(1, N // 10), max(1, N // 5)
    s0 = float(np.mean([lap(y) for y in Y[:a]])); s1 = float(np.mean([lap(y) for y in Y[-b:]]))
    means = Y.mean(axis=(1, 2)); S = np.stack([small(y) for y in Y])
    mse = float(((Y[0] - keyframe(n, w, h)) ** 2).mean())
    rows.append(dict(shot=n, model=model, frames=N, dur=round(dur, 2), res=f"{w}x{h}", bitrate_mbps=round(br, 1),
                     sharp_start=round(s0, 2), sharp_end=round(s1, 2), detail_keep=round(s1 / s0, 3),
                     grain=round(float(np.mean([grain(y) for y in Y[::max(1, N // 8)]])), 2),
                     flicker=round(float(np.abs(np.diff(means)).mean()), 3),
                     motion=round(float(np.abs(np.diff(S, axis=0)).mean()), 2),
                     kf_psnr=round(10 * np.log10(255 ** 2 / mse), 2)))
    print(rows[-1], flush=True)
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "metrics.json"), "w"), indent=1)
