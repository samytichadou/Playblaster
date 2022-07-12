import bpy

bpy.ops.render.opengl(
    animation=True,
    view_context=False,
    render_keyed_only=False,
)
bpy.ops.wm.quit_blender()