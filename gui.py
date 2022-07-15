import bpy


def view_header_gui(self, context):
    self.layout.operator('playblaster.render_playblast', text="", icon= 'FILE_MOVIE')


class PLAYBLASTER_UL_playblasts(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "name", text="", emboss=False)
        row=layout.row(align=True)
        row.operator("playblaster.render_playblast", text="", icon="FILE_MOVIE", emboss=False)
        sub=row.row(align=True)
        if not item.rendered_filepath:
            sub.enabled=False
        sub.operator("playblaster.play_playblast", text="", icon="PLAY", emboss=False)
        # sub.label(text="", icon="X")


class PLAYBLASTER_PT_playblast(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "Playblaster"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        props = context.scene.playblaster_properties
        playblasts = props.playblasts

        layout = self.layout

        if not bpy.data.is_saved:
            layout.label(text="Blend file is not saved", icon="INFO")

        row=layout.row(align=False)
        row.template_list("PLAYBLASTER_UL_playblasts", "", props, "playblasts", props, "playblast_index", rows=4)
        subcol=row.column(align=True)
        subcol.operator("playblaster.manage_actions",text="",icon="ADD").action="ADD"
        subcol.operator("playblaster.manage_actions",text="",icon="REMOVE").action="REMOVE"
        subcol.separator()
        subcol.operator("playblaster.manage_actions",text="",icon="TRIA_UP").action="UP"
        subcol.operator("playblaster.manage_actions",text="",icon="TRIA_DOWN").action="DOWN"


class PLAYBLASTER_PT_playblast_render_settings_sub(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "PLAYBLASTER_PT_playblast"
    bl_label = "Render Settings"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        props = context.scene.playblaster_properties
        playblasts = props.playblasts
        return props.playblast_index in range(0,len(playblasts))

    def draw(self, context):
        props = context.scene.playblaster_properties
        active = props.playblasts[props.playblast_index]

        layout = self.layout

        col=layout.column(align=True)
        col.prop(active, "render_type", text="Type")
        sub=col.row()
        if active.render_type!="OPENGLKEY":
            sub.enabled=False
        sub.prop(active, "preselection")
        col.separator()
        col.prop(active, "shading", text="Shading")
        col.separator()
        col.prop(active, "eevee_samples")
        col.prop(active, "eevee_ambient_occlusion")
        col.separator()
        col.prop(active, "show_overlays")
        col.separator()
        col.prop(active, "simplify")
        subcol=col.column(align=True)
        if not active.simplify:
            subcol.enabled=False
        subcol.prop(active, "simplify_subdivision")
        subcol.prop(active, "simplify_particles")


class PLAYBLASTER_PT_playblast_output_settings_sub(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "PLAYBLASTER_PT_playblast"
    bl_label = "Output Settings"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        props = context.scene.playblaster_properties
        playblasts = props.playblasts
        return props.playblast_index in range(0,len(playblasts))

    def draw(self, context):
        props = context.scene.playblaster_properties
        active = props.playblasts[props.playblast_index]

        layout = self.layout

        col=layout.column(align=True)
        col.prop(active, "resolution_percentage")
        col.separator()
        col.prop(active, "frame_range_type", text="")
        subcol=col.column(align=True)
        if active.frame_range_type!="OVERRIDE":
            subcol.enabled=False
        subcol.prop(active, "frame_range_in")
        subcol.prop(active, "frame_range_out")
        col.separator()
        col.prop(active, "use_compositing")
        col.prop(active, "use_3dviewport")
        col.separator()
        col.prop(active, "end_action")
        col.prop(active, "player")


### REGISTER ---
def register():
    bpy.types.VIEW3D_HT_header.append(view_header_gui)
    bpy.utils.register_class(PLAYBLASTER_UL_playblasts)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_render_settings_sub)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_output_settings_sub)

def unregister():
    bpy.types.VIEW3D_HT_header.remove(view_header_gui)
    bpy.utils.unregister_class(PLAYBLASTER_UL_playblasts)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_render_settings_sub)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_output_settings_sub)