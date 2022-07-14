import bpy


class PLAYBLASTER_UL_playblasts(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "name", text="", emboss=False)
        sub=layout.row(align=True)
        if not item.is_rendered:
            sub.enabled=False
        sub.label(text="", icon="FILE_MOVIE")
        sub.label(text="", icon="RENDER_ANIMATION")
        sub.label(text="", icon="X")


class PLAYBLASTER_PT_playblast(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Playblast"
    bl_label = "Playblasts"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def draw(self, context):
        props = context.scene.playblaster_properties
        playblasts = props.playblasts

        layout = self.layout

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
        col.prop(active, "render_engine", text="Engine")
        col.separator()
        subcol=col.column(align=True)
        if active.render_engine!="BLENDER_EEVEE":
            subcol.enabled=False
        subcol.prop(active, "eevee_samples")
        subcol.prop(active, "eevee_ambient_occlusion")
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


### REGISTER ---
def register():
    bpy.utils.register_class(PLAYBLASTER_UL_playblasts)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_render_settings_sub)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_output_settings_sub)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_UL_playblasts)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_render_settings_sub)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_output_settings_sub)