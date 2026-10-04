#!/usr/bin/env python3
"""GOLDEN HOUR s38 v6: H3 image-to-video for the interior / face shots (the "mix" plan; car action goes to Kling).

Per shot: the approved GPT Image 2.5 keyframe (keys6/final) is pinned at frame 0 with MiniMaxH3AddGuide,
1-2 asset sheets condition every step through MiniMaxH3ReferenceToVideo. 49 frames (2 s) at 1280x704,
Turbo LoRA, 8 steps. The edit trims each take to its board length.

usage: gen_shot6.py [--take K] [--steps N] 1 2 10 ...   -> shots6/s<NN>_t<K>.mp4
"""
import argparse, json, os, shutil, sys, time, urllib.request, uuid
from PIL import Image

COMFY = "http://127.0.0.1:8188"
HERE = os.path.dirname(os.path.abspath(__file__))
IN_ROOT = os.path.join(HERE, "..", "film", "comfy_in")        # the running ComfyUI's --input-directory
OUT_ROOT = os.path.join(HERE, "..", "film", "comfy_out")      # the running ComfyUI's --output-directory
W, H, LENGTH = 1280, 704, 49

LOOK = ("1997 late-90s action thriller, 35mm Kodak film stock, fine grain, gentle halation, low golden-hour sun, warm amber light, "
        "smoky haze, 24 fps real time. Keep every face, hand, prop and the cabin exactly as in the first frame. ")
SHEETS = {"device": "assets3/device.jpg", "eli_hands": "assets3/eli_hands.jpg", "eli_seated": "assets3/eli_seated.jpg",
          "eli_reaction": "assets3/eli_reaction.jpg", "kaz_seated": "assets2/kaz_seated.jpg", "car_b_dmg": "assets4/car_b_damaged.jpg"}
REF_TEXT = {"device": "<Picture {n}> is the rusted nuclear device with the red countdown; keep it exactly. ",
            "eli_hands": "<Picture {n}> shows Eli's hands and brown leather sleeves; keep them exactly. ",
            "eli_seated": "<Picture {n}> is Eli (short dark hair, stubble, brown leather jacket); keep his face exactly. ",
            "eli_reaction": "<Picture {n}> shows Eli's face in close-up; keep his face exactly. ",
            "kaz_seated": "<Picture {n}> is Kaz (black cap, black bomber jacket); keep his face exactly. ",
            "car_b_dmg": "<Picture {n}> is Kaz's red coupe with its crushed front-right corner; keep it exactly. "}

# shot: (refs, seed, directed motion)
SHOTS = {
 1: (["device", "eli_hands"], 601,
     "INSERT inside car A, slow push-in toward the device on the passenger seat. Eli's right hand lifts the heavy rusted lid on creaking hinges "
     "and the control panel is revealed; the red digits tick from 00:41:12 to 00:41:11; the green lamp pulses; dust floats in strobing sunlight; "
     "his left hand stays on the wheel; the cabin vibrates at speed."),
 2: (["eli_seated", "eli_reaction"], 602,
     "Camera car in front of car A, slow push-in on Eli through the windshield; the car sways gently on its suspension. Eli drives calm, "
     "then his eyes flick to his left door mirror and his brow tightens. Far behind him the red coupe approaches with its headlights on."),
 10: (["eli_hands", "device"], 610,
     "Inside car A, fast push-in on Eli's hands: he spins the wood-rim wheel hand over hand to the left, then counter-steers once to catch the slide. "
     "The whole cabin shakes hard, the device bounces against its seat belt, the horizon outside tilts and then levels. The white truck stays ahead."),
 11: (["kaz_seated", "car_b_dmg"], 611,
     "Slow push-in on Kaz through his open passenger window. He breathes hard, regrips the wheel, and a slow cold grin spreads; his eyes stay "
     "locked on camera. The loose bumper corner rattles; the background streams past at highway speed. He stays seated in his car."),
 12: (["eli_reaction", "eli_seated"], 612,
     "Quick snap zoom into Eli's eyes. His eyes narrow, his jaw clenches, a muscle twitches at his temple, sweat glints; sunlight flickers across his face."),
 13: (["device"], 613,
     "Macro on the device panel, static camera, slight vibration at speed. Rack focus from the keypad to the red digits; the digits glitch and "
     "flicker, then settle and tick from 00:09:59 to 00:09:58; the red warning lamp flashes fast."),
 14: (["eli_hands", "device"], 614,
     "INSERT over car A's console: Eli rams the chrome T-handle shifter forward; the whole car lunges, the camera jolts, and the view through "
     "the windshield surges toward the white truck ahead."),
}

def node(c, **i): return {"class_type": c, "inputs": i}

def post(p, d=None):
    r = urllib.request.Request(COMFY + p, data=json.dumps(d).encode() if d else None, headers={"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:2000]}")

def stage(n, refs):
    """Copy the keyframe (cropped to the video aspect) and the sheets into ComfyUI's input dir."""
    d = os.path.join(IN_ROOT, "gh6"); os.makedirs(d, exist_ok=True)
    im = Image.open(os.path.join(HERE, "keys6", "final", f"s{n:02d}.jpg")).convert("RGB")
    s = W / im.width; im = im.resize((W, round(im.height * s)), Image.LANCZOS)
    top = (im.height - H) // 2; im.crop((0, top, W, top + H)).save(os.path.join(d, f"key{n:02d}.png"))
    for r in refs:
        shutil.copy(os.path.join(HERE, SHEETS[r]), os.path.join(d, f"{r}.jpg"))

def graph(n, seed, steps):
    refs, _, action = SHOTS[n]
    prompt = LOOK + "".join(REF_TEXT[r].format(n=i + 1) for i, r in enumerate(refs)) + "SHOT: " + action
    g = {"unet": node("UNETLoader", unet_name="minimax_h3_fl2va_pruned_int8_convrot.safetensors", weight_dtype="default"),
         "lora": node("MiniMaxH3TurboLoRA", model=["unet", 0], lora_name="minimax_h3_turbo_4step_ema_ckpt850.safetensors", strength=1.0, low_vram=False),
         "clip": node("CLIPLoader", clip_name="qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", type="minimax", device="default"),
         "vae": node("VAELoader", vae_name="minimax_h3_video_vae_fp16.safetensors"),
         "avae": node("VAELoader", vae_name="minimax_h3_audio_vae_fp32.safetensors")}
    refin = {}
    for i, r in enumerate(refs):
        g[f"ref{i}"] = node("LoadImage", image=f"gh6/{r}.jpg")
        refin[f"ref_images.ref_image_{i}"] = [f"ref{i}", 0]
    g["r2v"] = {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": {
        "clip": ["clip", 0], "vae": ["vae", 0], "audio_vae": ["avae", 0], "prompt": prompt,
        "width": W, "height": H, "length": LENGTH, "ref_image_size": "match", **refin}}
    g["k0"] = node("LoadImage", image=f"gh6/key{n:02d}.png")
    g["g0"] = node("MiniMaxH3AddGuide", positive=["r2v", 0], latent=["r2v", 1], vae=["vae", 0], image=["k0", 0], frame_idx=0)
    g.update({
        "noise": node("RandomNoise", noise_seed=seed),
        "sampler": node("KSamplerSelect", sampler_name="res_multistep"),
        "sched": node("BasicScheduler", model=["lora", 0], scheduler="simple", steps=steps, denoise=1.0),
        "guider": node("BasicGuider", model=["lora", 0], conditioning=["g0", 0]),
        "sample": node("SamplerCustomAdvanced", noise=["noise", 0], guider=["guider", 0], sampler=["sampler", 0],
                       sigmas=["sched", 0], latent_image=["r2v", 1]),
        "dec": node("VAEDecode", samples=["sample", 0], vae=["vae", 0]),
        "adec": node("VAEDecodeAudio", samples=["sample", 0], vae=["avae", 0]),
        "video": node("CreateVideo", images=["dec", 0], fps=24, audio=["adec", 0]),
        "save": {"class_type": "SaveVideo", "inputs": {"video": ["video", 0], "filename_prefix": f"gh6/s{n:02d}",
                                                         "format": "auto", "format.codec": "auto"}},
    })
    return g, prompt

def run(n, take, steps):
    refs, seed0, _ = SHOTS[n]; seed = seed0 + 1000 * take
    stage(n, refs)
    g, prompt = graph(n, seed, steps)
    t0 = time.time()
    pid = post("/prompt", {"prompt": g, "client_id": str(uuid.uuid4())})["prompt_id"]
    while True:
        hist = post(f"/history/{pid}")
        if pid in hist:
            st = hist[pid]["status"]
            if st.get("status_str") == "error":
                print(f"s{n:02d}: error {json.dumps(st.get('messages', []))[-1500:]}", flush=True); return False
            fs = [f for o in hist[pid]["outputs"].values() for k in ("images", "videos") for f in o.get(k, [])]
            if fs:
                dst = os.path.join(HERE, "shots6", f"s{n:02d}_t{take}.mp4")
                shutil.copy(os.path.join(OUT_ROOT, fs[0]["subfolder"], fs[0]["filename"]), dst)
                with open(dst.replace(".mp4", ".txt"), "w") as fh:
                    fh.write(f"seed {seed} {W}x{H} {LENGTH}f {steps} steps\n{prompt}\n")
                print(f"s{n:02d} take {take}: {time.time() - t0:.0f}s -> shots6/{os.path.basename(dst)}", flush=True)
                return True
        time.sleep(5)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--take", type=int, default=1); ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("shots", nargs="+", type=int)
    a = ap.parse_args()
    os.makedirs(os.path.join(HERE, "shots6"), exist_ok=True)
    for s in a.shots:
        run(s, a.take, a.steps)
