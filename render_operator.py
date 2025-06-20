import bpy
import os
import shutil
import subprocess
import platform
import datetime
import random

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
    # Metadatas
    "stamp_font_size",
    "use_stamp_labels",
    "use_stamp",
    "use_stamp_date",
    "use_stamp_time",
    "use_stamp_render_time",
    "use_stamp_frame",
    "use_stamp_frame_range",
    "use_stamp_memory",
    "use_stamp_hostname",
    "use_stamp_camera",
    "use_stamp_lens",
    "use_stamp_scene",
    "use_stamp_marker",
    "use_stamp_filename",
    "use_stamp_note",
    "stamp_note_text",
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
    "view_distance",
    "view_location",
    "view_rotation",
    "view_perspective",

    # "view_matrix",
    # "view_camera_offset",
    # "view_camera_zoom",
    #"window_matrix",
)

list_overlay = (
    # Custom overlays
    "show_overlays",
    "show_ortho_grid",
    "show_floor",
    "show_axis_x",
    "show_axis_y",
    "show_axis_z",
    "show_text",
    "show_cursor",
    "show_stats",
    "show_annotation",
    "show_extras",
    "show_bones",
    "show_light_colors",
    "show_motion_paths",
    "show_relationship_lines",
    "show_object_origins",
    "show_outline_selected",
    "show_object_origins_all",
    "show_wireframes",
    "show_face_orientation",
    "show_viewer_attribute",
    "show_viewer_text",
)

list_preferences_view = (
    "render_display_type",
)

list_context_view = (
    "show_reconstruction",
)

list_scene_camera = (
    "show_background_images",
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

    # Preferences
    pref_view=context.preferences.view
    for p in list_preferences_view:
        datas[p] = getattr(pref_view, p)

    # Context view
    view=context.area.spaces[0]
    for p in list_context_view:
        datas[p] = getattr(view, p)

    # Scene camera
    cam=context.scene.camera.data
    for p in list_scene_camera:
        datas[p] = getattr(cam, p)

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
        # Deal with ffmpeg properties bug (enum not init)
        try:
            setattr(ffmpeg, p, datas[p])
        except TypeError:
            print(f"PLAYBLASTER --- Unable to restore ffmpeg {p} property")
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

    # Preferences
    pref_view=context.preferences.view
    for p in list_preferences_view:
        setattr(pref_view, p, datas[p])

    # Context view
    view=context.area.spaces[0]
    for p in list_context_view:
        setattr(view, p, datas[p])

    # Scene camera
    cam=context.scene.camera.data
    for p in list_scene_camera:
        setattr(cam, p, datas[p])

def get_timestamp():
    x = datetime.datetime.now()
    timestamp=(x.strftime("%Y%m%d_%H%M%S")) 
    return timestamp

def return_filepath(playblast):
    prefs=get_addon_preferences()
    blend_fp=bpy.data.filepath
    blend_name=os.path.splitext(os.path.basename(blend_fp))[0]

    # Build name
    file_name=""

    if playblast.include_timestamp:
        file_name+=f"{get_timestamp()}_"

    file_name+=f"{blend_name}"

    if playblast.playblast_name:
        file_name+=f"_{playblast.name}"

    if playblast.use_versions:
        file_name+="_v%s" % str(playblast.version).zfill(3)

    if playblast.frame_numbers:
        file_name+="_"

    if prefs.playblast_location=="ALONGSIDE":
        tmp = os.path.join(os.path.dirname(blend_fp), prefs.playblast_folder_name)

        folderpath = tmp
        if playblast.playblast_file_folder:
            folderpath = os.path.join(tmp, blend_name)
        fp = os.path.join(folderpath, file_name)

    else:

        folderpath = prefs.playblast_folderpath
        if playblast.playblast_file_folder:
            folderpath = os.path.join(prefs.playblast_folderpath, "playblasts")
        fp = os.path.join(folderpath, file_name)

    os.makedirs(folderpath, exist_ok=True)

    playblast.rendered_filepath = fp

    return fp

def set_render_parameters(scene, settings, filepath, context):
    # Scene
    scene.use_preview_range=False
    if settings.frame_range_type=='PREVIEW':
        scene.frame_start=scene.frame_preview_start
        scene.frame_end=scene.frame_preview_end
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
    if not settings.show_overlays:

        # Custom overlays to keep cam images
        if settings.show_camera_background_images:
            for p in list_overlay:
                setattr(space_3d.overlay, p, False)

            space_3d.overlay.show_overlays=True
            space_3d.show_reconstruction = False

        else:
            space_3d.overlay.show_overlays=False

    # Background images
    if not settings.show_camera_background_images:
        scene.camera.data.show_background_images = False

    # Render
    rd = scene.render
    rd.resolution_percentage=settings.resolution_percentage
    rd.filepath=filepath
    rd.use_compositing=settings.use_compositing
    rd.use_simplify=settings.simplify
    rd.simplify_subdivision_render=settings.simplify_subdivision
    rd.simplify_child_particles_render=settings.simplify_particles
    rd.use_sequencer=False
    # Metadata
    rd.stamp_font_size          = settings.stamp_font_size
    rd.use_stamp_labels         = settings.use_stamp_labels
    rd.use_stamp                = settings.use_stamp
    rd.use_stamp_date           = settings.use_stamp_date
    rd.use_stamp_time           = settings.use_stamp_time
    rd.use_stamp_render_time    = settings.use_stamp_render_time
    rd.use_stamp_frame          = settings.use_stamp_frame
    rd.use_stamp_frame_range    = settings.use_stamp_frame_range
    rd.use_stamp_memory         = settings.use_stamp_memory
    rd.use_stamp_hostname       = settings.use_stamp_hostname
    rd.use_stamp_camera         = settings.use_stamp_camera
    rd.use_stamp_lens           = settings.use_stamp_lens
    rd.use_stamp_scene          = settings.use_stamp_scene
    rd.use_stamp_marker         = settings.use_stamp_marker
    rd.use_stamp_filename       = settings.use_stamp_filename
    rd.use_stamp_note           = settings.use_stamp_note
    rd.stamp_note_text          = settings.stamp_note_text

    # Python datapath
    if settings.use_python_datapath:
        # Trigger update
        settings.python_datapath = settings.python_datapath

        if settings.python_datapath_result:
            if not rd.use_stamp_note:
                rd.use_stamp_note = True
                rd.stamp_note_text = ""
            else:
                rd.stamp_note_text += "   -   "

            # Burn in note
            rd.stamp_note_text += settings.python_datapath_result

        else:
            print("PLAYBLASTER --- Invalid python datapath result, avoiding")

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

    # Preferences
    context.preferences.view.render_display_type="NONE"

def play_video_external(video_filepath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', video_filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(video_filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', video_filepath))

def play_video_internal(video_filepath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', video_filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(video_filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', video_filepath))

def preselect_objects(context, settings):
    old_selection=context.selected_objects
    if settings.preselection=="ALL":
        for ob in context.view_layer.objects:
            ob.select_set(True)
    return old_selection

def restore_selection(context, old_selection):
    for ob in context.view_layer.objects:
        if ob in old_selection:
            ob.select_set(True)
        else:
            ob.select_set(False)

def delete_file(filepath):
    try:
        if os.path.isfile(filepath) :
            os.remove(filepath)
            print("PLAYBLASTER --- Removed : %s" % filepath)
            return True
    except PermissionError:
        print("PLAYBLASTER --- Unable to delete media file : %s" % filepath)
        return False

def get_files_by_pattern(pattern, folder):
    file_list=[]
    for f in os.listdir(folder):
        if pattern in f:
            file_list.append(os.path.join(folder, f))
    return file_list

def get_next_version(playblast):
    version_list=[]
    pattern="_%s_v" % playblast.hash
    for f in get_files_by_pattern(pattern, os.path.dirname(return_filepath(playblast))):
        file_name=os.path.basename(f)
        tmp=file_name.split("_%s_v" % playblast.hash)[1]
        v=tmp.split("_")[0]
        v=int(v)
        if v not in version_list:
            version_list.append(v)
    if version_list:
        version=max(version_list)+1
    else:
        version=1
    return version


datas={}
old_selection=None
keyed=False
index=0

# Macro operator to concatenate transform and our finalization
class PLAYBLASTER_OT_render_macro(bpy.types.Macro):
    bl_idname = "playblaster.render_macro"
    bl_label = "Render Macro"
    bl_options = {"INTERNAL"}

class PLAYBLASTER_OT_render_keyed_macro(bpy.types.Macro):
    bl_idname = "playblaster.render_keyed_macro"
    bl_label = "Render Macro"
    bl_options = {"INTERNAL"}

def create_playblast():
    scn = bpy.context.scene
    props = scn.playblaster_properties

    new_playblast=props.playblasts.add()
    new_playblast.name="Playblast"
    new_playblast.frame_range_in=scn.frame_start
    new_playblast.frame_range_out=scn.frame_end
    new_playblast.hash=generate_random()
    props.playblast_index=new_playblast.index=len(props.playblasts)-1

def generate_random():
    return(str(random.randrange(0,99999)).zfill(5))

class PLAYBLASTER_OT_render_playblast(bpy.types.Operator):
    bl_idname = "playblaster.render_playblast"
    bl_label = "Render Playblast"
    bl_options = {"INTERNAL"}

    index: bpy.props.IntProperty(
        default = -1,
        options = {"SKIP_SAVE"},
    )
    
    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def execute(self, context):

        scn = context.scene
        props = scn.playblaster_properties

        # Create playblast if needed
        if not props.playblasts:
            create_playblast()
            # Set index
            props.playblast_index = 0
            idx = 0

        else:

            if self.index != -1:
                idx = self.index

            else:
                idx = props.playblast_index

        # Check if playblast selected
        if idx==-1 \
        or idx not in range(0, len(props.playblasts)):
            self.report({'WARNING'}, "Playblast not existing")
            return {'FINISHED'}

        global datas, keyed, index
        index=idx
        active = props.playblasts[idx]

        # Change version if needed
        if active.use_versions and not active.manual_versions:
            active.version=get_next_version(active)
            print(get_next_version(active))
        
        fp = return_filepath(active)

        # Delete previous
        if active.rendered_filepath and not active.use_versions:
            delete_file(active.rendered_filepath)
        elif active.use_versions:
            if active.version==1:
                if active.rendered_filepath:
                    delete_file(active.rendered_filepath)
            else:
                pattern="%s_v%s_" % (active.hash, str(active.version).zfill(3))
                for f in get_files_by_pattern(pattern, os.path.dirname(fp)):
                    delete_file(f)

        # Render settings
        datas = store_parameters(scn, context)
        if active.render_type=="OPENGLKEY" and active.preselection!="NONE":
            global old_selection
            old_selection=preselect_objects(context, active)
        set_render_parameters(scn, active, fp, context)

        props._is_rendering=True

        if active.render_type=="OPENGL":
            bpy.ops.playblaster.render_macro('INVOKE_DEFAULT')
        else:
            bpy.ops.playblaster.render_keyed_macro('INVOKE_DEFAULT')

        return {'FINISHED'}

class PLAYBLASTER_OT_render_playblast_postactions(bpy.types.Operator):
    bl_idname = "playblaster.render_playblast_postactions"
    bl_label = "Render Playblast Post Actions"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        scn = context.scene
        props = scn.playblaster_properties

        props.is_rendering=False

        active = props.playblasts[index]
        rnd_path = scn.render.frame_path()

        # Rename file
        if not active.frame_numbers:
            ext = os.path.splitext(rnd_path)[1]
            new = f"{active.rendered_filepath}{ext}"

            if os.path.isfile(new):
                if not delete_file(new):
                    shutil.copy2(rnd_path, new)
                    delete_file(rnd_path)
                else:
                    os.rename(rnd_path, new)
            else:
                os.rename(rnd_path, new)

            active.rendered_filepath=new
        else:
            active.rendered_filepath=rnd_path

        # End Action
        if not props.is_cancelling:
            if active.end_action=="PLAY":
                if active.player=="DEFAULT":
                    play_video_external(active.rendered_filepath)
                elif active.player=="BLENDER":
                    # bpy.ops.render.play_rendered_anim()
                    play_video_internal(active.rendered_filepath)

        # Restore parameters
        restore_parameters(datas, scn, context)
        if active.render_type=="OPENGLKEY" and active.preselection!="NONE":
            restore_selection(context, old_selection)
        props.is_cancelling=False

        self.report({'INFO'}, "Playblast Done")

        return {'FINISHED'}

### REGISTER ---

def register():
    bpy.utils.register_class(PLAYBLASTER_OT_render_macro)
    bpy.utils.register_class(PLAYBLASTER_OT_render_keyed_macro)
    bpy.utils.register_class(PLAYBLASTER_OT_render_playblast)
    bpy.utils.register_class(PLAYBLASTER_OT_render_playblast_postactions)

    # Define macros
    # Non Keyed
    action=PLAYBLASTER_OT_render_macro.define("RENDER_OT_opengl")
    action.properties.animation=True
    action.properties.view_context=True
    action.properties.render_keyed_only=False
    PLAYBLASTER_OT_render_macro.define("PLAYBLASTER_OT_render_playblast_postactions")
    # Keyed
    action=PLAYBLASTER_OT_render_keyed_macro.define("RENDER_OT_opengl")
    action.properties.animation=True
    action.properties.view_context=True
    action.properties.render_keyed_only=True
    PLAYBLASTER_OT_render_keyed_macro.define("PLAYBLASTER_OT_render_playblast_postactions")


def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_render_macro)
    bpy.utils.unregister_class(PLAYBLASTER_OT_render_keyed_macro)
    bpy.utils.unregister_class(PLAYBLASTER_OT_render_playblast)
    bpy.utils.unregister_class(PLAYBLASTER_OT_render_playblast_postactions)
