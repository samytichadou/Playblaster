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

    playblast_location: bpy.props.EnumProperty(
        name = "Playblast Location",
        default = 'ALONGSIDE',
        items = (
        ('PREFS', "Preferences Folder", ""),
        ('ALONGSIDE', "Alongside blend file", ""),
        ),
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

    def draw(self, context) :
        layout = self.layout
        
        layout.prop(self, "playblast_location")
        row1=layout.row()
        row2=layout.row()
        if self.playblast_location=="PREFS":
            row2.enabled=False
        else:
            row1.enabled=False
        row1.prop(self, "playblast_folderpath")
        row2.prop(self, "playblast_folder_name")


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(PlayblasterAddonPrefs)

def unregister():
    bpy.utils.unregister_class(PlayblasterAddonPrefs)