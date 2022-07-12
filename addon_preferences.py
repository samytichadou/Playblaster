import bpy
import os


addon_name = os.path.basename(os.path.dirname(__file__))

class PlayblasterAddonPrefs(bpy.types.AddonPreferences) :
    bl_idname = addon_name

    playblast_folderpath : bpy.props.StringProperty(
            name = "Playblast Path",
            default = os.path.join(bpy.utils.user_resource('DATAFILES'), "playblaster"),
            description = "Folder where temporary Playblast are stored",
            subtype = "DIR_PATH"
            )

    playblast_folder_name : bpy.props.StringProperty(
            name = "Playblast Folder Name",
            description = "Name of the Playblast folder alongside blend file",
            default="playblasts",
            )

    player_path : bpy.props.StringProperty(
            name = "External Player Path",
            description = "Path of the executable of external player",
            subtype = "DIR_PATH"
            )

    # PROGRESS BAR
    progress_bar_color : bpy.props.FloatVectorProperty(
            name = "Progress Bar",
            size = 3,
            min = 0.0,
            max = 1.0,
            default = [1, 1, 1],
            subtype = 'COLOR'
            )

    progress_bar_background_color : bpy.props.FloatVectorProperty(
            name = "Background",
            size = 3,
            min = 0.0,
            max = 1.0,
            default = [0.2, 0.2, 0.2],
            subtype = 'COLOR'
            )

    progress_bar_size : bpy.props.IntProperty(
            name = "Progress Bar Size",
            min = 1,
            max = 100,
            default = 10
            )

    def draw(self, context) :
        layout = self.layout

        layout.prop(self, "playblast_folderpath")

        layout.prop(self, "playblast_folder_name")

        box = layout.box()
        row = box.row(align = False)
        row.label(text = "Progress Bar", icon = 'TIME')
        row.prop(self, 'progress_bar_color', text = '')
        row.prop(self, 'progress_bar_size', text = 'Size')
        row.prop(self, 'progress_bar_background_color')

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(PlayblasterAddonPrefs)

def unregister():
    bpy.utils.unregister_class(PlayblasterAddonPrefs)