# Builds the GOLDEN HOUR scene design board (index.html) from the shot data below.
import html, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape

GLOBAL = ("1997. Late-90s action thriller shot on 35mm Kodak film stock, anamorphic 2.39:1 lenses with oval flare, fine visible grain, gentle halation, "
          "slightly softer contrast, 24 fps real time, 180° shutter. Low golden-hour sun ahead of the cars, 3200 K warm key, warm rim light, smoky haze. "
          "Colour ratio 60 % warm asphalt and dry-grass ochre, 30 % olive-teal shadows and pine, 10 % red accent: Kaz's coupe and the countdown LED. "
          "Right-hand traffic: concrete median on the drivers' left, guardrail on their right; every vehicle drives forward in its own lane; 1990s traffic.")
FPS = 24
def tc(fr):  # first frame -> HH:MM:SS:FF
    f = fr - 1; return f"00:00:{f // FPS:02d}:{f % FPS:02d}"
SHOTS = [
 dict(n=1, name="The lid opens", frames=(1, 30), lens="35 mm macro", cam="Inside car A, over the passenger seat",
      move="Slow push-in onto the display", beat="Eli flips open the rusted lid. The red countdown reads 00:41:12. This is what both men want.",
      perf="Eli's hand lifts the lid, then returns to the shifter.", sb=("clay_0001", "device90"), bg="interior_a90",
      refs=["device90", "interior_a90", "eli_hands90"],
      key="Insert inside car A (left-hand drive, interior exactly as the interior sheet). The rusted Soviet-era nuclear device case from the device sheet is belted into the passenger seat. Eli's hand in a worn brown leather sleeve lifts the dented lid; the control panel is revealed: red seven-segment countdown reading 00:41:12, steel keypad, key slots, toggle switches under red flip covers, needle gauges, green armed lamp. Sun strobes through the window. 35mm film look.",
      vid="Slow push-in toward the display. 0–0.6 s: Eli's hand lifts the heavy lid on creaking hinges, dust in the sun. 0.6–1.25 s: the red digits tick 00:41:12 → 00:41:11; the green lamp pulses. 24 fps real time. The device stays belted to the seat."),
 dict(n=2, name="Something is coming", frames=(31, 60), lens="44→52 mm", cam="Camera car in front of car A, 1.4 m, looking back",
      move="Slow push-in (dolly, not a zoom)", beat="Eli drives calm. His eyes flick to his left mirror. His brow tightens.",
      perf="Calm, then wary.", sb=("clay_0031", "clay_0066"), bg="plate_back90", refs=["eli_seated90", "eli_reaction90", "interior_a90"],
      key="Medium close-up through the open windshield of car A, the gloss-black 1970s muscle car, from its hood. Eli at the wood-rim wheel on the left of the car (frame-right), calm. The rusted device on the passenger seat (frame-left), red digits glowing. Behind him the highway recedes; a tiny red car far back in the fast lane.",
      vid="Camera car in front of car A, slow forward push of 30 cm, constant speed, field of view constant. 0–0.6 s: Eli drives calm. 0.6–1.25 s: his eyes flick to his left mirror; his brow tightens. 24 fps real time."),
 dict(n=3, name="The hunter in the mirror", frames=(61, 78), lens="78→86 mm", cam="Eli's eye-line into his left door mirror",
      move="Locked to the door, mirror vibrates", beat="Kaz's red coupe weaves out of traffic behind and closes fast, head-on in the glass.",
      perf="—", sb=("clay_0067", "clay_0084"), bg="plate_back90", refs=["cars", "grade_key90"],
      key="Point of view from car A's driver seat into its chrome left door mirror. The mirror shows the road behind: car B, the candy-red 1990s coupe with the tall rear wing, head-on, headlights on, in the lane to our left, closing in. Beyond the window: the concrete median and the fast lane blur past.",
      vid="Camera locked to the door; the mirror vibrates at speed. In the glass, car B weaves out of 1990s traffic and grows fast, headlights toward us. 24 fps real time."),
 dict(n=4, name="Boxed in", frames=(79, 102), lens="30 mm drone", cam="Drone 3.6–4.8 m high, 11–17 m behind",
      move="Descending track at traffic speed", beat="Eli is boxed in behind the truck. Kaz surges up the fast lane and pulls level on his left, under the gantry.",
      perf="—", sb=("clay_0085", "clay_0114"), bg="plate_forward90", refs=["cars", "props90", "grade_key90", "map_detail"],
      key="High drone shot from behind and above; every car drives away from camera with red taillights. Car A in the middle lane boxed in behind the mid-1990s white box truck; the 1990s silver sedan in the right lane; the green sign gantry ahead; car B's red nose enters bottom-left in the empty fast lane.",
      vid="Drone tracks at traffic speed, descending. Car B surges up the fast lane, nose dips as it brakes, and settles level with car A on its left as both pass under the gantry. 24 fps real time."),
 dict(n=5, name="The stare", frames=(103, 120), lens="32→38 mm", cam="Inside car A behind Eli's right shoulder, looking left",
      move="Handheld drift, slow motion begins", beat="Side by side. Kaz turns. The two men look at each other.",
      perf="Kaz turns, jaw tight; Eli still.", sb=("clay_0115", "clay_0144"), bg="kaz_interior", refs=["eli_seated90", "kaz_seated", "kaz_interior", "cars"],
      key="Over Eli's right shoulder inside car A, looking out of his open window. The back of Eli's head soft in the right foreground. Car B alongside, side-on, nose toward frame-right. Kaz (black cap, black bomber) at car B's wheel on the far side, turning toward Eli.",
      vid="Slow motion begins (0.5×), gentle handheld drift. Kaz turns his head toward Eli, eyes hard. Wind ripples jackets. Both cars hold their lanes."),
 dict(n=6, name="“Stop or die!”", frames=(121, 144), lens="50→75 mm", cam="From car A across the gap into Kaz's window",
      move="Push-in to a close-up, slow motion", beat="Kaz explodes: he points at Eli and shouts “STOP OR DIE!”.",
      perf="Fury: mouth wide on “STOP”, finger jabbing on “DIE”, neck tendons straining.", sb=("clay_kaz_across", "clay_0144"), bg="kaz_interior",
      refs=["kaz_rage90", "kaz_seated", "kaz_interior"],
      key="Close-up of Kaz at the wheel of the red coupe, seen through his open passenger window from car A beside him. He is furious, mid-shout, mouth wide, pointing hard toward camera; face exactly as the rage sheet; red paint reflections on his face; golden-hour rim light; 35mm film look.",
      vid="Push-in from 50 to 75 mm. Slow motion 0.5×. Kaz leans toward his passenger window and shouts “STOP OR DIE!” with fury: mouth wide on “STOP”, finger jabbing toward camera on “DIE”, spit in the light. Lip movement matches the line. He stays seated in car B."),
 dict(n=7, name="The ram", frames=(145, 162), lens="30 mm drone", cam="Drone 7.5 m high, 16 m behind-left",
      move="Track at speed, shudders on impact", beat="Kaz yanks his wheel right. His coupe slams into car A's left rear door. Car A's tail kicks out.",
      perf="Kaz's answer to no answer.", sb=("clay_0144", "clay_hit_a"), bg="plate_forward90", refs=["cars", "props90", "grade_key90", "map_detail"],
      key="High drone shot from behind and to the left; every car drives away from camera with red taillights. Car B, the candy-red 1990s coupe, has swerved right out of the fast lane; its front-right corner slams into the left rear door of car A, the gloss-black 1970s muscle car, in the middle lane. Car A's rear kicks out, its nose turning right. The silver 1990s sedan just behind in the right lane; the white box truck ahead; tyre smoke; 35mm film look.",
      vid="Drone tracks at traffic speed. 0–0.3 s: car B jerks right across the lane line. 0.3 s: impact. Its nose crunches into car A's left rear door; sparks and paint flakes burst; both bodies rock on their suspension. 0.3–0.75 s: car A is shoved right, its rear stepping out, tyres smoking. The camera shudders on the hit. 24 fps real time."),
 dict(n=8, name="Metal on metal", frames=(163, 174), lens="24 mm", cam="Low between the two cars, 0.45 m, at the contact",
      move="Rig shakes hard", beat="Close on the contact: the coupe's fender grinds along car A's door in a shower of sparks.",
      perf="—", sb=("clay_hit_b", "clay_hit_b"), bg="plate_forward90", refs=["cars", "grade_key90", "car_a_dmg", "car_b_dmg"],
      key="Low extreme close shot between two cars at speed: the red coupe's front fender grinds along the black muscle car's dented left door. A bright fan of orange sparks sprays back toward camera, paint chips fly, chrome trim bends, the road is a streaked blur below; golden-hour backlight; 35mm film look.",
      vid="The camera shakes hard at speed. The fender grinds along the door for the whole shot; sparks spray back past the lens; the door panel crumples; a strip of chrome trim tears loose and flies. 24 fps real time."),
 dict(n=9, name="Inches", frames=(175, 192), lens="35 mm", cam="Camera car ahead in the right lane, 1.1 m, looking back",
      move="Car A slides at camera", beat="Car A is shoved into the right lane, nose first at the silver sedan. The sedan swerves onto the shoulder, horn blaring. Inches.",
      perf="—", sb=("clay_hit_c", "clay_hit_c"), bg="plate_back90", refs=["cars", "props90", "plate_back90", "grade_key90", "map_detail", "car_a_dmg"],
      key="From a camera car ahead looking back down our side of the highway: car A, the black muscle car with a fresh dent and scrape on its left side, slides diagonally into the right lane, nose angled right, headlights toward us. The silver 1990s sedan beside it swerves onto the shoulder; the gap between them is less than a hand. Car B drops back in the fast lane; the white truck behind; smoke from car A's tyres; 35mm film look.",
      vid="Car A slides toward the camera and the sedan, its body rolling hard. The sedan swerves right onto the shoulder, horn blaring, gravel spraying. The gap closes to inches, then car A snaps back left into the middle lane. Every car keeps moving forward. 24 fps real time."),
 dict(n=10, name="Catch it", frames=(193, 204), lens="50 mm", cam="Inside car A, passenger side, on the wheel",
      move="Fast push-in to the hands, cabin shakes", beat="Eli whips the wheel back hand over hand and catches the slide. The cabin shudders. The device jolts against its belt.",
      perf="Teeth clenched, white knuckles.", sb=("clay_0145", "interior_a90"), bg="interior_a90", refs=["eli_hands90", "interior_a90", "device90", "eli_reaction90"],
      key="Close-up inside car A: Eli's hands in worn brown leather jacket sleeves wrench the thin wood-rim steering wheel hard left, white knuckles, the wheel rim motion-blurred. Dashboard gauges shake. The rusted device on the passenger seat is jolted against its seat belt, red digits glowing. Sunlight strobes; 35mm film look.",
      vid="Fast push-in onto the wheel. Eli spins the wheel hand over hand to the left, then counter-steers once to catch the slide. The whole cabin shakes hard; the device bounces against the belt; dust floats in the sunlight. 24 fps real time."),
 dict(n=11, name="Kaz grins", frames=(205, 216), lens="85 mm", cam="From car A across the gap into Kaz's open passenger window",
      move="Slow push-in", beat="Kaz regrips the wheel. His crushed fender rattles. A cold, satisfied grin: the next hit ends it.",
      perf="Breathing hard, then a slow, cold grin; eyes stay on Eli.", sb=("clay_kaz_across", "clay_0144"), bg="kaz_interior",
      refs=["kaz_faces", "kaz_rage90", "kaz_seated", "kaz_interior", "car_b_dmg"],
      key="Tight close-up of Kaz at the wheel of his candy-red coupe, seen from car A beside him through his open passenger window: black cap, black bomber, both hands regripping the wheel, breathing hard, a cold thin grin, eyes locked on camera; at the frame edge the coupe's crumpled front-right fender and paint scraped to primer; warm golden-hour light, haze; 35mm film look.",
      vid="Slow push-in. Kaz breathes hard, then regrips the wheel; a slow, cold grin spreads; his eyes stay locked on Eli to his right. The loose bumper corner rattles in the wind. 24 fps real time."),
 dict(n=12, name="Eli's answer, in his eyes", frames=(217, 228), lens="100 mm", cam="Extreme close-up through car A's windshield",
      move="Snap zoom into the eyes", beat="He caught it. He does not blink. His eyes narrow in fury. Decision made.",
      perf="Eyes narrow, sweat at the temple, jaw clenches.", sb=("clay_eli_front", "clay_0031"), bg="interior_a90",
      refs=["eli_reaction90", "eli_seated90"],
      key="Extreme close-up of Eli's eyes and brow through car A's windshield: eyes narrowed, a bead of sweat at the temple, stubble, warm rim light, exactly as the reaction sheet; 35mm film grain.",
      vid="Quick snap zoom into Eli's eyes. His eyes narrow; his jaw clenches; a muscle twitches. 24 fps real time."),
 dict(n=13, name="The clock", frames=(229, 240), lens="100 mm macro", cam="Over the device's control panel",
      move="Static, rack focus to the digits", beat="The impact set it off. The device shrieks and the countdown jumps from 00:40:59 to 00:09:59. Ten minutes left.",
      perf="—", sb=("clay_0030", "device90"), bg="interior_a90", refs=["device90", "interior_a90"],
      key="Macro insert of the rusted device's control panel on car A's passenger seat: red seven-segment countdown now reading 00:09:59, worn steel keypad, toggle switches under red covers, the green armed lamp replaced by a flashing red warning lamp, a fresh crack across the display glass from the impact; shallow depth of field; the car vibrates; 35mm film look.",
      vid="Rack focus from the keypad to the red digits; the digits flicker and glitch, then jump from 00:40:59 to 00:09:59 and keep ticking; the red warning lamp starts flashing fast. Slight vibration at speed. 24 fps real time."),
 dict(n=14, name="The shifter", frames=(241, 252), lens="32 mm", cam="Over car A's centre console",
      move="Static, jolts on the lunge", beat="Eli rams the shifter forward. The car lunges.",
      perf="Decisive.", sb=("clay_0145", "clay_0162"), bg="interior_a90", refs=["eli_hands90", "interior_a90"],
      key="Insert over car A's centre console: wood-rim wheel on the left, chrome T-handle shifter in the centre, Eli's hand in a worn brown leather sleeve gripping it; the device's red digits glow out of focus on the passenger seat; through the windshield the white box truck directly ahead.",
      vid="Eli rams the chrome T-handle forward; the car lunges; the camera jolts; the view through the windshield surges. 24 fps real time."),
 dict(n=15, name="The squeeze", frames=(253, 288), lens="24 mm", cam="Bumper camera 7–10 m behind car A, 0.9→1.8 m",
      move="Chase, swings right and rises", beat="Eli darts into the right lane and passes the truck along its right side. Kaz holds the fast lane.",
      perf="—", sb=("clay_0163", "clay_0210"), bg="plate_forward90", refs=["cars", "props90", "grade_key90", "map_detail", "car_a_dmg", "car_b_dmg"],
      key="Low chase camera behind car A (its left rear door caved in, red paint streaks); all cars drive away from camera (red taillights). Car A in the middle lane; the mid-1990s white box truck directly ahead in the same lane; car B in the fast lane by the median, a fresh dent on its nose; the right lane open, the silver sedan stopped far back on the shoulder with hazard lights.",
      vid="Chase camera follows a beat late, rising and swinging right. Car A darts right out from behind the truck and rockets up the truck's right side, rear squatting; car B keeps pace beyond. The overpass rushes closer. 24 fps real time."),
 dict(n=16, name="Under the bridge", frames=(289, 312), lens="55→26 mm", cam="Right shoulder, 0.9 m, looking back",
      move="Locked off, zoom-out, whip pan", beat="Neck and neck, they rip under the overpass and past the lens.",
      perf="—", sb=("clay_0211", "clay_0240"), bg="plate_back90", refs=["cars", "plate_back90", "grade_key90", "car_a_dmg", "car_b_dmg"],
      key="Long lens from low on the right shoulder looking back: car A (nearer, screen-left) and car B (farther, screen-right) charge toward camera side by side, headlights on; the 1990s truck behind; the concrete overpass edge above; heat haze; 35mm film look.",
      vid="Locked-off camera; zoom out from 55 to 26 mm as the cars approach; they fill the frame and blast past the lens; a short whip pan follows. Cut to black on the pass."),
]
for s in SHOTS:
    a, b = s["frames"]; s["tc"] = (tc(a), tc(b + 1)); s["dur"] = f"{(b - a + 1) / FPS:g} s"; s["frames"] = f"{a}–{b}"
LABEL = {"interior_a90": "Car A interior + device", "eli_seated90": "Eli seated", "eli_hands90": "Eli's hands", "faces_lightkey": "Faces, light key",
         "kaz_seated": "Kaz seated", "kaz_interior": "Car B interior", "cars": "Car A + car B", "props90": "1990s truck + sedan",
         "plate_forward90": "Forward plate", "plate_back90": "Back plate", "grade_key90": "Grade key", "map_detail": "Lane map",
         "device90": "Nuclear device", "car_a_dmg": "Car A damaged", "car_b_dmg": "Car B damaged", "kaz_faces": "Kaz faces", "kaz_rage90": "Kaz rage sheet", "eli_reaction90": "Eli reaction sheet"}

def fig(src, cap, cls=""):
    return f'<figure class="{cls}"><img src="img/{src}.jpg" alt="{E(cap)}" loading="lazy"><figcaption>{E(cap)}</figcaption></figure>'

def shot_html(s):
    refs = "".join(fig(r, LABEL[r], "ref") for r in s["refs"])
    return f'''
<section class="shot" id="shot{s["n"]}">
  <header class="shot-head">
    <div class="slate"><span class="slate-k">SHOT</span><span class="slate-v">{s["n"]}</span></div>
    <div class="shot-title"><h3>{E(s["name"])}</h3><p class="beat">{E(s["beat"])}</p></div>
    <dl class="specs">
      <div><dt>TC</dt><dd>{s["tc"][0]}</dd></div><div><dt>Frames</dt><dd>{s["frames"]}</dd></div>
      <div><dt>Length</dt><dd>{s["dur"]}</dd></div><div><dt>Lens</dt><dd>{E(s["lens"])}</dd></div>
      <div class="wide"><dt>Camera</dt><dd>{E(s["cam"])}</dd></div><div class="wide"><dt>Move</dt><dd>{E(s["move"])}</dd></div>
      <div class="wide"><dt>Performance</dt><dd>{E(s["perf"])}</dd></div>
    </dl>
  </header>
  <figure class="keyframe"><img src="img/key{s["n"]:02d}.jpg" alt="Approved keyframe, shot {s["n"]}" loading="lazy"><figcaption>Approved keyframe · GPT Image 2.5 · 1920×1088 · passed QA</figcaption></figure>
  <div class="boards">
    {fig(s["sb"][0], "Storyboard: start (" + s["sb"][0].replace("clay_", "clay ") + ")", "sb")}
    {fig(s["sb"][1], "Storyboard: end (" + s["sb"][1].replace("clay_", "clay ") + ")", "sb")}
    {fig(s["bg"], "Background: " + LABEL[s["bg"]], "bgp")}
  </div>
  <div class="refrow"><span class="lbl">Reference images</span><div class="refs">{refs}</div></div>
  <details class="prompt" open><summary>Keyframe prompt · GPT Image 2.5</summary><p>{E(s["key"])}</p></details>
  <details class="prompt"><summary>Video prompt · image-to-video</summary><p>{E(s["vid"])}</p></details>
</section>'''

timeline = "".join(f'<a class="seg{" slow" if s["n"] in (5, 6) else ""}" href="#shot{s["n"]}" style="flex:{float(s["dur"].split()[0])}"><b>{s["n"]}</b><span>{E(s["name"])}</span></a>' for s in SHOTS)
library = "".join(fig(f, c, "lib") for f, c in [
    ("device90", "Nuclear device · countdown, keypad, rust"), ("interior_a90", "Car A interior + device"), ("eli_seated90", "Eli · seated"), ("eli_hands90", "Eli · hands"),
    ("eli_reaction90", "Eli · reaction close-ups"), ("eli_body", "Eli · full body"), ("eli_faces", "Eli · faces"), ("faces_lightkey", "Both faces · light key"),
    ("kaz_rage90", "Kaz · rage, “Stop or die!”"), ("kaz_seated", "Kaz · seated"), ("kaz_body", "Kaz · full body"), ("kaz_faces", "Kaz · faces"),
    ("cars", "Car A + car B"), ("car_a_dmg", "Car A · damaged, left rear"), ("car_b_dmg", "Car B · damaged, front right"), ("kaz_interior", "Car B interior"), ("props90", "1990s truck + sedan"), ("grade_key90", "Grade key · 35mm"),
    ("plate_forward90", "Forward plate · 35mm"), ("plate_back90", "Back plate · 35mm"), ("scale_lineup", "Scale lineup"), ("map_topdown", "Lane map · full")])

page = open(os.path.join(HERE, "template.html")).read()
page = page.replace("{{GLOBAL}}", E(GLOBAL)).replace("{{TIMELINE}}", timeline).replace("{{SHOTS}}", "".join(shot_html(s) for s in SHOTS)).replace("{{LIBRARY}}", library)
open(os.path.join(HERE, "index.html"), "w").write(page)
print("ok", len(page))
