import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

class PlayblasterAddonPrefs(bpy.types.AddonPreferences) :
    bl_idname = addon_name
 
    prefs_folderpath : bpy.props.StringProperty(
            name = "Preferences Folder Path",
            default = os.path.join(bpy.utils.user_resource('CONFIG'), "playblaster"),
            description = "Folder where temporary Playblast are stored",
            subtype = "DIR_PATH"
            )

    player_path : bpy.props.StringProperty(
            name = "External Player Path",
            description = "Path of the executable of external player",
            subtype = "DIR_PATH"
            )
            
    def draw(self, context) :
        layout = self.layout
        layout.prop(self, "prefs_folderpath")
        layout.prop(self, "player_path")
            

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)