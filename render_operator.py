import bpy
import os
import subprocess
import platform

from .addon_preferences import get_addon_preferences

list_scene = (
    "frame_start",
    "frame_end",
    "use_preview_range",
    "frame_current"
)

list_render = (
    "filepath",
    "resolution_percentage",
    "use_compositing",
    "use_sequencer",
    "use_simplify",
    "simplify_subdivision_render",
    "simplify_child_particles_render",
)

list_image_settings = (
    "file_format",
)

list_ffmpeg = (
    "format",
    "constant_rate_factor",
    "ffmpeg_preset",
    "gopsize",
    "codec",
    "audio_codec",
)

list_eevee = (
    "taa_samples",
    "use_gtao",
)

list_shading = (
    "type",
)

list_region3d = (
    "view_perspective",
    "view_matrix",
)

list_overlay = (
    "show_overlays",
)

def store_parameters(scene, context):
    datas={}

    # Scene
    for p in list_scene:
        datas[p] = getattr(scene, p)
    # Render
    rd=scene.render
    for p in list_render:
        datas[p] = getattr(rd, p)
    # Image settings
    img_settings=rd.image_settings
    for p in list_image_settings:
        datas[p] = getattr(img_settings, p)
    # FFMPEG
    ffmpeg=rd.ffmpeg
    for p in list_ffmpeg:
        datas[p] = getattr(ffmpeg, p)
    # EEVEE
    eevee=scene.eevee
    for p in list_eevee:
        datas[p] = getattr(eevee, p)

    # Shading
    shading=context.area.spaces[0].shading
    for p in list_shading:
        datas[p] = getattr(shading, p)

    # 3d region
    region_3d=context.area.spaces[0].region_3d
    for p in list_region3d:
        datas[p] = getattr(region_3d, p)

    # Overlay
    overlay=context.area.spaces[0].overlay
    for p in list_overlay:
        datas[p] = getattr(overlay, p)

    return datas

def restore_parameters(datas, scene, context):
    # Scene
    for p in list_scene:
        setattr(scene, p, datas[p])
    # Render
    rd=scene.render
    for p in list_render:
        setattr(rd, p, datas[p])
    # Image settings
    img_settings=rd.image_settings
    for p in list_image_settings:
        setattr(img_settings, p, datas[p])
    # FFMPEG
    ffmpeg=rd.ffmpeg
    for p in list_ffmpeg:
        setattr(ffmpeg, p, datas[p])
    # EEVEE
    eevee=scene.eevee
    for p in list_eevee:
        setattr(eevee, p, datas[p])

    # Shading
    shading=context.area.spaces[0].shading
    for p in list_shading:
        setattr(shading, p, datas[p])

    # 3d region
    region_3d=context.area.spaces[0].region_3d
    for p in list_region3d:
        setattr(region_3d, p, datas[p])

    # Overlay
    overlay=context.area.spaces[0].overlay
    for p in list_overlay:
        setattr(overlay, p, datas[p])

def return_filepath(playblast):
    prefs=get_addon_preferences()
    blend_fp=bpy.data.filepath
    blend_name=os.path.splitext(os.path.basename(blend_fp))[0]
    file_name="%s_%s_%s_" % (playblast.hash, playblast.name, blend_name)
    if prefs.playblast_location=="ALONGSIDE":
        tmp = os.path.join(os.path.dirname(blend_fp), prefs.playblast_folder_name)
        fp_dir = os.path.join(tmp, blend_name)
        fp = os.path.join(fp_dir, file_name)
    else:
        fp_dir = os.path.join(prefs.playblast_folderpath, "playblasts")
        fp = os.path.join(fp_dir, file_name)
    os.makedirs(fp_dir, exist_ok=True)
    return fp

def set_render_parameters(scene, settings, filepath, context):
    # Scene
    if settings.frame_range_type=='PREVIEW':
        scene.use_preview_range=True
    elif settings.frame_range_type=='OVERRIDE':
        scene.frame_start=settings.frame_range_in
        scene.frame_end=settings.frame_range_out

    space_3d=context.area.spaces[0]
    # Shading
    space_3d.shading.type=settings.shading

    # Region 3d
    if not settings.use_3dviewport:
        space_3d.region_3d.view_perspective="CAMERA"

    # Overlay
    space_3d.overlay.show_overlays=settings.show_overlays

    # Render
    rd = scene.render
    rd.filepath=filepath
    rd.use_compositing=settings.use_compositing
    rd.use_simplify=settings.simplify
    rd.simplify_subdivision_render=settings.simplify_subdivision
    rd.simplify_child_particles_render=settings.simplify_particles
    rd.use_sequencer=False

    # Image settings
    img_settings=rd.image_settings
    img_settings.file_format="FFMPEG"

    # FFMPEG
    ffmpeg=rd.ffmpeg
    ffmpeg.format = 'MPEG4'
    ffmpeg.codec = 'H264'
    ffmpeg.constant_rate_factor = 'HIGH'
    ffmpeg.ffmpeg_preset = 'REALTIME'
    ffmpeg.gopsize = 10
    ffmpeg.audio_codec = 'AAC'

    # EEVEE
    eevee=scene.eevee
    eevee.taa_samples = settings.eevee_samples
    eevee.use_gtao = settings.eevee_ambient_occlusion

def play_video_external(video_filepath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', video_filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(video_filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', video_filepath))

def preselect_objects(context, settings):
    old_selection=context.selected_objects
    if settings.preselection=="ALL":
        for ob in context.scene.objects:
            ob.select_set(True)
    return old_selection

def restore_selection(context, old_selection):
    for ob in context.scene.objects:
        if ob in old_selection:
            ob.select_set(True)
        else:
            ob.select_set(False)

class PLAYBLASTER_OT_render_playblast(bpy.types.Operator):
    bl_idname = "playblaster.render_playblast"
    bl_label = "Render Playblast"
    bl_options = {"INTERNAL"}

    index: bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved and len(context.scene.playblaster_properties.playblasts)!=0

    def execute(self, context):
        scn = context.scene
        props = scn.playblaster_properties

        if self.index not in range(0, len(props.playblasts)):
            self.report({'WARNING'}, "Playblast not existing")
            return {'FINISHED'}

        active = props.playblasts[self.index]
        fp = return_filepath(active)

        # Render settings
        datas = store_parameters(scn, context)
        if active.render_type=="OPENGLKEY" and active.preselection!="NONE":
            old_selection=preselect_objects(context, active)
        set_render_parameters(scn, active, fp, context)

        # Render
        if active.render_type=="OPENGL":
            bpy.ops.render.opengl(
                animation=True, 
                render_keyed_only=False, 
                view_context=True,
            )
        elif active.render_type=="OPENGLKEY":
            bpy.ops.render.opengl(
                animation=True,
                render_keyed_only=True,
                view_context=True,
            )

        active.rendered_filepath=scn.render.frame_path()

        # End Action
        if active.end_action=="PLAY":
            if active.player=="DEFAULT":
                play_video_external(scn.render.frame_path())
            elif active.player=="BLENDER":
                bpy.ops.render.play_rendered_anim()

        # Restore parameters
        restore_parameters(datas, scn, context)
        if active.render_type=="OPENGLKEY" and active.preselection!="NONE":
            restore_selection(context, old_selection)

        self.report({'INFO'}, "Playblast Done")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PLAYBLASTER_OT_render_playblast)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_render_playblast)