import bpy

class PlayblasterSetPreferences(bpy.types.Operator):
    """Set Playblaster scene settings"""
    bl_idname = "playblaster.set_preferences"
    bl_label = "Playblaster Settings"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        # debug
        box = layout.box()
        box.prop(scn, 'playblaster_debug')
        if scn.playblaster_debug :
            box.prop(scn, 'playblaster_is_rendering')

        # resolution percentage
        layout.prop(scn, 'playblaster_resolution_percentage', slider = True)
        # Compositing
        layout.prop(scn, 'playblaster_use_compositing')
        # Simplify
        layout.prop(scn, 'playblaster_simplify')
        if scn.playblaster_simplify :
            col = layout.column(align = True)
            col.prop(scn, 'playblaster_simplify_subdivision')
            col.prop(scn, 'playblaster_simplify_particles')
        # Frame range override
        layout.prop(scn, 'playblaster_frame_range_override')
        if scn.playblaster_frame_range_override :
            col = layout.column(align = True)
            col.prop(scn, 'playblaster_frame_range_in')
            col.prop(scn, 'playblaster_frame_range_out')

        layout.separator()

        box = layout.box()
        # render engine
        box.label(text = "Playblast Engine")
        box.prop(scn, 'playblaster_render_engine', text = "")

        # EEVEE
        if scn.playblaster_render_engine == "BLENDER_EEVEE" :
            # eevee settings
            box.prop(scn, 'playblaster_eevee_samples')
            box.prop(scn, 'playblaster_eevee_dof')
            # shadow cube size
            # shadow cascade size
            # AO
            # Motion blur
            # volumetric
            # overscan

        # workbench
        elif scn.playblaster_render_engine == "BLENDER_WORKBENCH" :
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


        layout.separator()

        layout.operator("playblaster.render", icon = 'RENDER_ANIMATION')
        #layout.prop(context.scene, "playblaster_previous_render")
        layout.operator("playblaster.play_rendered", icon = 'PLAY')
