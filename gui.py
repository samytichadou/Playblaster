import bpy
import os


def view_header_gui(self, context):
    props = context.scene.playblaster_properties
    playblasts = props.playblasts
    row=self.layout.row(align=True)
    if props.playblast_index in range(0, len(props.playblasts)) and len(props.playblasts)!=0:
        index=playblasts[props.playblast_index].index
    else:
        index=-1
        row.enabled=False
    row.operator('playblaster.render_playblast', text="", icon= 'FILE_MOVIE').index=index
    row.popover(panel="PLAYBLASTER_PT_playblasts_popover", text="")

def draw_entry_playblast_viewer(container, playblast):
    row=container.row(align=True)
    row.prop(playblast, "name", text="", emboss=False)
    row.operator("playblaster.render_playblast", text="", icon="FILE_MOVIE", emboss=False).index=playblast.index
    sub=row.row(align=True)
    if not playblast.rendered_filepath:
        sub.enabled=False
    sub.operator("playblaster.play_playblast", text="", icon="PLAY", emboss=False).index=playblast.index

class PLAYBLASTER_PT_playblasts_popover(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Playblasts"
    bl_ui_units_x = 8

    @classmethod
    def poll(cls, context):
        return len(context.scene.playblaster_properties.playblasts)!=0

    def draw(self, context):
        props = context.scene.playblaster_properties
        playblasts = props.playblasts

        layout = self.layout
        col=layout.column(align=True)

        for p in playblasts:
            draw_entry_playblast_viewer(col, p)

class PLAYBLASTER_UL_playblasts(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        draw_entry_playblast_viewer(layout, item)
        # layout.prop(item, "name", text="", emboss=False)
        # row=layout.row(align=True)
        # row.operator("playblaster.render_playblast", text="", icon="FILE_MOVIE", emboss=False).index=item.index
        # sub=row.row(align=True)
        # if not item.rendered_filepath:
        #     sub.enabled=False
        # sub.operator("playblaster.play_playblast", text="", icon="PLAY", emboss=False).index=item.index
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
        row.operator("playblaster.open_playblast_folder",icon="FILE_FOLDER")

        row=layout.row(align=False)
        row.template_list("PLAYBLASTER_UL_playblasts", "", props, "playblasts", props, "playblast_index", rows=4)
        subcol=row.column(align=True)
        subcol.operator("playblaster.manage_actions",text="",icon="ADD").action="ADD"
        subcol.operator("playblaster.manage_actions",text="",icon="REMOVE").action="REMOVE"
        subcol.separator()
        subcol.operator("playblaster.manage_actions",text="",icon="TRIA_UP").action="UP"
        subcol.operator("playblaster.manage_actions",text="",icon="TRIA_DOWN").action="DOWN"

class PLAYBLASTER_PT_playblast_file_settings_sub(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "PLAYBLASTER_PT_playblast"
    bl_label = "File Settings"
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
        col.prop(active, "include_timestamp")
        row=col.row()
        row.prop(active, "use_versions", text="Versions")
        sub=row.row()
        sub.enabled=active.use_versions
        sub.prop(active, "manual_versions", text="Manual", toggle=True)
        sub=sub.row()
        sub.enabled=active.manual_versions
        sub.prop(active, "version", text="")
        col.separator()
        col.prop(active, "end_action", text="End")
        col.prop(active, "player")

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
        col.prop(active, "use_3dviewport")
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

class PLAYBLASTER_PT_playblast_metadata_settings_sub(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "PLAYBLASTER_PT_playblast"
    bl_label = "Metadata"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        props = context.scene.playblaster_properties
        playblasts = props.playblasts
        return props.playblast_index in range(0,len(playblasts))

    def draw_header(self, context):
        props = context.scene.playblaster_properties
        active = props.playblasts[props.playblast_index]
        self.layout.prop(active, "use_stamp", text="")

    def draw(self, context):
        props = context.scene.playblaster_properties
        active = props.playblasts[props.playblast_index]

        layout = self.layout
        layout.active = active.use_stamp

        col = layout.column(align=True)
        col.prop(active, "stamp_font_size", text="Font Size")
        col.prop(active, "use_stamp_labels", text="Include Labels")
        
        box=layout.box()
        col=box.column(align=True)
        col.prop(active, "use_stamp_date")
        col.prop(active, "use_stamp_time")
        col.prop(active, "use_stamp_render_time")
        col.prop(active, "use_stamp_frame")
        col.prop(active, "use_stamp_frame_range")
        col.prop(active, "use_stamp_memory")
        col.prop(active, "use_stamp_hostname")
        col.prop(active, "use_stamp_camera")
        col.prop(active, "use_stamp_lens")
        col.prop(active, "use_stamp_scene")
        col.prop(active, "use_stamp_marker")
        col.prop(active, "use_stamp_filename")
        row=col.row(align=True)
        row.prop(active, "use_stamp_note", text="")
        sub=row.row(align=True)
        sub.enabled = active.use_stamp_note
        sub.prop(active, "stamp_note_text", text="")

class PLAYBLASTER_PT_playblast_infos_sub(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "PLAYBLASTER_PT_playblast"
    bl_label = "Informations"
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
        col.label(text="Name : %s" % os.path.basename(active.rendered_filepath))
        col.label(text="Path : %s" % active.rendered_filepath)
        col.label(text="Hash : %s" % active.hash)


### REGISTER ---
def register():
    bpy.types.VIEW3D_HT_header.append(view_header_gui)
    bpy.utils.register_class(PLAYBLASTER_PT_playblasts_popover)
    bpy.utils.register_class(PLAYBLASTER_UL_playblasts)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_file_settings_sub)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_render_settings_sub)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_output_settings_sub)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_metadata_settings_sub)
    bpy.utils.register_class(PLAYBLASTER_PT_playblast_infos_sub)

def unregister():
    bpy.types.VIEW3D_HT_header.remove(view_header_gui)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblasts_popover)
    bpy.utils.unregister_class(PLAYBLASTER_UL_playblasts)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_file_settings_sub)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_render_settings_sub)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_output_settings_sub)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_metadata_settings_sub)
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast_infos_sub)