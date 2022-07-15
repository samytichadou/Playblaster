import bpy
import os

from .render_operator import play_video_external

class PLAYBLASTER_OT_play_playblast(bpy.types.Operator):
    bl_idname = "playblaster.play_playblast"
    bl_label = "Play Playblast"
    bl_options = {"INTERNAL"}

    index: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def execute(self, context):
        scn = context.scene
        props = scn.playblaster_properties

        if self.index not in range(0, len(props.playblasts)):
            self.report({'WARNING'}, "Playblast not existing")
            return {'FINISHED'}

        active = props.playblasts[self.index]
        
        if not os.path.isfile(active.rendered_filepath):
            active.rendered_filepath=""
            self.report({'WARNING'}, "Playblast Missing")
            return {'FINISHED'}

        # End Action
        if active.player=="DEFAULT":
            play_video_external(active.rendered_filepath)
        elif active.player=="BLENDER":
            old_filepath=scn.render.filepath
            old_extension=scn.render.use_file_extension
            scn.render.filepath=active.rendered_filepath
            scn.render.use_file_extension=False
            bpy.ops.render.play_rendered_anim()
            scn.render.filepath=old_filepath
            scn.render.use_file_extension=old_extension

        self.report({'INFO'}, "Playblast Playing")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PLAYBLASTER_OT_play_playblast)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_play_playblast)