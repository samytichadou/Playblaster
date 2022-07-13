import bpy


# playblast panel
class PLAYBLASTER_PT_playblast(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Playblast"
    bl_label = "Playblast"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Playblast")



### REGISTER ---
def register():
    bpy.utils.register_class(PLAYBLASTER_PT_playblast)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_PT_playblast)