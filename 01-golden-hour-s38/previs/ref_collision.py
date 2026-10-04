# Clay storyboard stills for the new collision beat (after "STOP OR DIE!"):
# Kaz rams car A's left flank, car A is shoved right toward the sedan, near miss, Eli corrects.
# Run: blender -b highway_race.blend -P film2/ref_collision.py   (file is not saved)
import bpy, math, os
from mathutils import Vector
sc = bpy.context.scene
OUT = os.path.join(os.path.dirname(bpy.data.filepath), "film2", "clay_hit"); os.makedirs(OUT, exist_ok=True)
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 32; sc.cycles.use_denoising = False
sc.render.use_motion_blur = False; sc.render.image_settings.file_format = "PNG"; sc.timeline_markers.clear()   # markers bind the shot cameras
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
for o in bpy.data.objects:
    if "_Brow" in o.name: o.hide_render = True

sc.frame_set(144)                                   # end of the stare: both cars level, sedan in the right lane
A, B, S = (bpy.data.objects[n] for n in ("RacerA", "RacerB", "Sedan"))
a0, b0, s0 = A.location.copy(), B.location.copy(), S.location.copy()
print("frame 144  A", tuple(a0), " B", tuple(b0), " sedan", tuple(s0))
for o in (A, B, S): o.animation_data_clear()        # hold the poses we set (children keep their own animation)

cd = bpy.data.cameras.new("HitCam"); cam = bpy.data.objects.new("HitCam", cd); sc.collection.objects.link(cam); sc.camera = cam
aim = bpy.data.objects.new("HitAim", None); sc.collection.objects.link(aim)
tc = cam.constraints.new("TRACK_TO"); tc.target = aim; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
cd.sensor_width = 36

def pose(o, x, dy, yaw_deg, base):                  # yaw > 0 = nose turns right (+x); heading z = -yaw
    o.location = Vector((x, base.y + dy, base.z)); o.rotation_euler.z = -math.radians(yaw_deg)

def shot(name, cam_loc, look, lens):
    cam.location = Vector(cam_loc); aim.location = Vector(look); cd.lens = lens
    sc.render.filepath = os.path.join(OUT, name + ".png"); bpy.ops.render.render(write_still=True)

y = a0.y
# 1) IMPACT: Kaz cuts right, his front-right corner hits car A's left rear door; car A starts to yaw right
pose(B, 3.75, -2.6, 9, a0); pose(A, 6.1, 0, 7, a0); pose(S, 9.4, -3.0, 0, a0)
shot("hit_a_impact_drone", (1.0, y - 16, 7.5), (5.0, y - 1.0, 0.6), 30)          # high, behind-left
shot("hit_b_spark_low", (4.6, y - 6.5, 0.45), (4.9, y - 1.6, 0.55), 30)          # low between the cars at the contact
# 2) NEAR MISS: car A shoved into the right lane, nose right, inches from the sedan's left side; sedan swerves
pose(A, 7.9, 0, 12, a0); pose(B, 3.2, -6.0, -4, a0); pose(S, 10.1, 1.8, 6, a0)
shot("hit_c_nearmiss_front", (8.6, y + 14, 1.1), (8.6, y + 1.0, 0.8), 35)        # camera car ahead, looking back
# 3) CORRECTION: inside car A, the wheel and Eli's hands from the passenger side
M = A.matrix_world
shot("hit_d_wheel_ecu", M @ Vector((0.15, 0.15, 1.15)), M @ Vector((-0.4, 0.55, 0.95)), 28)
print("done")
