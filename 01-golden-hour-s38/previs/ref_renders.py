# Clay pose/angle grids for character reference sheets. Each driver is rendered seated, with the car body and the
# world hidden (seat, wheel and shifter kept), on a plain studio background, from the angles our shots need.
import bpy, math, os
from mathutils import Vector
sc = bpy.context.scene
OUT = os.path.join(os.path.dirname(bpy.data.filepath), "film2", "sheets", "clay")
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48; sc.cycles.use_denoising = False
sc.render.use_motion_blur = False; sc.render.image_settings.file_format = "PNG"
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 768, 768, 100
sc.timeline_markers.clear()
w = sc.world; w.node_tree.nodes["Background"].inputs[0].default_value = (0.6, 0.6, 0.6, 1)
KEEP = {"RacerA": ("_Driver_", "_SteeringWheel", "_Column", "_Shifter", "_SeatP", "_Console", "_Cooler", "_Belt"),
        "RacerB": ("_Driver_", "_SteeringWheel", "_Column")}
cam_d = bpy.data.cameras.new("RefCam"); cam = bpy.data.objects.new("RefCam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
aim = bpy.data.objects.new("RefAim", None); sc.collection.objects.link(aim)
tc = cam.constraints.new("TRACK_TO"); tc.target = aim; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"

def shoot(car, frame, views, prefix):
    sc.frame_set(frame)
    root = bpy.data.objects[car]
    for o in bpy.data.objects:
        if o.type in ("MESH", "CURVE"):
            o.hide_render = not (o.name.startswith(car) and any(k in o.name for k in KEEP[car])) or "_Brow" in o.name
    M = root.matrix_world
    for name, loc, look, lens in views:
        cam.location = M @ Vector(loc); aim.location = M @ Vector(look); cam_d.lens = lens
        sc.render.filepath = os.path.join(OUT, f"{prefix}_{name}.png")
        bpy.ops.render.render(write_still=True)
    for o in bpy.data.objects: o.hide_render = False

H = (-0.38, -0.55, 1.26)          # Eli's head, car-A space
def off(p, d): return tuple(a + b for a, b in zip(p, d))
shoot("RacerA", 40, [
    ("front",      off(H, (0, 1.7, 0.05)),    off(H, (0, 0, -0.12)), 50),
    ("threeq",     off(H, (-1.3, 1.2, 0.05)), off(H, (0, 0, -0.12)), 50),
    ("profile",    off(H, (-1.7, 0, 0)),      off(H, (0, 0, -0.12)), 50),
    ("back",       off(H, (0.55, -1.1, 0.1)), off(H, (-0.3, 0.6, -0.05)), 40),
    ("hands_wheel", (-0.15, 0.45, 1.35),       (-0.38, -0.08, 1.05), 40),
    ("cooler",     (0.6, -0.02, 1.42),         (0.22, -0.62, 1.12), 30),
], "eli")
HB = (-0.38, -0.45, 1.14)        # Kaz's head, car-B space
shoot("RacerB", 100, [
    ("front",      off(HB, (0, 1.7, 0.05)),   off(HB, (0, 0, -0.12)), 50),
    ("threeq",     off(HB, (1.4, 1.1, 0.05)), off(HB, (0, 0, -0.12)), 50),
    ("profile",    off(HB, (2.0, 0, 0)),      off(HB, (0, 0, -0.12)), 50),   # his right side: what Eli sees across the gap
    ("back",       off(HB, (0.5, -1.1, 0.1)), off(HB, (0, 0.5, -0.05)), 40),
    ("across",     off(HB, (2.6, -0.1, 0.15)), off(HB, (0, 0, -0.1)), 75),     # seen through his passenger window from Eli's car
    ("hands_wheel", (0.15, 0.55, 1.25),        (-0.38, 0.02, 0.92), 40),
], "kaz")
