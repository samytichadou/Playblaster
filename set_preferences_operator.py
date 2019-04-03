import bpy

class PlayblasterSetPreferences(bpy.types.Operator):
    bl_idname = "playblaster.set_preferences"
    bl_label = "Playblaster Preferences"
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        
        # render engine
        layout.prop(scn, 'playblaster_render_engine')
        # resolution percentage
        layout.prop(scn, 'playblaster_resolution_percentage', slider = True)

        
        