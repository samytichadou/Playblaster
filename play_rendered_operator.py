import bpy, os

from .misc_functions import open_video_file


class PlayblasterPlayRendered(bpy.types.Operator):
    """Play Rendered Video"""
    bl_idname = "playblaster.play_rendered"
    bl_label = "Playblaster Play Rendered"

    @classmethod
    def poll(cls, context):
        previous = context.scene.playblaster_previous_render
        return bpy.data.is_saved and previous != "" and os.path.isfile(previous)

    def execute(self, context):

        open_video_file(context.scene.playblaster_previous_render)

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(PlayblasterPlayRendered)

def unregister():
    bpy.utils.unregister_class(PlayblasterPlayRendered)