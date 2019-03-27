import bpy
import os
import shutil

from .preferences import get_addon_preferences
from .misc_functions import absolute_path, create_dir, get_file_in_folder, delete_file
from .global_variables import blender_executable
from .thread_functions import threading_render

class RenderOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "playblaster.simple_render"
    bl_label = "Playblaster Simple Render"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def execute(self, context):
        # variables
        prefs = get_addon_preferences()
        folder_path = absolute_path(prefs.prefs_folderpath)

        scn = context.scene
        blender = blender_executable
        blend_filepath = bpy.data.filepath
        blend_dir = os.path.dirname(blend_filepath)
        blend_file = bpy.path.basename(blend_filepath)
        blend_name = os.path.splitext(blend_file)[0]
        new_blend_filepath = os.path.join(blend_dir, "temp_" + blend_file)
        output_name = "playblast_" + blend_name + "_" + scn.name + "_"
        output_filepath = os.path.join(folder_path, output_name)
        render_engine = scn.playblaster_render_engine

        total_frame = context.scene.frame_end - context.scene.frame_start + 1

        scn.playblaster_is_rendering = True
        scn.playblaster_completion = 0

        # delete old playblast
        to_delete = get_file_in_folder(folder_path, output_name)
        if to_delete != "" :
            delete_file(to_delete)

        # create dir if does not exist
        create_dir(folder_path)


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

        ### change settings ###
        rd.filepath = output_filepath
        rd.image_settings.file_format = 'FFMPEG'
        rd.resolution_percentage = 50
        ffmpeg.format = 'MPEG4'
        ffmpeg.codec = 'H264'
        ffmpeg.constant_rate_factor = 'HIGH'
        ffmpeg.ffmpeg_preset = 'REALTIME'
        ffmpeg.gopsize = 10
        ffmpeg.audio_codec = 'AAC'

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
        ffmpeg.ffmpeg_preset = old_ffmpeg_preset
        ffmpeg.gopsize = old_gopsize
        ffmpeg.codec = old_codec
        ffmpeg.audio_codec = old_audio_codec

        # save current file
        bpy.ops.wm.save_as_mainfile(filepath = blend_filepath)

        new_scn = bpy.context.scene

        cmd = blender + " -b " + new_blend_filepath + " -E " + render_engine + " -a"

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
