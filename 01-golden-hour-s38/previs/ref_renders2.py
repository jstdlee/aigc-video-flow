# Asset library v2 clay renders: top-down lane/landmark map and car B (Kaz) interior views.
import bpy, math, os
from mathutils import Vector
sc = bpy.context.scene
OUT = os.path.join(os.path.dirname(bpy.data.filepath), "film2", "assets2", "clay")
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 32; sc.cycles.use_denoising = False
sc.render.use_motion_blur = False; sc.render.image_settings.file_format = "PNG"; sc.timeline_markers.clear()
for o in bpy.data.objects:
    if "_Brow" in o.name: o.hide_render = True
cd = bpy.data.cameras.new("AssetCam"); cam = bpy.data.objects.new("AssetCam", cd); sc.collection.objects.link(cam); sc.camera = cam
aim = bpy.data.objects.new("AssetAim", None); sc.collection.objects.link(aim)
tc = cam.constraints.new("TRACK_TO"); tc.target = aim; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"

# 1) top-down map at frame 114 (Kaz level with Eli under the gantry), road running left -> right
sc.frame_set(114)
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
cam.constraints.remove(tc)
cd.type = "ORTHO"; cd.ortho_scale = 230
cam.location = (2.0, 205.0, 300.0); cam.rotation_euler = (0, 0, math.pi / 2)    # travel direction (+Y) points screen-right
sc.render.filepath = os.path.join(OUT, "map_topdown.png"); bpy.ops.render.render(write_still=True)
cd.ortho_scale = 60; cam.location = (5.0, 140.0, 300.0)                         # close-up of the gantry block
sc.render.filepath = os.path.join(OUT, "map_detail.png"); bpy.ops.render.render(write_still=True)

# 2) car B interior (clay) from three angles, car body kept, world hidden behind a grey background
cd.type = "PERSP"; cd.sensor_width = 36
tc = cam.constraints.new("TRACK_TO"); tc.target = aim; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
sc.frame_set(100); B = bpy.data.objects["RacerB"]; M = B.matrix_world
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
for name, loc, look, lens in [
    ("b_int_from_passenger", (0.45, -0.35, 1.25), (-0.4, 0.1, 1.0), 24),    # what Eli sees across Kaz's passenger seat
    ("b_int_from_rear",      (0.0, -1.35, 1.3),   (-0.1, 0.8, 0.95), 24),   # back seat looking forward
    ("b_int_dash",           (0.2, -0.2, 1.2),    (-0.38, 0.5, 0.95), 28),  # driver area: wheel, dash
]:
    cam.location = M @ Vector(loc); aim.location = M @ Vector(look); cd.lens = lens
    sc.render.filepath = os.path.join(OUT, f"{name}.png"); bpy.ops.render.render(write_still=True)
