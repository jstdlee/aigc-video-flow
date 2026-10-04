# Clay blockout: two cars racing on a public highway. 10 s, 7 shots @ 24 fps, for video-gen reference.
import bpy, math, random
from mathutils import Vector
random.seed(7)
FPS = 24
# Seven-shot edit, 10 s. Each shot runs at its own speed (1.0 = real time) over one continuous story clock,
# so slow motion is just a slower clock and every shot stays physically consistent with the others.
SHOTS = [  # name, first frame, last frame, speed      ("GOLDEN HOUR", scene 38: "The Squeeze")
    ("01_Cooler_Insert",   1,  30, 1.0),   # the stakes: donor heart strapped in the passenger seat (generated, no clay)
    ("02_Eli_CU",         31,  66, 1.0),   # Eli calm and focused, eyes flick to the mirror
    ("03_Mirror",         67,  84, 1.0),   # Kaz's red coupe slicing out of traffic in Eli's door mirror
    ("04_Kaz_Arrives",    85, 114, 1.0),   # drone behind: Kaz pulls level on Eli's left
    ("05_Stare_OTS",     115, 144, 0.35),  # slow motion, over Eli's shoulder: Kaz smirks, points at the cooler
    ("06_Shifter_Insert",145, 162, 0.6),   # Eli's answer: hand slams the shifter (generated, no clay)
    ("07_Squeeze",       163, 210, 1.0),   # bumper cam: Eli darts right around the truck, threads the traffic
    ("08_Overpass",      211, 240, 1.0),   # shoulder cam: both rip under the overpass and past the lens
]
FRAMES = SHOTS[-1][2]

def world_t(f):
    """Story time (s) on frame f."""
    t = 0.0
    for _, first, last, speed in SHOTS:
        if f <= last or (first, last) == SHOTS[-1][1:3]:
            return t + (f - first) * speed / FPS
        t += (last - first + 1) * speed / FPS
    return t

# wipe the current file without resetting prefs (a factory reset would unload the MCP add-on)
for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.actions, bpy.data.images):
    for d in list(coll): coll.remove(d)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = FRAMES

def clay(name, v):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (v, v, v, 1); b.inputs["Roughness"].default_value = 0.6
    m.diffuse_color = (v, v, v, 1); return m
WHITE, ROAD, LINE, GROUND, GLASS = clay("Clay", 0.8), clay("Road", 0.42), clay("Lines", 0.9), clay("Ground", 0.62), clay("Glass", 0.2)
MIRROR = clay("MirrorGlass", 0.95)
_mb = MIRROR.node_tree.nodes["Principled BSDF"]; _mb.inputs["Metallic"].default_value = 1.0; _mb.inputs["Roughness"].default_value = 0.02

def box(name, loc, size, m, bevel=0.0, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name; o.scale = [s / 2 for s in size]
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = o.modifiers.new("Bevel", "BEVEL"); b.width = bevel; b.segments = 3
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def strut(name, p0, p1, t, m, parent=None):
    """Square bar of thickness t from p0 to p1 (pillars, arms)."""
    p0, p1 = Vector(p0), Vector(p1); d = p1 - p0
    bpy.ops.mesh.primitive_cube_add(location=(p0 + p1) / 2, rotation=d.to_track_quat("Y", "Z").to_euler())
    o = bpy.context.object; o.name = name; o.scale = (t / 2, d.length / 2, t / 2)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def blob(name, loc, scale, m, parent=None, segs=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=segs // 2, radius=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.shade_smooth(); o.data.materials.append(m)
    if parent: o.parent = parent
    return o

# ---------- highway (runs along +Y, right-hand traffic) ----------
Y0, Y1 = -150, 650; L = Y1 - Y0; YC = (Y0 + Y1) / 2
LANES = [2.0, 5.7, 9.4]                     # our carriageway, fast lane nearest median
box("Carriageway_R", (5.7, YC, 0), (11.4, L, 0.1), ROAD)
box("Carriageway_L", (-5.7, YC, 0), (11.4, L, 0.1), ROAD)
box("Shoulder_R", (12.6, YC, 0), (2.4, L, 0.08), ROAD)
box("Shoulder_L", (-12.6, YC, 0), (2.4, L, 0.08), ROAD)
box("Median", (0, YC, 0.45), (0.5, L, 0.8), WHITE, 0.08)
for s in (1, -1):
    box(f"Guardrail_{s}", (s * 14.0, YC, 0.75), (0.15, L, 0.35), WHITE, 0.03)
    for x in (3.85, 7.55):                  # dashed lane lines
        for y in range(Y0, Y1, 12):
            box("Dash", (s * x, y, 0.06), (0.15, 3.0, 0.02), LINE)
    box(f"EdgeLine_{s}", (s * 11.3, YC, 0.06), (0.15, L, 0.02), LINE)
    box(f"EdgeLineIn_{s}", (s * 0.5, YC, 0.06), (0.12, L, 0.02), LINE)
    for y in range(Y0, Y1, 40):             # guardrail posts + light poles
        box("Post", (s * 14.0, y, 0.4), (0.12, 0.12, 0.8), WHITE)
    for y in range(Y0 + 20, Y1, 60):
        box("Pole", (s * 14.6, y, 5), (0.25, 0.25, 10), WHITE)
        box("PoleArm", (s * 13.2, y, 9.9), (3.0, 0.25, 0.2), WHITE)
        box("Lamp", (s * 11.9, y, 9.75), (0.9, 0.4, 0.15), WHITE)
# ground + hills
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, YC, -0.3)); g = bpy.context.object
g.name = "Ground"; g.scale = (600, L + 600, 1); g.data.materials.append(GROUND)
for i in range(18):
    s = random.choice((-1, 1)); x = s * random.uniform(70, 220)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x, random.uniform(Y0, Y1 + 300), -6))
    h = bpy.context.object; h.name = "Hill"; h.scale = (random.uniform(40, 90), random.uniform(50, 120), random.uniform(14, 30))
    h.data.materials.append(GROUND); bpy.ops.object.shade_smooth()
# blocky trees
for i in range(140):
    s = random.choice((-1, 1)); x = s * random.uniform(19, 60); y = random.uniform(Y0, Y1)
    hgt = random.uniform(5, 11)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=hgt * 0.28, depth=hgt, location=(x, y, hgt / 2 + 1))
    t = bpy.context.object; t.name = "Tree"; t.data.materials.append(WHITE)
    box("Trunk", (x, y, 0.5), (0.4, 0.4, 1.4), WHITE)
# overpass bridge
OY = 285
box("Overpass_Deck", (0, OY, 7.2), (60, 12, 1.2), WHITE, 0.1)
for s in (1, -1):
    box("Overpass_Rail", (0, OY + s * 5.8, 8.3), (60, 0.3, 1.0), WHITE, 0.05)
    box("Overpass_Pier", (s * 15.5, OY, 3.3), (1.2, 9, 6.6), WHITE, 0.1)
box("Overpass_PierMid", (0, OY, 3.3), (0.9, 8, 6.6), WHITE, 0.1)
# sign gantry
GY = 125
for s in (1, -1): box("Gantry_Leg", (s * 14.3, GY, 4), (0.4, 0.4, 8), WHITE)
box("Gantry_Beam", (0, GY, 7.6), (29, 0.4, 0.6), WHITE)
for x in (3.5, 9.0): box("Sign", (x, GY - 0.3, 6.4), (5, 0.15, 2.4), WHITE, 0.05)

# ---------- vehicles ----------
def driver(name, root, dx, sy, z0, wheel_dy, hat):
    """Seated clay driver with a readable face. Returns a small rig: head pivot (rotate .z to turn),
    brows / eyes / mouth for expressions, and the steering wheel."""
    box(name + "_Torso", (dx, sy - 0.03, z0), (0.42, 0.24, 0.36), WHITE, 0.06, root)
    box(name + "_SeatBack", (dx, sy - 0.2, z0 + 0.09), (0.48, 0.1, 0.5), WHITE, 0.04, root)
    box(name + "_SeatBackP", (-dx, sy - 0.2, z0 + 0.09), (0.48, 0.1, 0.5), WHITE, 0.04, root)
    strut(name + "_Neck", (dx, sy, z0 + 0.13), (dx, sy, z0 + 0.23), 0.08, WHITE, root)
    wc = Vector((dx, sy + wheel_dy, z0 + 0.04))   # rim top at chest height, clear of the face
    bpy.ops.mesh.primitive_torus_add(major_radius=0.16, minor_radius=0.018, location=wc, rotation=(math.radians(65), 0, 0))
    sw = bpy.context.object; sw.name = name + "_SteeringWheel"; sw.data.materials.append(GLASS); sw.parent = root
    sw.rotation_mode = "ZXY"                  # spin about its own axis first, then the 65 deg rake
    strut(name + "_Column", wc, wc + Vector((0, 0.3, -0.1)), 0.05, GLASS, root)
    for s in (1, -1):                       # shoulder -> elbow -> hand on the wheel rim
        sh, el = Vector((dx + s * 0.19, sy, z0 + 0.14)), Vector((dx + s * 0.23, sy + 0.24, z0 + 0.0))
        hand = wc + Vector((s * 0.15, -0.02, 0.02))
        strut(name + "_UpperArm", sh, el, 0.08, WHITE, root); strut(name + "_Forearm", el, hand, 0.07, WHITE, root)
        blob(name + "_Hand", hand, (0.04, 0.04, 0.04), WHITE, root, 8)
    neck = bpy.data.objects.new(name + "_HeadPivot", None); sc.collection.objects.link(neck)
    neck.parent = root; neck.location = (dx, sy, z0 + 0.17)
    blob(name + "_Skull", (0, 0, 0.12), (0.093, 0.108, 0.125), WHITE, neck)
    blob(name + "_Jaw", (0, 0.03, 0.06), (0.075, 0.08, 0.06), WHITE, neck)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.022, depth=0.05, location=(0, 0.115, 0.115), rotation=(-math.pi / 2, 0, 0))
    n = bpy.context.object; n.name = name + "_Nose"; n.data.materials.append(WHITE); n.parent = neck
    rig = {"head": neck, "wheel": sw, "eyes": [], "brows": []}
    for s in (1, -1):
        rig["eyes"].append((blob(name + "_Eye", (s * 0.036, 0.098, 0.135), (0.017, 0.012, 0.012), GLASS, neck, 10), s))
        rig["brows"].append((box(name + "_Brow", (s * 0.037, 0.106, 0.163), (0.045, 0.016, 0.013), WHITE, 0.003, neck), s))
        blob(name + "_Ear", (s * 0.095, 0, 0.12), (0.014, 0.028, 0.034), WHITE, neck, 10)
    rig["mouth"] = box(name + "_Mouth", (0, 0.104, 0.07), (0.05, 0.012, 0.01), GLASS, 0.002, neck)
    if hat:                                 # B's driver wears a cap, so the two read differently
        blob(name + "_Cap", (0, -0.01, 0.19), (0.1, 0.115, 0.07), WHITE, neck)
        box(name + "_Brim", (0, 0.12, 0.18), (0.16, 0.09, 0.012), WHITE, 0.004, neck)
    else:
        blob(name + "_Hair", (0, -0.03, 0.165), (0.098, 0.112, 0.095), WHITE, neck)
    return rig

def car(name, kind):
    root = bpy.data.objects.new(name, None); sc.collection.objects.link(root)
    if kind == "coupe":   # low wide sports car
        box(name + "_Body", (0, 0, 0.55), (1.95, 4.5, 0.6), WHITE, 0.18, root)
        box(name + "_Nose", (0, 1.95, 0.42), (1.9, 0.9, 0.35), WHITE, 0.15, root)
        box(name + "_Wing", (0, -2.15, 1.15), (1.9, 0.35, 0.06), WHITE, 0.02, root)
        for s in (1, -1): box(name + "_WingPost", (s * 0.6, -2.15, 0.95), (0.08, 0.2, 0.35), WHITE, 0, root)
        wb, track, r = 1.45, 0.88, 0.36
        z0, z1, cw, yfb, yfr, yrr, yrb, by, seat = 0.85, 1.32, 1.56, 0.85, 0.15, -0.85, -1.5, -0.8, -0.45
    else:                 # muscle / GT sedan
        box(name + "_Body", (0, 0, 0.62), (1.9, 4.7, 0.7), WHITE, 0.15, root)
        box(name + "_Scoop", (0, 1.2, 1.0), (0.6, 0.9, 0.12), WHITE, 0.04, root)
        wb, track, r = 1.5, 0.86, 0.38
        z0, z1, cw, yfb, yfr, yrr, yrb, by, seat = 0.97, 1.45, 1.6, 0.75, 0.15, -1.1, -1.6, -1.0, -0.55
    # open greenhouse (roof + pillars, no glass) so the drivers are visible
    box(name + "_Roof", (0, (yfr + yrr) / 2, z1 + 0.02), (cw, yfr - yrr + 0.06, 0.06), WHITE, 0.02, root)
    for s in (1, -1):
        x = s * (cw / 2 - 0.04)
        strut(name + "_APillar", (x, yfb, z0), (x, yfr, z1), 0.07, WHITE, root)
        strut(name + "_BPillar", (x, by, z0), (x, by, z1), 0.07, WHITE, root)
        strut(name + "_CPillar", (x, yrb, z0), (x, yrr, z1), 0.07, WHITE, root)
    box(name + "_Dash", (0, yfb - 0.22, z0 + 0.06), (cw - 0.1, 0.28, 0.14), WHITE, 0.03, root)
    rig = driver(name + "_Driver", root, -0.38, seat, z0, 0.47, kind == "coupe")
    if kind == "muscle":                    # left door mirror, angled for the driver's eye-line (shot 03 looks into it)
        box(name + "_MirrorArm", (-0.98, 0.5, 0.98), (0.12, 0.05, 0.05), WHITE, 0, root)
        n = Vector((0.25, -0.96, 0.09)).normalized()
        rot = Vector((0, 0, 1)).rotation_difference(n).to_euler()
        bpy.ops.mesh.primitive_cube_add(location=(-1.02, 0.47, 1.05), rotation=rot)
        h = bpy.context.object; h.name = name + "_MirrorHousing"; h.scale = (0.1, 0.07, 0.03)
        bpy.ops.object.transform_apply(scale=True); h.data.materials.append(WHITE); h.parent = root
        bpy.ops.mesh.primitive_plane_add(size=1, location=Vector((-1.02, 0.47, 1.05)) + n * 0.032, rotation=rot)
        mp = bpy.context.object; mp.name = name + "_MirrorGlass"; mp.scale = (0.18, 0.12, 1)
        bpy.ops.object.transform_apply(scale=True); mp.data.materials.append(MIRROR); mp.parent = root
    wheels = []
    for sx in (1, -1):
        for sy in (1, -1):
            # build at the origin so only the rotation is baked; spin is rotation_euler.x about the axle
            bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=0.3, location=(0, 0, 0), rotation=(0, math.pi / 2, 0))
            w = bpy.context.object; w.name = name + "_Wheel"; w.data.materials.append(GLASS)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            w.location = (sx * track, sy * wb, r); w.parent = root
            hub = box(name + "_Hub", (0, 0, 0), (0.32, 0.12, 0.12), WHITE, 0, w)  # off-centre spoke so the spin reads
            hub.location = (sx * 0.02, 0, r * 0.5)
            wheels.append((w, r))
    return root, wheels, rig

def traffic(name, size):
    root = bpy.data.objects.new(name, None); sc.collection.objects.link(root)
    w, l, h = size
    box(name + "_Body", (0, 0, h / 2 + 0.3), (w, l, h), WHITE, 0.1, root)
    for sx in (1, -1):
        for sy in (1, -1):
            box(name + "_Tyre", (sx * w * 0.42, sy * l * 0.35, 0.35), (0.3, 0.7, 0.7), GLASS, 0.1, root)
    return root

A, A_w, A_rig = car("RacerA", "muscle")       # the everyman: muscle sedan, middle lane
B, B_w, B_rig = car("RacerB", "coupe")        # the predator: winged coupe, fast lane, driver in a cap
truck = traffic("Truck", (2.5, 12, 3.4))
van = traffic("Van", (2.0, 5.2, 1.9))
sedan = traffic("Sedan", (1.85, 4.7, 1.45))        # right lane, the car Eli cuts in front of
far = [traffic(f"Far{i}", (1.9, 4.6 + 4 * (i == 1), 1.5 + 1.5 * (i == 1))) for i in range(3)]
oncoming = [traffic(f"Oncoming{i}", (1.9, 4.6 + i % 2 * 5, 1.5 + i % 2 * 1.6)) for i in range(7)]
# cab on truck
box("Truck_Cab", (0, 7.0, 1.9), (2.4, 2.2, 2.8), WHITE, 0.1, truck)

def smooth(t, a, b):
    if t <= a: return 0.0
    if t >= b: return 1.0
    u = (t - a) / (b - a); return u * u * (3 - 2 * u)
def bump(t, a, b, c, d): return smooth(t, a, b) * (1 - smooth(t, c, d))
def lerp(a, b, u): return a + (b - a) * u

# ---------- motion plan (story seconds) ----------
T_LOOK, T_LAUNCH = 4.75, 5.64     # Kaz draws level / Eli floors it
def yA(t):
    if t < T_LAUNCH: return 30.0 * t                                   # 108 km/h, boxed in behind the truck
    tau = t - T_LAUNCH; return 30.0 * T_LAUNCH + 30.0 * tau + 4.5 * tau * tau
def gapB(t):                     # Kaz.y - Eli.y: 100 m back, closing at 24 m/s, braking to pace Eli
    if t < 3.5: return -15.3 - 24.0 * (3.5 - t)
    if t < T_LOOK: return -0.3 - 15.0 * ((T_LOOK - t) / 1.25) ** 2
    if t < T_LAUNCH: return -0.3
    tau = t - T_LAUNCH; return -0.3 + 5.0 * math.sin(1.4 * tau) * min(1.0, tau / 2.0)   # Kaz leads, then Eli
def posA(t):
    tau = t - T_LAUNCH            # dart right in front of the sedan, past the truck, cut back in ahead of it
    return Vector((LANES[1] + (LANES[2] - LANES[1]) * (smooth(tau, 0.1, 0.6) - smooth(tau, 2.0, 2.5)), yA(t), 0))
def posB(t): return Vector((LANES[0] + 0.12 * math.sin(t * 3.0) * smooth(t, T_LAUNCH, T_LAUNCH + 0.6), yA(t) + gapB(t), 0))
def posTruck(t): return Vector((LANES[1], 44.0 + 25.0 * t, 0))          # the box truck Eli is stuck behind
def posSedan(t): return Vector((LANES[2], 9.2 + 27.0 * t, 0))           # right lane, just behind Eli at launch
def posVan(t): return Vector((LANES[2], 330 + 28.0 * t, 0))
FAR = [(LANES[0], 430, 33), (LANES[1], 380, 27), (LANES[2], 470, 29)]   # ahead in every lane, all moving
ONC = [(-LANES[0], 160, 36), (-LANES[1], 120, 29), (-LANES[2], 260, 27), (-LANES[1], 330, 31),
       (-LANES[0], 420, 38), (-LANES[2], 520, 26), (-LANES[1], 600, 33)]

def key_vehicle(o, p, prev, f, wheels=()):
    o.location = p
    d = p - prev
    if d.length > 1e-4:
        o.rotation_euler = (0, 0, -math.atan2(d.x, d.y))
    o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)
    for w, r in wheels:
        w.rotation_euler.x = -p.y / r
        w.keyframe_insert("rotation_euler", index=0, frame=f)

EPS = 0.01
def heading(v): return -math.atan2(v.x, v.y)          # same convention as the cars' rotation_euler.z
def wrap(a): return (a + math.pi) % (2 * math.pi) - math.pi
A_HEAD = Vector((-0.38, -0.55, 1.26)); B_HEAD = Vector((-0.38, -0.45, 1.14))   # head centres in car space

def yaw_to(me, me_prev, my_head, other, other_head, limit):
    want = wrap(heading((other + other_head) - (me + my_head)) - heading(me - me_prev))
    return max(-limit, min(limit, want))

def lateral_acc(pos, t, h=0.05): return (pos(t + h).x - 2 * pos(t).x + pos(t - h).x) / (h * h)

def perform(rig, f, yaw, pitch, roll, anger, squint, set_jaw, smirk, steer):
    """Key one frame of a driver's performance."""
    rig["head"].rotation_euler = (pitch, roll, yaw); rig["head"].keyframe_insert("rotation_euler", frame=f)
    for brow, s in rig["brows"]:
        brow.location.z = 0.163 - 0.008 * anger
        brow.rotation_euler = (0, -s * 0.42 * anger, 0)
        brow.keyframe_insert("location", frame=f); brow.keyframe_insert("rotation_euler", frame=f)
    for eye, s in rig["eyes"]:
        eye.scale = (0.017, 0.012, 0.012 * (1 - 0.55 * squint)); eye.keyframe_insert("scale", frame=f)
    m = rig["mouth"]
    m.scale = (1 + 0.25 * set_jaw - 0.1 * smirk, 1, 1 - 0.5 * set_jaw)
    m.rotation_euler = (0, 0.32 * smirk, 0)
    m.location = (0.005 * smirk, 0.104, 0.07 + 0.004 * smirk)
    for prop in ("scale", "rotation_euler", "location"): m.keyframe_insert(prop, frame=f)
    rig["wheel"].rotation_euler = (math.radians(65), 0, steer); rig["wheel"].keyframe_insert("rotation_euler", frame=f)

D = math.radians
for f in range(0, FRAMES + 2):
    t = world_t(f)
    a, b = posA(t), posB(t)
    key_vehicle(A, a, posA(t - EPS), f, A_w)
    key_vehicle(B, b, posB(t - EPS), f, B_w)
    key_vehicle(truck, posTruck(t), posTruck(t - EPS), f)
    key_vehicle(van, posVan(t), posVan(t - EPS), f)
    key_vehicle(sedan, posSedan(t), posSedan(t - EPS), f)
    for o, (x, y0, v) in zip(far, FAR):
        key_vehicle(o, Vector((x, y0 + v * t, 0)), Vector((x, y0 + v * (t - EPS), 0)), f)
    for o, (x, y0, v) in zip(oncoming, ONC):
        o.location = (x, y0 - v * t, 0); o.rotation_euler = (0, 0, math.pi)
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)

    # ----- performances -----
    look = smooth(t, 4.77, 4.86) * (1 - smooth(t, 5.2, 5.4))           # the stare-down (slow motion)
    calm = 1 - smooth(t, 5.3, 5.6)
    hA, hB = heading(a - posA(t - EPS)), heading(b - posB(t - EPS))
    # Eli: focused -> mirror check -> stare -> turns back, decides -> braced, leaning into the swerves
    yawA = D(30) * bump(t, 2.2, 2.35, 2.6, 2.75) + look * yaw_to(a, posA(t - EPS), A_HEAD, b, B_HEAD, D(95))
    pitchA = D(1.2) * math.sin(t * 2.2) * calm
    rollA = max(-D(9), min(D(9), -0.012 * lateral_acc(posA, t)))
    angerA = lerp(lerp(0.0, 0.35, smooth(t, 2.4, 2.7)), 1.0, smooth(t, 4.9, 5.2))
    squintA = max(0.3 * look, 0.7 * smooth(t, 5.25, 5.5))
    perform(A_rig, f, yawA, pitchA, rollA, angerA, squintA, smooth(t, 5.25, 5.45), 0.0, max(-1.5, min(1.5, -9 * hA)))
    # Kaz: cocky on the approach, wide smirk during the stare, wiped off once Eli takes the lead
    lost = smooth(t, T_LAUNCH + 2.2, T_LAUNCH + 2.5)
    yawB = look * yaw_to(b, posB(t - EPS), B_HEAD, a, A_HEAD, D(75))
    pitchB = -D(10) * bump(t, 5.0, 5.05, 5.08, 5.14)
    rollB = max(-D(9), min(D(9), -0.012 * lateral_acc(posB, t)))
    smirkB = (0.5 + 0.5 * smooth(t, 4.8, 4.9)) * (1 - lost)
    perform(B_rig, f, yawB, pitchB, rollB, 0.7 * lost, 0.4 * lost, 0.0, smirkB, max(-1.5, min(1.5, -9 * hB)))

# ---------- cameras: one per shot, cut with timeline markers ----------
def shot_cam(name, lens):
    cd = bpy.data.cameras.new(name); cd.sensor_width = 36; cd.lens = lens; cd.clip_start = 0.05
    c = bpy.data.objects.new(name, cd); sc.collection.objects.link(c)
    tgt = bpy.data.objects.new(name + "_Aim", None); sc.collection.objects.link(tgt)
    tc = c.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    return c, cd, tgt

def head_world(car_pos, local): return car_pos + local

MIRROR_POS = Vector((-1.02, 0.47, 1.05))          # Eli's left door mirror, car space

def shot_frame(i, f, t, u):
    """Camera location, aim point and lens for shot i at frame f (story time t, shot progress u 0..1).
    Rule: any shot with both cars in frame keeps the camera behind or beside them, so Kaz is always
    screen-left and Eli screen-right (no crossing the line)."""
    a, b = posA(t), posB(t)
    e = smooth(u, 0.0, 1.0)
    if i == 0:   # cooler insert: inside Eli's car, passenger footwell looking at the seat (repainted from refs)
        return a + Vector((0.6, -0.02, 1.42)), a + Vector((0.22, -0.62, 1.12)), 30   # from the passenger door: cooler, shifter, Eli's arm
    if i == 1:   # Eli through the windshield from the passenger side of the hood, slow push
        loc = a + Vector((lerp(0.05, -0.05, e), 1.45, 1.38))
        return loc, a + A_HEAD + Vector((0, 0, -0.01)), lerp(44, 52, e)
    if i == 2:   # Eli's eye-line into his door mirror: Kaz grows in the reflection
        return a + A_HEAD + Vector((0.12, 0.02, 0.02)), a + MIRROR_POS, lerp(78, 86, e)
    if i == 3:   # drone low behind the pair: Kaz slides up on the left and pulls level
        mid = (a + b) / 2
        loc = Vector((lerp(4.6, 4.2, e), a.y + lerp(-17.0, -11.0, e), lerp(4.8, 3.6, e)))
        return loc, Vector((3.9, mid.y + 10.0, 0.6)), 30
    if i == 4:   # over Eli's right shoulder from the passenger seat, looking out of his window at Kaz
        loc = a + Vector((0.25, -0.88, 1.41))   # just above the passenger seatback
        return loc, b + B_HEAD + Vector((0, 0.05, 0)), lerp(32, 38, e)
    if i == 5:   # shifter insert (repainted from refs)
        return a + Vector((0.3, -0.5, 1.45)), a + Vector((0.0, 0.03, 1.12)), 32    # over the console: shifter, wheel beyond on the left
    if i == 6:   # bumper cam chasing Eli: follows him right around the truck, a beat late
        lag = posA(t - 0.3)
        loc = Vector((lag.x, a.y - lerp(7.0, 10.0, e), lerp(0.9, 1.8, e)))   # trails wider so the truck being passed stays in frame
        return loc, Vector((lerp(lag.x, 6.0, 0.5), a.y + 14.0, 0.9)), 24
    # overpass: locked-off low on the right shoulder past the bridge, panning as they rip by
    mid = (a + b) / 2
    loc = Vector((12.9, OY + 12.0, 0.9))
    return loc, Vector((lerp(6.0, 4.5, e), max(mid.y, loc.y - 30.0) + 1.0, 1.0)) if mid.y < loc.y - 2 else Vector((4.0, mid.y + 6.0, 1.0)), lerp(55, 26, smooth(u, 0.0, 0.85))

sc.timeline_markers.clear()
for i, (name, first, last, speed) in enumerate(SHOTS):
    c, cd, tgt = shot_cam("Cam" + name, 30)
    for f in range(first - 1, last + 2):                 # one frame either side keeps motion blur honest at cuts
        u = (f - first) / max(1, last - first)
        t = world_t(f)
        loc, aim_at, lens = shot_frame(i, f, t, u)
        jitter = (0.02 if i in (3, 6) else 0.004) * (1 + 2 * (i == 6) * smooth(u, 0.0, 0.3))
        loc = loc + Vector((math.sin(f * 1.7) * jitter, 0, math.sin(f * 2.3 + 1) * jitter * 0.8))
        c.location = loc; c.keyframe_insert("location", frame=f)
        tgt.location = aim_at; tgt.keyframe_insert("location", frame=f)
        cd.lens = lens; cd.keyframe_insert("lens", frame=f)
    sc.timeline_markers.new(name, frame=first).camera = c
    if i == 0: sc.camera = c

# every key linear: eased keys at shot edges make a camera lag its car and smear the frame
for o in list(bpy.data.objects) + list(bpy.data.cameras):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            for k in fc.keyframe_points: k.interpolation = "LINEAR"

# ---------- readable previs: colour, lamps and props, so the image model can't misread the clay ----------
# The image model ignored front/back, seating and lanes when everything was white. Every rule from BIBLE.md that
# can be drawn is drawn here: car colours, skin and wardrobe, glowing head/tail lamps, the cooler and shifter.
def paint(name, rgb, rough=0.5, metal=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m
P = {k: paint(k, *v) for k, v in {
    "BlackPaint": ((0.015, 0.015, 0.018), 0.25), "RedPaint": ((0.55, 0.02, 0.02), 0.25),
    "TruckWhite": ((0.85, 0.85, 0.83), 0.5), "Silver": ((0.5, 0.52, 0.55), 0.3, 0.6),
    "Asphalt": ((0.07, 0.07, 0.075), 0.9), "Concrete": ((0.5, 0.49, 0.46), 0.85), "Metal": ((0.55, 0.56, 0.58), 0.4, 0.8),
    "Grass": ((0.16, 0.26, 0.08), 0.9), "Pine": ((0.05, 0.15, 0.06), 0.9), "Bark": ((0.2, 0.12, 0.06), 0.9),
    "SignGreen": ((0.02, 0.25, 0.1), 0.6), "Tyre": ((0.025, 0.025, 0.025), 0.7), "Chrome": ((0.8, 0.8, 0.82), 0.1, 1.0),
    "Skin": ((0.62, 0.42, 0.3), 0.6), "Hair": ((0.05, 0.03, 0.02), 0.8), "LeatherBrown": ((0.22, 0.11, 0.05), 0.6),
    "BlackCloth": ((0.03, 0.03, 0.03), 0.8), "Seat": ((0.04, 0.04, 0.04), 0.5), "Interior": ((0.05, 0.05, 0.05), 0.6),
    "CoolerWhite": ((0.9, 0.9, 0.9), 0.4), "CoolerRed": ((0.6, 0.03, 0.03), 0.4),
    "Head": ((1.0, 0.95, 0.8), 0.3, 0.0, 6.0), "Tail": ((1.0, 0.03, 0.02), 0.3, 0.0, 6.0),
    "CarBlue": ((0.1, 0.18, 0.35), 0.4), "CarGrey": ((0.3, 0.3, 0.3), 0.4), "CarGreen": ((0.12, 0.2, 0.15), 0.4),
}.items()}

def set_mat(o, m):
    if o.type == "MESH":
        o.data.materials.clear(); o.data.materials.append(m)

def car_paint(n):
    if n.startswith("RacerA"): return P["BlackPaint"]
    if n.startswith("RacerB"): return P["RedPaint"]
    if n.startswith("Truck"): return P["TruckWhite"]
    if n.startswith("Sedan"): return P["Silver"]
    if n.startswith("Van"): return P["TruckWhite"]
    return [P["CarBlue"], P["CarGrey"], P["CarGreen"], P["Silver"]][sum(map(ord, n)) % 4]

for o in bpy.data.objects:
    n = o.name
    if "_Driver_" in n:
        eli = n.startswith("RacerA")
        if any(k in n for k in ("_Skull", "_Jaw", "_Nose", "_Ear", "_Hand", "_Neck")): set_mat(o, P["Skin"])
        elif "_Hair" in n: set_mat(o, P["Hair"])
        elif "_Cap" in n or "_Brim" in n: set_mat(o, P["BlackCloth"])
        elif any(k in n for k in ("_Torso", "_UpperArm", "_Forearm")): set_mat(o, P["LeatherBrown"] if eli else P["BlackCloth"])
        elif "_SeatBack" in n: set_mat(o, P["Seat"])
        elif "_Brow" in n: set_mat(o, P["Hair"])
        continue
    if n.startswith(("RacerA", "RacerB", "Truck", "Sedan", "Van", "Far", "Oncoming")):
        if "_Wheel" in n or "_Tyre" in n: set_mat(o, P["Tyre"])
        elif "_Hub" in n: set_mat(o, P["Chrome"])
        elif "_Dash" in n: set_mat(o, P["Interior"])
        elif "_Mirror" in n and "Glass" not in n: set_mat(o, P["BlackPaint"])
        elif "MirrorGlass" not in n: set_mat(o, car_paint(n))
        continue
    if n.startswith(("Carriageway", "Shoulder")): set_mat(o, P["Asphalt"])
    elif n.startswith(("Median", "Overpass")): set_mat(o, P["Concrete"])
    elif n.startswith(("Guardrail", "Post", "Pole", "PoleArm", "Gantry")): set_mat(o, P["Metal"])
    elif n.startswith("Sign"): set_mat(o, P["SignGreen"])
    elif n.startswith(("Ground", "Hill")): set_mat(o, P["Grass"])
    elif n.startswith("Tree"): set_mat(o, P["Pine"])
    elif n.startswith("Trunk"): set_mat(o, P["Bark"])

def lamps(root, half_w, front_y, rear_y, z):
    """White headlights at +Y (front), red taillights at -Y (rear): orientation can't be misread."""
    for sx in (1, -1):
        box(root.name + "_HeadLamp", (sx * (half_w - 0.22), front_y, z), (0.3, 0.06, 0.14), P["Head"], 0, root)
        box(root.name + "_TailLamp", (sx * (half_w - 0.22), rear_y, z), (0.32, 0.06, 0.12), P["Tail"], 0, root)
lamps(A, 0.95, 2.36, -2.36, 0.68); lamps(B, 0.97, 2.41, -2.26, 0.62)
for v in [truck, van, sedan] + far + oncoming:
    body = next(c for c in v.children if c.name.endswith("_Body"))
    w, l, h = body.dimensions
    front = l / 2 + (2.2 if v is truck else 0.0)       # the truck's cab sticks out in front of its box
    lamps(v, w / 2, front + 0.03, -l / 2 - 0.03, 0.75)

# car A interior: centre console, chrome T-handle shifter, the organ cooler belted into the passenger seat
z0A = 0.97
box("RacerA_Console", (0, -0.25, z0A - 0.02), (0.26, 0.9, 0.16), P["Interior"], 0.02, A)
strut("RacerA_Shifter", (0, -0.02, z0A + 0.05), (0, 0.02, z0A + 0.26), 0.025, P["Chrome"], A)
box("RacerA_ShifterT", (0, 0.025, z0A + 0.27), (0.12, 0.03, 0.03), P["Chrome"], 0.01, A)
box("RacerA_SeatP", (0.38, -0.6, z0A - 0.02), (0.46, 0.5, 0.14), P["Seat"], 0.03, A)
box("RacerA_Cooler", (0.38, -0.58, z0A + 0.2), (0.38, 0.3, 0.3), P["CoolerWhite"], 0.03, A)
box("RacerA_CoolerLid", (0.38, -0.58, z0A + 0.37), (0.4, 0.32, 0.06), P["CoolerRed"], 0.02, A)
box("RacerA_CoolerLED", (0.38, -0.425, z0A + 0.27), (0.04, 0.01, 0.025), P["Tail"], 0, A)
strut("RacerA_Belt", (0.6, -0.78, z0A + 0.5), (0.16, -0.4, z0A + 0.02), 0.04, P["BlackCloth"], A)

# ---------- lighting / world ----------
sun_d = bpy.data.lights.new("Sun", "SUN"); sun_d.energy = 4.0; sun_d.angle = math.radians(2)
sun = bpy.data.objects.new("Sun", sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = Vector((0.45, 0.8, -0.38)).normalized().to_track_quat("-Z", "Y").to_euler()   # light travels forward-right: sun behind-left
w = bpy.data.worlds.new("Sky"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.68, 0.85, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.9
w.color = (0.85, 0.87, 0.9)

sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.3
sc.view_settings.view_transform = "Standard"
# render: Cycles CPU (this Blender has no GB10 CUDA kernels or OIDN), written straight to MP4
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 64
sc.cycles.use_denoising = False; sc.cycles.max_bounces = 4
r = sc.render; r.resolution_percentage = 100
r.image_settings.file_format = "FFMPEG"; r.ffmpeg.format = "MPEG4"; r.ffmpeg.codec = "H264"
r.ffmpeg.constant_rate_factor = "HIGH"; r.ffmpeg.ffmpeg_preset = "GOOD"; r.ffmpeg.audio_codec = "NONE"
r.filepath = "//golden_hour_previs_"
print("scene ok", len(bpy.data.objects), "objects,", FRAMES, "frames")
