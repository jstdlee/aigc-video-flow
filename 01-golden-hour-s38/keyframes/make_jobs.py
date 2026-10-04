# Build GPT Image 2.5 keyframe jobs (one start keyframe per shot) from the board's shot data.
import json, runpy, os
B = "../board/build.py"
src = open(B).read(); src = src[:src.index("def fig(")]          # data only
d = {"__file__": B}; exec(src, d); SHOTS, GLOBAL, LABEL = d["SHOTS"], d["GLOBAL"], d["LABEL"]
URL = {}
for line in open(os.path.expanduser("~/dev/blender/highway-race/film2/fal/urls.txt")):
    n, u = line.split(); URL[n[:-4]] = u                          # later lines win (90s versions)
ALIAS = {"cars": "cars", "props90": "props", "device90": "device", "interior_a90": "interior_a", "eli_seated90": "eli_seated",
         "eli_hands90": "eli_hands", "kaz_rage90": "kaz_rage", "eli_reaction90": "eli_reaction", "grade_key90": "grade_key",
         "plate_forward90": "plate_forward", "plate_back90": "plate_back", "car_a_dmg": "car_a_damaged", "car_b_dmg": "car_b_damaged"}
CODES = ("Its flat colours are only codes: the dark car is car A, the red car is car B, the white box is the box truck, "
         "the grey box is the silver sedan; skin-tone figures are the drivers.")
FIX = {
 1: "Screen layout, follow image 1: the camera is at the passenger door looking across the device toward the driver. Eli sits beyond the device at frame-right with the steering wheel in front of him at frame-right; his right arm reaches in from frame-right and lifts the lid. There is no steering wheel at frame-left. No red car anywhere; only distant traffic far ahead.",
 2: "Screen layout: the camera is in front of car A looking back. Eli and the steering wheel are at frame-right; the passenger seat with the device is at frame-left. Behind the car the concrete median runs along frame-RIGHT and the guardrail along frame-left. Far behind, the tiny red coupe is in the lane next to the median, on the frame-right half, headlights on toward us. Every car behind faces us with headlights on.",
 5: "Screen layout, follow image 1: car B is side-on with its tall rear wing at frame-LEFT and its nose at frame-RIGHT. Kaz faces frame-right with both hands on his wheel. Both cars travel toward frame-right.",
 7: "Screen layout, follow image 1: the red coupe is on the LEFT of the frame, between the concrete median and the black muscle car; the black muscle car is to the right of the red coupe; the silver sedan is to the right of the black car and a little behind. The red coupe's front-right corner touches the black car's left rear door.",
 8: "Screen layout, follow image 1: the camera is low BEHIND both cars, between them, looking forward in the direction of travel toward the low sun. We see both cars from behind: their rear bumpers and red taillights are nearest to camera. The red coupe is on frame-LEFT (its rear wing visible), the black muscle car on frame-RIGHT. Ahead of us, the red coupe's front-right corner grinds into the black car's left rear door; the sparks fly backward toward the camera. Traffic far ahead drives away from us. The concrete median is at the far left.",
 9: "Screen layout: the camera is ahead looking back, so frame-left is the drivers' right. The silver sedan and the right shoulder are on frame-LEFT. The concrete median and the red coupe are on frame-RIGHT. Car A is in the centre, its nose angled toward frame-left at the sedan. Its dented left side faces frame-right. Its driver sits on the frame-right side of its windshield.",
 10: "Through the windshield: only the white box truck directly ahead in our lane and the open road. No red car and no other car ahead. The horizon is tilted by the swerve. The display reads 00:40:59.",
 12: "Behind Eli, through the rear window: only the blurred sunlit road and trees. No cars behind him.",
 14: "Through the windshield: only the white box truck directly ahead in our lane. No red car and no other car ahead.",
 15: "The right lane ahead is completely empty. No car in the right lane or on the right shoulder ahead; the silver sedan is not in this frame.",
}
jobs = []
for s in SHOTS:
    clay = {7: "clay_hit_a"}.get(s["n"], s["sb"][0]); refs = [r for r in s["refs"]]
    urls = [URL[ALIAS.get(clay, clay)]] + [URL[ALIAS.get(r, r)] for r in refs]
    if "grade_key90" not in refs: urls.append(URL["grade_key"]); refs.append("grade_key90")
    def role(r):
        if r == "grade_key90": return "the grade key: use it only for light, colour, haze and film texture, never for composition"
        if r.startswith("plate_"): return f"the {LABEL[r]}: use it only for the look of the road, landscape and sky"
        if r == "map_detail": return "the labelled top-down lane map: use it only to place cars in the correct lanes"
        if r == "cars": return "the design sheet of car A (black muscle car) and car B (red coupe): match both designs exactly"
        return f"the {LABEL.get(r, r)} reference sheet: match it exactly"
    lines = [f"Image {i+2} is {role(r)}." for i, r in enumerate(refs)]
    p = (f"Image 1 is the 3D previs frame of this shot. It is the ground truth for camera position, lens, framing and the position "
         f"of every car and person. {CODES} Re-render it as one photoreal frame from a 1997 feature film.\n"
         f"SHOT {s['n']}, {s['name']}. Camera: {s['cam']}, {s['lens']} lens.\n{s['key']}\n" + (FIX[s['n']] + "\n" if s['n'] in FIX else "") + " ".join(lines) +
         f"\nLook: {GLOBAL}\nOne single image that fills the whole 16:9 frame, no letterbox bars. No text, no captions, no borders, no watermark.")
    jobs.append({"n": s["n"], "input": {"prompt": p, "image_urls": urls, "image_size": {"width": 1920, "height": 1088},
                                        "quality": "high", "output_format": "jpeg"}})
json.dump(jobs, open(os.path.join(os.path.dirname(__file__), "jobs.json"), "w"), indent=1)
json.dump([j for j in jobs if j["n"] in FIX], open(os.path.join(os.path.dirname(__file__), "jobs_r2.json"), "w"), indent=1)
print(len(jobs), "jobs;", sum(len(j["input"]["image_urls"]) for j in jobs), "image refs;", max(len(j["input"]["prompt"]) for j in jobs), "max prompt chars")
