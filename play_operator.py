import bpy
import os

from .render_operator import play_video_external

class PLAYBLASTER_OT_play_playblast(bpy.types.Operator):
    bl_idname = "playblaster.play_playblast"
    bl_label = "Play Playblast"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        props = context.scene.playblaster_properties
        return props.playblast_index in range(0, len(props.playblasts)) and bpy.data.is_saved

    def execute(self, context):
        scn = context.scene
        props = scn.playblaster_properties
        active = props.playblasts[props.playblast_index]
        
        if not os.path.isfile(active.rendered_filepath):
            active.rendered_filepath=""
            self.report({'WARNING'}, "Playblast Missing")
            return {'FINISHED'}

        # End Action
        if active.player=="DEFAULT":
            play_video_external(active.rendered_filepath)
        elif active.player=="BLENDER":
            bpy.ops.render.play_rendered_anim()

        self.report({'INFO'}, "Playblast Playing")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PLAYBLASTER_OT_play_playblast)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_play_playblast)