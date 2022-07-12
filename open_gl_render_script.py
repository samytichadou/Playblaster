import bpy, sys

bpy.ops.render.opengl(
    animation=True,
    view_context=True,
    render_keyed_only=False,
)
print("test" + sys.argv)
bpy.ops.wm.quit_blender()