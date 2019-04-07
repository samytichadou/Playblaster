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

        # resolution percentage
        layout.prop(scn, 'playblaster_resolution_percentage', slider = True)
        # Compositing
        layout.prop(scn, 'playblaster_use_compositing')
        # Simplify
        
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

        layout.operator("playblaster.render")