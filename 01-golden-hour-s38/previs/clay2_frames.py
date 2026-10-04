# render shot boundary frames of the clay previs as PNG keyframe guides
import bpy, sys
sc = bpy.context.scene
sc.render.image_settings.file_format = "PNG"
sc.cycles.samples = 40
sc.render.resolution_percentage = 100
sc.render.filepath = "//film2/clay2/f_"
