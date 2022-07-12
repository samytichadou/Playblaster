import bpy

class PLAYBLASTER_OT_set_preferences(bpy.types.Operator):
    """Set Playblaster scene settings"""
    bl_idname = "playblaster.set_preferences"
    bl_label = "Playblaster Settings"

    # UI props
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        pb_props = scn.playblaster_properties
        pb_settings = pb_props.playblast_settings

        # main
        box = layout.box()
        # file storage
        box.prop(pb_settings, 'playblast_location', text="Location")
        box.prop(pb_settings, 'render_type', text="Type")
        box.prop(pb_settings, 'exclude_datetime')

        # general settings
        box = layout.box()
        # resolution percentage
        box.prop(pb_settings, 'resolution_percentage', slider = True)
        # Compositing
        box.prop(pb_settings, 'use_compositing')

        # Frame range override
        box = layout.box()
        box.prop(pb_settings, 'frame_range_override', text = 'Frame Range')
        col = box.column(align = True)
        if not pb_settings.frame_range_override :
            col.enabled = False
        col.prop(pb_settings, 'frame_range_in')
        col.prop(pb_settings, 'frame_range_out')

        # Simplify
        box = layout.box()
        box.prop(pb_settings, 'simplify', text = 'Simplify')
        col = box.column(align = True)
        if not pb_settings.simplify :
            col.enabled = False
        col.prop(pb_settings, 'simplify_subdivision')
        col.prop(pb_settings, 'simplify_particles')

        # render engine
        box = layout.box()
        box.prop(pb_settings, 'render_engine', text = "")

        # EEVEE
        if pb_settings.render_engine == "BLENDER_EEVEE" :
            # eevee settings
            box.prop(pb_settings, 'eevee_samples')
            # box.prop(scn, 'playblaster_eevee_dof')
            # shadow cube size
            # shadow cascade size
            # AO
            # Motion blur
            # volumetric
            # overscan
        # workbench
        elif pb_settings.render_engine == "BLENDER_WORKBENCH" :
            pass
            # lighting type
            # color type
            # backface
            # xray
            # shadow
            # cavity
            # dof
            # outline
            # specular

        # debug
        box = layout.box()
        box.prop(pb_props, 'debug', text = 'Debug')
        row = box.row()
        if not pb_props.debug :
            row.enabled = False
        row.prop(pb_props, 'is_rendering')

        layout.separator()

        layout.operator("playblaster.render", icon = 'RENDER_ANIMATION')
        #layout.prop(context.scene, "playblaster_previous_render")
        layout.operator("playblaster.play_rendered", icon = 'PLAY')

        layout.separator()

    def execute(self, context):
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(PLAYBLASTER_OT_set_preferences)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_set_preferences)