import bpy
import os

blender_executable = bpy.app.binary_path
playblaster_completion = 0
playblaster_is_rendering = False
modal_refreshing = "Playblast in Progress - Esc to Cancel"
render_openglkey_script = os.path.join(os.path.dirname(os.path.realpath(__file__)), "open_gl_render_keyed_script.py")
render_opengl_script = os.path.join(os.path.dirname(os.path.realpath(__file__)), "open_gl_render_script.py")