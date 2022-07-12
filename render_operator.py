import bpy
import os
import shutil

from .addon_preferences import get_addon_preferences
from .misc_functions import absolute_path, create_dir, get_file_in_folder, delete_file
from . import global_variables as gv
from .thread_functions import threading_render


blend_temp = ""
video_temp = ""

class PlayblasterRenderOperator(bpy.types.Operator):
    """Create Playblast of current scene"""
    bl_idname = "playblaster.render"
    bl_label = "Playblaster Render"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved and not context.scene.playblaster_properties.is_rendering

    def execute(self, context):
        # global
        global blend_temp
        global video_temp

        # variables
        prefs = get_addon_preferences()

        scn = context.scene
        pb_props = scn.playblaster_properties
        pb_settings = pb_props.playblast_settings
        blender = gv.blender_executable
        blend_filepath = bpy.data.filepath
        blend_dir = os.path.dirname(blend_filepath)
        blend_file = bpy.path.basename(blend_filepath)
        blend_name = os.path.splitext(blend_file)[0]
        render_engine = pb_settings.render_engine

        new_blend_filepath = blend_temp = os.path.join(blend_dir, "playblast_temp_" + blend_file)
        
        if pb_settings.playblast_location=="PREFS":
            folder_path = absolute_path(prefs.playblast_folderpath)
        else:
            folder_path = os.path.join(blend_dir, prefs.playblast_folder_name)

        #output_name = "playblast_" + datetime + blend_name + "_" + scn.name + "_"
        if pb_settings.exclude_datetime:
            output_name = "playblast__%s_%s_" % (blend_name, scn.name)
        else:
            from datetime import datetime
            datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = "playblast_%s_%s_%s_" % (datetime, blend_name, scn.name)
        output_filepath = video_temp = os.path.join(folder_path, output_name)

        pb_props.completion = 0

        # create dir if does not exist
        create_dir(folder_path)

        # delete old playblast
        to_delete = get_file_in_folder(folder_path, output_name)
        if to_delete != "" :
            deletion = delete_file(to_delete)          

        rd = scn.render
        ffmpeg = rd.ffmpeg

        ### store settings ###
        old_filepath = rd.filepath
        old_file_format = rd.image_settings.file_format
        old_res_pct = rd.resolution_percentage
        old_format = ffmpeg.format
        old_rate_factor = ffmpeg.constant_rate_factor
        old_ffmpeg_preset = ffmpeg.ffmpeg_preset
        old_gopsize = ffmpeg.gopsize
        old_codec = ffmpeg.codec
        old_audio_codec = ffmpeg.audio_codec
        # postprod
        old_compositing = rd.use_compositing
        old_sequencer = rd.use_sequencer
        old_preview_range = False
            # simplify
        if pb_settings.simplify :
            old_simplify_toggle = rd.use_simplify
            old_simplify_subdiv_render = rd.simplify_subdivision_render
            old_simplify_particles = rd.simplify_child_particles_render
            # EEVEE
        if render_engine == "BLENDER_EEVEE" :
            old_render_samples = scn.eevee.taa_render_samples
            #old_eevee_dof = scn.eevee.use_dof
            old_eevee_ao = scn.eevee.use_gtao

            # frame range
        if pb_settings.frame_range_override and pb_settings.frame_range_in < pb_settings.frame_range_out :
            old_range_in = scn.frame_start
            old_range_out = scn.frame_end
        if scn.use_preview_range:
            old_preview_range = True
            scn.use_preview_range = False

        ### change settings ###
        rd.filepath = output_filepath
        rd.image_settings.file_format = 'FFMPEG'
        rd.resolution_percentage = pb_settings.resolution_percentage
        ffmpeg.format = 'MPEG4'
        ffmpeg.codec = 'H264'
        ffmpeg.constant_rate_factor = 'HIGH'
        ffmpeg.ffmpeg_preset = 'REALTIME'
        ffmpeg.gopsize = 10
        ffmpeg.audio_codec = 'AAC'
            # postprod
        rd.use_compositing = pb_settings.use_compositing
        rd.use_sequencer = False
            # simplify
        if pb_settings.simplify :
            rd.use_simplify = True
            rd.simplify_subdivision_render = pb_settings.simplify_subdivision
            rd.simplify_child_particles_render = pb_settings.simplify_particles
            # EEVEE
        if render_engine == "BLENDER_EEVEE" :
            scn.eevee.taa_render_samples = pb_settings.eevee_samples
            #scn.eevee.use_dof = scn.playblaster_eevee_dof
            scn.eevee.use_gtao = pb_settings.eevee_ambient_occlusion
            # frame range
        if pb_settings.frame_range_override and pb_settings.frame_range_in < pb_settings.frame_range_out :
            scn.frame_start = scn.playblaster_frame_range_in
            scn.frame_end = scn.playblaster_frame_range_out

        # get total number of frames
        total_frame = context.scene.frame_end - context.scene.frame_start + 1

        # save current file
        bpy.ops.wm.save_as_mainfile(filepath = blend_filepath)

        # save temporary file
        shutil.copy(blend_filepath, new_blend_filepath)

        ### restore settings ###
        rd.filepath = old_filepath
        rd.image_settings.file_format = old_file_format
        rd.resolution_percentage = old_res_pct
        ffmpeg.format = old_format
        ffmpeg.constant_rate_factor = old_rate_factor
        if old_ffmpeg_preset != "" :
            ffmpeg.ffmpeg_preset = old_ffmpeg_preset
        ffmpeg.gopsize = old_gopsize
        ffmpeg.codec = old_codec
        ffmpeg.audio_codec = old_audio_codec
            # postprod
        rd.use_compositing = old_compositing
        rd.use_sequencer = old_sequencer
            # simplify
        if pb_settings.simplify :
            rd.use_simplify = old_simplify_toggle
            rd.simplify_subdivision_render = old_simplify_subdiv_render
            rd.simplify_child_particles_render = old_simplify_particles
            # EEVEE
        if render_engine == "BLENDER_EEVEE" :
            scn.eevee.taa_render_samples = old_render_samples
            #scn.eevee.use_dof = old_eevee_dof
            scn.eevee.use_gtao = old_eevee_ao
            # frame range
        if pb_settings.frame_range_override and pb_settings.frame_range_in < pb_settings.frame_range_out :
            scn.frame_start = old_range_in
            scn.frame_end = old_range_out
        
        scn.use_preview_range = old_preview_range

        # save current file
        bpy.ops.wm.save_as_mainfile(filepath = blend_filepath)

        pb_props.is_rendering = True

        new_scn = bpy.context.scene

        if pb_settings.render_type=='FULL':
            #cmd = '"' + blender + '"' + " -b " + '"' + new_blend_filepath + '"' + " -E " + render_engine + " -a"
            cmd = '"%s" -b "%s" -E %s -a' % (blender, new_blend_filepath, render_engine)
        elif pb_settings.render_type=='OPENGL':
            #cmd = '"' + blender + '"' + '"' + new_blend_filepath + '"' + " -P " + '"'gv.render_opengl_script
            cmd = '"%s" "%s" -P "%s"' % (blender, new_blend_filepath, gv.render_opengl_script)
        elif pb_settings.render_type=='OPENGLKEY':
            #cmd = '"' + blender + '"' + '"' + new_blend_filepath + '"' + " -P " + gv.render_openglkey_script
            cmd = '"%s" "%s" -P "%s"' % (blender, new_blend_filepath, gv.render_openglkey_script)
        threading_render([cmd, total_frame, new_scn, folder_path, output_name, new_blend_filepath])


        # launch modal check
        for w in bpy.context.window_manager.windows :
            s = w.screen
            for a in s.areas:
                if a.type == 'VIEW_3D' :
                    window = w
                    area = a
                    screen = window.screen
        override = {'window': window, 'screen': screen, 'area': area}

        bpy.ops.playblaster.modal_check(override)

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(PlayblasterRenderOperator)

def unregister():
    bpy.utils.unregister_class(PlayblasterRenderOperator)