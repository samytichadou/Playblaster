import bpy, os, gpu, blf

from gpu_extras.batch import batch_for_shader

from .preferences import get_addon_preferences
from .global_variables import modal_refreshing

### UI ###

# callback for loading bar in 3D view
def draw_callback_px(self, context):
    # get color and size of progress bar
    addon_preferences = get_addon_preferences()
    color_bar = addon_preferences.progress_bar_color
    background = addon_preferences.progress_bar_background_color
    bar_thickness = addon_preferences.progress_bar_size

    # Progress Bar
    width = context.area.width

    completion = context.scene.playblaster_completion / 100
    size = int(width * completion)

    # rectangle background
    vertices_2 = (
        (0, 0), (width, 0),
        (0, bar_thickness + 20), (width, bar_thickness + 20))

    indices = (
        (0, 1, 2), (2, 1, 3))

    shader2 = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch2 = batch_for_shader(shader2, 'TRIS', {"pos": vertices_2}, indices=indices)

    shader2.bind()
    shader2.uniform_float("color", [*background, 1])
    batch2.draw(shader2)

    # rectangle 1
    vertices = (
        (0, 0), (size, 0),
        (0, bar_thickness), (size, bar_thickness))

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

    shader.bind()
    shader.uniform_float("color", [*color_bar, 1])
    batch.draw(shader)

    # Text
    text = modal_refreshing

    blf.color(0, *color_bar, 1)
    blf.size(0, 12, 72)
    blf.position(0, 10, bar_thickness + 5, 0)
    blf.draw(0, text)

class PlayblasterModalCheck(bpy.types.Operator):
    bl_idname = "playblaster.modal_check"
    bl_label = "Playblaster Modal Check"
    bl_options = {'INTERNAL'}

    _timer = None

    @classmethod
    def poll(cls, context):
        return context.scene.playblaster_is_rendering

    def modal(self, context, event):
        scn = context.scene
        completion = scn.playblaster_completion

        # redraw area
        try:
            for window in bpy.context.window_manager.windows :
                for area in window.screen.areas :
                    if area.type == 'VIEW_3D' :
                        area.tag_redraw()
        except AttributeError:
            pass

        #if event.type in {'ESC'} :
        #    self.cancel(context)
        #    return {'CANCELLED'}

        if event.type == 'TIMER' :
            if completion == 100 :
                self.finish(context)
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        args = (self, context)
        self._timer = wm.event_timer_add(0.1, window = context.window)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        self.report({'INFO'}, "Render Canceled")

    def finish(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        self.report({'INFO'}, "Render Finished")
