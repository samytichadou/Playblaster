import bpy

# topbar function
def playblasterViewportFunction(self, context):
    self.layout.menu('PLAYBLASTER_MT_viewport_menu')

# topbar menu
class PLAYBLASTER_MT_viewport_menu(bpy.types.Menu):
    bl_label = "Playblaster"
    bl_idname = "PLAYBLASTER_MT_viewport_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator('playblaster.render')
        layout.operator('playblaster.play_rendered')
        layout.operator('playblaster.set_preferences')
