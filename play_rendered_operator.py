import bpy, os

from .misc_functions import open_video_file


class PLAYBLASTER_OT_play_rendered(bpy.types.Operator):
    """Play Rendered Video"""
    bl_idname = "playblaster.play_rendered"
    bl_label = "Playblaster Play Rendered"

    @classmethod
    def poll(cls, context):
        pb_props = context.scene.playblaster_properties
        previous = pb_props.previous_render
        return bpy.data.is_saved and previous != "" and os.path.isfile(previous)

    def execute(self, context):

        open_video_file(context.scene.playblaster_properties.previous_render)

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(PLAYBLASTER_OT_play_rendered)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_play_rendered)