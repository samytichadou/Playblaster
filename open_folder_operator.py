import bpy
import platform
import subprocess
import os

from .addon_preferences import get_addon_preferences

def open_folder(path) :
    #windows
    if platform.system() == "Windows":
        #os.startfile(path)
        subprocess.Popen(['explorer', path])
        # subprocess.Popen(r'explorer /select,%s' % path)
        #subprocess.call("explorer %s" % path, shell=True)
        #subprocess.Popen(r'explorer /select, "%s"' % path)
    #mac
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
        #subprocess.Popen(["open", "-a", "Finder", path])
    #linux
    else:
        subprocess.Popen(["xdg-open", path])

def return_folderpath():
    prefs=get_addon_preferences()
    blend_fp=bpy.data.filepath
    blend_name=os.path.splitext(os.path.basename(blend_fp))[0]
    if prefs.playblast_location=="ALONGSIDE":
        tmp = os.path.join(os.path.dirname(blend_fp), prefs.playblast_folder_name)
        return os.path.join(tmp, blend_name)
    else:
        return os.path.join(prefs.playblast_folderpath, "playblasts")


class PLAYBLASTER_OT_open_playblast_folder(bpy.types.Operator):
    bl_idname = "playblaster.open_playblast_folder"
    bl_label = "Open Folder"
    #bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def execute(self, context):
        fp_dir = return_folderpath()
        if not os.path.isdir(fp_dir):
            self.report({'WARNING'}, "No playblast folder yet")
            return {'FINISHED'}

        open_folder(fp_dir)

        self.report({'INFO'}, "Folder opened")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PLAYBLASTER_OT_open_playblast_folder)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_open_playblast_folder)