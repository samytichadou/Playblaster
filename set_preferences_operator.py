import bpy


class PLAYBLASTER_OT_set_preferences(bpy.types.Operator):
    """Set Playblaster scene settings"""
    bl_idname = "playblaster.set_preferences"
    bl_label = "Playblaster Settings"

    # UI props
    show_debug: bpy.props.BoolProperty()
    show_general: bpy.props.BoolProperty()
    show_frame_range: bpy.props.BoolProperty()
    show_engine: bpy.props.BoolProperty()
    show_simplify: bpy.props.BoolProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        pb_props = scn.playblaster_properties
        pb_settings = pb_props.playblast_settings

        # debug
        box = layout.box()
        row = box.row(align = True)
        icon_debug = 'TRIA_DOWN' if self.show_debug else 'TRIA_RIGHT'
        row.prop(self, 'show_debug', text = '', icon = icon_debug, emboss = False)
        row.label(text = 'Debug')
        row.prop(pb_props, 'debug', text = '')
        if self.show_debug :
            row = box.row()
            if not pb_props.debug :
                row.enabled = False
            row.prop(pb_props, 'is_rendering')


        # general settings
        box = layout.box()
        row = box.row(align = True)
        icon_general = 'TRIA_DOWN' if self.show_general else 'TRIA_RIGHT'
        row.prop(self, 'show_general', text = '', icon = icon_general, emboss = False)
        row.label(text = 'General Settings')

        if self.show_general :
            # file storage
            box.prop(pb_props, 'playblast_location', text="Location")

            # resolution percentage
            box.prop(pb_settings, 'resolution_percentage', slider = True)

            # Compositing
            box.prop(pb_settings, 'use_compositing')

            # Frame range override
            subbox = box.box()
            row = subbox.row(align = True)
            icon_frame_range = 'TRIA_DOWN' if self.show_frame_range else 'TRIA_RIGHT'
            row.prop(self, 'show_frame_range', text = '', icon = icon_frame_range, emboss = False)
            row.label(text = "Frame Range")
            row.prop(pb_settings, 'frame_range_override', text = '')
            if self.show_frame_range :
                col = subbox.column(align = True)
                if not pb_settings.frame_range_override :
                    col.enabled = False
                col.prop(pb_settings, 'frame_range_in')
                col.prop(pb_settings, 'frame_range_out')

            # Simplify
            subbox = box.box()
            row = subbox.row(align = True)
            icon_simplify = 'TRIA_DOWN' if self.show_simplify else 'TRIA_RIGHT'
            row.prop(self, 'show_simplify', text = '', icon = icon_simplify, emboss = False)
            row.label(text = 'Simplify')
            row.prop(pb_settings, 'simplify', text = '')
            if self.show_simplify :
                col = subbox.column(align = True)
                if not pb_settings.simplify :
                    col.enabled = False
                col.prop(pb_settings, 'simplify_subdivision')
                col.prop(pb_settings, 'simplify_particles')


        # render engine
        box = layout.box()
        row = box.row(align = True)
        icon_engine = 'TRIA_DOWN' if self.show_engine else 'TRIA_RIGHT'
        row.prop(self, 'show_engine', text = '', icon = icon_engine, emboss = False)
        row.label(text = "Engine")
        row.prop(pb_settings, 'render_engine', text = "")

        if self.show_engine :

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

        layout.separator()

        layout.operator("playblaster.render", icon = 'RENDER_ANIMATION')
        #layout.prop(context.scene, "playblaster_previous_render")
        layout.operator("playblaster.play_rendered", icon = 'PLAY')

    def execute(self, context):
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(PLAYBLASTER_OT_set_preferences)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_set_preferences)