import bpy
import os

from .misc_functions import kill_subprocess
from .render_operator import p

class PlayblasterModalCheck(bpy.types.Operator):
    bl_idname = "playblaster.modal_check"
    bl_label = "Playblaster Modal Check"
    #bl_options = {'INTERNAL'}

    _timer = None

    def modal(self, context, event):
        poll = p.poll()

        if event.type in {'ESC'} :
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER' :
            if poll != None :
                self.finish(context)
                return {'FINISHED'}
            else:
                self.report({'INFO'}, "Rendering")

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window = context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        global p

        self.report({'INFO'}, "Render Canceled")
        
        # kill render process
        kill_subprocess(p)
        
        # delete temp file

        # clean p variable
        p = None


    def finish(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        global p

        self.report({'INFO'}, "Render Finished")

        # delete temp file
                        
        # launch player

        # clean p variable
        p = None